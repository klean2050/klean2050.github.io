# Editing the website

## Shared design and navigation

- `assets/css/site.css`: colors, typography, header, homepage, responsive layout, dark theme.
- `assets/css/publications.css`, `teaching.css`, `clicks.css`, `research.css`: page-specific layouts.
- `assets/js/site.js`: mobile navigation and theme controls, loaded on every page.
- `assets/js/home.js`: expand/collapse Updates.
- `assets/js/publications.js`: publication search, type filter, years, BibTeX and copy controls.
- `assets/js/citations.js`: BibTeX and copy controls on research pages.

Navigation is ordinary HTML repeated in the eight pages, including 404. When changing a global
navigation label or destination, update each `<header class="site-header">`.
Preserve the active page's `aria-current` attribute. Research directions remain
linked from the homepage cards rather than the main navbar.

## Homepage

Edit the biography in `index.html` and replace `assets/portrait.jpg` if needed.
Updates are `.news-item` articles. Newest first. Exact dates and month-only dates are both supported; do not invent a day. The November 4 additions are documented in `updates-sources.json`. The first five show; `home.js` hides the rest behind the More updates button, which appears once there are more than five. The three research cards
link to their matching direction pages. Each direction is a separate rounded panel. The title is always visible; The original description and Read more expand together on hover or keyboard focus, and stay visible on touch devices. The entire panel is the link. Edit `.research-card` and `.research-more` in `assets/css/site.css` for this interaction.

## Publications

Edit `publications/index.html`. Duplicate an `<article class="paper">` inside the
correct `.publication-year` section. Use a unique key consistently in the article
ID, title ID, BibTeX control, and citation ID, and put the title in the Copy button's
`aria-label`. For a new year, add both the year section and its `.year-index` link.

Every article needs a `data-type`: `journal`, `conference`, `preprint`, `abstract`,
`patent` or `misc` (books, theses and software). The type buttons above the list
filter by it, combine with search, and count entries automatically; `?type=patent`
links to a pre-filtered view. `scripts/check.py` rejects missing or unknown types.
Workshop papers count as conferences; a preprint moves to its venue's type once published.

List all authors and bold Kleanthis Avramidis. Keep paper titles capitalized
consistently and venue names expanded. Do not add equal-contribution symbols or
notes. Keep the selected portfolio focused; earlier exclusions are recorded in
`publication-selection.md`. EMBC wording is:
`IEEE Engineering in Medicine and Biology Society Conference (EMBC)`.

Update the inline citation and `publications/publications.bib` together, then
record changes in `docs/publication-sources.json`. The footer's "Last updated" date
on every page fills in automatically.
The JSON is a provenance snapshot; editing it alone does not change the page.

## Teaching

Each `.course-entry` in `teaching/index.html` has a term on the left and a course
code/title, role and institution on the right. Keep newest first. Roles are per
course, so the list can include both teaching and TA appointments.

Mentees use `.mentoring-entry` inside a three-column `.mentee-grid` (one panel per third of the desktop content width, stacked on mobile): photo on the left; name, year and any future
details on the right. The list includes eight user-confirmed mentees. Details and image sources are recorded in `mentee-photo-sources.json`. Add program, topic or outcome only when confirmed. Images live in
`assets/mentees/`; source records are in `docs/mentee-photo-sources.json`.

## Research directions

Edit the `index.html` in each `research/` subdirectory. Each page has one
continuous `.direction-text` narrative, followed by a single
`.direction-references` section headed References. Do not interleave project
cards, publication blocks or future-work sections with the narrative.

Cite work with numbered inline links to the corresponding reference IDs. Keep
references in first-citation order. The full references use the Publications
author, venue and action styles, with full author lists, year, direct links and
expandable/copyable BibTeX. Unique IDs use a `work-` prefix. Keep metadata in sync
with the matching Publications entries. BrainCodes includes Website and Code.

Keep future plans distinct from completed results within the prose. No
prospective lab or draft research-statement PDF is published. The three-way
navigation stays local to these pages.

## Clicks

In `clicks/index.html`, each `.occasion` article is one photo occasion. Use
`<time datetime="YYYY-MM">` (or an exact date when known), a short title, and a
unique heading ID. Put newest occasions first. The current seven supplied photos
are grouped into six occasions; their dates and filenames are recorded in
`clicks-photo-sources.json`.

Store photos under `assets/photos/<occasion>/`. Each current photo has a 480px and
960px WebP preview plus a JPEG capped at 1800px for the larger viewer. Keep the
natural image proportions, and add useful alt text and width/height attributes.
The `.photo-link` anchor points to the larger JPEG; without JavaScript it remains
a normal image link. `assets/js/clicks.js` opens the native dialog, supports Escape
and the Close button, and returns focus to the clicked photo. The responsive grid
uses two columns on desktop and one on narrow phones.

Example (replace dimensions to match your own image):

```html
<figure>
  <a class="photo-link" href="../assets/photos/occasion/photo.jpg"
     aria-label="View photo: A short description.">
    <img src="../assets/photos/occasion/photo-480.webp"
         srcset="../assets/photos/occasion/photo-480.webp 480w,
                 ../assets/photos/occasion/photo-960.webp 960w"
         sizes="(max-width:460px) calc(100vw - 70px), 440px"
         width="960" height="720" alt="A short description."
         loading="lazy" decoding="async">
  </a>
</figure>
```

Keep the `#photo-viewer` dialog at the end of the page and preserve its IDs when
adding occasions. Color and spacing remain in `assets/css/clicks.css`.

## CV

The linked PDF is `assets/Kleanthis-Avramidis-CV.pdf`. The current CV comes from
its live Overleaf project (`cv_2.tex`). See [CV-AUTOMATION.md](CV-AUTOMATION.md) for
the optional hourly pull/build workflow and local refresh commands. GitHub
activation is still required. Keep the PDF filename to preserve navbar links.
`cv/latex/main.tex` and `res.cls` retain the earlier November 5 manual fallback;
they are not synchronized copies of the live project. The website itself needs
no TeX dependencies.

After edits, run `python3 scripts/check.py` and preview desktop and mobile sizes.

Verified destinations appear in `.mentee-after` paragraphs with the visible label “After:”. Source URLs and verification notes are stored in `mentee-photo-sources.json`. Andreas and Simon have no destination line because their post-thesis positions are not established. Eileen and Kranti have no destination line at the user’s request. “PhD” and “MS” identify destinations, not completed degrees.
