#!/usr/bin/env python3
"""
Macro Desk - bouwt het dashboard met verse koersen.
Draait automatisch via GitHub Actions. Haalt prijzen bij Twelve Data,
vult ze in het HTML-template, en schrijft index.html.

De API-sleutel wordt NIET in dit bestand gezet. Hij komt uit een
'GitHub Secret' (veilig opgeslagen), zodat hij nooit publiek zichtbaar is.
"""

import os
import json
import datetime
import urllib.request
import urllib.parse

# ── instellingen ─────────────────────────────────────────────
API_KEY = os.environ.get("TWELVE_DATA_KEY", "")
# Twelve Data symbolen. Goud en forex werken op gratis tier.
# US100 (Nasdaq) kan vertraagd zijn op gratis tier; dat is prima voor macro.
SYMBOLS = {
    "XAUUSD": "XAU/USD",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "US100":  "NDX",      # Nasdaq 100 index
}

# ── statische analyse (verander deze teksten wanneer het nieuws verandert) ──
# Dit is het "brein". De koersgetallen komen live binnen; deze duiding
# update je een paar keer per dag, of vraag Claude om een verse versie.
ANALYSIS = {
    "XAUUSD": {
        "nm": "Goud", "bias": "NEUTRAAL → BEARISH", "biascls": "neu", "note": "korte termijn",
        "conf": 60, "confcls": "amber", "accent": "rgba(255,193,77,.12)",
        "analysis": [
            "Goud onder druk nu sterke Amerikaanse arbeidsdata de 'higher-for-longer' Fed-verwachting versterkt.",
            "Ongebruikelijke dynamiek: de oorlog stookt inflatie op en houdt de Fed restrictief. Goud heeft het <b>einde</b> van de oorlog nodig om te stijgen.",
            "Stevige bodem door centrale-bank-aankopen (1.100+ ton in 2025) — prijs-ongevoelige vraag.",
        ],
        "sup": "$4.424 → 4.370", "res": "$4.500 → 4.510",
        "events": [{"t": "JOLTS", "hot": False}, {"t": "Beige Book", "hot": False}, {"t": "NFP morgen", "hot": True}],
        "concl": "Klem tussen safe-haven vraag en hoge rentes. Een <b>staakt-het-vuren</b> is het meest bullish scenario.",
    },
    "EURUSD": {
        "nm": "Euro / Dollar", "bias": "BEARISH", "biascls": "bear", "note": "korte termijn",
        "conf": 65, "confcls": "red", "accent": "rgba(255,93,108,.10)",
        "analysis": [
            "EURUSD zwak, dollar gesteund door sterke arbeidsmarktrapporten. Smalle range.",
            "Het grotere plaatje is <b>tweezijdig</b>: dollar-zwakte-calls rusten allemaal op Fed-renteverlagingen.",
            "Met inflatie op 3,8% zijn die verlagingen uitgesteld — daarom is de dollar sterker dan verwacht.",
        ],
        "sup": "1,1600 → 1,1550", "res": "1,1650 → 1,1700",
        "events": [{"t": "EZ detailhandel", "hot": False}, {"t": "NFP morgen", "hot": True}],
        "concl": "Vooral een <b>dollar-verhaal</b>. Neiging neerwaarts zolang VS-data sterk is. Zwakke NFP draait dit snel om.",
    },
    "GBPUSD": {
        "nm": "Pond / Dollar", "bias": "NEUTRAAL → BEARISH", "biascls": "neu", "note": "range-gebonden",
        "conf": 60, "confcls": "amber", "accent": "rgba(255,193,77,.10)",
        "analysis": [
            "GBPUSD in smalle zijwaartse range, heeft sterk nieuws nodig voor richting.",
            "Sterling niet zozeer verzwakt — de <b>dollar is verstevigd</b>. BoE hield rente op 3,75%.",
            "UK-inflatie verhoogd op 3,3%, beperkt de ruimte van de BoE. Volgende beslissing 18 juni.",
        ],
        "sup": "1,3400 → 1,3350", "res": "1,3500 → 1,3550",
        "events": [{"t": "NFP morgen", "hot": True}, {"t": "BoE 18 jun", "hot": False}],
        "concl": "Range-gebonden. Pas bij <b>breakout uit 1,3400–1,3500</b> ontstaat richting.",
    },
    "US100": {
        "nm": "Nasdaq 100", "bias": "BEARISH / structureel BULLISH", "biascls": "bear", "note": "kort vs lang",
        "conf": 65, "confcls": "red", "accent": "rgba(31,216,127,.10)",
        "analysis": [
            "Nasdaq daalt nu <b>Broadcom teleurstelt</b> en chipaandelen zakken.",
            "Markt is zwaar gepositioneerd voor een <b>dovish Fed</b>; sterk banenrapport kan short-covering in de dollar triggeren — tegen tech.",
            "Structureel blijft de <b>uptrend intact</b>: dips zijn correctie, geen distributie.",
        ],
        "sup": "24.800 → 24.500", "res": "25.300 → ATH-zone",
        "events": [{"t": "Chip-sector", "hot": False}, {"t": "NFP morgen", "hot": True}],
        "concl": "Kort voorzichtig (chip-zwakte + NFP-risico). <b>Structureel trend opwaarts.</b>",
    },
}

TOP_OPP = {
    "sym": "US100",
    "bias": "Bearish (korte termijn)",
    "why": ("De asymmetrie is duidelijk: de markt is extreem gepositioneerd voor een <b>dovish Fed</b>, "
            "waardoor het banenrapport morgen een binaire trigger is. Korte termijn bearish het meest waarschijnlijke pad — "
            "<b>chip-zwakte (Broadcom)</b> plus risico op sterke banendata → hogere rentes → druk op tech. "
            "Structureel blijft de uptrend intact. <b>Wacht op de NFP-uitslag morgen voor de entry-trigger.</b>"),
}

NEWS = [
    {"tag": "neg", "t": "Goud onder $4.500", "m": "Sterke VS-arbeidsdata versterkt 'higher-for-longer' Fed-verwachting.", "src": "TradingEconomics"},
    {"tag": "neg", "t": "Broadcom stelt teleur", "m": "Chip-aandelen onder druk, Nasdaq zakt mee vóór NFP.", "src": "Forex.com"},
    {"tag": "neu", "t": "USD stalt bij weerstand", "m": "Dollar-index oversold — asymmetrisch opwaarts risico bij sterk rapport.", "src": "DailyFX"},
    {"tag": "pos", "t": "Iran-deal mogelijk dichtbij", "m": "Trump wijst op heropenen Straat van Hormuz; zou inflatie-tegenwind wegnemen.", "src": "Reuters"},
]

FLOW = [
    {"sym": "USD (DXY)", "val": "+1,46%", "pct": 62, "dir": "into"},
    {"sym": "Defensief / cash", "val": "+0,68%", "pct": 34, "dir": "into"},
    {"sym": "Goud (XAU)", "val": "−0,52%", "pct": -40, "dir": "out"},
    {"sym": "Tech / chips", "val": "−0,90%", "pct": -58, "dir": "out"},
    {"sym": "EUR", "val": "−0,24%", "pct": -22, "dir": "out"},
]


# ── koersen ophalen ──────────────────────────────────────────
def fetch_price(td_symbol):
    """Haalt laatste prijs + dag-verandering op. Geeft (prijs, change%) of (None, None)."""
    if not API_KEY:
        return None, None
    try:
        url = "https://api.twelvedata.com/quote?" + urllib.parse.urlencode({
            "symbol": td_symbol, "apikey": API_KEY,
        })
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read().decode())
        if "close" in data:
            price = float(data["close"])
            change = data.get("percent_change")
            change = float(change) if change not in (None, "") else None
            return price, change
    except Exception as e:
        print(f"  ! kon {td_symbol} niet ophalen: {e}")
    return None, None


def fmt_price(sym, price):
    """Nette opmaak per asset-type."""
    if price is None:
        return "—"
    if sym in ("EURUSD", "GBPUSD"):
        return f"{price:.4f}".replace(".", ",")
    # goud + index: duizendtallen met punt
    return f"{price:,.0f}".replace(",", ".") if price >= 1000 else f"{price:,.2f}"


def fmt_change(change):
    if change is None:
        return "", "flat"
    cls = "up" if change > 0 else ("down" if change < 0 else "flat")
    sign = "+" if change > 0 else ("−" if change < 0 else "")
    return f"{sign}{abs(change):.1f}%".replace(".", ","), cls


# ── dashboard bouwen ─────────────────────────────────────────
def build():
    print("Koersen ophalen bij Twelve Data...")
    assets = []
    for sym, td in SYMBOLS.items():
        price, change = fetch_price(td)
        print(f"  {sym}: {price} ({change})")
        chg_txt, chg_cls = fmt_change(change)
        a = dict(ANALYSIS[sym])
        a["sym"] = sym
        a["price"] = fmt_price(sym, price)
        a["chg"] = chg_txt
        a["chgcls"] = chg_cls
        assets.append(a)

    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)  # CET
    stamp = now.strftime("%d-%m-%Y · %H:%M CET")

    payload = {
        "assets": assets, "news": NEWS, "flow": FLOW,
        "top": TOP_OPP, "stamp": stamp,
    }

    template = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
    html = template.replace("/*__DATA__*/", json.dumps(payload, ensure_ascii=False))

    out = os.path.join(os.path.dirname(__file__), "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Klaar -> {out}")


if __name__ == "__main__":
    build()
