# Package validation

Checked October 17, 2026.

- Seven pages retain the approved prototype's text, authors, citations and dates.
- All 148 local references, fragments and control targets pass scripts/check.py.
- All three JavaScript files pass Node syntax checks.
- Packaged pages were served under a subpath to verify relative navigation and asset paths.
- Desktop layout and mentee image loading were checked visually.
- At 390px, the mobile menu works and Clicks has no horizontal overflow.
- Publication search for BioCodec returns Neural Codecs as Biosignal Tokenizers; its BibTeX expands.
- More updates reveals five entries and collapses again.
- Theme switching works.
- The original website repository's files match the pre-edit SHA-256 snapshot.

External publication URLs were preserved rather than freshly revalidated during
packaging. Research statements and the Clicks timeline intentionally contain
placeholders; see CONTENT-TODO.md.

## October 25, 2026 — separate research panels

The homepage now has three separate rounded panels with unchanged titles and destinations. Read more expands on hover or keyboard focus, is always visible for touch input, and respects reduced-motion preferences. Local reference checks pass. Browser access was blocked by the app security policy, so this revision has not been visually checked in-browser.

Descriptions restored from the pre-change homepage text on October 25, 2026. Description and Read more now expand together; keyboard focus and touch support are retained. Browser visual verification remains unavailable.

Research-page headings now use the full content width instead of an 850px cap. Balanced wrapping was removed on desktop, while mobile wrapping is retained.

## November 4, 2026 — research content and citations

- All three direction pages populated from the supplied six-page research statement, with personal introductions, selected projects and future questions. No prospective lab or figure placeholders appear in page content.
- Fourteen research-page citations match the selected publication source records exactly for full author lists and BibTeX; venue names and years are shown underneath every title.
- BrainCodes and Probing Spatial and Spectral Grounding in EEG Foundation Models added as October 21 preprints. Selection is now 22 papers, including 15 first/co-first-author papers. Prior exclusions remain applied.
- BrainCodes Website and Code verified against the official Microsoft repository. The project website returned HTTP 200 with the BrainCodes title.
- All eight pages and 204 local references pass scripts/check.py. Inline publication BibTeX matches the downloadable bibliography.
- All JavaScript files pass Node syntax checks. Citation expand/collapse, copy and clipboard-unavailable behavior pass a small DOM-stub check.
- Standalone research exports contain the updated prose, full citations, styles and controls.
- The original website repository matches the pre-edit SHA-256 snapshot, with zero changed files.
- This revision was not visually checked in the app browser because browser access had been blocked by its security policy. No alternate browser automation was used.
- The canonical package is served locally at http://127.0.0.1:8770/. Older preview ports are occupied by the app proxy.

## November 4, 2026 — CV and recent Updates

The linked CV is rebuilt from the Fall 2026 source and the user's later corrections. It has six pages, all eight mentees, two TA courses, and the 22 selected papers with full authors, confirmed venues, and direct links. Every page was rendered and inspected. No source PDF or original repository file was overwritten. Editable data and an optional PDF builder are included in cv/. All seven portable prototype exports embed the replacement CV.

Seven Updates were added through October 21, 2026. Month-only source dates remain month-only. Original older entries are retained. The first five still show by default; More updates reveals the rest.

Final CV checks: six pages with all 22 selected titles and author lists, all eight mentees, and both TA courses. PDF text bounds were checked; no words extend beyond the page margins. Every final page was visually inspected after the title/date gutter adjustment. All portable CV embeds match the linked PDF byte-for-byte. Updates now contains 45 entries, including seven additions; all five initially visible entries are from 2026. Local checks still pass for eight pages and 204 references.

## November 4, 2026 — continuous research text and end references

All three research pages now present their entire narrative first, including future questions, followed by a single References section. Project cards and interleaved citation blocks were removed. Numbered in-text links correspond to reference order; all 14 full references, authors, venues, years, links and BibTeX are retained. The homepage research panels are unchanged. Canonical pages, preview copies and standalone exports were updated together. Static checks pass for eight pages and 212 local references. This layout revision has not been visually checked in the app browser because of the previously reported access restriction.

## November 5, 2026 — Overleaf CV source

The CV is now compiled from the user's adapted res-class LaTeX source. The package includes main.tex and res.cls in cv/latex/; the optional build wrapper uses latexmk, pdfLaTeX or Tectonic. The earlier ReportLab reconstruction is replaced.

- Current source compiles successfully with the desktop LaTeX compiler and Tectonic.
- All seven final PDF pages were rendered and visually inspected, including the contact icons, dates, accents and Polish names.
- All 22 selected titles and their full author lists are present, with each complete citation on one page. All eight confirmed mentees are included.
- The final TeX log has no missing-character or overfull-box warnings.
- The build wrapper reproduces the exact reviewed page content streams.
- The website asset, preview asset and all seven portable CV embeds use the replacement PDF.
- Both the Overleaf source ZIP and refreshed website ZIP are validated against their source files.
- The original website repository is unchanged.

## November 6, 2026 — research narrative flow

Small connective additions to all three direction pages: +35, +44 and +34 words.
All three full References sections are byte-for-byte unchanged. Canonical pages,
preview copies and portable exports were updated together. Eight pages and 212
local references pass the static checker. The CV asset and the open LaTeX
publication fragment were not edited by this revision.


## November 6, 2026 — live Overleaf CV and Updates

- Pulled the configured private project using existing local Git authentication;
  main file `cv_2.tex`, revision recorded in `cv/overleaf-state.json`.
- Built and inspected all five final PDF pages. A local Tectonic compatibility
  wrapper preserves curly apostrophes in legacy T1 fonts without editing the
  Overleaf source. The build rejects missing-character warnings.
- The canonical PDF, preview asset and all seven portable CV embeds match.
- Prepared hourly GitHub Actions synchronization, gated by an enable variable
  and a repository secret. It is not running from this local, remote-less repo.
  Workflow passes actionlint 1.7.12. Actual hosted execution/publication remains
  untested until the owner completes setup. No changes were pushed to Overleaf.
- Thirteen focused automation tests pass: successful update/checksum recording,
  unchanged-source skipping, changed-source/PDF detection, failed compilation
  and wrong-identity preservation, credential redaction, source path isolation,
  and Pages build/retry/configuration handling.
- A second build correctly skipped unchanged Overleaf source.
- Updates now has 44 entries (six recent additions and 38 retained archive items).
  CuttingEEG renamed and dated September 24 from the official program; the
  probing-preprint update was removed. Microsoft is dated August 7 per the
  user's closest-Friday instruction. Apple remains October 2025 because no
  reliable exact day was found in public sources or the supplied poster/CV.
- Static checks pass for eight pages and 212 local references. This revision has
  no browser visual verification because of the previously reported restriction.


## November 6, 2026 — Clicks photographs

- Replaced the timeline placeholders with seven user-supplied photos grouped into
  six occasions, newest first. USC SAIL turns 25 is dated January 2026 from the official
  reunion program; the remaining dates come from embedded capture metadata.
- Preserved each image's natural proportions. Added 480px/960px WebP previews and
  1800px maximum JPEGs for larger viewing. All 21 assets decode successfully,
  retain aspect ratio, and omit EXIF/GPS metadata. The original files are unchanged.
- Added a native-dialog viewer with descriptive image links, Close/Escape support,
  focus restoration, and a normal JPEG-link fallback when JavaScript is unavailable.
- Mirrored the page/assets to the preview folder and embedded all seven photos in
  the portable Clicks export. Other pages and the CV are unchanged by this revision.
- Static checks pass for eight pages and 232 local references, including all full
  image links. Responsive srcset targets and portable image payloads are checked
  separately. JavaScript syntax checks pass. Browser visual verification remains
  unavailable under the previously reported access restriction.
