import os, sys
from playwright.sync_api import sync_playwright
# usage: render_carousel.py file.html outprefix  -> outprefix_1.png ... (1080x1350 each)
src, pre = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 6480, 'height': 1350})
    pg.goto('file://' + src); pg.wait_for_function('document.fonts.status === "loaded" && typeof render === "function"')
    pg.wait_for_timeout(400)
    n = pg.evaluate('window.SLIDES')
    for i in range(n):
        pg.screenshot(path='%s_%d.png' % (pre, i + 1), clip={'x': i * 1080, 'y': 0, 'width': 1080, 'height': 1350})
    b.close()
print('ok', n)
