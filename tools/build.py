"""Build 966Ph Branding from src/.
  python3 tools/build.py            -> dist/966Ph Branding.html (laptop) + www/index.html (APK)
The app source is src/app.html (light version: logo and built-in images as placeholders).
"""
import os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(R, 'src/app.html'), encoding='utf-8').read()
logo = open(os.path.join(R, 'src/logo.txt'), encoding='utf-8').read().strip()
bimg = open(os.path.join(R, 'src/bimg.json'), encoding='utf-8').read().strip()
for k, n in (('__LOGO_DATA_URI__', None), ('/*__BIMG__*/{}', 1), ('/*__FONT_FACE__*/', 1)):
    if n and s.count(k) != n: sys.exit('placeholder count wrong: ' + k)
jq = open(os.path.join(R, 'src/vendor/jsQR.js'), encoding='utf-8').read().replace('</script', '<\\/script')
full = s.replace('__LOGO_DATA_URI__', logo).replace('/*__BIMG__*/{}', '/*__BIMG__*/' + bimg).replace('<script>/*__JSQR__*/</script>', '<script>/* jsQR 1.4.0 (Apache-2.0) https://github.com/cozmo/jsQR */\n' + jq + '</script>', 1)
ver = re.search(r"VER='(v[\d.]+)'", s).group(1)
os.makedirs(os.path.join(R, 'dist'), exist_ok=True)
out = os.path.join(R, 'dist', '966Ph Branding ' + ver + '.html')
open(out, 'w', encoding='utf-8').write(full)
ff = '@font-face{font-family:"Cairo";src:url("fonts/Cairo.ttf") format("truetype");font-weight:200 1000;font-display:swap}'
open(os.path.join(R, 'www/index.html'), 'w', encoding='utf-8').write(full.replace('/*__FONT_FACE__*/', ff))
# syntax check
i = s.rfind('<script>'); j = s.rfind('</script>')
js = os.path.join(R, 'dist', '_check.js'); open(js, 'w', encoding='utf-8').write(s[i + 8:j])
r = subprocess.run(['node', '--check', js]); os.remove(js)
if r.returncode: sys.exit('JS syntax error')
print('built', ver, '->', out, 'and www/index.html')
