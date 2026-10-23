#!/bin/bash
# Run every test on the base build and on the new build, then diff the full outputs.
# usage: tests/compare.sh BASE.html NEW.html   (run from the work folder that holds the fixtures)
B="$1"; N="$2"; mkdir -p cmp
for t in t6 t7 t9 t10 t11 t12 t13 t14 test3; do
  for k in base new; do
    [ $k = base ] && cp "$B" full28.html || cp "$N" full28.html
    timeout 300 python3 $t.py 2>&1 | grep -v "agent-proxy\|connect_rejected\|Allowed domains\|For details\|and [0-9]* more\|^- " \
      | sed -E 's/[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9:.]+Z?/<TIME>/g; s/[0-9]{13}/<ID>/g; s/blob:[^"]*/<BLOB>/g' > cmp/$t.$k.txt
  done
  if diff -q cmp/$t.base.txt cmp/$t.new.txt >/dev/null; then echo "$t SAME"; else echo "$t DIFF"; diff cmp/$t.base.txt cmp/$t.new.txt | head -20; fi
done
cp "$N" full28.html

echo "--- computed styles (10 screens, light + dark)"
python3 /home/claude/apk/tests/cssdiff.py "$B" "$N" 2>&1 | grep -E "^(same|DIFF)" | grep -c same | sed "s/^/same screens: /"
python3 /home/claude/apk/tests/cssdiff.py "$B" "$N" 2>&1 | grep "^DIFF" | cut -c1-300

echo "--- totals/report functions"
python3 /home/claude/apk/tests/unitcmp.py "$B" "$N" 2>&1 | grep -E "^(same|DIFF)"
