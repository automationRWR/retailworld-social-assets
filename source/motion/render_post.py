import os, sys, shutil, subprocess
from playwright.sync_api import sync_playwright
# usage: render_post.py file.html out.mp4 [still_time]   -> out.mp4 + out.png (still)
src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
still = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
FPS = 30
fr = out + '_frames'; shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    pg.goto('file://' + src); pg.wait_for_function('document.fonts.status === "loaded" && typeof render === "function"')
    pg.wait_for_timeout(300)
    pg.evaluate('render(%f)' % still); pg.screenshot(path=out[:-4] + '.png')
    if os.environ.get('STILL_ONLY'):
        b.close(); sys.exit()
    n = int(pg.evaluate('window.DURATION') * FPS)
    for i in range(n):
        pg.evaluate('render(%f)' % (i / FPS)); pg.screenshot(path=os.path.join(fr, 'f%04d.jpg' % i), type='jpeg', quality=94)
    b.close()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(fr, 'f%04d.jpg'), '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'medium', '-movflags', '+faststart', out], check=True)
shutil.rmtree(fr); print('ok', out)
