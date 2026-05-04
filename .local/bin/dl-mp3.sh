#!/usr/bin/env bash

# yt2mp3.sh - Download YouTube audio as MP3 with thumbnail metadata

set -euo pipefail

# ── Colours ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Dependency check ───────────────────────────────────────────────────────────
for cmd in yt-dlp ffmpeg; do
  if ! command -v "$cmd" &>/dev/null; then
    echo -e "${RED}Error: '$cmd' is not installed or not in PATH.${RESET}"
    exit 1
  fi
done

# ── Banner ─────────────────────────────────────────────────────────────────────
echo -e "${CYAN}${BOLD}"
echo "  ╔══════════════════════════════╗"
echo "  ║       yt2mp3 downloader      ║"
echo "  ╚══════════════════════════════╝"
echo -e "${RESET}"

# ── Prompt: single or playlist ─────────────────────────────────────────────────
echo -e "${BOLD}What would you like to download?${RESET}"
echo "  1) Single video"
echo "  2) Playlist"
echo ""
read -rp "Enter choice [1/2]: " choice

case "$choice" in
  1) mode="single" ;;
  2) mode="playlist" ;;
  *)
    echo -e "${RED}Invalid choice. Please enter 1 or 2.${RESET}"
    exit 1
    ;;
esac

# ── Prompt: URL ────────────────────────────────────────────────────────────────
echo ""
if [[ "$mode" == "single" ]]; then
  read -rp "Enter video URL: " url
else
  read -rp "Enter playlist URL: " url
fi

if [[ -z "$url" ]]; then
  echo -e "${RED}No URL provided. Exiting.${RESET}"
  exit 1
fi

# ── Prompt: output directory ───────────────────────────────────────────────────
echo ""
read -rp "Output directory [default: current folder]: " outdir
outdir="${outdir:-.}"

if [[ ! -d "$outdir" ]]; then
  read -rp "Directory '$outdir' doesn't exist. Create it? [y/N]: " create
  if [[ "$create" =~ ^[Yy]$ ]]; then
    mkdir -p "$outdir"
    echo -e "${GREEN}Created: $outdir${RESET}"
  else
    echo -e "${RED}Aborted.${RESET}"
    exit 1
  fi
fi

# ── Build output template ──────────────────────────────────────────────────────
if [[ "$mode" == "playlist" ]]; then
  output_template="${outdir}/%(playlist_index)s - %(title)s.%(ext)s"
else
  output_template="${outdir}/%(title)s.%(ext)s"
fi

# ── Run yt-dlp ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}Starting download...${RESET}"
echo ""

yt-dlp \
  -x \
  --audio-format mp3 \
  --audio-quality 0 \
  --embed-thumbnail \
  --add-metadata \
  -o "$output_template" \
  "$url"

echo ""
echo -e "${GREEN}${BOLD}Done! Files saved to: ${outdir}${RESET}"
