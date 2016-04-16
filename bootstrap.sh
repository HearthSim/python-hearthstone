#!/bin/bash

BASEDIR="$(dirname $0)"
HSDATA_URL="https://github.com/HearthSim/hs-data.git"
HSDATA_DIR="$BASEDIR/build/hs-data"
CARDDEFS_OUT="$BASEDIR/hearthstone/CardDefs.xml"

command -v git &>/dev/null || {
	>&2 echo "ERROR: git is required to bootstrap this project."
	exit 1
}

mkdir -p "$BASEDIR/build"

echo "Fetching data files from $HSDATA_URL"
if [[ ! -e "$HSDATA_DIR" ]]; then
	git clone --depth=1 "$HSDATA_URL" "$HSDATA_DIR"
else
	git -C "$HSDATA_DIR" fetch &&
	git -C "$HSDATA_DIR" reset --hard origin/master
fi

cp "$HSDATA_DIR/CardDefs.xml" "$CARDDEFS_OUT"
