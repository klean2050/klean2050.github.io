"""Fetch or build the Overleaf CV without publishing its private source files."""
from pathlib import Path
from urllib.parse import urlsplit
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def config():
    data = json.loads((ROOT/'cv/overleaf.json').read_text())
    url = urlsplit(data['git_url'])
    if (url.scheme != 'https' or url.hostname != 'git.overleaf.com'
            or url.username not in (None, 'git') or url.password is not None
            or url.query or url.fragment or url.port not in (None, 443)
            or not re.fullmatch(r'/[0-9a-f]{24}/?', url.path)):
        raise ValueError('Configure an Overleaf HTTPS Git URL without a password or token.')
    for field in ('output', 'state_file'):
        target = (ROOT/data[field]).resolve()
        if not target.is_relative_to(ROOT):
            raise ValueError(field+' must stay inside the website directory.')
    main = Path(data['main_file'])
    if main.is_absolute() or '..' in main.parts or main.suffix != '.tex':
        raise ValueError('main_file must be a project-relative .tex path.')
    return data


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def revision(source):
    value = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if not re.fullmatch(r'[0-9a-f]{40,64}', value):
        raise ValueError('Unexpected Git revision.')
    return value


def source_main(source, settings):
    main = (source/settings['main_file']).resolve()
    if not main.is_relative_to(source.resolve()) or not main.is_file():
        raise ValueError('Configured main TeX file is missing from the fetched project.')
    return main


def needs_build(source, settings, force=False):
    source_main(source, settings)
    output = ROOT/settings['output']
    state_path = ROOT/settings['state_file']
    if force or not output.is_file() or not state_path.is_file():
        return True
    state = json.loads(state_path.read_text())
    return not (state.get('overleaf_commit') == revision(source)
                and state.get('git_url') == settings['git_url']
                and state.get('main_file') == settings['main_file']
                and state.get('pdf_sha256') == digest(output))


def output_flag(changed):
    value = str(changed).lower()
    print('CV update needed: '+value)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
            stream.write('changed='+value+'\n')


def fetch(source, settings, force=False):
    if source.exists():
        raise ValueError('Use a new temporary directory for the Overleaf checkout.')
    source.parent.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment.update(GIT_TERMINAL_PROMPT='0', GIT_LFS_SKIP_SMUDGE='1')
    with tempfile.TemporaryDirectory(prefix='overleaf-auth-') as folder:
        command = ['git']
        if environment.get('OVERLEAF_GIT_TOKEN'):
            helper = Path(folder)/'askpass'
            helper.write_text('#!'+sys.executable+'\nimport os, sys\n'
                              'print("git" if "username" in sys.argv[1].lower() '
                              'else os.environ["OVERLEAF_GIT_TOKEN"])\n')
            helper.chmod(0o700)
            environment['GIT_ASKPASS'] = str(helper)
            # Do not store or query a token through a credential helper in CI.
            command += ['-c', 'credential.helper=']
        else:
            # Local Git may use an already-configured credential helper.
            environment['GIT_ASKPASS'] = '/usr/bin/false'
        command += ['clone', '--quiet', '--', settings['git_url'], str(source)]
        result = subprocess.run(command, env=environment, capture_output=True, text=True)
        if result.returncode:
            # Never relay authentication output or put a token in the remote URL.
            raise RuntimeError('Could not fetch the Overleaf project. Check Git access and OVERLEAF_GIT_TOKEN.')
    output_flag(needs_build(source, settings, force))


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.'+path.name, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    temporary.chmod(0o644)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def build(source, settings, engine=None, force=False):
    if not needs_build(source, settings, force):
        print('CV is already current; no compilation needed.')
        return
    from pypdf import PdfReader
    with tempfile.TemporaryDirectory(prefix='overleaf-cv-') as folder:
        candidate = Path(folder)/'cv.pdf'
        command = [sys.executable, str(ROOT/'cv/build.py'), '--source-dir', str(source),
                   '--main-file', settings['main_file'], '--output', str(candidate)]
        if engine:
            command += ['--engine', engine]
        environment = os.environ.copy()
        environment.pop('OVERLEAF_GIT_TOKEN', None)
        subprocess.run(command, env=environment, check=True)
        reader = PdfReader(candidate)
        if reader.is_encrypted or not 1 <= len(reader.pages) <= 50:
            raise ValueError('The compiled CV is not a readable document of the expected size.')
        name = re.sub(r'\s+', '', reader.pages[0].extract_text()).lower()
        if 'kleanthisavramidis' not in name:
            raise ValueError('The compiled PDF does not identify Kleanthis Avramidis on its first page.')
        state = dict(git_url=settings['git_url'], main_file=settings['main_file'],
                     overleaf_commit=revision(source), pdf_sha256=digest(candidate),
                     page_count=len(reader.pages))
        # Replace the website asset only after successful compilation/validation.
        atomic_write(ROOT/settings['output'], candidate.read_bytes())
        atomic_write(ROOT/settings['state_file'], (json.dumps(state, indent=2)+'\n').encode())
        print('Website CV updated: '+str(len(reader.pages))+' pages.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['fetch', 'build'])
    parser.add_argument('--source-dir', type=Path, required=True,
                        help='Temporary checkout, never the public website directory.')
    parser.add_argument('--engine', help='Optional path/name of the TeX compiler.')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    source = args.source_dir.resolve()
    if source == ROOT or source.is_relative_to(ROOT):
        raise ValueError('Keep the private Overleaf checkout outside the public website directory.')
    settings = config()
    if args.operation == 'fetch':
        fetch(source, settings, args.force)
    else:
        build(source, settings, args.engine, args.force)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
