"""Ensure branch-based GitHub Pages publishes the CV commit from this workflow."""
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
import os
import re
import subprocess
import sys
import time


def ensure_build(api, head, branch, wait=True):
    site = api('GET', '')
    if site.get('build_type') == 'workflow':
        raise RuntimeError('This CV workflow uses branch-based Pages. Set Pages to Deploy from a branch, default branch / (root).')
    source = site.get('source', {})
    if source.get('branch') != branch or source.get('path') != '/':
        raise RuntimeError('Configure Pages to publish the repository default branch from / (root).')
    latest = api('GET', '/builds/latest', allow_missing=True)
    if not latest or latest.get('commit') != head or latest.get('status') == 'errored':
        api('POST', '/builds')
        print('Requested a GitHub Pages rebuild for the current CV commit.', flush=True)
    elif latest.get('status') == 'built':
        print('GitHub Pages already serves the current commit.')
        return
    if not wait:
        return
    deadline = time.monotonic()+300
    previous = None
    while time.monotonic() < deadline:
        latest = api('GET', '/builds/latest', allow_missing=True)
        if latest and latest.get('commit') == head:
            status = latest.get('status')
            if status != previous:
                print('GitHub Pages build: '+str(status), flush=True)
                previous = status
            if status == 'built':
                return
            if status == 'errored':
                raise RuntimeError('GitHub Pages reported a build error; check the Pages build log.')
        time.sleep(10)
    raise RuntimeError('Timed out waiting for the GitHub Pages build. The next sync checks publication again.')


def main():
    repository = os.environ.get('GITHUB_REPOSITORY', '')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('GITHUB_REPOSITORY must identify the website repository.')
    token = os.environ.get('GH_TOKEN')
    if not token:
        raise ValueError('GH_TOKEN is required for the Pages build request.')
    base = 'https://api.github.com/repos/'+repository+'/pages'

    def api(method, suffix, allow_missing=False):
        request = Request(base+suffix, method=method,
                          headers={'Accept': 'application/vnd.github+json',
                                   'Authorization': 'Bearer '+token,
                                   'X-GitHub-Api-Version': '2026-03-10',
                                   'User-Agent': 'website-cv-sync'})
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if allow_missing and error.code == 404:
                return None
            raise RuntimeError('GitHub Pages API returned HTTP '+str(error.code)+'. Check Pages configuration and workflow permissions.') from None

    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    branch = os.environ['CV_BRANCH']
    ensure_build(api, head, branch)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
