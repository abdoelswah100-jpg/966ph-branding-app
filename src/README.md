# 966Ph Branding — source (since 1.1)

The app is still **one HTML file** when built (APK, laptop, web link). Only the source is split, so each part is easy to find and change.

| Folder / file | What is inside |
|---|---|
| `manifest.txt` | The order the files are joined in. **Do not reorder**: it is one shared script, a file can use what an earlier file defined. |
| `shell/` | The HTML around the app (`top.html`, `middle.html`, `bottom.html`). |
| `styles/app.css` | All the styles. |
| `js/core/` | The base of the app, in order: names (`01-names.js`), sizes (`03-sizes.js`), ad types (`05-ad-types.js`), language, storage, forms, totals, reports, checklists, home, backups, Excel, lock, pictures, photos, import, calculator. |
| `js/features/` | Custody (`custody.js`), maintenance (`maintenance.js`), warehouse (`warehouse.js`). |
| `js/updates/` | What each version added on top (v1.9 … v3.9), one file per version, in order. A later file may wrap a function of an earlier one. |
| `js/app/` | Users and supervisors' files, PDF, and the start of the app (last). |
| `data/` | `en.json` (English texts), `bimg.json` (built-in pictures), `logo.txt`, `cdocs.json`. |
| `vendor/jsQR.js` | QR reader (Apache-2.0). |

## Build
`python3 tools/build.py` → `dist/966Ph Branding vX.html` (laptop), `dist/966Ph Branding vX - AI-lite.html` (light, for AI tools) and `www/index.html` (APK + web link). It also checks the script syntax.

## Changing the app
- Edit the file that holds the part. New behaviour for a version goes in that part's file when it is a change of it, or in `js/updates/vX.Y.js` when it adds on top of several parts.
- Version: `VER` in `js/core/06-language.js`, changelog in `js/core/16-types-trash-backups.js`, `appVersion` / `versionCode` in `package.json` (versionCode always grows).
- Old patch scripts (`tools/legacy/`) worked on the single `src/app.html` of v3.9 and earlier; they are kept for history only.
- Tests: `tests/` (Playwright). `tests/compare.sh OLD.html NEW.html` runs everything on two builds and shows the differences.
