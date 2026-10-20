#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/upstream"
mkdir -p "$DEST"

sync_one() {
  name="$1"
  sha="$2"
  dir="$DEST/$name"
  url="https://github.com/storytold/$name.git"
  if [ ! -d "$dir/.git" ]; then
    mkdir -p "$dir"
    git -C "$dir" init -q
    git -C "$dir" remote add origin "$url"
  fi
  git -C "$dir" fetch --depth 1 origin "$sha"
  git -C "$dir" checkout -q FETCH_HEAD
  printf '%s\n' "$name $sha" >> "$DEST/.manifest"
  echo "synced $name at $sha"
}

: > "$DEST/.manifest"
sync_one photocraft 03d0c7e3b39cfb401cdbba590431141ee4c6c8fa
sync_one vectorcraft 9e7929ee8966977e6daf200f457c570f7aaf7c51
sync_one filmcraft fb4cbda47a134eedabd89fe02cd59ebc69462737
sync_one effectcraft ef74d82902ba486891b02afa87e42963cc9b84cc
sync_one lightcraft d999e382bafbb5d5c54482fdb1d11f6a63bfdf69
sync_one soundcraft 25d52c646aea780c8076ff966076f994ad256221
sync_one designcraft 443ea4640ca368fcf0241b04813bd3817acd5df8
sync_one pdfcraft ec0a965074f376a5bf610435948e4e5184bf3299

echo "Upstream listo en $DEST"
