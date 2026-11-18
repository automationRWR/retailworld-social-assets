import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
# usage: render_blog.py outdir [set ...]  -> outdir/<set>_<n>.png and .jpg (1080x1350 each)
HERE = os.path.dirname(os.path.abspath(__file__))
out = os.path.abspath(sys.argv[1]); os.makedirs(out, exist_ok=True)
sets = sys.argv[2:] or ['cv', 'role', 'interview', 'reoty', 'keep', 'speed', 'standout', 'brand']
with sync_playwright() as p:
    b = p.chromium.launch()
    for s in sets:
        pg = b.new_page(viewport={'width': 1080 * 8, 'height': 1350})
        pg.goto('file://' + os.path.join(HERE, 'blog.html') + '#' + s)
        pg.wait_for_function('document.fonts.status === "loaded" && window.SLIDES > 0')
        pg.wait_for_timeout(500)
        n = pg.evaluate('window.SLIDES')
        for i in range(n):
            png = os.path.join(out, '%s_%d.png' % (s, i + 1))
            pg.screenshot(path=png, clip={'x': i * 1080, 'y': 0, 'width': 1080, 'height': 1350})
            Image.open(png).convert('RGB').save(png[:-4] + '.jpg', quality=95)
        pg.close(); print(s, n)
    b.close()
