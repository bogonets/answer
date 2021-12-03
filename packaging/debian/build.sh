#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
PACKAGE_NAME=$(grep --color=never 'Package: .*' "$SCRIPT_DIR/DEBIAN/control" | sed 's/Package: //')
PACKAGE_VERSION=$(grep --color=never 'Version: .*' "$SCRIPT_DIR/DEBIAN/control" | sed 's/Version: //')
PACKAGE_FILE="${PACKAGE_NAME}_${PACKAGE_VERSION}.deb"

dpkg-deb --build "$SCRIPT_DIR" "$PACKAGE_FILE"
