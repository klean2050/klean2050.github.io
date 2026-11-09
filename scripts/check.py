"""Check local HTML links, assets and basic document structure. No dependencies."""
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def wrong_case(path):
    # macOS ignores filename case, GitHub Pages does not.
    rel = path.relative_to(ROOT)
    return any(part.name not in os.listdir(ROOT / part.parent) for part in [rel, *rel.parents][:-1])


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.references = []
        self.images = []
        self.heading_count = 0
        self.title = ''
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.heading_count += 1
        if tag == 'title':
            self.in_title = True
        if tag == 'img':
            self.images.append(attrs)
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.references.append(attrs[attr])
        for attr in ('aria-controls', 'aria-labelledby'):
            for identifier in attrs.get(attr, '').split():
                self.references.append('#' + identifier)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def main():
    pages = {}
    errors = []
    for path in sorted(ROOT.rglob('*.html')):
        if '.git' in path.relative_to(ROOT).parts:
            continue
        page = Page(path)
        page.feed(path.read_text())
        pages[path] = page

    references = 0
    for path, page in pages.items():
        label = str(path.relative_to(ROOT))
        if not page.title.strip():
            errors.append(f'{label}: missing page title')
        if page.heading_count != 1:
            errors.append(f'{label}: expected one h1, found {page.heading_count}')
        for identifier, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f'{label}: duplicate ID {identifier}')
        for image in page.images:
            if 'alt' not in image:
                errors.append(f'{label}: image missing alt: {image.get("src")}')
        for value in page.references:
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            references += 1
            if url.path:
                parent = ROOT if url.path.startswith('/') else path.parent
                target = (parent / unquote(url.path).lstrip('/')).resolve()
            else:
                target = path
            if not target.is_relative_to(ROOT):
                errors.append(f'{label}: reference escapes site root: {value}')
                continue
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                errors.append(f'{label}: missing local target: {value}')
                continue
            if wrong_case(target):
                errors.append(f'{label}: filename case differs on disk: {value}')
                continue
            if url.fragment and target.suffix == '.html':
                other = pages.get(target)
                if other and unquote(url.fragment) not in other.ids:
                    errors.append(f'{label}: missing fragment target: {value}')

    publications = ROOT / 'publications'
    inline = {unescape(c).strip() for c in re.findall(r'<code>(.*?)</code>', (publications / 'index.html').read_text(), re.S)}
    download = {e.strip() for e in re.split(r'\n(?=@)', (publications / 'publications.bib').read_text().strip())}
    types = {'journal', 'conference', 'preprint', 'abstract', 'patent', 'misc'}
    for tag in re.findall(r'<article class="paper"[^>]*>', (publications / 'index.html').read_text()):
        kind = re.search(r'data-type="([^"]*)"', tag)
        if not kind or kind.group(1) not in types:
            errors.append(f'publications: missing or unknown data-type: {tag}')
    for entry in inline ^ download:
        where = 'page' if entry in inline else 'publications.bib'
        errors.append(f'publications: BibTeX only in {where}: {entry.splitlines()[0]}')

    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'OK: {len(pages)} pages and {references} local references checked.')
    print('External links and factual content were not checked.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
