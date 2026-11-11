"""v1.6: gondola acrylic helpers moved next to the shelf-type helpers (they are used by the load-time migration)."""
import os, sys, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
a = s.index("// Old Turkish gondola: what is needed (old items = full)\n")
b = s.index("pkv=(r,k)=>+r[k+'p']||0;", a) + len("pkv=(r,k)=>+r[k+'p']||0;")
blk = s[a:b]; s = s[:a] + s[b:]
blk = blk.replace(":egAO(r,s)?qn(r):(r.pq!==undefined&&r.pq!==null&&r.pq!==''?Math.max(0,Math.round(+r.pq||0)):qn(r))", ":egAO(r,s)?(r.q==null?1:(+r.q||0)):(r.pq!==undefined&&r.pq!==null&&r.pq!==''?Math.max(0,Math.round(+r.pq||0)):(r.q==null?1:(+r.q||0)))")
assert '(r.q==null?1:(+r.q||0))' in blk
k = s.index("const RSHT=['fh','wh','ec','eg','md'],RSAME=")
k = s.index('\n', k) + 1
s = s[:k] + blk + '\n' + s[k:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
