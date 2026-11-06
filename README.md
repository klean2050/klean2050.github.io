# Kleanthis Avramidis — personal website

The finished academic website, packaged as a standalone static site.
It contains About, Publications, Teaching, Clicks, and three research direction pages.
The original website repository has not been modified.

## Preview locally

Requires Python 3.9 or newer. No package installation or build step is needed.

```sh
python3 scripts/serve.py
```

Open http://127.0.0.1:8766/. Use `--port 8000` to choose another port.
Stop the server with Ctrl+C. Keep the server local; its default bind address is 127.0.0.1.

## Structure

```text
index.html                         About, research overview, updates
404.html                           Page-not-found (root-absolute paths; user site only)
publications/index.html            Selected papers, search and citations
publications/publications.bib      Downloadable bibliography
teaching/index.html                Courses and mentees
clicks/index.html                  Photo timeline grouped by occasion
research/
  biosignal-representations/       First research direction
  multimodal-dynamics/             Second research direction
  clinical-translation/            Third research direction
assets/
  css/                            Shared and page-specific styles
  js/                             Shared controls and page interactions
  mentees/                        Public profile portraits
  portrait.jpg                    Homepage portrait
  Kleanthis-Avramidis-CV.pdf        Current CV download
cv/                               Overleaf sync configuration, fallback source, TeX builder
docs/                             Editing guide, remaining content, source notes
scripts/                          Preview, validation and CV synchronization
.github/workflows/sync-cv.yml      Optional hourly Overleaf CV refresh
.github/workflows/check-site.yml   Website checks on pushes and pull requests
```

## Edit content

Start with [the editing guide](docs/EDITING.md). Pages are plain HTML; they are the
canonical published content. Styles and scripts are shared, with no framework or
external runtime dependency. Source and selection notes are documentation, not
an automatic publication feed.

The design uses indigo `#4F46E5`, a pale `#F5F5FF` panel, Charter headings and
Avenir Next body text with system fallbacks. Mobile navigation and a dark theme
are included.

## Current status

The layout and navigation are complete. The three research pages contain personal
research narratives followed by full references, drawing
from the supplied research statement. See [RESEARCH-CONTENT.md](docs/RESEARCH-CONTENT.md)
for source notes. The CV was refreshed from the live Overleaf project on November 6
and has five pages. Recent Updates were revised on November 6.
Clicks now contains seven supplied photographs grouped into six occasions, newest
first, with responsive images and a larger photo viewer. Missing mentee portraits
are optional.
See [CONTENT-TODO.md](docs/CONTENT-TODO.md).
The October 17 publication selection was supplemented on November 4 with two
October 21 first-author preprints and BrainCodes Website/Code links. There is no
automatic publication sync. Optional hourly **CV** synchronization from Overleaf is
prepared but inactive until configured: see [CV setup](docs/CV-AUTOMATION.md).

## Validate

```sh
python3 scripts/check.py
# Optional CV automation checks (requires pypdf):
python3 -m unittest discover -s scripts/tests -v
```

This checks local page/asset references, fragment targets, accessible image text,
page titles, navigation links and HTML IDs. It does not claim to validate external
publisher URLs, factual accuracy or image reuse permissions.

## Git and hosting

**Updating the existing site?** Use the prepared `klean2050-website-migration`
clone and its `redesign/academic-website` branch. See [MIGRATION.md](docs/MIGRATION.md)
for the exact push, pull request and Pages steps. Keep the existing repository
name and `gh-pages` publishing branch.


This folder is the prepared migration clone of `klean2050/klean2050.github.io`,
on branch `redesign/academic-website`, based on `origin/gh-pages`. It retains the
existing repository history and license. The new site is committed locally;
nothing has been pushed. Follow [MIGRATION.md](docs/MIGRATION.md) to push this
review branch and merge it into `gh-pages` when ready.

The site can be hosted directly from the repository root. For GitHub Pages,
choose a `gh-pages` / root deployment in the repository settings; `.nojekyll` keeps the
static files intact. The relative links support both a user site and a project
subpath. No deployment or remote changes have been made by this package.

The folder contains no generated previews, design experiments, standalone HTML
duplicates, credentials, or machine-specific build paths. This migration clone
retains the existing repository history.
Photos and academic material retain their original rights; no blanket license
for third-party material is granted. See [SOURCES.md](docs/SOURCES.md).
