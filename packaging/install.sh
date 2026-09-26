#!/bin/bash
# Installe auto-yes sous une racine : packaging/install.sh <racine>   (ex. "$pkgdir", %{buildroot})
set -euo pipefail
DEPOT="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$1"
install -d "$ROOT/usr/bin" "$ROOT/etc/auto-yes" "$ROOT/usr/share/auto-yes" "$ROOT/usr/share/man/man1" \
    "$ROOT/usr/share/licenses/auto-yes"
install -m 755 "$DEPOT"/bin/auto-yes "$DEPOT"/bin/auto-yes-shell \
    "$DEPOT"/bin/auto-yes-configurer-gnome-terminal "$ROOT/usr/bin/"
install -m 644 "$DEPOT/etc/patterns.conf" "$ROOT/etc/auto-yes/patterns.conf"
install -m 644 "$DEPOT/share/auto-yes/commun.tcl" "$ROOT/usr/share/auto-yes/"
for page in "$DEPOT"/man/*.1; do
    gzip -9n < "$page" > "$ROOT/usr/share/man/man1/$(basename "$page").gz"
done
install -m 644 "$DEPOT/LICENSE" "$ROOT/usr/share/licenses/auto-yes/LICENSE"
