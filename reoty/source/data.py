# 2026 placings, display names as agreed in the winners kit
WINNERS = [
    ("NZ", "New Zealand", "Small", "Travelex"),
    ("NZ", "New Zealand", "Medium", "Flo & Frankie"),
    ("NZ", "New Zealand", "Large", "2degrees Retail"),
    ("AU", "Australia", "Small", "Morrison Clothing"),
    ("AU", "Australia", "Medium", "Travelex"),
    ("AU", "Australia", "Large", "Essilor Luxottica"),
]
RUNNERS = [
    ("NZ", "New Zealand", "Small", "Swanndri"),
    ("NZ", "New Zealand", "Medium", "VAPO"),
    ("NZ", "New Zealand", "Large", "Foodstuffs"),
    ("AU", "Australia", "Small", "Atlas Fuel Global"),
    ("AU", "Australia", "Medium", "Crown Currency Exchange"),
    ("AU", "Australia", "Large", "Freedom"),
]
def slug(s):
    return s.replace("&", "and").replace(" ", "-")
