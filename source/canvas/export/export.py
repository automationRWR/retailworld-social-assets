import os, re, sys, glob, shutil
from playwright.sync_api import sync_playwright

SRC, ASSETS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
WORK = os.path.join(os.path.dirname(OUT.rstrip('/')), 'work')
shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
BLOBS = {
 '224e3061193210f17b6c1f6a26e0892e': 'logo.png', 'cf3136879b228d16e56fbb0a06d0b5df': 'logo_white.png',
 '7bbc97d34fd273dbd0b9cbf7a4a61e75': 'poppins-latin-300-normal.woff2', '3487c72fb714c51623709dd964151ec2': 'poppins-latin-300-italic.woff2',
 'b4dad672053bd01e9f0a5880908bc91a': 'poppins-latin-400-normal.woff2', '4a731a7dca3a3ca607aefd49b2ac7d46': 'poppins-latin-500-normal.woff2',
 'faf3f69bf3ab73e90b25a6d2e02a39cd': 'poppins-latin-600-normal.woff2', '4ae2377146376c5858b18a78faa76a7e': 'poppins-latin-700-normal.woff2'}
for f in BLOBS.values(): shutil.copy(os.path.join(ASSETS, f), WORK)
shutil.copy(os.path.join(os.path.dirname(__file__), 'support.js'), WORK)

# board: (file, export name, number of 540x675 slides or None for a single 1080x1350 board, gap columns to skip)
BOARDS = [
 ('Main.dc.html', '00_Look', None),
 ('Walk.dc.html', '01_Reintroduce', [(i * 540) for i in range(6)]),
 ('Travel.dc.html', '02_Roster', [(i * 540) for i in range(3)]),
 ('Line.dc.html', '03_FollowTheLine', [(i * 540) for i in range(4)]),
 ('Zoom.dc.html', '04_ThisClose', [(i * 540) for i in range(4)]),
 ('Blast.dc.html', '05_NoSarah', [(i * 540) for i in range(4)]),
 ('Meme.dc.html', '06_Bloodline', [(i * 540) for i in range(3)]),
 ('Tour.dc.html', '07_SevenLocations', [(i * 540) for i in range(8)]),
 ('Review.dc.html', '08_HypeMan', [0] + [620 + i * 540 for i in range(3)]),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    for fn, name, xs in BOARDS:
        s = open(os.path.join(SRC, fn)).read()
        for k, v in BLOBS.items(): s = s.replace('/_blob/' + k, v)
        s = re.sub(r'border-(right|left): 1px dashed #[0-9A-Fa-f]{6,8}', 'border-\\1: none', s)
        s = s.replace('border-right: 1px dashed #00000033', 'border-right: none')
        path = os.path.join(WORK, fn); open(path, 'w').write(s)
        pg = b.new_page(viewport={'width': 4400, 'height': 1400}, device_scale_factor=(1 if xs is None else 2))
        pg.goto('file://' + path); pg.wait_for_function('window.__ready === true', timeout=20000)
        if xs is None:
            pg.screenshot(path=os.path.join(OUT, name + '.png'), clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
        else:
            for i, x in enumerate(xs):
                pg.screenshot(path=os.path.join(OUT, '%s_%d.png' % (name, i + 1)), clip={'x': x, 'y': 0, 'width': 540, 'height': 675})
        pg.close()
    b.close()
print(len(os.listdir(OUT)), 'images')
