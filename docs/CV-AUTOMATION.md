# Automatic CV updates from Overleaf

The workflow is configured for the supplied Overleaf project and its main file,
`cv_2.tex`. It checks for changes hourly, compiles the source when it changes,
updates the existing CV PDF, and requests a GitHub Pages rebuild. The CV navbar
link stays the same. You can also run it from the Actions tab at any time.

## One-time setup

1. In Overleaf Account Settings, create a **Git authentication token**.
2. In the website's GitHub repository, open **Settings > Secrets and variables >
   Actions**. Add a repository secret named **OVERLEAF_GIT_TOKEN** containing that
   token. Do not add the token to the source or send it in chat.
3. Under repository **Settings > Pages**, select **Deploy from a branch**, the
   default branch (`gh-pages` for the existing website repository), and **/ (root)**. This matches the static-site
   hosting instructions in the README.
4. Add an Actions repository variable **OVERLEAF_CV_SYNC_ENABLED** with value
   **true**. In **Actions > Sync CV from Overleaf**, select **Run workflow** for
   the first run. The workflow requires contents-write and pages-write access.

The local pull/build was tested on November 6, 2026; the resulting five-page CV
is included. The bundled `cv/latex/` files are an older manual fallback, not a
copy of the live project. No private Overleaf source was added to the package.

The workflow runs on the repository default branch, `gh-pages`. It remains
disabled unless `OVERLEAF_CV_SYNC_ENABLED` is set to `true`.

## What the workflow does

- Pulls the current Overleaf source into a temporary, private checkout.
- Uses the project and main-file configuration in `cv/overleaf.json`.
- Compares the Git revision and current PDF checksum with `cv/overleaf-state.json`.
  Unchanged source skips TeX installation and compilation.
- Compiles with pdfLaTeX through latexmk, validates the PDF, and atomically
  replaces `assets/Kleanthis-Avramidis-CV.pdf` only after success.
- Commits only the public PDF and a small revision/checksum record. It does not
  copy the Overleaf sources into the public website or push changes to Overleaf.
- Explicitly requests a branch-based GitHub Pages build, since a commit made with
  GITHUB_TOKEN does not trigger another workflow/Pages build automatically.
- Checks publication again on later runs if a previous Pages build failed.

The runner builds a PDF from your Overleaf source; it does not scrape or download
Overleaf's existing compiled PDF. Keep the compiler/packages compatible with your
Overleaf settings. All dependencies used by the current project are included in
the workflow. If you rename the main file, update `cv/overleaf.json`.

Hourly schedules are best-effort, not an immediate publish-on-save hook. GitHub
may pause schedules on inactive public repositories; re-enable the workflow if
needed. Branch protection must permit the workflow's CV commit. A failed fetch, compile, missing-character check or PDF validation leaves the last working website PDF in place.

## Local refresh

Local Git can use an existing credential helper. Alternatively, provide an
Overleaf Git token through the `OVERLEAF_GIT_TOKEN` environment variable. The
script never embeds it in a remote URL or prints it.

```sh
python3 scripts/sync_cv_from_overleaf.py fetch --source-dir /tmp/my-overleaf-cv
python3 -m pip install 'pypdf>=5,<7'
python3 scripts/sync_cv_from_overleaf.py build --source-dir /tmp/my-overleaf-cv --engine pdflatex
```

Use a new temporary checkout path for each fetch. `--force` requests rebuilding
even when the recorded revision is unchanged. For a local Tectonic installation,
pass its path/name to `--engine`. Local refresh updates the preview asset only;
it does not deploy the website.

## Sources

- [Overleaf Git integration](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git-integration)
- [Overleaf Git authentication tokens](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git-integration/git-integration-authentication-tokens)
- [GitHub workflow triggering and GITHUB_TOKEN](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [GitHub Pages build API](https://docs.github.com/en/rest/pages/pages#request-a-github-pages-build)
