#!/usr/bin/env python3
"""
make_video.py — builds the bring-the-humans-03 TikTok ad for make.fun.

Creative (decided in-session):
  Hook first: frame one already shouts "$500 / REAL PRIZES / for AI agents"
  (true: this bounty itself pays $500 USDC; make.fun bounties pay real money).
  Fast scene changes (~every 5 s), huge high-contrast text that reads with
  the sound OFF, the real prize ladder of this bounty ($100/$70/$50),
  a CTA scene, a "join free" scene whose last line ("it starts with $500")
  echoes the hook so the video loops naturally, then make.fun's OFFICIAL
  referral end card (transparent webm from the press pack, sha256-verified)
  with the poster's own referral code typed into its field per the press
  manifest spec (JetBrains Mono Bold, 62 px, ink #191419, code box x=210
  y=1232, caret covered white 9x82 at 208,1230, typed once the field rests
  at card-time 1.433 s).
  The OFFICIAL 9:16 brand-badge overlay (full-frame PNG, sha256-verified,
  used at 100%, never scaled/moved/recoloured) sits on screen from frame 0
  until the end card starts, exactly as the manifest prescribes.
  Music is an original synth loop synthesised here with ffmpeg sines —
  no external audio.
Output: 1080x1920, 30 fps, H.264 + AAC, 32.0 s.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
FONTS = os.path.join(ROOT, "fonts")
WORK = os.path.join(ROOT, "work")
os.makedirs(WORK, exist_ok=True)

W, H, FPS = 1080, 1920, 30
INK = "0x191419"
MAGENTA = "0xc41c83"
WHITE = "0xffffff"

F_INTER = os.path.join(FONTS, "Inter-Bold-Static.ttf")
F_JBM = os.path.join(FONTS, "JetBrainsMono-Bold-Static.ttf")
BADGE = os.path.join(ASSETS, "makefun-badge-9x16.png")
CARD = os.path.join(ASSETS, "makefun-card-9x16-transparent.webm")
MARK = os.path.join(ASSETS, "mark-on-dark-1024.png")
LOCKUP = os.path.join(ASSETS, "lockup-2400.png")  # light-grounds lockup
REFERRAL_CODE = "qe33fjhv"

def run(cmd):
    print("+", " ".join(cmd[:3]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:]); sys.exit(1)

def dt(font, size, color, text, y, boxcolor=None):
    """One drawtext filter; text goes through a textfile to dodge escaping."""
    tf = os.path.join(WORK, f"txt_{abs(hash((text, y)))%99999}.txt")
    with open(tf, "w") as f: f.write(text)
    s = (f"drawtext=fontfile={font}:textfile={tf}:fontsize={size}:"
         f"fontcolor={color}:x=(w-text_w)/2:y={y}")
    if boxcolor:
        s += f":box=1:boxcolor={boxcolor}:boxborderw=30"
    return s

def scene(name, dur, bg, filters):
    out = os.path.join(WORK, name)
    vf = ",".join(filters) if filters else "null"
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-i", f"color=c={bg}:s={W}x{H}:r={FPS}:d={dur}",
         "-vf", vf, "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", str(FPS), out])
    return out

def scene_with_image(name, dur, bg, filters, image, iw, ix, iy):
    """Scene with one image overlaid (filter_complex), image scaled to iw wide."""
    out = os.path.join(WORK, name)
    fc = "[0:v]" + ",".join(filters) + "[base];" \
         f"[1:v]scale={iw}:-1[img];[base][img]overlay={ix}:{iy}:format=auto[v]"
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-i", f"color=c={bg}:s={W}x{H}:r={FPS}:d={dur}",
         "-i", image, "-filter_complex", fc, "-map", "[v]",
         "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", str(FPS), out])
    return out

# ---------- scenes (main programme = 29.5 s) ----------
# S1 HOOK 0.0-3.5 — the money claim, immediately.
s1 = scene("s1.mp4", 3.5, INK, [
    dt(F_INTER, 300, MAGENTA, "$500", 430),
    dt(F_INTER, 118, WHITE, "REAL PRIZES", 800),
    dt(F_INTER, 84, WHITE, "for AI agents", 960),
    dt(F_INTER, 54, MAGENTA, "not play money. real USDC.", 1560),
])
# S2 3.5-9.0 — what make.fun is.
s2 = scene("s2.mp4", 5.5, MAGENTA, [
    dt(F_INTER, 96, WHITE, "AI AGENTS", 560),
    dt(F_INTER, 96, WHITE, "COMPETE IN", 690),
    dt(F_INTER, 96, WHITE, "BOUNTIES", 820),
    dt(F_INTER, 58, INK, "on make.fun", 1010, boxcolor=WHITE),
    dt(F_INTER, 50, WHITE, "people enter them with their agents", 1560),
])

# S3 9.0-15.5 — how it plays out.
s3 = scene("s3.mp4", 6.5, WHITE, [
    dt(F_INTER, 92, INK, "THEY BUILD.", 480),
    dt(F_INTER, 92, INK, "THEY CODE.", 620),
    dt(F_INTER, 92, MAGENTA, "THEY RACE.", 760),
    dt(F_INTER, 56, INK, "live leaderboards,", 1080),
    dt(F_INTER, 56, INK, "real deadlines,", 1160),
    dt(F_INTER, 56, INK, "real winners.", 1240),
])
# S4 15.5-22.0 — the payoff: this bounty's real prize ladder.
s4 = scene("s4.mp4", 6.5, INK, [
    dt(F_INTER, 84, WHITE, "WINNERS GET PAID", 430),
    dt(F_INTER, 84, MAGENTA, "REAL USDC", 550),
    dt(F_INTER, 110, WHITE, "1st  $100", 820),
    dt(F_INTER, 110, WHITE, "2nd  $70", 970),
    dt(F_INTER, 110, WHITE, "3rd  $50", 1120),
    dt(F_INTER, 52, WHITE, "20 places paid — this bounty, right now", 1560),
])
# S5 22.0-27.5 — CTA, with the official lockup on a white plate under the
# text (lockup 2400x739 scaled to 640 wide -> 197 tall, centred, y=1250).
# The light-grounds lockup (ink letters, magenta dot) sits on the white
# plate so every part of it stays visible on the magenta scene — the
# on-dark lockup's magenta dot would vanish on this ground (QA round 1).
# The plate is clear of the badge, which ends at y=400.
s5 = scene_with_image("s5.mp4", 5.5, MAGENTA, [
    dt(F_INTER, 104, WHITE, "YOUR MOVE", 520),
    dt(F_INTER, 66, WHITE, "enter your AI agent", 700),
    dt(F_INTER, 66, WHITE, "in a bounty", 790),
    dt(F_INTER, 58, INK, "make.fun", 1030, boxcolor=WHITE),
    "drawbox=x=200:y=1218:w=680:h=262:color=white:t=fill",
], LOCKUP, 640, "(W-w)/2", 1250)
# S6 27.5-29.5 — join line; last frame is the end-card backdrop + loop echo.
s6 = scene("s6.mp4", 2.0, WHITE, [
    dt(F_INTER, 96, INK, "JOIN FREE", 620),
    dt(F_INTER, 58, MAGENTA, "make.fun/r/" + REFERRAL_CODE, 790),
    dt(F_INTER, 54, INK, "it starts with $500", 1560),
])

# ---------- concat main programme ----------
lst = os.path.join(WORK, "concat.txt")
with open(lst, "w") as f:
    for p in [s1, s2, s3, s4, s5, s6]:
        f.write(f"file '{p}'\n")
main = os.path.join(WORK, "main.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
     "-i", lst, "-c", "copy", main])

# ---------- brand badge from frame 0 until the end card ----------
badged = os.path.join(WORK, "main_badged.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", main, "-i", BADGE,
     "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v]",
     "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
     badged])

# ---------- end card (2.5 s): official transparent card over the blurred,
# desaturated last frame; referral code typed in once the field rests.
lastframe = os.path.join(WORK, "lastframe.png")
run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i", badged,
     "-frames:v", "1", lastframe])
end = os.path.join(WORK, "end.mp4")
fc = ("[0:v]gblur=sigma=28,hue=s=0.35[bg];"
      "[bg][1:v]overlay=0:0:format=auto[card];"
      "[card]drawbox=x=208:y=1230:w=9:h=82:color=white:t=fill[cb];"
      f"[cb]drawtext=fontfile={F_JBM}:text='{REFERRAL_CODE}':fontsize=62:"
      f"fontcolor={INK}:x=210:y=1240:enable='gte(t,1.5)'[out]")
run(["ffmpeg", "-y", "-loglevel", "error",
     "-loop", "1", "-framerate", str(FPS), "-t", "2.5", "-i", lastframe,
     "-i", CARD, "-filter_complex", fc, "-map", "[out]", "-t", "2.5",
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), end])

# ---------- original synth music (32 s, made here from sines) ----------
music = os.path.join(WORK, "music.wav")
run(["ffmpeg", "-y", "-loglevel", "error",
     "-f", "lavfi", "-i", "sine=frequency=55:duration=32",
     "-f", "lavfi", "-i", "sine=frequency=110:duration=32",
     "-f", "lavfi", "-i", "sine=frequency=220:duration=32",
     "-f", "lavfi", "-i", "sine=frequency=440:duration=32",
     "-filter_complex",
     "[0:a]volume=0.50,tremolo=f=2:d=0.4[a0];"
     "[1:a]volume=0.30,tremolo=f=4:d=0.6[a1];"
     "[2:a]volume=0.16,tremolo=f=8:d=0.8[a2];"
     "[3:a]volume=0.07,tremolo=f=8:d=0.9[a3];"
     "[a0][a1][a2][a3]amix=inputs=4:normalize=0,"
     "afade=t=in:st=0:d=0.3,afade=t=out:st=31.0:d=1.0[a]",
     "-map", "[a]", "-t", "32", music])

# ---------- final mux ----------
out = os.path.join(ROOT, "bring-the-humans-03.mp4")
run(["ffmpeg", "-y", "-loglevel", "error",
     "-i", badged, "-i", end, "-i", music,
     "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
     "-map", "[v]", "-map", "2:a",
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
     "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out])
print("DONE:", out)
