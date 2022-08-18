#!/usr/bin/env bash

RECC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
VERSION=$(cat "$RECC_DIR/VERSION")

DEBIAN_VERSION_PATH="$RECC_DIR/packaging/debian/DEBIAN/control"
CORE_VERSION_PATH="$RECC_DIR/core/recc/util/version.py"
API_VERSION_PATH="$RECC_DIR/api/package.json"
FE_VERSION_PATH="$RECC_DIR/fe/package.json"

sed -i.tmp -e "s/Version: .*/Version: $VERSION/" "$DEBIAN_VERSION_PATH"
sed -i.tmp -e "s/version_text: Final[str] = \".*\"/version_text = \"$VERSION\"/" "$CORE_VERSION_PATH"
sed -i.tmp -e "s/  \"version\": \".*\",/  \"version\": \"$VERSION\",/" "$API_VERSION_PATH"
sed -i.tmp -e "s/  \"version\": \".*\",/  \"version\": \"$VERSION\",/" "$FE_VERSION_PATH"

rm "$DEBIAN_VERSION_PATH.tmp"
rm "$CORE_VERSION_PATH.tmp"
rm "$API_VERSION_PATH.tmp"
rm "$FE_VERSION_PATH.tmp"
