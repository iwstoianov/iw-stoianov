# Macro Desk — jouw zelf-verversende dashboard

Dit mapje bevat een complete "robot" die elke 15 minuten verse koersen ophaalt
en je dashboard online vers houdt. Je hoeft niets te programmeren — alleen een
paar dingen klikken en plakken. Reken op ±30 minuten, één keer.

Daarna draait het vanzelf. Geen refreshen meer.

────────────────────────────────────────────────────────
WAT ZIT ERIN
────────────────────────────────────────────────────────
- build.py ............ haalt de koersen op en bouwt het dashboard
- template.html ....... het uiterlijk van het dashboard
- .github/workflows/update.yml ... de robot (draait elke 15 min)
- index.html .......... wordt automatisch gemaakt; hoef je niet aan te raken

────────────────────────────────────────────────────────
STAP 1 — Haal je gratis API-sleutel (2 min)
────────────────────────────────────────────────────────
1. Ga naar  https://twelvedata.com
2. Klik "Sign up", maak een gratis account (e-mail + wachtwoord).
   Geen creditcard nodig.
3. Na inloggen zie je je API key — een lange reeks tekens.
   Kopieer die. Bewaar 'm even (bijv. in een kladblok). NIET online delen.

────────────────────────────────────────────────────────
STAP 2 — Maak een gratis GitHub-account (3 min)
────────────────────────────────────────────────────────
1. Ga naar  https://github.com
2. Klik "Sign up", maak een gratis account.

────────────────────────────────────────────────────────
STAP 3 — Maak een nieuw project ("repository") (3 min)
────────────────────────────────────────────────────────
1. Klik rechtsboven op "+" → "New repository".
2. Naam: bijv.  macro-desk
3. Kies "Public" (gratis Pages werkt alleen op public, maar je sleutel
   blijft veilig — die zetten we apart in stap 5, niet in de code).
4. Klik "Create repository".

────────────────────────────────────────────────────────
STAP 4 — Zet deze bestanden in je project (5 min)
────────────────────────────────────────────────────────
1. Op de nieuwe repository-pagina, klik "uploading an existing file".
2. Sleep deze bestanden erin:
      - build.py
      - template.html
3. Voor de robot-map: klik bij de bestandsupload op "create new file",
   typ als naam exact:
      .github/workflows/update.yml
   (de schuine strepen maken automatisch de mapjes)
   en plak daar de inhoud van update.yml in.
4. Klik "Commit changes".

────────────────────────────────────────────────────────
STAP 5 — Zet je sleutel veilig weg (2 min) ⚠ belangrijk
────────────────────────────────────────────────────────
Je sleutel hoort NOOIT in de code. Hij gaat in een afgeschermde kluis:
1. In je repository: klik "Settings" (bovenin).
2. Links: "Secrets and variables" → "Actions".
3. Klik "New repository secret".
4. Name:   TWELVE_DATA_KEY
   Secret: (plak hier je sleutel uit stap 1)
5. Klik "Add secret".

────────────────────────────────────────────────────────
STAP 6 — Zet de gratis website aan (2 min)
────────────────────────────────────────────────────────
1. In "Settings" → links "Pages".
2. Onder "Source", kies "GitHub Actions".
3. Klaar — meer hoef je hier niet te doen.

────────────────────────────────────────────────────────
STAP 7 — Start de robot voor het eerst (1 min)
────────────────────────────────────────────────────────
1. Klik bovenin op "Actions".
2. Kies links "Update Macro Dashboard".
3. Klik rechts "Run workflow" → "Run workflow".
4. Wacht ~1 minuut (er verschijnt een groen vinkje).
5. Je dashboard staat nu live op:
      https://JOUWNAAM.github.io/macro-desk/
   (vervang JOUWNAAM door je GitHub-gebruikersnaam)

Vanaf nu draait de robot vanzelf elke 15 minuten. Open de link op je
telefoon en kies "Zet op beginscherm" → je hebt je dashboard als app-icoon.

────────────────────────────────────────────────────────
DE ANALYSE-TEKSTEN VERVERSEN
────────────────────────────────────────────────────────
De koersen verversen vanzelf. De duiding (bias, conclusie, nieuws) staat in
build.py onder ANALYSIS / NEWS / TOP_OPP. Vraag Claude een paar keer per dag:
"geef me de verse ANALYSIS-blokken voor mijn macro-bot" — plak die in build.py,
commit, en de robot pakt het automatisch op.

────────────────────────────────────────────────────────
KOSTEN
────────────────────────────────────────────────────────
Alles gratis: Twelve Data (gratis tier), GitHub (gratis), GitHub Pages (gratis).
Let op: bij 4 assets x elke 15 min blijf je ruim onder de gratis limiet van
800 calls/dag (±384/dag). Wil je sneller verversen, pas de cron in update.yml aan,
maar blijf onder ~8 calls/minuut.

────────────────────────────────────────────────────────
LET OP
────────────────────────────────────────────────────────
Dit is een analyse-overzicht, geen beleggingsadvies. De koersen kunnen op de
gratis tier licht vertraagd zijn (vooral de Nasdaq-index). Voor macro-context
prima; niet bedoeld als seconde-precieze trading-feed.
