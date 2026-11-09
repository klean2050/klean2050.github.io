# Website checks

Run from the repository root:

```sh
python3 scripts/check.py
for script in assets/js/*.js; do node --check "$script"; done
python3 -m unittest discover -s scripts/tests -v
```

The CV tests require `pypdf`; page/link checks use only Python's standard library.
The same checks run in `.github/workflows/check-site.yml`.

Checks cover page structure, local references, navigation/fragment IDs,
publication bibliography consistency, JavaScript syntax, and CV update failure
handling. External links and factual content require separate review.

After layout edits, review desktop/mobile widths, both themes, navigation,
research-card expansion, publication search/citations, Updates expansion, and
the photo viewer. After CV changes, render and inspect every PDF page.
