"""Fill a Google review template and render it.

usage: python3 source/motion/make_review.py <reel|static|grid> <config.json> <out_basename>
  reel   -> <out>.mp4          (1080x1920, 14s)
  static -> <out>.png          (1080x1350)
  grid   -> <out>.mp4 + <out>.png still (1080x1350, 8s loop)

config.json keys
  reel:   recruiter, date, preview, bubbles (2-3 strings), ctaWord
  static: recruiter, hook, sub, foot
  grid:   recruiter, quote
Wrap one phrase per line in {curly braces} to highlight it. Never include the reviewer's name.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
kind, cfg_path, out = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
src = os.path.join(HERE, {'reel': 'review_reel.html', 'static': 'review_static.html', 'grid': 'review_grid.html'}[kind])
cfg = json.load(open(cfg_path))
for k, v in cfg.items():
    for s in (v if isinstance(v, list) else [v]):
        if isinstance(s, str) and '—' in s:
            sys.exit('No em dashes allowed: ' + k)
html = open(src, encoding='utf-8').read()
html, n = re.subn(r'const REVIEW = \{.*?\n\};', 'const REVIEW = ' + json.dumps(cfg, ensure_ascii=False) + ';', html, count=1, flags=re.S)
if n != 1:
    sys.exit('REVIEW block not found in ' + src)
tmp = os.path.join(HERE, '_filled_%s.html' % kind)  # must sit next to lib.js and a/
open(tmp, 'w', encoding='utf-8').write(html)
try:
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    if kind == 'reel':
        subprocess.run([sys.executable, os.path.join(HERE, 'render.py'), tmp, out + '.mp4'], check=True)
    elif kind == 'static':
        subprocess.run([sys.executable, os.path.join(HERE, 'render_post.py'), tmp, out + '.mp4'], check=True, env=dict(os.environ, STILL_ONLY='1'))
    else:
        subprocess.run([sys.executable, os.path.join(HERE, 'render_post.py'), tmp, out + '.mp4', '4'], check=True)
finally:
    os.remove(tmp)
    import shutil; shutil.rmtree(out + '.mp4_frames', ignore_errors=True)
print('done', out)
