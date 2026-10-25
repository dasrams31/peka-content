#!/usr/bin/env bash
# pick_reel_track.sh - Print the full path of the next reel track.
# Each call advances a persistent counter (flock-guarded), so
# consecutive reel renders always get a DIFFERENT track until the
# 9-track cyberpunk lane cycles. Call ONCE per reel render (IG and FB
# publish the same file, so they share one pick).
# Caption title: basename without "-kevin-macleod.mp3", dashes to
# spaces, title case, e.g. "Crypto by Kevin MacLeod".
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
LIST="$DIR/CYBERPUNK_TRACKS.txt"
STATE="$DIR/reel_track_state.txt"
LOCK="$DIR/reel_track_state.lock"
exec 9>"$LOCK"
flock 9
mapfile -t TRACKS < <(grep -v '^#' "$LIST" | grep -v '^$')
N=${#TRACKS[@]}
LAST=-1
[ -f "$STATE" ] && LAST=$(cat "$STATE")
NEXT=$(( (LAST + 1) % N ))
echo "$NEXT" > "$STATE"
echo "$DIR/${TRACKS[$NEXT]}"
