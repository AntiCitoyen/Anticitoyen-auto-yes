#!/bin/bash
# Construit dist/auto-yes_<version>_all.deb
# Usage : packaging/build-deb.sh
set -euo pipefail
umask 022

DEPOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(sed -n '1s/^auto-yes (\([^)]*\)).*/\1/p' "$DEPOT/packaging/changelog")"
ROOT="$DEPOT/build/auto-yes"

rm -rf "$ROOT"
install -d "$ROOT/usr/bin" "$ROOT/etc/auto-yes" "$ROOT/usr/share/doc/auto-yes" "$ROOT/DEBIAN"
install -m 755 "$DEPOT"/bin/auto-yes "$DEPOT"/bin/auto-yes-shell \
    "$DEPOT"/bin/auto-yes-configurer-gnome-terminal "$ROOT/usr/bin/"
install -m 644 "$DEPOT/etc/patterns.conf" "$ROOT/etc/auto-yes/patterns.conf"
install -m 644 "$DEPOT/packaging/copyright" "$ROOT/usr/share/doc/auto-yes/copyright"
sed "s/@DATE@/$(date -R)/" "$DEPOT/packaging/changelog" | gzip -9n \
    > "$ROOT/usr/share/doc/auto-yes/changelog.Debian.gz"

sed "s/@VERSION@/$VERSION/; s/@SIZE@/$(du -sk --exclude=DEBIAN "$ROOT" | cut -f1)/" \
    "$DEPOT/packaging/control" > "$ROOT/DEBIAN/control"
install -m 644 "$DEPOT/packaging/conffiles" "$ROOT/DEBIAN/conffiles"
install -m 755 "$DEPOT/packaging/postinst" "$DEPOT/packaging/postrm" "$ROOT/DEBIAN/"

mkdir -p "$DEPOT/dist"
dpkg-deb --root-owner-group -Zxz --build "$ROOT" "$DEPOT/dist/auto-yes_${VERSION}_all.deb"
