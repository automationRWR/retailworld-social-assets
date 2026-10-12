# Retailworld social assets

Public asset store for Retailworld Resourcing's Instagram refresh (October 2026). Buffer and Notion both pull media straight from the raw URLs in this repo, so files here should not be renamed, moved or deleted while posts that use them are scheduled.

Raw URL pattern: `https://raw.githubusercontent.com/automationRWR/retailworld-social-assets/main/<path>`

## Folders

| Folder | What it holds | Size |
|---|---|---|
| `reels/` | 8 finished reels, MP4, 1080x1920, 30fps | 8 to 15s each |
| `grid/videos/` | 9 animated grid posts, seamless loops, MP4, 1080x1350 | 8s each |
| `grid/stills/` | Still frame of each grid post, PNG, 1080x1350 | |
| `posts/` | Carousels and single posts, PNG, 1080x1350 | 36 images |
| `monday/` | Monday motivation stills and carousels, JPEG, 1080x1350 (Buffer-ready) | 18 images |
| `source/motion/` | HTML/CSS/JS motion kit and Playwright + ffmpeg render scripts for reels, grid posts and Monday posts | |
| `source/canvas/` | Design canvas boards for the static carousels and the offline PNG exporter | |

## Re-rendering

Requires Python 3, Playwright with Chromium, and ffmpeg.

- Reel: `python3 source/motion/render.py source/motion/r6_hype_man.html out.mp4` (add `7.0,10.5` as a third argument to save preview frames at those seconds instead)
- Grid post loop: `python3 source/motion/render_post.py source/motion/p7_sarah.html out.mp4` (writes `out.mp4` plus `out.png` as a still; an optional third argument sets the still time in seconds)
- Monday carousel: `python3 source/motion/render_carousel.py source/motion/mmc_checklist.html out/check` (writes `out/check_1.png` to `out/check_6.png`)
- Static canvas boards: `python3 source/canvas/export/export.py "$PWD/source/canvas/project" "$PWD/source/motion/a" "$PWD/out/png"` (logo and Poppins files live in `source/motion/a`)

## Style

The approved style rules live in Notion on the skill page "Retailworld Social Content: Style and Production". Short version: Poppins, Retailworld orange #F27C10 at full vibrancy with white and light grey, no gradients, no black backgrounds, Apple-style short lines, everyday phone UI as the medium, word-by-word kinetic type, logo only on first and last slides or scenes.
