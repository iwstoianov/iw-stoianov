#!/usr/bin/env bash
# Installeert / werkt de TradingView MCP-server bij voor Claude Code.
# Bron: https://github.com/tradesdontlie/tradingview-mcp
#
# Gebruik:  ./scripts/setup-tradingview-mcp.sh
set -euo pipefail

REPO_URL="https://github.com/tradesdontlie/tradingview-mcp.git"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT_DIR}/vendor/tradingview-mcp"

echo "==> TradingView MCP installeren in: ${DEST}"
mkdir -p "${ROOT_DIR}/vendor"

if [ -d "${DEST}/.git" ]; then
  echo "==> Bestaande installatie gevonden, bijwerken..."
  git -C "${DEST}" pull --ff-only
else
  git clone --depth 1 "${REPO_URL}" "${DEST}"
fi

echo "==> npm-dependencies installeren..."
( cd "${DEST}" && npm install --no-audit --no-fund )

echo ""
echo "Klaar. De server is geregistreerd via .mcp.json (server-naam: 'tradingview')."
echo "Start Claude Code opnieuw zodat de MCP-server wordt opgepikt."
echo ""
echo "LET OP: voor live data moet de TradingView Desktop-app lokaal draaien met"
echo "Chrome DevTools op poort 9222. Controleer daarna met de tool 'tv_health_check'."
