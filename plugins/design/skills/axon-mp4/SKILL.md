---
name: "axon-mp4"
description: "Turn an /axon animated build page (axon-build.html) into a branded MP4 for Shorts, Reels, TikTok (9:16) or the Instagram feed (4:5), with a circular logo and brand name in the header."
---

# Axon build page to MP4 (/axon-mp4)

Takes the `axon-build.html` that the `exploded-axon` skill makes and renders it into a smooth, ready-to-post video. One command; no screen recording and no manual editing.

The video is recorded frame by frame against a virtual clock, so there are no dropped frames and the lines stay sharp. A full render takes about 50 seconds. The logo and brand name appear **only in the video**, never in the PNG, SVG or build page.

## 1. Ask first (one AskUserQuestion call; skip anything the user already said)
- **Format.** Options:
  - **9:16, 1080×1920** (YouTube Shorts, Reels, TikTok). The drawing is scaled to 900 px wide and centered, with clear space under the top bar, the right-side buttons and the caption area, so the platform UI doesn't crop it. Default.
  - **4:5, 1080×1350** (Instagram feed).
  - **Both.**
- **Logo.** Ask the user to upload a logo image, or to say "no logo". A circular PNG with a transparent background is used as-is. Any other image is center-cropped to a circle with a white ring automatically. If the logo has text or detail near the edges, ask for a pre-cropped circle instead.
- **Brand name** (shown beside the logo, in capitals). Default: the credit line from the user's style, otherwise none.

If the user isn't around, use 9:16, the logo they gave, and no brand text if none was given. State what you did.

## 2. Setup (once per session)
```bash
pip install --break-system-packages -q playwright pillow
which ffmpeg || echo "ffmpeg missing"
ls /usr/bin/google-chrome /usr/bin/chromium /usr/bin/chromium-browser 2>/dev/null || python3 -m playwright install chromium
mkdir -p ~/.fonts && [ -f ~/.fonts/Manrope.ttf ] || curl -sSLf -o ~/.fonts/Manrope.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf"; fc-cache -f
```
If the Chromium download is blocked and no system Chrome exists, say so and give the user the build page to screen-record instead (Space to run).

Write the script in section 5 to `axon_mp4.py` exactly as given.

## 3. Render
```bash
# 9:16 for Shorts / Reels / TikTok
python3 axon_mp4.py axon-build.html axon-9x16.mp4 --ratio 9x16 --logo logo.png --brand "THE ARCHITECTURE GRIND"
# 4:5 for Instagram feed
python3 axon_mp4.py axon-build.html axon-4x5.mp4 --ratio 4x5 --logo logo.png --brand "THE ARCHITECTURE GRIND"
```
Options: `--bg "#F5F3EE"` (must match the sheet background, so use the style block's `bg`), `--ink "#2A2A2A"` (brand text color, so use the style's `ink`), `--duration 21` (seconds of animation to capture), `--hold 1` (extra seconds holding the final frame), `--fps 30`, `--brand none` to drop the text.

The default build page runs about 20 seconds. If a plan has many rooms or a different style makes it longer, make sure the last frame shows the finished sheet (see the check below) and raise `--duration`.

## 4. Check before delivering
Extract the final frame and one frame from about 3 seconds in:
```bash
ffmpeg -y -loglevel error -sseof -0.4 -i axon-9x16.mp4 -frames:v 1 last.png
ffmpeg -y -loglevel error -ss 3 -i axon-9x16.mp4 -frames:v 1 mid.png
```
Open both. Confirm: the final frame shows the complete sheet (title, legend and footer all visible); the logo is a clean circle with no cropped edges; the brand text and logo sit together in the top-right and don't overlap the sheet header; the background matches around the drawing. If the sheet isn't finished, raise `--duration` and re-render.

Send the MP4(s) with SendUserFile. Mention the duration and size.

## 5. Script: axon_mp4.py
```python
#!/usr/bin/env python3
"""
axon_mp4.py - Turn an /axon animated build page (HTML) into a branded MP4.
Deterministic frame-by-frame capture (virtual clock), so no dropped frames, then ffmpeg.

Usage:
  python3 axon_mp4.py build.html out.mp4 [--ratio 9x16|4x5] [--logo logo.png]
         [--brand "THE ARCHITECTURE GRIND"] [--bg "#F5F3EE"] [--ink "#2A2A2A"]
         [--duration 21] [--hold 1] [--fps 30]
Needs: playwright (+ system Chrome/Chromium), ffmpeg, Pillow. Font: Manrope (~/.fonts) else DejaVu Sans Bold.
--logo: a circular PNG with transparency is used as-is; any other image is center-cropped to a circle with a white ring.
"""
import asyncio, glob, os, shutil, subprocess, sys, tempfile, time
from PIL import Image, ImageDraw, ImageFilter, ImageFont

VT = r"""
(()=>{
 const oST = window.setTimeout.bind(window);
 let vnow = 0, tid = 1; const timers = [], rafs = [], anims = [];
 const flush = () => new Promise(r => oST(r, 0));
 window.setTimeout = (fn, ms = 0, ...a) => { const id = tid++; timers.push({t: vnow + Math.max(0, ms||0), fn: () => fn(...a), id}); return id; };
 window.clearTimeout = id => { const i = timers.findIndex(t => t.id === id); if (i >= 0) timers.splice(i, 1); };
 performance.now = () => vnow;
 window.requestAnimationFrame = f => { rafs.push(f); return rafs.length; };
 const orig = Element.prototype.animate;
 Element.prototype.animate = function(kf, opt) {
   const a = orig.call(this, kf, opt); a.pause(); a.currentTime = 0;
   const dur = (opt.duration || 0) + (opt.delay || 0); let res; const p = new Promise(r => res = r);
   anims.push({a, start: vnow, end: vnow + dur, res, done: false});
   Object.defineProperty(a, 'finished', {value: p}); return a;
 };
 const tickAnims = () => anims.forEach(r => { r.a.currentTime = Math.max(0, vnow - r.start);
   if (!r.done && vnow >= r.end) { r.done = true; r.res(); } });
 window.__vt = { async step(ms) {
   const target = vnow + ms;
   for (let guard = 0; guard < 500; guard++) {
     timers.sort((a, b) => a.t - b.t || a.id - b.id);
     const nextT = timers.length ? timers[0].t : Infinity;
     const nextA = Math.min(...anims.filter(r => !r.done).map(r => r.end), Infinity);
     const nxt = Math.min(nextT, nextA);
     if (nxt > target) break;
     vnow = Math.max(vnow, nxt);
     if (nextT <= nextA) { const t = timers.shift(); try { t.fn(); } catch (e) {} }
     tickAnims(); await flush(); await flush();
   }
   vnow = target;
   const rs = rafs.splice(0); rs.forEach(f => { try { f(vnow); } catch (e) {} });
   tickAnims(); await flush(); await flush();
 }};
})();
"""

def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def find_chrome():
    for c in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if os.path.exists(c): return c
    return None

def font(size):
    for p in (os.path.expanduser("~/.fonts/Manrope.ttf"), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            try: f.set_variation_by_name("Bold")
            except Exception: pass
            return f
    return ImageFont.load_default()

def prep_logo(path, size=512, ring=16):
    src = Image.open(path).convert("RGBA")
    a = src.split()[3]
    if a.getextrema()[0] < 250:                      # already has transparency (circle) -> use as is
        out = src.resize((size, size), Image.LANCZOS)
    else:                                            # opaque image -> center circle + white ring
        s = min(src.size); l, t = (src.width - s) // 2, (src.height - s) // 2
        sq = src.crop((l, t, l + s, t + s)).convert("RGB")
        inner = size // 2 - ring; S = 4
        disc = sq.resize((inner * 2, inner * 2), Image.LANCZOS)
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        m = Image.new("L", (size * S, size * S), 0); ImageDraw.Draw(m).ellipse((0, 0, size * S - 1, size * S - 1), fill=255)
        out.paste(Image.new("RGBA", (size, size), (255, 255, 255, 255)), (0, 0), m.resize((size, size), Image.LANCZOS))
        m2 = Image.new("L", (inner * 2 * S,) * 2, 0); ImageDraw.Draw(m2).ellipse((0, 0, inner * 2 * S - 1, inner * 2 * S - 1), fill=255)
        out.paste(disc, (ring, ring), m2.resize((inner * 2, inner * 2), Image.LANCZOS))
    pad = 40
    c = Image.new("RGBA", (size + 2 * pad,) * 2, (0, 0, 0, 0))
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.paste(Image.new("RGBA", out.size, (0, 0, 0, 90)), (pad, pad + 8), out.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(14)); sh.alpha_composite(out, (pad, pad))
    return sh, pad / size                            # shadowed logo, pad as fraction of logo size

def header_overlay(W, H, cy, right, D, logo, brand, ink):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    lg, pf = None, 0
    if logo:
        lg, pf = logo
        k = D / 512; lg = lg.resize((round(lg.width * k), round(lg.height * k)), Image.LANCZOS)
        pad = (lg.width - D) / 2
        ov.alpha_composite(lg, (round(right - D - pad), round(cy - D / 2 - pad)))
    if brand:
        f = font(round(D * 0.4)); sp = D * 0.053
        tw = sum(d.textlength(c, font=f) + sp for c in brand) - sp
        x = right - (D + D / 3 if logo else 0) - tw
        for c in brand:
            d.text((x, cy), c, font=f, fill=hex2rgb(ink) + (255,), anchor="lm"); x += d.textlength(c, font=f) + sp
    return ov

async def capture(html, frames_dir, fps, dur):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        kw = {}
        ch = find_chrome()
        if ch: kw["executable_path"] = ch
        b = await p.chromium.launch(**kw)
        ctx = await b.new_context(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        await ctx.add_init_script(VT)
        pg = await ctx.new_page()
        await pg.goto("file://" + os.path.abspath(html))
        await pg.add_style_tag(content="#sheet{height:100vh!important;max-width:100vw!important;border-radius:0!important;box-shadow:none!important}#hint{display:none!important}#caret{animation:none!important}")
        await asyncio.sleep(0.3)
        await pg.evaluate("run(); 0")
        n = int(fps * dur)
        for i in range(n):
            await pg.evaluate(f"__vt.step({1000 / fps})")
            await pg.screenshot(path=os.path.join(frames_dir, f"f{i:04d}.png"))
        await b.close()
    return n

def main():
    a = sys.argv[1:]
    opt = dict(ratio="9x16", logo=None, brand="THE ARCHITECTURE GRIND", bg="#F5F3EE", ink="#2A2A2A", duration="21", hold="1", fps="30")
    pos = []
    i = 0
    while i < len(a):
        if a[i].startswith("--"): opt[a[i][2:]] = a[i + 1]; i += 2
        else: pos.append(a[i]); i += 1
    html, out = pos[0], pos[1]
    fps, dur, hold = int(opt["fps"]), float(opt["duration"]), float(opt["hold"])
    if opt["brand"].lower() in ("none", ""): opt["brand"] = ""
    tmp = tempfile.mkdtemp(prefix="axonmp4_")
    try:
        t0 = time.time()
        n = asyncio.run(capture(html, tmp, fps, dur))
        print(f"captured {n} frames in {time.time() - t0:.0f}s")
        logo = prep_logo(opt["logo"]) if opt["logo"] else None
        if opt["ratio"] == "9x16":
            W, H, sw, sh, px, py, cy, D, right = 1080, 1920, 900, 1125, 90, 300, 232, 60, 990
        elif opt["ratio"] == "4x5":
            W, H, sw, sh, px, py, cy, D, right = 1080, 1350, 950, 1188, 65, 150, 78, 54, 1015
        else:
            sys.exit("ratio must be 9x16 or 4x5")
        ov = header_overlay(W, H, cy, right, D, logo, opt["brand"], opt["ink"])
        ovp = os.path.join(tmp, "header.png"); ov.save(ovp)
        bg = opt["bg"].lstrip("#")
        fc = (f"[0:v]scale={sw}:{sh}:flags=lanczos,pad={W}:{H}:{px}:{py}:color=0x{bg},format=rgba[b];"
              f"[b][1:v]overlay=0:0,tpad=stop_mode=clone:stop_duration={hold},format=yuv420p")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%04d.png"),
                        "-i", ovp, "-filter_complex", fc, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                        "-movflags", "+faststart", out], check=True)
        print("wrote", out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
```