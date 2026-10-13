import sys
from engine import *
from data import WINNERS, RUNNERS, slug
from reels import EXTRA

W, H = 1080, 1350
CSS = EXTRA + """
.slide{position:absolute;inset:0;overflow:hidden}
.namehl{white-space:normal;max-width:920px}
.cnt{font-size:22px;font-weight:600;letter-spacing:.14em}
.ph{position:absolute;border:4px dashed currentColor;border-radius:28px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:600;padding:30px}
.stripes{background:#E4D9F2;color:var(--ink)}
"""

def HL(text, fit=None, lines=1, cls=""):
    f = f' data-fit="{fit}" data-lines="{lines}"' if fit else ""
    return f'<span class="hl {cls}"{f}><span class="blk"></span><span class="txt">{text}</span></span>'

def ctx(ground):
    return {"purple": ("purple", PURPLE, "logo-white", "var(--lilac)", "var(--lilac)", "var(--soft)"),
            "cream": ("cream", CREAM, "logo-purple", "var(--purple)", "var(--mid)", "var(--muted)"),
            "ink": ("ink", INK, "logo-white", "var(--lilac)", "var(--lilac)", "var(--soft)")}[ground]

def chrome(ground, n=None, total=None):
    cls, bg, logo, kick, num, soft = ctx(ground)
    c = f'<div class="cnt" style="position:absolute;right:84px;top:92px;color:{kick}">{n:02d} / {total:02d}</div>' if n else ""
    return f'<img src="{A}{logo}.png" style="position:absolute;left:84px;top:76px;width:220px">{c}'

def slide(name, ground, inner, n=None, total=None, w=W, h=H, star_bg=False):
    cls, bg, *_ = ctx(ground)
    bgstar = f'<img src="{A}star-white.svg" style="position:absolute;width:760px;right:-300px;top:330px;opacity:.09;transform:rotate(-14deg)">' if star_bg else ""
    body = f'<div class="slide {cls}" style="background:{bg}">{bgstar}{chrome(ground, n, total)}{inner}</div>'
    return dict(kind="still", name=name, body=body, w=w, h=h, bg=bg, css=CSS)

def headline(lines, size, top, hl_last=True, fit=920):
    out = "".join(f'<div data-fit="{fit}" data-lines="1">{l}</div>' for l in lines[:-1])
    out += f'<div data-fit="{fit}" data-lines="1" style="margin-top:.05em">{HL(lines[-1]) if hl_last else lines[-1]}</div>'
    return f'<div class="disp" style="position:absolute;left:84px;top:{top}px;width:920px;font-size:{size}px">{out}</div>'

def swipe(ground):
    cls, bg, logo, kick, *_ = ctx(ground)
    col = "var(--white)" if ground != "cream" else "var(--purple)"
    txt = "var(--purple)" if ground != "cream" else "var(--white)"
    return f'<div style="position:absolute;left:84px;bottom:84px"><span class="pill" style="font-size:24px;padding:14px 30px;background:{col};color:{txt}">Swipe &rarr;</span></div>'

def sign_off(ground, top=None):
    cls, bg, logo, kick, num, soft = ctx(ground)
    col = "var(--white)" if ground != "cream" else "var(--purple)"
    txt = "var(--purple)" if ground != "cream" else "var(--white)"
    return f'<div style="position:absolute;left:84px;bottom:84px"><span class="pill" style="font-size:24px;padding:14px 30px;background:{col};color:{txt}">voteretail.com</span></div>'

# ---------------------------------------------------------------- C1 winners
def placing_slide(prefix, i, total, country, size, name, placing, ground):
    cls, bg, logo, kick, num, soft = ctx(ground)
    badge = ("badge-reversed" if ground != "cream" else "badge") if placing == "Winner" else "badge-runner"
    voice = "Decided by the people who actually work there."
    inner = f"""
<div class="disp" style="position:absolute;left:84px;top:200px;font-size:260px;color:{num}">0{i}</div>
<div class="kick" style="position:absolute;left:90px;top:500px;font-size:22px;color:{kick}">{country}, {size} Business Category</div>
<div class="disp" style="position:absolute;left:84px;top:556px;width:920px;font-size:170px">{HL(name + '.', 920, 2, 'namehl')}</div>
<div style="position:absolute;left:84px;bottom:96px;width:520px">
  <div style="font-size:34px;font-weight:700">{placing}, Retail Employer of the Year 2026</div>
  <div style="font-size:26px;margin-top:8px;color:{soft}">{voice}</div>
</div>
<img src="{A}{badge}.png" style="position:absolute;right:60px;bottom:64px;width:380px;transform:rotate(10deg)">"""
    return slide(f"{prefix}-{i+1:02d}-{slug(name)}", ground, inner, i + 1, total)

def c1():
    T = 8; out = []
    out.append(slide("C1-winners-01-cover", "purple", f"""
<div class="kick" style="position:absolute;left:90px;top:300px;font-size:24px;color:var(--lilac)">Retail Employer of the Year 2026</div>
{headline(["Meet your", "2026", "winners."], 190, 350)}
<div style="position:absolute;left:84px;top:1000px;font-size:38px;font-weight:600;width:560px;line-height:1.25">Six winners. Two countries. Zero judges.</div>
<img src="{A}badge-reversed.png" style="position:absolute;right:60px;bottom:64px;width:330px;transform:rotate(10deg)">
{swipe('purple')}""", 1, T, star_bg=True))
    for i, (_, c, s, n) in enumerate(WINNERS):
        out.append(placing_slide("C1-winners", i + 1, T, c, s, n, "Winner", "cream" if i % 2 else "purple"))
    out.append(slide("C1-winners-08-close", "cream", f"""
{headline(["Take", "a bow,", "retail."], 210, 300)}
<div style="position:absolute;left:84px;top:1000px;font-size:40px;font-weight:600;width:820px;line-height:1.3">Thank you to everyone who voted. It all happens again next year.</div>
{sign_off('cream')}""", T, T))
    return out

# ---------------------------------------------------------------- C2 runners up
def c2():
    T = 8; out = []
    out.append(slide("C2-runners-up-01-cover", "cream", f"""
<div class="kick" style="position:absolute;left:90px;top:300px;font-size:24px;color:var(--purple)">Retail Employer of the Year 2026</div>
{headline(["Hats off,", "runners", "up."], 200, 350)}
<div style="position:absolute;left:84px;top:1000px;font-size:38px;font-weight:600;width:560px;line-height:1.25">Six businesses their own people backed.</div>
<img src="{A}badge-runner.png" style="position:absolute;right:60px;bottom:64px;width:330px;transform:rotate(10deg)">
{swipe('cream')}""", 1, T))
    for i, (_, c, s, n) in enumerate(RUNNERS):
        out.append(placing_slide("C2-runners-up", i + 1, T, c, s, n, "Runner Up", "purple" if i % 2 else "cream"))
    out.append(slide("C2-runners-up-08-close", "purple", f"""
{headline(["Backed by", "their own", "people."], 190, 300)}
<div style="position:absolute;left:84px;top:960px;font-size:40px;font-weight:600;width:820px;line-height:1.3">Runner up is still a vote of confidence from the people who know you best.</div>
{sign_off('purple')}""", T, T, star_bg=True))
    return out

# ---------------------------------------------------------------- C3 what good looks like
SIX = [
    ("Career progression", "Career", "progression.", "Retail is a career, not a stopgap. The best employers show you the next step and help you take it."),
    ("Training and development", "Training that", "is real.", "Not a binder on day one. Real skills, taught by people who have done the job."),
    ("Work life balance", "A job and", "a life.", "Rosters that respect a life outside the store. Retail runs late. Good employers plan for it."),
    ("Recognition", "Being", "noticed.", "Someone seeing when you have done it well, and saying so out loud."),
    ("Leadership style", "Leaders worth", "following.", "Managers you would follow to the next store, and the one after that."),
    ("The team", "A team you", "show up for.", "The people on the floor with you. On a Saturday in December, they are everything."),
]
def c3():
    T = 8; out = []
    out.append(slide("C3-what-good-looks-like-01-cover", "purple", f"""
<div class="kick" style="position:absolute;left:90px;top:300px;font-size:24px;color:var(--lilac)">What makes a great retail employer</div>
{headline(["What", "good", "looks like."], 200, 350)}
<div style="position:absolute;left:84px;top:1010px;font-size:38px;font-weight:600;width:600px;line-height:1.25">Six things retail people tell us matter most.</div>
{swipe('purple')}""", 1, T, star_bg=True))
    for i, (k, a, b, body) in enumerate(SIX):
        out.append(slide(f"C3-what-good-looks-like-{i+2:02d}", "cream", f"""
<div class="disp" style="position:absolute;left:84px;top:190px;font-size:300px;color:var(--mid)">0{i+1}</div>
<div class="kick" style="position:absolute;left:90px;top:520px;font-size:24px;color:var(--purple)">{k}</div>
{headline([a, b], 130, 580)}
<div style="position:absolute;left:84px;top:900px;font-size:42px;font-weight:500;line-height:1.35;width:860px">{body}</div>
<img src="{A}star-purple.svg" style="position:absolute;right:110px;top:230px;width:150px;transform:rotate({[14,-10,20,-6,10,-16][i]}deg)">""", i + 2, T))
    out.append(slide("C3-what-good-looks-like-08-close", "purple", f"""
{headline(["Know a", "workplace that", "does all six?"], 160, 300)}
<div style="position:absolute;left:84px;top:930px;font-size:40px;font-weight:600;width:820px;line-height:1.3">Voting opens again next year. Start thinking about who you would back.</div>
{sign_off('purple')}""", T, T, star_bg=True))
    return out

# ---------------------------------------------------------------- C4 myths
MYTHS = [
    (("You have to", "enter."), "There is no entry form. No submission, no pitch deck. Retail staff and the public vote, and that is the whole process."),
    (("A panel picks", "the winner."), "There is no panel. The businesses with the most votes in their category win. That is it."),
    (("Only big", "businesses win."), "There are small, medium and large categories in both countries. In 2026, Travelex and Morrison Clothing took out the small categories."),
]
def c4():
    T = 5; out = []
    out.append(slide("C4-myths-01-cover", "purple", f"""
<div class="kick" style="position:absolute;left:90px;top:300px;font-size:24px;color:var(--lilac)">Retail Employer of the Year</div>
{headline(["Three", "myths.", "Busted."], 220, 350)}
<div style="position:absolute;left:84px;top:1040px;font-size:38px;font-weight:600;width:600px;line-height:1.25">Things people get wrong about this award.</div>
{swipe('purple')}""", 1, T, star_bg=True))
    for i, (m, t) in enumerate(MYTHS):
        out.append(slide(f"C4-myths-{i+2:02d}", "cream", f"""
<div style="position:absolute;left:84px;top:250px"><span class="pill" style="font-size:24px;padding:12px 28px;background:var(--ink);color:var(--white)">Myth</span></div>
<div class="disp" style="position:absolute;left:84px;top:340px;width:920px;font-size:130px;color:var(--muted)">{"".join(f'<div data-fit="920" data-lines="1"><span style="position:relative;display:inline-block">{l}<span style="position:absolute;left:-12px;right:-12px;top:44%;height:16px;background:var(--purple);border-radius:8px;transform:rotate({-3 if j else 2}deg)"></span></span></div>' for j, l in enumerate(m))}</div>
<div style="position:absolute;left:84px;top:760px"><span class="pill" style="font-size:24px;padding:12px 28px;background:var(--purple);color:var(--white)">Truth</span></div>
<div style="position:absolute;left:84px;top:850px;font-size:44px;font-weight:600;line-height:1.35;width:900px">{t}</div>""", i + 2, T))
    out.append(slide("C4-myths-05-close", "purple", f"""
{headline(["Now", "you", "know."], 240, 300)}
<div style="position:absolute;left:84px;top:1080px;font-size:40px;font-weight:600;width:820px;line-height:1.3">Decided by votes. Nothing else.</div>
{sign_off('purple')}""", T, T, star_bg=True))
    return out

# ---------------------------------------------------------------- posts
SAMPLE = '<div style="position:absolute;right:84px;top:84px;font-size:22px;font-weight:700;letter-spacing:.12em;border:3px dashed currentColor;border-radius:999px;padding:8px 20px;opacity:.75">SAMPLE TEXT</div>'
def quote_post(ground, name, who="[Role], Travelex", lines=("The quote", "goes here."), placing="Winner", sample=True):
    cls, bg, logo, kick, num, soft = ctx(ground)
    badge = ("badge-reversed" if ground != "cream" else "badge") if placing == "Winner" else "badge-runner"
    q = "".join(f'<div data-fit="920" data-lines="1">{l}</div>' for l in lines[:-1]) + f'<div data-fit="920" data-lines="2" style="margin-top:.05em">{HL(lines[-1], cls="namehl")}</div>'
    return slide(name, ground, f"""
{SAMPLE if sample else ''}
<div class="kick" style="position:absolute;left:90px;top:250px;font-size:24px;color:{kick}">In their words</div>
<div style="position:absolute;left:76px;top:250px;font-size:330px;font-weight:700;color:var(--lilac);line-height:1">&ldquo;</div>
<div class="disp" style="position:absolute;left:84px;top:520px;width:920px;font-size:120px">{q}</div>
<div style="position:absolute;left:84px;bottom:96px;width:560px">
  <div style="font-size:34px;font-weight:700">{who}</div>
  <div style="font-size:26px;margin-top:8px;color:{soft}">{placing}, Retail Employer of the Year 2026</div>
</div>
<img src="{A}{badge}.png" style="position:absolute;right:60px;bottom:64px;width:320px;transform:rotate(10deg)">""")

def badge_spotted():
    return slide("P-badge-spotted-TEMPLATE", "cream", f"""
<div class="ph stripes" style="left:84px;top:200px;width:912px;height:560px;font-size:30px;border-color:var(--purple)">Photo: the badge in the wild.<br>A shop window, a job ad, a team shirt, a cake.</div>
<img src="{A}badge.png" style="position:absolute;right:70px;top:600px;width:260px;transform:rotate(10deg)">
{headline(["Badge", "spotted."], 150, 820)}
<div style="position:absolute;left:84px;top:1130px;font-size:32px;font-weight:600;width:600px;line-height:1.3">Winners, show us where yours lives. Tag us and we will share it.</div>""")

# ---------------------------------------------------------------- stories
def story(name, ground, inner):
    cls, bg, logo, *_ = ctx(ground)
    body = f'<div class="slide {cls}" style="background:{bg}"><img src="{A}{logo}.png" style="position:absolute;left:84px;top:260px;width:240px">{inner}</div>'
    return dict(kind="still", name=name, body=body, w=1080, h=1920, bg=bg, css=CSS)

def stories():
    return [
        story("S-poll-would-you-vote", "purple", f"""
<div class="kick" style="position:absolute;left:90px;top:440px;font-size:28px;color:var(--lilac)">Quick one</div>
{headline(["Would you", "vote for your", "workplace?"], 170, 500)}
<div class="ph" style="left:140px;top:1120px;width:800px;height:300px;font-size:30px;color:var(--lilac)">Poll sticker<br>Yes, in a heartbeat / Ask me after payday</div>
<img src="{A}star-lilac.svg" style="position:absolute;right:100px;top:240px;width:150px;transform:rotate(14deg)">"""),
        story("S-question-tag-a-workplace", "cream", f"""
<div class="kick" style="position:absolute;left:90px;top:440px;font-size:28px;color:var(--purple)">Your turn</div>
{headline(["Tag a workplace", "that deserves", "a bow."], 150, 500)}
<div class="ph" style="left:140px;top:1080px;width:800px;height:300px;font-size:30px;color:var(--purple)">Question sticker<br>Which workplace deserves a bow?</div>
<img src="{A}star-purple.svg" style="position:absolute;right:100px;top:240px;width:140px;transform:rotate(-12deg)">"""),
    ]

def all_jobs():
    js = c1() + c2() + c3() + c4()
    js += [quote_post("purple", "P-quote-purple-TEMPLATE"), quote_post("cream", "P-quote-cream-TEMPLATE"), badge_spotted()]
    js += stories()
    return js

if __name__ == "__main__":
    run(all_jobs(), concurrency=6)
