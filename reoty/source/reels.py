import sys
from engine import *
from data import WINNERS, RUNNERS

W, H = 1080, 1920
EXTRA = """
.lilac{background:var(--lilac);color:var(--ink)}
.lilac .hl>.blk{background:var(--purple)} .lilac .hl>.txt{color:var(--white)}
.namehl{white-space:normal;max-width:920px}
.namehl>.txt{display:block}
.bgstar{position:absolute;opacity:.09}
.scene.purple,.scene.ink,.scene.cream,.scene.lilac{background:transparent}
"""

def bg_star(size=900, right=-330, top=520):
    return (f'<img data-global class="bgstar" src="{A}star-white.svg" '
            f'style="width:{size}px;right:{right}px;top:{top}px;{an("drift", 0, 9, "ease-in-out", "both", "infinite alternate")}">')

def star(color, size, x, y, delay, rot=12, bob=True):
    anim = f"animation:spinin .7s var(--bounce) {delay:.2f}s both" + (f", bob 2.4s ease-in-out {delay+0.7:.2f}s infinite" if bob else "") + ";"
    return f'<img src="{A}star-{color}.svg" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;--rot:{rot}deg;{anim}">'

def scene(s, d, inner, cls="", ground_anim=True, out=True, ground="transparent"):
    g = f'<div style="position:absolute;inset:0;background:{ground};{an("wipeup", 0, 0.38, "var(--out)") if ground_anim and ground!="transparent" else ""}"></div>' if ground != "transparent" else ""
    wrap_out = an("outup", d - 0.28, 0.28, "var(--in)") if out else ""
    return (f'<div class="scene {cls}" data-s="{s}" data-d="{d}">{g}'
            f'<div style="position:absolute;inset:0;{wrap_out}">{inner}</div></div>')

def fl(text, delay, step=0.09):
    return f'<div class="line" data-fit="920" data-lines="1">{words_rise(text, delay, step)}</div>'

def fhl(text, delay):
    return f'<div data-fit="920" data-lines="1" style="margin-top:.04em">{hl(text, delay)}</div>'

def end_card(s, d, lines, closer, cls="purple"):
    head = "".join(fl(t, 0.15 + i*0.12, 0.08) for i, t in enumerate(lines[:-1]))
    head += fhl(lines[-1], 0.15 + (len(lines)-1)*0.12 + 0.1)
    logo = "logo-white" if cls in ("purple", "ink") else "logo-purple"
    inner = f"""
<div style="position:absolute;left:84px;top:330px;width:920px">
  <div class="disp" style="font-size:210px">{head}</div>
  <div style="margin-top:56px;font-size:46px;font-weight:600;line-height:1.25;max-width:820px;{an('fadeup', 1.0, .6)}">{closer}</div>
</div>
<div style="position:absolute;left:84px;top:1330px;display:flex;align-items:center;gap:44px;{an('fadeup', 1.25, .6)}">
  <img src="{A}{logo}.png" style="width:330px">
</div>
<div style="position:absolute;left:84px;top:1470px;{an('pop', 1.45, .5, 'var(--bounce)')}">
  <span class="pill" style="font-size:38px;padding:18px 36px;background:{'var(--white)' if cls in ('purple','ink') else 'var(--purple)'};color:{'var(--purple)' if cls in ('purple','ink') else 'var(--white)'}">voteretail.com</span>
</div>"""
    return scene(s, d, inner, cls, ground={"purple": "transparent", "ink": INK, "cream": CREAM, "lilac": LILAC}[cls], out=False)

def placing_scene(s, d, i, country, size, name, placing, cls):
    badge = "badge-reversed" if placing == "Winner" and cls in ("purple", "ink") else ("badge" if placing == "Winner" else "badge-runner")
    num_col = "var(--lilac)" if cls in ("purple", "ink") else "var(--mid)"
    kick_col = "var(--lilac)" if cls in ("purple", "ink") else "var(--purple)"
    inner = f"""
<div class="disp" style="position:absolute;left:84px;top:300px;font-size:150px;color:{num_col};{an('pop', 0.1, .5, 'var(--bounce)')}">0{i+1}</div>
<div class="kick" style="position:absolute;left:90px;top:520px;font-size:36px;color:{kick_col};{an('pop', 0.16, .45, 'var(--bounce)')}">{country}</div>
<div style="position:absolute;left:84px;top:600px;width:920px">
  <div class="disp" style="font-size:190px">{hl(name, 0.22, 0.32, cls='namehl', style='', txt_delay=0.34).replace('<span class="hl namehl"', '<span data-fit="920" data-lines="2" class="hl namehl"')}</div>
  <div style="margin-top:40px;font-size:46px;font-weight:600;line-height:1.25;{an('fadeup', 0.5, .5)}">{placing}. {size} Business Category</div>
</div>
<img src="{A}{badge}.png" style="position:absolute;right:120px;top:1130px;width:400px;--rot:10deg;{an('stamp', 0.55, .55, 'ease-out')}">"""
    ground = {"purple": "transparent", "ink": INK, "cream": CREAM, "lilac": LILAC}[cls]
    return scene(s, d, inner, cls, ground=ground)

# ---------------------------------------------------------------- R1 winners reveal
def r1():
    sc = []
    sc.append(scene(0, 2.7, f"""
<div class="kick" style="position:absolute;left:90px;top:400px;font-size:32px;color:var(--lilac);{an('pop', .1, .45, 'var(--bounce)')}">Retail Employer of the Year 2026</div>
<div class="disp" style="position:absolute;left:84px;top:490px;width:920px;font-size:250px">
  {fl('The', .25)}{fl('votes', .37)}{fl('are', .49)}{fhl('in.', .7)}
</div>
{star('lilac', 210, 560, 470, 1.0, 14)}{star('white', 96, 640, 1290, 1.25, -10)}""", "purple"))
    sc.append(scene(2.7, 2.4, f"""
<div style="position:absolute;left:84px;top:430px;width:920px">
  <div style="font-size:66px;font-weight:700;{an('pop', .35, .5, 'var(--bounce)')}">Twelve businesses.</div>
  <div class="disp" style="font-size:430px;color:var(--purple);line-height:.86;margin-top:10px;{an('pop', .6, .55, 'var(--bounce)')}">Zero</div>
  <div style="font-size:96px;font-weight:600;line-height:1;margin-top:6px;{an('pop', .85, .5, 'var(--bounce)')}">judges.</div>
  <div class="disp" style="font-size:150px;margin-top:70px">{hl('Just votes.', 1.25)}</div>
</div>
{star('purple', 150, 820, 360, 1.5, 16)}""", "cream", ground=CREAM))
    t = 5.1
    for i, (_, country, size, name) in enumerate(WINNERS):
        sc.append(placing_scene(t, 1.45, i, country, size, name, "Winner", "ink" if i % 2 else "purple"))
        t += 1.45
    sc.append(end_card(round(t, 2), 3.4, ["Take", "a bow,", "retail."], "Decided by the people who actually work there."))
    total = round(t + 3.4, 2)
    return dict(kind="video", name="R1-the-votes-are-in", body=bg_star() + "".join(sc), w=W, h=H, dur=total, bg=PURPLE, css=EXTRA)

# ---------------------------------------------------------------- R2 runners up
def r2():
    sc = []
    sc.append(scene(0, 2.7, f"""
<div class="kick" style="position:absolute;left:90px;top:400px;font-size:32px;color:var(--purple);{an('pop', .1, .45, 'var(--bounce)')}">Retail Employer of the Year 2026</div>
<div class="disp" style="position:absolute;left:84px;top:490px;width:920px;font-size:250px">
  {fl('Hats', .25)}{fl('off,', .37)}{fl('runners', .49)}{fhl('up.', .75)}
</div>
{star('purple', 190, 700, 470, 1.0, 14)}{star('mid', 90, 700, 1300, 1.25, -10)}""", "cream", ground=CREAM, ground_anim=False))
    t = 2.7
    for i, (_, country, size, name) in enumerate(RUNNERS):
        sc.append(placing_scene(t, 1.4, i, country, size, name, "Runner Up", "purple" if i % 2 else "cream"))
        t += 1.4
    sc.append(end_card(round(t, 2), 3.4, ["Backed by", "their own", "people."], "Six runners up. Every one of them backed by the people who work there."))
    total = round(t + 3.4, 2)
    return dict(kind="video", name="R2-hats-off-runners-up", body=bg_star() + "".join(sc), w=W, h=H, dur=total, bg=PURPLE, css=EXTRA)

# ---------------------------------------------------------------- R3 quote reel, template
def r3(quote_lines=("The quote", "goes here."), support="Short, specific and in their own words.",
       who="[Role], Travelex", name="R3-in-their-words-TEMPLATE", placing="Winner", sample=True):
    q = "".join(fl(l, .55 + i*.22, .09) for i, l in enumerate(quote_lines[:-1]))
    q += fhl(quote_lines[-1], .55 + (len(quote_lines)-1)*.22 + .1)
    badge = "badge" if placing == "Winner" else "badge-runner"
    tag = ('<div style="position:absolute;right:84px;top:250px;font-size:26px;font-weight:700;letter-spacing:.12em;'
           'color:var(--muted);border:3px dashed var(--muted);border-radius:999px;padding:10px 24px">SAMPLE TEXT</div>') if sample else ""
    sc = [scene(0, 7.2, f"""
{tag}
<div class="kick" style="position:absolute;left:90px;top:380px;font-size:34px;color:var(--purple);{an('pop', .1, .45, 'var(--bounce)')}">In their words</div>
<div style="position:absolute;left:76px;top:400px;font-size:380px;font-weight:700;color:var(--lilac);line-height:1;{an('pop', .25, .6, 'var(--bounce)')}">&ldquo;</div>
<div style="position:absolute;left:84px;top:700px;width:920px">
  <div class="disp" style="font-size:150px">{q}</div>
  <div style="margin-top:64px;font-size:44px;font-weight:500;line-height:1.3;max-width:860px;{an('fadeup', 1.6, .6)}">{support}</div>
  <div style="margin-top:30px;font-size:40px;font-weight:700;color:var(--purple);{an('fadeup', 1.9, .6)}">{who}</div>
</div>
<img src="{A}{badge}.png" style="position:absolute;right:90px;top:300px;width:240px;--rot:10deg;{an('stamp', 2.2, .55, 'ease-out')}">
""", "cream", ground=CREAM, ground_anim=False)]
    sc.append(end_card(7.2, 3.2, ["No judges.", "No panel.", "Just votes."], "Retail Employer of the Year 2026. Decided by the people who actually work there."))
    return dict(kind="video", name=name, body="".join(sc), w=W, h=H, dur=10.4, bg=PURPLE, css=EXTRA)

JOBS = {"r1": r1, "r2": r2, "r3": r3}

if __name__ == "__main__":
    which = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
    preview = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
    jobs = []
    for k in which:
        j = JOBS[k]()
        if preview:
            for t in preview:
                jobs.append(dict(j, kind="still", name=f"_prev-{j['name']}-{t}", t=t))
        else:
            jobs.append(j)
    run(jobs)
