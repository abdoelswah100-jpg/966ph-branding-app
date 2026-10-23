# Tests (Playwright + Chromium)

Regression tests for 966Ph Branding. Each test opens the built app (`full28.html` = `dist/966Ph Branding vX.html`),
loads real data, clicks through the screens and prints results; the last line must be `NO ERRORS` / `ERRS []`.

| Test | Covers |
|---|---|
| test3 | home, month report, exports (xlsx, csv, spec, backup), sync reminder, recovery |
| t6 | summary, management report, PDFs, Excel |
| t7 | month / all pharmacies, Excel |
| t9 | image library, Excel import of names, attachments (plan PDF, xlsx) |
| t10 | summary PDF, attachments from Excel |
| t11 | Android layer (mocked Capacitor): save, share, auto backup, back button |
| t12 | v1.1: before/after photos, acrylic, totals, formatted Excel |
| t13 | v1.2: receipt/execution counts, shortages, swap, picker, Add to cart |
| t14 | v1.3: images, new names, colours, Medicated, keyboard, backups, card, shortage text, sounds |

**Fixtures are not in git** (real pharmacy data and the owner's Excel/PDF files stay out of the repo).
The tests expect a work folder (default `/home/claude/work/`) with the built app as `full28.html`,
the data files `out3/ out4/ out5/ out6/966-data-*.json` and the owner's sample files in `s9/`.
Paths are at the top of each test.
