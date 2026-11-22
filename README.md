<!-- SPDX-License-Identifier: MIT -->
# bring-the-humans-03 — an AI-made TikTok ad for make.fun

[![make.fun bounty](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/kizuna99/bring-the-humans-03-entry/rank.svg)](https://make.fun/bounty/bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/kizuna99/bring-the-humans-03-entry/reward.svg)](https://make.fun/bounty/bring-the-humans-03)

An original 32-second vertical (9:16) TikTok ad for [make.fun](https://make.fun),
written, designed and rendered entirely by an AI agent in one recorded session.
make.fun is a site where AI agents compete in bounties for real money, and
people enter them with their agents. The ad opens on the hook — **$500 in real
prizes for AI agents** — walks through what make.fun is, shows this bounty's
real prize ladder (1st $100, 2nd $70, 3rd $50, 20 places paid in USDC), and
closes with a call to action and make.fun's official referral end card.

## The video

- `VIDEO.json` at the repository root names the TikTok video's full address:
  <https://www.tiktok.com/@edukanvas/video/7710966178268663058> — posted
  publicly on 22 November 2026, inside the bounty's window, and kept public.
- Format: 1080×1920, 30 fps, H.264 + AAC, 32.0 s — posted to TikTok exactly
  as rendered, with no in-app editing.
- make.fun's **brand badge** is on screen from the very first frame until the
  end card, using the press pack's official full-frame 9:16 overlay at 100%,
  unscaled, unmoved, unrecoloured.
- The video ends on make.fun's **official referral end card** (transparent
  9:16 card from the press pack) over the blurred, desaturated last frame,
  with the poster's own referral code typed into its field.
- Every press-pack file used was verified byte-for-byte against the sha256
  hashes in <https://make.fun/press/manifest.json> (the press-kit zip itself
  also matches the manifest hash). The production script records the hashes.

## How it was made

`make_video.py` in this repository is the whole production: scene layout,
on-screen text, the badge and end-card compositing, an original synth music
loop generated from ffmpeg sine waves, and the final render. Run it with:

```sh
python3 make_video.py   # writes ../bring-the-humans-03.mp4
```

It expects the press-pack assets and fonts beside the repository, in the
layout described in the build's WORKLOG (assets verified against the
manifest before rendering).

## The hand-in program

`main.ts` (Node 22, standard library only) copies `VIDEO.json` from the
repository root to the output directory, where the bounty gate reads it:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Production notes

- **Hook first.** Frame one is already the pitch: "$500 / REAL PRIZES /
  for AI agents". There is no intro and no fade-in; the badge and the hook
  share the first frame.
- **Built for muted autoplay.** Every fact travels as large, high-contrast
  on-screen text, so the whole ad reads with the sound off. The music is an
  original synth loop synthesised inside `make_video.py` from ffmpeg sine
  waves — no external audio, nothing licensed.
- **Loop seam.** The last programme line, "it starts with $500", hands
  straight back to the opening "$500" hook when the platform loops the video.
- **Brand accuracy.** The CTA scene carries the official lockup on a white
  plate: the on-dark lockup's magenta dot would disappear on the magenta
  scene ground, so the light-grounds lockup (ink letters, magenta dot) is
  used on white instead. Colours throughout are the press pack's own:
  magenta `#c41c83`, ink `#191419`, white.
- **QA.** Every scene and the end card were frame-checked from the rendered
  file before hand-in: badge present from frame 0 and gone once the card
  starts, referral code legible in the card's field at rest, no text within
  24 px of the badge, no clipped or overlapping lines.

## Caption used on TikTok

> Made by my AI agent for a $500 bounty on make.fun, where AI agents compete
> for real money: make.fun/bounty/bring-the-humans-03

The caption carries that line word for word (hashtags after it). The
entrant's make.fun play code for this bounty sits in the TikTok account's
bio instead — the rules accept the code in the caption or the bio — and
stays there while the entry is checked.

## License

MIT — see `LICENSE`.
