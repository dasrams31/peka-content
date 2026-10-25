#!/usr/bin/env bash
# make_reel.sh - Build a vertical 9:16 reel from slide images.
# Proven recipe (SPILL v2 + bansos reels, 2026-10-25).
#
# Usage:
#   make_reel.sh OUT.mp4 COVER.jpg MUSIC.mp3 SLIDE1 [SLIDE2 ...]
#
# Spec:
#   - 4 seconds per slide, 0.5s xfade transitions alternating
#     fade / slideleft, vertical 1080x1920, yuv420p, 30fps.
#   - Slides are scaled to FIT 1080x1080 preserving aspect ratio,
#     then centered on a #111111 canvas (no squashing).
#   - Audio: track fades in 0.5s and out over the last 0.5s.
#   - Cover: frame at 1s.
# Music must be a CC-BY track with credit written in the caption.
set -euo pipefail

OUT=$1; COVER=$2; MUSIC=$3; shift 3
SLIDES=("$@")
N=${#SLIDES[@]}
if [ "$N" -lt 1 ]; then echo "need at least 1 slide" >&2; exit 1; fi

INPUTS=()
for s in "${SLIDES[@]}"; do INPUTS+=(-loop 1 -t 4 -i "$s"); done
INPUTS+=(-ss 10 -i "$MUSIC")

FILTER=""
for i in $(seq 0 $((N - 1))); do
  FILTER+="[$i:v]scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:0x111111,setsar=1,fps=30,format=yuv420p[v$i];"
done

PREV="v0"
CUR_DUR=4
for i in $(seq 1 $((N - 1))); do
  OFFSET=$(python3 -c "print($CUR_DUR - 0.5)")
  TRANS=fade
  if [ $((i % 2)) -eq 0 ]; then TRANS=slideleft; fi
  FILTER+="[$PREV][v$i]xfade=transition=$TRANS:duration=0.5:offset=$OFFSET[x$i];"
  PREV="x$i"
  CUR_DUR=$(python3 -c "print($CUR_DUR + 3.5)")
done
TOTAL=$CUR_DUR
AOUT=$(python3 -c "print($TOTAL - 0.5)")
FILTER+="[$N:a]aformat=sample_fmts=fltp:channel_layouts=stereo,afade=t=in:st=0:d=0.5,afade=t=out:st=$AOUT:d=0.5[aout]"

ffmpeg -y -v error "${INPUTS[@]}" -filter_complex "$FILTER" \
  -map "[$PREV]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 160k -t "$TOTAL" "$OUT"
ffmpeg -y -v error -ss 1 -i "$OUT" -frames:v 1 -q:v 2 "$COVER"
echo "reel: $OUT (${TOTAL}s, ${N} slides)"
