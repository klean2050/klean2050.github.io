# Moving the redesign into the existing website repository

Keep **klean2050/klean2050.github.io**. Its default branch is **gh-pages**, verified
from GitHub on November 6, 2026. The redesign is a complete static site; it replaces
the old site's files rather than being inserted into the Jekyll theme.

## Prepared repositories

- `klean2050-website`: the standalone site, with an initial commit on `main` and
  no remote. Use this if you want a completely separate repository.
- `klean2050-website-migration`: a separate clone of the existing GitHub repository,
  with the finished site committed on **redesign/academic-website**. This is the
  recommended folder for updating the current website. The branch is based on
  the current `origin/gh-pages`, so it retains the existing repository history.
  The original checkout is untouched.

No branch has been pushed and no GitHub Pages setting has been changed.

## Review locally

In the prepared migration folder:

```sh
python3 scripts/check.py
python3 scripts/serve.py --port 8771
```

Open http://127.0.0.1:8771/. To inspect the exact replacement:

```sh
git diff --stat origin/gh-pages...HEAD
git log -1 --oneline
```

The old pages and assets remain recoverable in Git history. The old license is
retained. The new site includes the approved page structure and photographs,
research narratives/references, selected publications, teaching and the current CV.
Old project/blog pages are not carried into the new navigation or page tree.

## Publish when ready

Run this from **klean2050-website-migration**, not the standalone repository:

```sh
git push -u origin redesign/academic-website
```

That uploads the review branch. Then open:

[Create the redesign pull request](https://github.com/klean2050/klean2050.github.io/compare/gh-pages...redesign%2Facademic-website?expand=1)

Use **gh-pages** as the base branch. Review the changes and merge the pull request.
In the repository's **Settings > Pages**, use **Deploy from a branch**, select
**gh-pages** and **/ (root)**. If that is already the setting, leave it in place.
The URL remains **https://klean2050.github.io/**. The `.nojekyll` file serves the
HTML/CSS/JavaScript directly; Ruby, Bundler and a Jekyll build are unnecessary.

The included **Check website** workflow validates references, JavaScript syntax
and CV sync logic on pushes and pull requests. It does not deploy the site.

To roll back after merging, revert the migration pull request on GitHub. This
adds a normal history-preserving revert commit; no force push is needed.

## Optional Overleaf CV automation

The site works immediately with the bundled PDF. Automatic updates remain
disabled until you add the Overleaf Git token as a repository secret and enable
the repository variable described in [CV-AUTOMATION.md](CV-AUTOMATION.md).
For this existing repository, the default/publishing branch is **gh-pages**.
Do not change it to `main` just to use the new site.

GitHub's official reference:
[Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
