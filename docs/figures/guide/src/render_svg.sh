#!/usr/bin/env bash
# render_svg.sh SVG PNG WIDTH HEIGHT : rasterise an SVG at 2x with headless Chrome
set -euo pipefail
svg=$(realpath "$1"); png="$2"; w="$3"; h="$4"
test ! -e "$png"
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --default-background-color=FFFFFFFF --window-size="$w,$h" --screenshot="$png" "file://$svg"
