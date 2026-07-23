#!/bin/bash
# Double-click installer for macOS.
cd "$(dirname "$0")" || exit 1
echo "Installing Ingesta - Media Importer..."
if python3 install.py; then
  echo ""
  echo "Done. Press Enter to close."
else
  echo ""
  echo "Install failed. If you saw a permission error, retry with:"
  echo "  sudo python3 \"$(pwd)/install.py\""
  echo ""
  echo "Press Enter to close."
fi
read -r _
