"""REOTY social motion engine.

Scenes are absolutely positioned divs with data-s (start, seconds) and data-d (duration).
Everything inside a scene animates with CSS keyframes whose delays are relative to the scene
start. Each frame, every animation is paused and seeked, so output is frame exact.
"""
import asyncio, os, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "pages")
FRAMES = os.path.join(ROOT, "frames")
OUT = os.path.join(ROOT, "out")
A = "../assets/"   # asset path from pages/

INK, PURPLE, MID, LILAC, CREAM, WHITE, MUTED = "#2A0E3F", "#482861", "#7B5A9E", "#C9B3E6", "#FBF5EC", "#FFFFFF", "#5B4A6B"
SOFT_ON_PURPLE = "#E4D9F2"   # solid tint for secondary text on purple

BASE_CSS = """
@font-face{font-family:'Bricolage Grotesque';font-weight:200 800;src:url(../fonts/bricolage-grotesque-latin-opsz-normal.woff2) format('woff2')}
@font-face{font-family:Poppins;font-weight:400;src:url(../fonts/poppins-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Poppins;font-weight:500;src:url(../fonts/poppins-latin-500-normal.woff2) format('woff2')}
@font-face{font-family:Poppins;font-weight:600;src:url(../fonts/poppins-latin-600-normal.woff2) format('woff2')}
@font-face{font-family:Poppins;font-weight:700;src:url(../fonts/poppins-latin-700-normal.woff2) format('woff2')}
:root{--ink:#2A0E3F;--purple:#482861;--mid:#7B5A9E;--lilac:#C9B3E6;--cream:#FBF5EC;--white:#FFFFFF;--muted:#5B4A6B;--soft:#E4D9F2;
 --display:'Bricolage Grotesque',Poppins,sans-serif;--body:Poppins,sans-serif;
 --bounce:cubic-bezier(.2,1.45,.35,1);--out:cubic-bezier(.16,1,.3,1);--in:cubic-bezier(.7,0,.84,0)}
html,body{margin:0;padding:0;-webkit-font-smoothing:antialiased;font-family:var(--body)}
*{box-sizing:border-box}
.stage{position:relative;overflow:hidden}
.scene{position:absolute;inset:0;overflow:hidden}
.purple{background:var(--purple);color:var(--white)}
.ink{background:var(--ink);color:var(--white)}
.cream{background:var(--cream);color:var(--ink)}
.disp{font-family:var(--display);font-weight:800;text-transform:uppercase;letter-spacing:-0.03em;line-height:.92}
.kick{font-family:var(--body);font-weight:600;text-transform:uppercase;letter-spacing:.22em;display:flex;align-items:center;gap:.7em}
.kick::before{content:"";width:.62em;height:.62em;border-radius:50%;background:currentColor;flex:none}
.pill{display:inline-block;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;white-space:nowrap}
.hl{position:relative;display:inline-block;white-space:nowrap;padding:.02em .18em .08em .18em;transform:rotate(-1.5deg)}
.hl>.blk{position:absolute;inset:0;border-radius:.14em;transform-origin:left center}
.hl>.txt{position:relative;display:inline-block}
.purple .hl>.blk,.ink .hl>.blk{background:var(--white)} .purple .hl>.txt{color:var(--purple)} .ink .hl>.txt{color:var(--ink)}
.cream .hl>.blk{background:var(--purple)} .cream .hl>.txt{color:var(--white)}
.line{display:block;overflow:hidden;padding:0 .04em .06em 0;margin-bottom:-.06em}
.w{display:inline-block}
img{display:block}

@keyframes rise{from{transform:translateY(110%)}to{transform:none}}
@keyframes pop{0%{transform:translateY(.5em) scale(.5);opacity:0}60%{opacity:1}100%{transform:none;opacity:1}}
@keyframes fadeup{from{transform:translateY(30px);opacity:0}to{transform:none;opacity:1}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes swipe{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes stamp{0%{transform:scale(2.4) rotate(-30deg);opacity:0}55%{transform:scale(.9) rotate(var(--rot,10deg));opacity:1}75%{transform:scale(1.05) rotate(var(--rot,10deg))}100%{transform:scale(1) rotate(var(--rot,10deg));opacity:1}}
@keyframes spinin{from{transform:scale(0) rotate(-200deg)}to{transform:scale(1) rotate(var(--rot,0deg))}}
@keyframes drift{from{transform:rotate(-14deg)}to{transform:rotate(16deg)}}
@keyframes bob{0%,100%{transform:translateY(0) rotate(var(--rot,0deg))}50%{transform:translateY(-14px) rotate(calc(var(--rot,0deg) + 8deg))}}
@keyframes wipeup{from{transform:translateY(100%)}to{transform:none}}
@keyframes wipedown{from{transform:none}to{transform:translateY(100%)}}
@keyframes outup{from{transform:none;opacity:1}to{transform:translateY(-80px);opacity:0}}
@keyframes outscale{from{transform:none;opacity:1}to{transform:scale(1.15);opacity:0}}
@keyframes slidein{from{transform:translateX(110%)}to{transform:none}}
@keyframes roll{from{transform:translateY(0)}to{transform:translateY(var(--to))}}
@keyframes shake{0%,100%{transform:none}25%{transform:translateX(-8px) rotate(-1deg)}75%{transform:translateX(8px) rotate(1deg)}}
"""

def an(name, delay, dur=0.6, ease="var(--out)", fill="both", extra=""):
    """Inline animation style. delay/dur in seconds, relative to the scene start."""
    return f"animation:{name} {dur:.3f}s {ease} {delay:.3f}s {fill}{(' '+extra) if extra else ''};"

def words_rise(text, start, step=0.09, cls="", dur=0.55, style=""):
    """One line of words, each rising from behind a mask."""
    out = []
    for i, w in enumerate(text.split(" ")):
        out.append(f'<span class="line" style="display:inline-block;vertical-align:top;margin-right:.22em"><span class="w" style="{an("rise", start+i*step, dur)}">{w}</span></span>')
    return f'<span class="{cls}" style="{style}">{"".join(out)}</span>'

def hl(text, start, swipe=0.35, cls="", style="", txt_delay=None):
    """Highlighter block that swipes in, text pops on top."""
    td = start + swipe*0.55 if txt_delay is None else txt_delay
    return (f'<span class="hl {cls}" style="{style}"><span class="blk" style="{an("swipe", start, swipe, "var(--out)")}"></span>'
            f'<span class="txt" style="{an("pop", td, 0.5, "var(--bounce)")}">{text}</span></span>')

SEEK_JS = """
window.__seek = (t) => {
  for (const sc of document.querySelectorAll('[data-s]')) {
    const s = +sc.dataset.s, d = +sc.dataset.d;
    const on = t >= s && t < s + d;
    sc.style.visibility = on ? 'visible' : 'hidden';
    const local = Math.max(0, t - s) * 1000;
    for (const a of sc.getAnimations({subtree: true})) { a.pause(); a.currentTime = local; }
  }
  for (const el of document.querySelectorAll('[data-global]')) {
    for (const a of el.getAnimations({subtree: true})) { a.pause(); a.currentTime = t * 1000; }
  }
};
window.__fit = () => {
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = 1e6; }
  // shrink [data-fit] text until it fits its max width (and max lines, if given)
  for (const el of document.querySelectorAll('[data-fit]')) {
    const max = +el.dataset.fit, lines = +(el.dataset.lines || 1);
    let size = parseFloat(getComputedStyle(el).fontSize);
    const lh = () => parseFloat(getComputedStyle(el).lineHeight) || size * 0.92;
    let guard = 0; const floor = size * 0.35;
    while (guard++ < 400 && size > floor) {
      const inner = el.querySelector('.txt');
      const tooWide = el.scrollWidth > max + 0.5 || el.offsetWidth > max + 0.5 || (inner && inner.scrollWidth > inner.clientWidth + 0.5);
      const tooTall = el.offsetHeight > lh() * lines + size * 0.35;
      if (!tooWide && !tooTall) break;
      size -= 1; el.style.fontSize = size + 'px';
    }
    el.dataset.size = size;
  }
};
"""

def page(name, body, w, h, bg=PURPLE, extra_css=""):
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}{extra_css}"
            f"body{{width:{w}px;height:{h}px;background:{bg}}}</style><script>{SEEK_JS}</script></head>"
            f"<body><div class='stage' style='width:{w}px;height:{h}px;background:{bg}'>{body}</div></body></html>")
    p = os.path.join(PAGES, name + ".html")
    open(p, "w").write(html)
    return p

async def _prep(pg, path):
    await pg.goto("file://" + path)
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_timeout(150)
    await pg.evaluate("window.__fit()")

async def _video(browser, name, body, w, h, dur, fps, bg, extra_css):
    p = page(name, body, w, h, bg, extra_css)
    fd = os.path.join(FRAMES, name)
    shutil.rmtree(fd, ignore_errors=True); os.makedirs(fd)
    pg = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    await _prep(pg, p)
    n = int(round(dur * fps))
    for i in range(n):
        await pg.evaluate(f"window.__seek({i / fps})")
        await pg.screenshot(path=os.path.join(fd, f"f{i:05d}.jpg"), type="jpeg", quality=95)
    await pg.close()
    out = os.path.join(OUT, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(fd, "f%05d.jpg"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    return out

async def _still(browser, name, body, w, h, bg, extra_css, t=None):
    p = page(name, body, w, h, bg, extra_css)
    pg = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    await _prep(pg, p)
    await pg.evaluate(f"window.__seek({t if t is not None else 1000})")
    out = os.path.join(OUT, name + ".png")
    await pg.screenshot(path=out, type="png")
    await pg.close()
    return out

def run(jobs, concurrency=4):
    """jobs: list of dicts {kind: video|still, name, body, w, h, dur, fps, bg, css, t}"""
    from playwright.async_api import async_playwright
    async def main():
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(concurrency)
            async def one(j):
                async with sem:
                    if j["kind"] == "video":
                        r = await _video(browser, j["name"], j["body"], j["w"], j["h"], j["dur"], j.get("fps", 30), j.get("bg", PURPLE), j.get("css", ""))
                    else:
                        r = await _still(browser, j["name"], j["body"], j["w"], j["h"], j.get("bg", PURPLE), j.get("css", ""), j.get("t"))
                    print("done", r, flush=True)
            await asyncio.gather(*[one(j) for j in jobs])
            await browser.close()
    asyncio.run(main())
