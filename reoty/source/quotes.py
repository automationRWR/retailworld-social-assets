"""Employee quotes from the 2026 voting form, anonymised. Trimmed only; typos fixed."""
import sys
from engine import run
from reels import r3
from stills import quote_post

# (slug, business, placing, kind, display lines, support line, who)
Q = [
 ("Flo-and-Frankie", "Flo & Frankie", "Winner", "reel",
  ["The culture", "isn’t something", "written on a wall,", "it’s the team."],
  "Everyone’s invested, everyone pitches in, and there’s a genuine warmth that’s hard to fake and even harder to build.",
  "Team member, Flo & Frankie"),
 ("2degrees-Retail", "2degrees Retail", "Winner", "reel",
  ["They know me,", "and I know", "them."],
  "I feel like I’m part of the team.",
  "Team member, 2degrees Retail"),
 ("Essilor-Luxottica", "Essilor Luxottica", "Winner", "reel",
  ["Never felt such", "support at a job", "before."],
  "I have been an employee for 12 months. I thoroughly enjoy going to work each shift.",
  "Team member, Essilor Luxottica"),
 ("Travelex-NZ", "Travelex", "Winner", "reel",
  ["It has challenged me,", "promoted me and", "grown me."],
  "This company has been home to me for 11 years, starting in the NZ business and now Australia.",
  "Team member, Travelex"),
 ("Travelex-AU", "Travelex", "Winner", "reel",
  ["Now a career", "which I am", "proud of."],
  "Fell in love with the culture and how fun it was to talk to people who were going on holidays as my job.",
  "Manager, Travelex Australia"),
 ("Crown-Currency-Exchange", "Crown Currency Exchange", "Runner Up", "card",
  ["Nobody is", "above another."],
  "A casual consultant can call the CEO for help.",
  "Team member, Crown Currency Exchange"),
 ("Swanndri", "Swanndri", "Runner Up", "card",
  ["We look out", "for each other."],
  "There’s this vibe to them that makes you genuinely love coming back.",
  "Team member, Swanndri"),
 ("Foodstuffs", "Foodstuffs", "Runner Up", "card",
  ["I love coming", "to work every day."],
  "Foodstuffs is a fun place to work, great culture, great people.",
  "Team member, Foodstuffs"),
 ("VAPO", "VAPO", "Runner Up", "card",
  ["Not planning on", "leaving anytime", "soon."],
  "I’ve been here for 6 years.",
  "Team member, VAPO"),
]

def jobs():
    out = []
    for i, (slug, biz, placing, kind, lines, support, who) in enumerate(Q):
        if kind == "reel":
            out.append(r3(tuple(lines), support, who, f"Q-reel-{slug}", placing, sample=False))
        else:
            out.append(quote_post("purple" if i % 2 else "cream", f"Q-card-{slug}", who, tuple(lines), placing, sample=False, support=support))
    return out

if __name__ == "__main__":
    js = jobs()
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        js = [dict(j, kind="still", name="_prev-" + j["name"], t=6.0) for j in js]
    run(js)
