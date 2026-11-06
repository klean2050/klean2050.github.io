# CV source and synchronization

The website PDF was refreshed from the supplied live Overleaf project on
November 6, 2026: five pages, main file `cv_2.tex`. The Git revision and PDF
checksum are recorded in `overleaf-state.json`. This is the latest user-edited
CV, with 12 selected publications; it need not mirror the larger website selection.
All five pages were rendered and visually checked.

The optional hourly workflow pulls that project and rebuilds its PDF. It is
**not enabled** until the GitHub setup in [CV-AUTOMATION.md](../docs/CV-AUTOMATION.md)
is completed. The live project remains in Overleaf; its private source is never
copied into this public package. A local Tectonic build uses a small stdin
compatibility wrapper for curly apostrophes in T1 fonts, without editing the
Overleaf project. CI uses pdfLaTeX through latexmk. Missing-character warnings
stop replacement of the existing website PDF.

## Bundled fallback source (November 5 snapshot)

The earlier self-contained, editable snapshot is retained as a manual fallback:

- `latex/main.tex`: the complete editable document.
- `latex/res.cls`: the original resume class, including its copyright and reuse notice.
- `../assets/Kleanthis-Avramidis-CV.pdf`: the current live-project build, not the older snapshot.

The supplied `res` template, classic serif typography, left-margin section
labels, contact icons, and indigo `#4338CA` name/section styling are retained.
The original research-project descriptions and document order are preserved,
with corrected typos and updated SAIL/Microsoft summaries. Long headings use
separate date columns to prevent collisions.

Confirmed updates remain in place: three research directions, all eight mentees
with the user's latest years and destinations, the two TA appointments in reverse
chronological order, and 22 selected papers with full author lists, expanded venue
names and direct links. BioCodec uses its 2025 preprint year. Prior publication
exclusions and the request to omit equal-contribution notes remain applied.

## Edit in Overleaf

Upload everything in `latex/` into an Overleaf project, set `main.tex` as the main
document, and select pdfLaTeX. No external bibliography or image upload is needed.
Font Awesome and the other standard TeX packages are provided by Overleaf.

## Rebuild the fallback locally

With a TeX distribution or Tectonic installed, run from the website root:

```sh
python3 cv/build.py
```

Or select a compiler explicitly:

```sh
python3 cv/build.py --engine /path/to/tectonic
```

`--output /path/to/review.pdf` produces a review copy. The builder compiles in a
temporary directory and replaces the target only after a successful PDF build.
Render and inspect the final PDF after editing, then refresh the website ZIP and
portable exports. The website itself needs no TeX installation or build step.

`content.json` is a companion snapshot of the previously confirmed structured
content; editing it does not regenerate the TeX document. Publications are in
`../docs/publication-sources.json`; keep edits to that record, the Publications
page and the CV in sync. The live Overleaf project is authoritative for the current CV; this snapshot is not automatically updated.

The user-supplied source attachment, original PDFs and original website repository
are unchanged. The class is included under its original notice, which permits
copying except for resale and requires retaining that notice.

The older November 5 snapshot has seven pages, with complete publication entries kept
together and balanced across three reference pages. The two explicit page breaks
in the publication list may need adjustment after adding or removing papers.
All seven final pages were rendered and visually checked.
