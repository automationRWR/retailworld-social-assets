import sys
from engine import *
from data import WINNERS, slug
from reels import EXTRA, fl, fhl, star, bg_star

W, H = 1080, 1350

def namehl(text, d):
    return hl(text, d, cls="namehl").replace('<span class="hl namehl"', '<span data-fit="920" data-lines="2" class="hl namehl"', 1)

def loop_fade(colour, at, dur):
    # cover fades in at the very end so the loop restarts cleanly from an empty ground
    return f'<div style="position:absolute;inset:0;background:{colour};z-index:20;{an("fade", at, dur, "linear")}"></div>'

def take_a_bow(country, size, name, dur=8.0):
    long = len(name) > 9
    if long:
        head = fl("Take a bow,", .5) + f'<div style="margin-top:.04em">{namehl(name + ".", .85)}</div>'
    else:
        head = fl("Take", .5) + fl("a bow,", .62) + fhl(name + ".", .85)
    body = f"""{bg_star(820, -300, 300)}
<div class="scene purple" data-s="0" data-d="{dur}">
  <img src="{A}logo-white.png" style="position:absolute;left:84px;top:76px;width:252px;{an('fadeup', .1, .5)}">
  <div style="position:absolute;right:84px;top:82px;{an('pop', .2, .5, 'var(--bounce)')}"><span class="pill" style="font-size:22px;padding:13px 26px;background:var(--white);color:var(--purple)">voteretail.com</span></div>
  <div class="kick" style="position:absolute;left:90px;top:300px;font-size:22px;color:var(--lilac);{an('pop', .35, .45, 'var(--bounce)')}">The votes are in</div>
  <div class="disp" style="position:absolute;left:84px;top:356px;width:920px;font-size:150px">{head}</div>
  <div style="position:absolute;left:84px;bottom:84px;width:600px;display:flex;flex-direction:column;gap:8px">
    <div style="font-size:33px;font-weight:700;{an('fadeup', 1.5, .5)}">Retail Employer of the Year 2026</div>
    <div style="font-size:23px;font-weight:600;white-space:nowrap;color:var(--lilac);{an('fadeup', 1.65, .5)}">Winner. {country}, {size} Business Category</div>
    <div style="font-size:24px;color:var(--soft);{an('fadeup', 1.8, .5)}">Decided by the people who actually work there.</div>
  </div>
  <img src="{A}badge-reversed.png" style="position:absolute;right:56px;bottom:70px;width:310px;--rot:10deg;{an('stamp', 2.0, .55, 'ease-out')}">
  {star('lilac', 92, 912, 196, 2.5, 14)}
  {loop_fade(PURPLE, dur - .45, .45)}
</div>"""
    code = "NZ" if country == "New Zealand" else "AU"
    return dict(kind="video", name=f"A-take-a-bow-{code}-{size}-{slug(name)}", body=body, w=W, h=H, dur=dur, bg=PURPLE, css=EXTRA)

def judges_zero(dur=7.0):
    digits = "".join(f'<div style="height:560px;line-height:560px">{d}</div>' for d in "9876543210")
    body = f"""
<div class="scene cream" data-s="0" data-d="{dur}">
  <div class="kick" style="position:absolute;left:90px;top:120px;font-size:22px;color:var(--purple);{an('pop', .05, .45, 'var(--bounce)')}">Retail Employer of the Year</div>
  <div style="position:absolute;left:84px;top:180px;font-size:64px;font-weight:700;color:var(--ink);{an('pop', .2, .5, 'var(--bounce)')}">Judges on the panel:</div>
  <div style="position:absolute;left:60px;top:290px;height:560px;overflow:hidden">
    <div class="disp" style="font-size:640px;color:var(--purple);letter-spacing:-0.05em;--to:-5040px;{an('roll', .45, 1.7, 'cubic-bezier(.3,0,.1,1)')}">{digits}</div>
  </div>
  <div style="position:absolute;left:520px;top:420px;--rot:-12deg;{an('stamp', 2.15, .5, 'ease-out')}">
    <div style="background:var(--ink);color:var(--white);border-radius:999px;padding:18px 34px;font-size:34px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;transform:rotate(-8deg)">Not one</div>
  </div>
  {star('purple', 130, 860, 300, 2.3, 16)}{star('mid', 70, 800, 760, 2.45, -12)}
  <div style="position:absolute;left:84px;top:900px;font-size:52px;font-weight:600;color:var(--ink);{an('fadeup', 2.5, .5)}">Votes that decided it:</div>
  <div class="disp" style="position:absolute;left:84px;top:980px;font-size:140px">{hl('All of them.', 2.75)}</div>
  <div style="position:absolute;left:84px;bottom:76px;display:flex;align-items:center;gap:30px;{an('fadeup', 3.2, .5)}">
    <img src="{A}logo-purple.png" style="width:230px"><span class="pill" style="font-size:22px;padding:12px 24px;background:var(--purple);color:var(--white)">voteretail.com</span>
  </div>
  {loop_fade(CREAM, dur - .45, .45)}
</div>"""
    return dict(kind="video", name="A-judges-zero", body=body, w=W, h=H, dur=dur, bg=CREAM, css=EXTRA)

def christmas(dur=7.5):
    body = f"""{bg_star(820, -300, 380)}
<div class="scene purple" data-s="0" data-d="{dur}">
  {star('lilac', 150, 820, 150, .2, 14)}{star('white', 80, 700, 1020, .45, -10)}{star('lilac', 60, 960, 760, .6, 20)}
  <div class="kick" style="position:absolute;left:90px;top:150px;font-size:22px;color:var(--lilac);{an('pop', .15, .45, 'var(--bounce)')}">Peak season</div>
  <div style="position:absolute;left:84px;top:210px;width:920px">
    <div style="font-size:60px;font-weight:600;line-height:1.15">{words_rise('To everyone working', .35, .08)}</div>
    <div class="disp" style="font-size:150px;margin-top:14px">{fl('the Christmas', .6)}{fl('trade,', .75)}</div>
    <div class="disp" style="font-size:190px;margin-top:20px" data-fit="920" data-lines="1">{hl('thank you.', 1.1)}</div>
    <div style="margin-top:56px;font-size:40px;font-weight:500;line-height:1.3;max-width:760px;color:var(--soft);{an('fadeup', 1.7, .6)}">The best places to work are made by the people in them. That is you.</div>
  </div>
  <div style="position:absolute;left:84px;bottom:76px;display:flex;align-items:center;gap:30px;{an('fadeup', 2.1, .5)}">
    <img src="{A}logo-white.png" style="width:230px"><span class="pill" style="font-size:22px;padding:12px 24px;background:var(--white);color:var(--purple)">voteretail.com</span>
  </div>
  {loop_fade(PURPLE, dur - .45, .45)}
</div>"""
    return dict(kind="video", name="A-christmas-thank-you", body=body, w=W, h=H, dur=dur, bg=PURPLE, css=EXTRA)

def all_jobs():
    js = [take_a_bow(c, s, n) for _, c, s, n in WINNERS]
    js += [judges_zero(), christmas()]
    return js

if __name__ == "__main__":
    jobs = all_jobs()
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        t = float(sys.argv[2]) if len(sys.argv) > 2 else 5
        jobs = [dict(j, kind="still", name="_prev-" + j["name"], t=t) for j in jobs]
    run(jobs)
