#!/usr/bin/env bash
# fetch_track.sh - Download a new Kevin MacLeod track into a lane.
# Usage: fetch_track.sh "<Track Name>" <cyberpunk|light>
# Example: fetch_track.sh "Sneaky Adventure" light
# - Downloads from incompetech.com (direct mp3 URL, CC-BY royalty-free).
# - Verifies with ffprobe (must be a valid mp3, duration >= 30s).
# - Saves as <slug>-kevin-macleod.mp3 and appends it to the lane file
#   (skips if already listed). Does NOT reset any picker counter, so
#   the new track enters the rotation on the next cycle.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
NAME="${1:?usage: fetch_track.sh \"<Track Name>\" <cyberpunk|light>}"
LANE="${2:?usage: fetch_track.sh \"<Track Name>\" <cyberpunk|light>}"
case "$LANE" in
  cyberpunk) LIST="$DIR/CYBERPUNK_TRACKS.txt" ;;
  light) LIST="$DIR/LIGHT_TRACKS.txt" ;;
  *) echo "unknown lane: $LANE (use cyberpunk or light)" >&2; exit 1 ;;
esac
SLUG="$(echo "$NAME" | tr 'A-Z' 'a-z' | tr ' ' '-')"
FILE="${SLUG}-kevin-macleod.mp3"
URL_NAME="$(echo "$NAME" | sed 's/ /%20/g')"
URL="https://incompetech.com/music/royalty-free/mp3-royaltyfree/${URL_NAME}.mp3"
if [ -f "$DIR/$FILE" ]; then
  echo "already downloaded: $FILE"
else
  echo "downloading $URL ..."
  curl -sf --max-time 120 -o "$DIR/$FILE" "$URL" || {
    echo "download failed (track name may not exist on incompetech): $NAME" >&2
    rm -f "$DIR/$FILE"
    exit 1
  }
fi
DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$DIR/$FILE")"
DUR_INT="${DUR%.*}"
if [ "$DUR_INT" -lt 30 ]; then
  echo "track too short (${DUR}s), not adding: $FILE" >&2
  exit 1
fi
if grep -qx "$FILE" "$LIST"; then
  echo "already in $LANE lane: $FILE (${DUR}s)"
else
  echo "$FILE" >> "$LIST"
  echo "added to $LANE lane: $FILE (${DUR}s)"
fi
