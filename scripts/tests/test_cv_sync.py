"""Run with: python3 -m unittest discover -s scripts/tests -v (requires pypdf)."""
from pathlib import Path
from unittest.mock import patch
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sync = load('sync_cv_from_overleaf')
pages = load('request_pages_build')
VALID_PDF = (SCRIPTS.parent/'assets/Kleanthis-Avramidis-CV.pdf').read_bytes()


class CvSyncTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.base = Path(self.folder.name).resolve()
        self.root = self.base/'website'
        (self.root/'cv').mkdir(parents=True)
        (self.root/'assets').mkdir()
        self.source = self.base/'private'
        self.source.mkdir()
        (self.source/'cv_2.tex').write_text('test source')
        self.settings = dict(git_url='https://git@git.overleaf.com/634a384ef5154b7120e68967',
                             main_file='cv_2.tex', output='assets/cv.pdf', state_file='cv/state.json')
        (self.root/'cv/overleaf.json').write_text(json.dumps(self.settings))
        self.output = self.root/'assets/cv.pdf'
        self.output.write_bytes(b'previous PDF')
        self.state = self.root/'cv/state.json'
        self.state.write_text('{}')
        self.root_patch = patch.object(sync, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.rev_patch = patch.object(sync, 'revision', return_value='a'*40)
        self.rev_patch.start()
        self.addCleanup(self.rev_patch.stop)

    def marker(self):
        self.state.write_text(json.dumps(dict(overleaf_commit='a'*40,
            git_url=self.settings['git_url'], main_file='cv_2.tex', pdf_sha256=sync.digest(self.output))))

    def fake_compiler(self, payload):
        def compile_result(command, **kwargs):
            self.assertNotIn('OVERLEAF_GIT_TOKEN', kwargs['env'])
            Path(command[command.index('--output')+1]).write_bytes(payload)
        return compile_result

    def test_success_records_commit_and_pdf_checksum(self):
        with patch.object(sync.subprocess, 'run', side_effect=self.fake_compiler(VALID_PDF)):
            sync.build(self.source, self.settings)
        self.assertEqual(self.output.read_bytes(), VALID_PDF)
        state = json.loads(self.state.read_text())
        self.assertEqual(state['overleaf_commit'], 'a'*40)
        self.assertEqual(state['pdf_sha256'], sync.digest(self.output))
        self.assertGreater(state['page_count'], 0)

    def test_unchanged_revision_skips_compiler(self):
        self.marker()
        with patch.object(sync.subprocess, 'run') as compiler:
            sync.build(self.source, self.settings)
        compiler.assert_not_called()

    def test_changed_source_and_changed_pdf_require_build(self):
        self.marker()
        self.assertFalse(sync.needs_build(self.source, self.settings))
        with patch.object(sync, 'revision', return_value='b'*40):
            self.assertTrue(sync.needs_build(self.source, self.settings))
        self.output.write_bytes(b'different PDF')
        self.assertTrue(sync.needs_build(self.source, self.settings))

    def test_force_requires_build(self):
        self.marker()
        self.assertTrue(sync.needs_build(self.source, self.settings, force=True))

    def test_compile_failure_preserves_both_files(self):
        with patch.object(sync.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, ['compiler'])):
            with self.assertRaises(subprocess.CalledProcessError):
                sync.build(self.source, self.settings)
        self.assertEqual(self.output.read_bytes(), b'previous PDF')
        self.assertEqual(self.state.read_text(), '{}')

    def test_wrong_identity_preserves_both_files(self):
        from pypdf import PdfWriter
        candidate = self.base/'wrong.pdf'
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.write(candidate)
        with patch.object(sync.subprocess, 'run', side_effect=self.fake_compiler(candidate.read_bytes())):
            with self.assertRaisesRegex(ValueError, 'identify'):
                sync.build(self.source, self.settings)
        self.assertEqual(self.output.read_bytes(), b'previous PDF')
        self.assertEqual(self.state.read_text(), '{}')

    def test_config_rejects_credentials_and_path_escape(self):
        for bad in ({'git_url': self.settings['git_url'].replace('git@', 'git:secret@')},
                    {'git_url': 'https://example.org/634a384ef5154b7120e68967'},
                    {'output': '../escape.pdf'}, {'main_file': '../cv.tex'}):
            with self.subTest(bad=bad):
                (self.root/'cv/overleaf.json').write_text(json.dumps(self.settings | bad))
                with self.assertRaises(ValueError):
                    sync.config()

    def test_auth_failure_redacts_git_output_and_does_not_embed_token(self):
        checkout = self.base/'new-private'
        with patch.dict(os.environ, {'OVERLEAF_GIT_TOKEN': 'test-token-never-published'}):
            def reject(command, **kwargs):
                self.assertNotIn('test-token-never-published', ' '.join(command))
                self.assertNotIn('test-token-never-published', Path(kwargs['env']['GIT_ASKPASS']).read_text())
                return subprocess.CompletedProcess(command, 1, stderr='secret diagnostic')
            with patch.object(sync.subprocess, 'run', side_effect=reject):
                with self.assertRaises(RuntimeError) as error:
                    sync.fetch(checkout, self.settings)
                self.assertNotIn('secret diagnostic', str(error.exception))
                self.assertNotIn('test-token-never-published', str(error.exception))
        self.assertEqual(self.output.read_bytes(), b'previous PDF')

    def test_private_source_cannot_be_inside_website(self):
        with patch('sys.argv', ['sync', 'fetch', '--source-dir', str(self.root/'private')]):
            with self.assertRaisesRegex(ValueError, 'outside'):
                sync.main()


class PagesBuildTests(unittest.TestCase):
    def api(self, latest, site=None):
        site = site or dict(build_type='legacy', source=dict(branch='main', path='/'))
        calls = []
        def request(method, suffix, **kwargs):
            calls.append((method, suffix))
            return site if suffix == '' else latest
        return request, calls

    def test_published_commit_does_not_request_build(self):
        api, calls = self.api(dict(commit='abc', status='built'))
        pages.ensure_build(api, 'abc', 'main')
        self.assertNotIn(('POST', '/builds'), calls)

    def test_missing_stale_or_failed_build_requests_publication(self):
        for latest in (None, dict(commit='old', status='built'), dict(commit='abc', status='errored')):
            with self.subTest(latest=latest):
                api, calls = self.api(latest)
                pages.ensure_build(api, 'abc', 'main', wait=False)
                self.assertIn(('POST', '/builds'), calls)

    def test_queued_commit_is_not_requested_twice(self):
        api, calls = self.api(dict(commit='abc', status='queued'))
        pages.ensure_build(api, 'abc', 'main', wait=False)
        self.assertNotIn(('POST', '/builds'), calls)

    def test_incompatible_pages_config_rejected_before_post(self):
        for site in (dict(build_type='workflow'), dict(source=dict(branch='old', path='/')),
                     dict(source=dict(branch='main', path='/docs'))):
            with self.subTest(site=site):
                api, calls = self.api(None, site)
                with self.assertRaises(RuntimeError):
                    pages.ensure_build(api, 'abc', 'main', wait=False)
                self.assertNotIn(('POST', '/builds'), calls)


if __name__ == '__main__':
    unittest.main()
