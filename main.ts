// bring-the-humans-03 hand-in program (Node 22, standard library only).
//
// It copies VIDEO.json from the repository root to the output directory,
// where the bounty gate reads it. That is all the program has to do: the
// entry is the video itself — an original short vertical ad for make.fun,
// made and rendered by the agent in the recorded session (see make_video.py),
// posted publicly on TikTok from a public account with the bounty's line and
// the entrant's play code in its caption, and named by VIDEO.json. The house
// reads the video's views from TikTok; nothing this program writes about the
// video is scored.
//
// The VIDEO.json in this repository is a PLACEHOLDER until the video is
// posted: replace its url with the video's full TikTok address
// (https://www.tiktok.com/@<handle>/video/<id> — full address only, short
// links are refused) before submitting. The placeholder handle is
// deliberately not a real account, so a premature check fails loudly
// instead of pointing at somebody else's video.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'VIDEO.json'), join(OUTPUT_DIR, 'VIDEO.json'));
} catch (err) {
  console.error(`VIDEO.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
