# Kleanthis Avramidis — personal website

Static academic website at https://klean2050.github.io/.
Pages: About, Publications, Teaching, Clicks, and three research directions.

## Preview locally

Requires Python 3.9 or newer. No build step or package installation is needed.

```sh
python3 scripts/serve.py
```

Open http://127.0.0.1:8766/. Use `--port 8770` to choose another port.

## Structure

```text
index.html               Biography, research overview and updates
publications/            Selected publications and bibliography
teaching/                Courses and mentees
clicks/                  Photo timeline
research/                Three research direction pages
assets/                  Styles, scripts, photographs and current CV PDF
cv/                      CV synchronization configuration and compiler
scripts/                 Local preview, validation and CV synchronization
docs/                    Content sources and editing instructions
.github/workflows/       Website checks and optional CV updates
```

## Edit and check

Pages are plain HTML. See [the editing guide](docs/EDITING.md).
Colors and shared layout are in `assets/css/site.css`.

```sh
python3 scripts/check.py
```

Optional CV automation checks require `pypdf`:

```sh
python3 -m pip install 'pypdf>=5,<7'
python3 -m unittest discover -s scripts/tests -v
```

## Update the website

The website lives on `gh-pages`, tracking `origin/gh-pages`.

```sh
git pull --ff-only
# Edit and check the site, then commit the changed files.
git push
```

GitHub Pages publishes from **gh-pages / (root)**. `.nojekyll` serves the static
files directly. The Check website workflow validates pushes and pull requests.
For automated CV updates from Overleaf, follow [CV-AUTOMATION.md](docs/CV-AUTOMATION.md).

Photos and academic materials retain their original rights. Content and asset
sources are recorded in [SOURCES.md](docs/SOURCES.md).
