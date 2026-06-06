# TradingView MCP gekoppeld aan Claude

Deze repo is geconfigureerd zodat Claude Code (en de Claude Desktop/Code-clients)
de [TradingView MCP-server](https://github.com/tradesdontlie/tradingview-mcp) kan
gebruiken. Daarmee kan Claude o.a. charts, indicatoren en Pine Script-data uit
TradingView opvragen.

> ⚠️ Onofficiële tool — niet verbonden met TradingView Inc. of Anthropic.
> Zorg dat je gebruik voldoet aan de gebruiksvoorwaarden van TradingView.

## Wat is er ingesteld

- **`.mcp.json`** — registreert de MCP-server onder de naam `tradingview`.
  Claude Code pikt dit automatisch op zodra je het project opent.
- **`scripts/setup-tradingview-mcp.sh`** — cloned de server naar
  `vendor/tradingview-mcp` en installeert de npm-dependencies.
- **`vendor/`** staat in `.gitignore` — de servercode wordt lokaal geïnstalleerd,
  niet meegecommit.

## Installeren (eenmalig)

Vereisten: **Node.js 18+** en **git**.

```bash
./scripts/setup-tradingview-mcp.sh
```

Start daarna Claude Code opnieuw, zodat de `tradingview`-server wordt geladen.
Geen API-keys nodig.

## Snelstart macOS (overal beschikbaar in Claude)

De `.mcp.json` hierboven activeert de server alleen binnen déze repo. Wil je
TradingView in **elk** Claude Code-project gebruiken, installeer de server dan op
een vaste plek en registreer hem op user-niveau:

```bash
# 1) Server clonen + installeren (eenmalig)
git clone https://github.com/tradesdontlie/tradingview-mcp.git ~/tradingview-mcp
cd ~/tradingview-mcp && npm install

# 2) Aan Claude Code koppelen (user-scope = beschikbaar in elk project)
claude mcp add tradingview --scope user -- node ~/tradingview-mcp/src/server.js

# 3) TradingView Desktop starten met debug-poort (script vindt de app automatisch)
~/tradingview-mcp/scripts/launch_tv_debug_mac.sh

# 4) Controleren of de koppeling staat
claude mcp list
```

Open daarna een nieuwe Claude Code-sessie en vraag: *"Gebruik `tv_health_check`."*

## Verbinden met live data

De server praat met de **TradingView Desktop-app** via het Chrome DevTools
Protocol op poort `9222`. Start TradingView lokaal met debugging aan:

```bash
# macOS
/Applications/TradingView.app/Contents/MacOS/TradingView --remote-debugging-port=9222

# Windows
"%LOCALAPPDATA%\TradingView\TradingView.exe" --remote-debugging-port=9222

# Linux
/path/to/TradingView --remote-debugging-port=9222
```

> Voor real-time data is een betaald TradingView-abonnement nodig.

## Controleren of het werkt

Vraag Claude in een sessie:

> "Gebruik `tv_health_check` om te controleren of TradingView verbonden is."

Een positief antwoord betekent dat de koppeling werkt.
