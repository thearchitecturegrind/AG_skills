---
name: "exploded-axon"
description: "Turn an uploaded floor plan image or PDF into an exploded axonometric (roof / walls / floor) diagram with imperial units, zone areas and an animated build page. Supports custom style blocks."
---

# Exploded Axon from a Floor Plan (/axon)

The user uploads a floor plan. You turn it into a presentation-ready exploded axonometric with three layers: a roof slab, walls (with window and door openings and glass), and a floor slab colored by zone (night / day / wet-service / circulation). The sheet also gets callouts, a legend with areas in **sq ft**, and a title block. Everything is in feet and inches.

The drawing is generated in code from a plan JSON that you transcribe, so geometry and areas are computed, not estimated. Every run produces:
- **axon.png** and **axon.svg** (editable in Illustrator, Figma or Affinity): the static sheet.
- **axon-build.html**: an animated build made for screen recording. A command bar types `/axon floor-plan.jpg`, the input plan card appears, the floor fills in zone by zone, the walls lift and print face by face, the roof drops in, the callout leaders draw, the title types out and the legend numbers count up. Space or click runs it, R resets.

To turn the build page into a video, use the separate `axon-mp4` skill.

## 1. Ask first (one AskUserQuestion call, only for what the plan doesn't answer)
1. **Style reference.** "Do you want to add a style reference?" Options:
   - **Default style**: warm off-white background, charcoal ink, yellow accent, Manrope + STIX Two Text.
   - **Upload a reference image**: see section 2b.
   - **Paste a style block**: the user pastes JSON from their own style doc (schema in section 2a).
2. **Scale:** if there's no overall dimension string or scale bar, ask for one overall dimension.
3. **North:** is plan-up north? If not, which way is north?
4. **Sheet text:** project name, subtitle, sheet number (e.g. "01 / 06"). Defaults: "Project", blank, "01 / 01". Wall height defaults to 9'-0".

If the user isn't around, use the defaults and list them in your reply.

## 2a. Style block
A style block is a small JSON file. Every key is optional; missing keys use the default style.
```json
{
  "bg": "#F5F3EE",          // sheet background
  "ink": "#2A2A2A",         // text, rules, outlines, wall tops
  "mute": "#6E6A63",        // secondary text
  "accent": "#F2C230",      // title rule, north arrow
  "glass": "#F7DA74",       // window / slider glass
  "surface": "#FFFFFF",     // wall, slab and roof faces (shaded sides are derived)
  "edge": "#2A2A2A",        // outline color on faces
  "guide": "#8A857D",       // dashed explode guides
  "zones": {"day": "#F7D774", "night": "#D9D5CD", "wet": "#AFA99F", "circ": "#FBEDBC", "outdoor": "#ECE8E1"},
  "fonts": {"sans": "Manrope", "serif": "STIX Two Text"},   // Google Fonts family names
  "credit": "Your Studio"   // bottom-right credit line
}
```
Save it as `style.json` and pass `--style style.json` when rendering.

**Fonts.** The script embeds fonts named `<FamilyNoSpaces>.ttf` found in `~/.fonts`. For each family in the style block, try:
```bash
F="Manrope"; L=$(echo $F | tr 'A-Z' 'a-z' | tr -d ' ')
curl -sSLf -o ~/.fonts/$(echo $F | tr -d ' ').ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/$L/$(echo $F | tr -d ' ')%5Bwght%5D.ttf" && fc-cache -f
```
If the download fails (404 or a non-variable font), fall back to the default fonts and tell the user which font you couldn't get.

## 2b. Style from a reference image
Look at the image. Sample its dominant colors with Pillow (`Image.quantize(6)`), then choose: `bg` (lightest or darkest large area), `ink` (high-contrast text color), `accent` (the most saturated color), `surface` (a near-white or a lighter tint of the bg), and four zone tints from the palette. Pick the closest Google Fonts pair to the lettering you see. Write `style.json`, render once, and show the PNG. Tell the user what you picked and offer one round of tweaks.

## 3. Setup (once per session)
```bash
pip install --break-system-packages -q shapely
mkdir -p ~/.fonts && cd ~/.fonts && \
curl -sSLf -o Manrope.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf" && \
curl -sSLf -o STIXTwoText.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/stixtwotext/STIXTwoText%5Bwght%5D.ttf" && fc-cache -f
```
Write the script in section 7 to `explode_axon.py` exactly as given. `rsvg-convert` exports the PNG.

## 4. Transcribe the plan to JSON (the step that matters most)
Work in **feet**. Use plan coordinates with the origin at the top-left outer corner, x to the right and **y down** (the same way the image reads).

1. **Scale.** Take the pixel positions of the outer wall faces and divide by the overall dimension to get px per ft. Check the result against the second dimension; the two should agree within about 2%.
2. **footprint.** Trace the outer face of the *enclosed* building as a polygon. Leave out porches and decks.
3. **walls.** Enter centerlines, axis-aligned, with `t` = thickness in feet. Typical values: exterior 0.75 (9"), interior 0.42 (5"). An exterior centerline sits t/2 inside the footprint. Make walls meet at shared centerline points, and stop each partition at the centerline of the wall it hits.
4. **openings.** Give two points on the host wall's centerline plus a `type`:
   - `window`: default sill 3 and head 7. Use sill 5 for baths and 3.5–4 over counters.
   - `door`: a gap from 0 to 7.
   - `slider`: full glass from 0 to 7.

   Read door positions from the swing arcs. Open-plan boundaries get **no** wall.
5. **rooms.** Give rectangles (or a `poly`) drawn to the wall centerlines; the script subtracts the walls. Zones:
   - `night`: bedrooms
   - `day`: living, dining, kitchen
   - `wet`: baths, laundry, mechanical
   - `circ`: halls and entries
6. **outdoor.** Add porches and decks, with `"covered": true` if the roof extends over them.
7. **furniture** (optional). Rectangles for beds, sofas, tables and counters, drawn as faint outlines on the floor.

Example (the test house, 41'-0" × 30'-10"):
```json
{
  "project": "Single-Story House", "subtitle": "Example Project", "sheet": "01 / 06",
  "source": "plan A-101", "north": 0,
  "heights": {"wall": 9, "slab": 1, "roof": 1.5, "overhang": 1.5, "sill": 3, "head": 7},
  "view": {"azimuth": 15, "elevation": 35, "explode": 19},
  "footprint": [[0,0],[41,0],[41,30.83],[33.6,30.83],[33.6,22.8],[0,22.8]],
  "walls": [
    {"a":[0.375,0.375],"b":[40.625,0.375],"t":0.75},
    {"a":[0.375,0.375],"b":[0.375,22.425],"t":0.75},
    {"a":[0.375,22.425],"b":[40.625,22.425],"t":0.75},
    {"a":[40.625,0.375],"b":[40.625,30.455],"t":0.75},
    {"a":[33.975,22.425],"b":[33.975,30.455],"t":0.75},
    {"a":[33.975,30.455],"b":[40.625,30.455],"t":0.75},
    {"a":[12.7,0.375],"b":[12.7,12.95],"t":0.42},
    {"a":[0.375,12.95],"b":[12.7,12.95],"t":0.42},
    {"a":[12.7,6.9],"b":[28.2,6.9],"t":0.42},
    {"a":[20.5,0.375],"b":[20.5,6.9],"t":0.42},
    {"a":[28.2,0.375],"b":[28.2,12.95],"t":0.42},
    {"a":[28.2,12.95],"b":[40.625,12.95],"t":0.42}
  ],
  "openings": [
    {"type":"window","a":[6.5,0.375],"b":[8.7,0.375]},
    {"type":"window","a":[18.3,0.375],"b":[20.0,0.375],"sill":5},
    {"type":"slider","a":[28.4,22.425],"b":[33.6,22.425]},
    {"type":"door","a":[12.7,9.5],"b":[12.7,12.3]}
  ],
  "rooms": [
    {"name":"Bedroom","zone":"night","rect":[0,0,12.7,12.95]},
    {"name":"Bathroom","zone":"wet","rect":[12.7,0,20.5,6.9]},
    {"name":"Living Room","zone":"day","rect":[12.7,6.9,28.2,22.8]},
    {"name":"Laundry","zone":"wet","rect":[33.975,22.425,41,30.83]}
  ],
  "outdoor": [{"name":"Covered porch","rect":[25.5,22.8,33.6,30.0],"covered":true}],
  "furniture": [{"rect":[2.7,0.8,8.4,7.5]}, {"rect":[16.9,12.8,24.3,15.5]}]
}
```
(Openings and rooms are trimmed here. Transcribe every one from the real plan.) Use "Story" spelling (US) unless the user writes "Storey".

## 5. Render and check
Copy the uploaded plan next to the script as `floor-plan.jpg` (or `.png`); the animated page shows it as the input card.
```bash
python3 explode_axon.py plan.json axon.svg --html axon-build.html --input floor-plan.jpg   # add --style style.json or --theme dark
rsvg-convert -w 2160 axon.svg -o axon.png
```
**Always open the PNG and check it before delivering:**
- Every wall, window and door is in the right place. Compare against the source plan wall by wall.
- The overall size in the summary line matches the plan's dimension strings.
- The zone colors make sense, and the net area is a little smaller than the gross.
- The layers don't collide. If walls overlap the floor, raise `view.explode` (try 19–24). For a flatter, more plan-like look, raise `elevation` (try 35–45).

Fix the JSON and re-render until it's right.

## 6. Deliver
- Publish `axon-build.html` as an artifact (title: "/axon - exploded axonometric build"). To screen-record it, open it, go full screen, start recording, then press Space.
- Send `axon.png` and `axon.svg` with SendUserFile.
- In your reply, list the assumptions you made (scale, north, heights, sills, style) and mention the `axon-mp4` skill for a video.

**Limits:** walls must be orthogonal (angled walls aren't supported yet), the roof is a flat slab, and only single-storey plans work.

## 7. Script: explode_axon.py
```python
#!/usr/bin/env python3
"""
explode_axon.py - Exploded axonometric (roof / walls / floor) from a floor-plan JSON.
Imperial units. Default style: charcoal + yellow, STIX Two Text + Manrope.

Usage:
    python3 explode_axon.py plan.json out.svg [--theme light|dark] [--style style.json] [--html build.html --input plan.jpg]
    rsvg-convert -w 2160 out.svg -o out.png        # PNG export
All values in FEET, plan coords x right / y DOWN. See SKILL.md for the plan and style schemas.
"""
import json, math, sys
from shapely.geometry import LineString, Polygon, box, Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

THEMES = {
    "light": dict(bg="#F5F3EE", ink="#2A2A2A", mute="#6E6A63", rule="#2A2A2A",
                  poche="#2A2A2A", face_s="#FFFFFF", face_e="#E2DED6", edge="#2A2A2A",
                  slab_top="#FFFFFF", slab_s="#D9D5CD", slab_e="#C8C3BA",
                  roof_top="#FFFFFF", glass="#F7DA74", guide="#8A857D", accent="#F2C230",
                  floorwall="#9A958C", furn="#2A2A2A",
                  zones=dict(day="#F7D774", night="#D9D5CD", wet="#AFA99F", circ="#FBEDBC",
                             outdoor="#ECE8E1")),
    "dark": dict(bg="#1E1E1E", ink="#F1EEE7", mute="#A8A39A", rule="#F1EEE7",
                 poche="#F2C230", face_s="#3A3A3A", face_e="#2F2F2F", edge="#0F0F0F",
                 slab_top="#454545", slab_s="#2B2B2B", slab_e="#242424",
                 roof_top="#4A4A4A", glass="#F2C230", guide="#77736C", accent="#F2C230",
                 floorwall="#1A1A1A", furn="#F1EEE7",
                 zones=dict(day="#C99E22", night="#6B6862", wet="#55524D", circ="#8C7A44",
                            outdoor="#3C3C3C")),
}
SANS_DEFAULT, SERIF_DEFAULT = "Manrope", "STIX Two Text"


def apply_style(style):
    """Build THEMES['custom'] from a style block. Missing keys fall back to the light theme."""
    import copy
    t = copy.deepcopy(THEMES["light"])
    for k in ("bg", "ink", "mute", "accent", "glass", "guide"):
        if k in style:
            t[k] = style[k]
    if "ink" in style:
        t["rule"] = t["edge"] = t["poche"] = t["furn"] = style["ink"]
    if "surface" in style:
        def shade(c, f):
            c = c.lstrip("#"); return "#%02X%02X%02X" % tuple(int(int(c[i:i + 2], 16) * f) for i in (0, 2, 4))
        sf = style["surface"]
        t.update(face_s=sf, roof_top=sf, slab_top=sf, face_e=shade(sf, .88), slab_s=shade(sf, .85), slab_e=shade(sf, .76))
        t["floorwall"] = shade(sf, .62)
    if "edge" in style:
        t["edge"] = style["edge"]
    if "accent" in style and "glass" not in style:
        t["glass"] = style["accent"]
    for z, c in style.get("zones", {}).items():
        t["zones"][z] = c
    t["sans"] = style.get("fonts", {}).get("sans", SANS_DEFAULT)
    t["serif"] = style.get("fonts", {}).get("serif", SERIF_DEFAULT)
    THEMES["custom"] = t
    return "custom"


ZONE_LABEL = dict(night="Night", day="Day", wet="Wet / service", circ="Circulation")


def fi(v):
    neg = v < 0
    inches = round(abs(v) * 12)
    s = f"{inches // 12}'-{inches % 12}\""
    return "-" + s if neg else s


def W(p):
    return (p[0], -p[1])


def rect_poly(r):
    x1, y1, x2, y2 = r
    return box(min(x1, x2), -max(y1, y2), max(x1, x2), -min(y1, y2))


def room_poly(r):
    return rect_poly(r["rect"]) if "rect" in r else Polygon([W(p) for p in r["poly"]])


def polys(g):
    if g.is_empty:
        return []
    return [g] if g.geom_type == "Polygon" else [p for p in g.geoms if p.geom_type == "Polygon"]


class Cam:
    def __init__(self, az, el):
        a, e = math.radians(az), math.radians(el)
        self.c = (math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))
        self.r = (math.cos(a), math.sin(a), 0.0)
        cx, cy, cz = self.c
        rx, ry, rz = self.r
        self.u = (cy * rz - cz * ry, cz * rx - cx * rz, cx * ry - cy * rx)
        self.ch = (math.sin(a), -math.cos(a))

    def p(self, x, y, z):
        return (x * self.r[0] + y * self.r[1] + z * self.r[2],
                -(x * self.u[0] + y * self.u[1] + z * self.u[2]))

    def depth(self, x, y, z):
        return x * self.c[0] + y * self.c[1] + z * self.c[2]


def side_faces(cam, poly, z0, z1, fill_s, fill_e, edge, zrange_fn=None, chunk=1.0):
    out = []
    poly = orient(poly, 1.0)
    for ring in [poly.exterior] + list(poly.interiors):
        pts = list(ring.coords)
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy)
            if L < 1e-6:
                continue
            nx, ny = dy / L, -dx / L
            if nx * cam.ch[0] + ny * cam.ch[1] <= 1e-6:
                continue
            zz0, zz1 = z0, z1
            if zrange_fn:
                zr = zrange_fn((x1 + x2) / 2 + nx * 0.05, (y1 + y2) / 2 + ny * 0.05)
                if zr:
                    zz0, zz1 = max(z0, zr[0]), min(z1, zr[1])
                    if zz1 - zz0 < 1e-3:
                        continue
            n = max(1, math.ceil(L / chunk))
            fill = fill_s if abs(ny) >= abs(nx) else fill_e
            for i in range(n):
                ax, ay = x1 + dx * i / n, y1 + dy * i / n
                bx, by = x1 + dx * (i + 1) / n, y1 + dy * (i + 1) / n
                quad = [(ax, ay, zz0), (bx, by, zz0), (bx, by, zz1), (ax, ay, zz1)]
                d = sum(cam.depth(*q) for q in quad) / 4
                lines = [(quad[0], quad[1]), (quad[3], quad[2])]
                if i == 0: lines.append((quad[0], quad[3]))
                if i == n - 1: lines.append((quad[1], quad[2]))
                out.append((d, quad, fill, edge, 0.9, lines))
    return out


def poly_path(cam, poly, z):
    s = ""
    for ring in [poly.exterior] + list(poly.interiors):
        pts = [cam.p(x, y, z) for x, y in ring.coords]
        s += "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in pts) + " Z "
    return s


def build(plan, theme="light"):
    T = THEMES[theme]
    H = dict(wall=9, slab=1, roof=1.5, overhang=1.5, sill=3, head=7)
    H.update(plan.get("heights", {}))
    V = dict(azimuth=15, elevation=35, explode=19)
    V.update(plan.get("view", {}))
    cam = Cam(V["azimuth"], V["elevation"])
    gap = V["explode"]
    zW = gap
    zR = gap * 2 + H["wall"]

    foot = Polygon([W(p) for p in plan["footprint"]])
    walls = [(LineString([W(w["a"]), W(w["b"])]), w.get("t", 0.5)) for w in plan["walls"]]
    walls_u = unary_union([ls.buffer(t / 2, cap_style="square", join_style="mitre") for ls, t in walls])

    ops = []
    for o in plan.get("openings", []):
        ls = LineString([W(o["a"]), W(o["b"])])
        host = max(walls, key=lambda w: w[0].buffer(0.05).intersection(ls).length)
        t = host[1]
        typ = o.get("type", "window")
        sill = o.get("sill", 0 if typ in ("door", "slider") else H["sill"])
        head = o.get("head", H["head"])
        rect = ls.buffer(t / 2 + 0.02, cap_style="flat")
        ops.append(dict(type=typ, ls=ls, t=t, sill=sill, head=head, rect=rect,
                        piece=walls_u.intersection(rect)))
    ops_u = unary_union([o["rect"] for o in ops]) if ops else Polygon()
    solid = walls_u.difference(ops_u)

    def jamb_z(mx, my):
        pt = Point(mx, my)
        for o in ops:
            if o["rect"].contains(pt):
                return (o["sill"], o["head"])
        return None

    minx, miny, maxx, maxy = foot.bounds
    guide_lines = []
    for cx_, cy_ in [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)]:
        guide_lines.append((cam.p(cx_, cy_, 0), cam.p(cx_, cy_, zW)))
        guide_lines.append((cam.p(cx_, cy_, zW + H["wall"]), cam.p(cx_, cy_, zR + H["wall"])))

    # FLOOR (tagged groups so the build page can animate each part)
    floor_items = []
    out_polys = [(rect_poly(o["rect"]) if "rect" in o else Polygon([W(p) for p in o["poly"]]), o)
                 for o in plan.get("outdoor", [])]
    sides = []
    for p in polys(foot):
        sides += side_faces(cam, p, -H["slab"], 0, T["slab_s"], T["slab_e"], T["edge"])
    for op_, _ in out_polys:
        for p in polys(op_.difference(foot)):
            sides += side_faces(cam, p, -H["slab"], -0.35, T["slab_s"], T["slab_e"], T["edge"])
    sides.sort(key=lambda f: f[0])
    floor_items += [("open", "fl-slab")] + [("quad", f) for f in sides]
    for op_, _ in out_polys:
        for p in polys(op_.difference(foot)):
            floor_items.append(("path", poly_path(cam, p, -0.35), T["zones"]["outdoor"], T["edge"], 0.9))
    for p in polys(foot):
        floor_items.append(("path", poly_path(cam, p, 0), T["slab_top"], T["edge"], 1.1))
    floor_items += [("close",), ("open", "fl-zones")]
    zone_area, rooms_net = {}, 0.0
    for r in plan.get("rooms", []):
        rp = room_poly(r).intersection(foot).difference(walls_u)
        z = r.get("zone", "day")
        zone_area[z] = zone_area.get(z, 0) + rp.area
        rooms_net += rp.area
        floor_items.append(("open", None, f"zone z-{z}"))
        for p in polys(rp):
            floor_items.append(("path", poly_path(cam, p, 0), T["zones"].get(z, T["zones"]["day"]), "none", 0))
        floor_items.append(("close",))
    floor_items += [("close",), ("open", "fl-walls")]
    for p in polys(solid.union(unary_union([o["piece"] for o in ops if o["type"] == "window"] or [Polygon()]))):
        floor_items.append(("path", poly_path(cam, p, 0), T["floorwall"], "none", 0))
    floor_items += [("close",), ("open", "fl-furn")]
    for f in plan.get("furniture", []):
        for p in polys(rect_poly(f["rect"])):
            floor_items.append(("path", poly_path(cam, p, 0), "none", T["furn"], 0.6, 0.45))
    floor_items.append(("close",))

    # WALLS
    wf = []
    for p in polys(solid):
        wf += side_faces(cam, p, zW, zW + H["wall"], T["face_s"], T["face_e"], T["edge"], jamb_z)
    tops = list(polys(solid))
    for o in ops:
        for p in polys(o["piece"]):
            if o["sill"] > 0:
                wf += side_faces(cam, p, zW, zW + o["sill"], T["face_s"], T["face_e"], T["edge"])
                qt = [(x, y, zW + o["sill"]) for x, y in list(orient(p).exterior.coords)[:-1]]
                wf.append((sum(cam.depth(*q) for q in qt) / len(qt), qt, T["face_e"], T["edge"], 0.9))
            if o["head"] < H["wall"]:
                wf += side_faces(cam, p, zW + o["head"], zW + H["wall"], T["face_s"], T["face_e"], T["edge"])
                tops.append(p)
        if o["type"] in ("window", "slider"):
            (ax, ay), (bx, by) = list(o["ls"].coords)
            n = max(1, math.ceil(o["ls"].length / 1.0))
            for i in range(n):
                x1, y1 = ax + (bx - ax) * i / n, ay + (by - ay) * i / n
                x2, y2 = ax + (bx - ax) * (i + 1) / n, ay + (by - ay) * (i + 1) / n
                q = [(x1, y1, zW + o["sill"]), (x2, y2, zW + o["sill"]), (x2, y2, zW + o["head"]), (x1, y1, zW + o["head"])]
                ln = [(q[0], q[1]), (q[3], q[2])]
                if i == 0: ln.append((q[0], q[3]))
                if i == n - 1: ln.append((q[1], q[2]))
                wf.append((sum(cam.depth(*v) for v in q) / 4 + 0.01, q, T["glass"], T["edge"], 0.6, ln))
    wf.sort(key=lambda f: f[0])
    wall_items = [("open", "wl-faces")] + [("quad", f) for f in wf] + [("close",), ("open", "wl-top")]
    for p in polys(unary_union(tops)):
        wall_items.append(("path", poly_path(cam, p, zW + H["wall"]), T["poche"], T["poche"], 0.6))
    wall_items.append(("close",))

    # ROOF
    covered = unary_union([foot] + [op_ for op_, o in out_polys if o.get("covered")])
    roof = covered.buffer(H["overhang"], join_style="mitre")
    rz0, rz1 = zR + H["wall"], zR + H["wall"] + H["roof"]
    rs = []
    for p in polys(roof):
        rs += side_faces(cam, p, rz0, rz1, T["slab_s"], T["slab_e"], T["edge"])
    rs.sort(key=lambda f: f[0])
    roof_items = [("quad", f) for f in rs]
    for p in polys(roof):
        roof_items.append(("path", poly_path(cam, p, rz1), T["roof_top"], T["edge"], 1.1))

    def leftmost(geom, z):
        pts = [cam.p(x, y, z) for p in polys(geom) for x, y in p.exterior.coords]
        return min(pts, key=lambda q: q[0])
    anchors = dict(roof=leftmost(roof, rz1), walls=leftmost(walls_u, zW + H["wall"] * 0.55),
                   floor=leftmost(foot, 0))

    stats = dict(zone_area=zone_area, net=rooms_net, gross=foot.area,
                 n_win=sum(1 for o in ops if o["type"] == "window"),
                 n_door=sum(1 for o in ops if o["type"] == "door"),
                 n_sl=sum(1 for o in ops if o["type"] == "slider"),
                 rooms=len(plan.get("rooms", [])),
                 ext_t=max((t for _, t in walls), default=0), int_t=min((t for _, t in walls), default=0),
                 outdoor=[(o.get("name", "Outdoor"), op_.difference(foot).area) for op_, o in out_polys])
    na = math.radians(plan.get("north", 0))
    n0, n1 = cam.p(0, 0, 0), cam.p(math.sin(na), math.cos(na), 0)
    return dict(T=T, H=H, V=V, cam=cam, guides=guide_lines, floor=floor_items, walls=wall_items,
                roof=roof_items, anchors=anchors, stats=stats, north=(n0, n1),
                overall=(foot.bounds[2] - foot.bounds[0], foot.bounds[3] - foot.bounds[1]))


def render(plan, theme="light"):
    B = build(plan, theme)
    T, H, V, S = B["T"], B["H"], B["V"], B["stats"]
    PW, PH = 1080, 1350
    allpts = []
    for layer in ("floor", "walls", "roof"):
        for it in B[layer]:
            if it[0] == "quad":
                allpts += [B["cam"].p(*q) for q in it[1][1]]
    for a, b in B["guides"]:
        allpts += [a, b]
    xs, ys = [p[0] for p in allpts], [p[1] for p in allpts]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    X0, X1, Y0, Y1 = 330, 1010, 150, 930
    sc = min((X1 - X0) / (bx1 - bx0), (Y1 - Y0) / (by1 - by0))
    ox = X0 + ((X1 - X0) - (bx1 - bx0) * sc) / 2 - bx0 * sc
    oy = Y0 + ((Y1 - Y0) - (by1 - by0) * sc) / 2 - by0 * sc
    tf = lambda p: (p[0] * sc + ox, p[1] * sc + oy)
    tr = f'transform="matrix({sc:.5f},0,0,{sc:.5f},{ox:.2f},{oy:.2f})"'
    SANS = 'font-family="%s, Helvetica, Arial, sans-serif"' % T.get("sans", SANS_DEFAULT)
    SERIF = 'font-family="\'%s\', Georgia, serif"' % T.get("serif", SERIF_DEFAULT)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}">',
         f'<rect width="{PW}" height="{PH}" fill="{T["bg"]}"/>', '<g id="hdr">']
    title = f'{plan.get("project", "Project").upper()}  ·  {plan.get("subtitle", "").upper()}'.strip(" ·")
    o.append(f'<text x="70" y="88" {SANS} font-size="15" font-weight="700" letter-spacing="2.2" fill="{T["ink"]}">{title}</text>')
    o.append(f'<text x="1010" y="88" {SANS} font-size="15" font-weight="700" letter-spacing="2" text-anchor="end" fill="{T["ink"]}">{plan.get("sheet", "01 / 01")}</text>')
    o.append(f'<rect x="70" y="104" width="940" height="1.5" fill="{T["rule"]}"/>')
    o.append(f'<rect x="70" y="102" width="56" height="5" fill="{T["accent"]}"/>')
    o.append('</g>')
    o.append(f'<g id="guides" stroke="{T["guide"]}" stroke-width="1" stroke-dasharray="4 5" fill="none">')
    for gi, (a, b) in enumerate(B["guides"]):
        (x1, y1), (x2, y2) = tf(a), tf(b)
        o.append(f'<line class="{"g-lo" if gi % 2 == 0 else "g-hi"}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    o.append('</g>')

    def emit(items, gid):
        g = [f'<g id="{gid}"><g {tr} stroke-linejoin="round">']
        w = 1 / sc
        P = B["cam"].p
        for it in items:
            if it[0] == "open":
                i_d = f' id="{it[1]}"' if it[1] else ""
                cls = f' class="{it[2]}"' if len(it) > 2 else ""
                g.append(f"<g{i_d}{cls}>")
            elif it[0] == "close":
                g.append("</g>")
            elif it[0] == "quad":
                d, quad, fill, edge, sw = it[1][:5]
                lines = it[1][5] if len(it[1]) > 5 else None
                pts = " ".join(f"{P(*q)[0]:.3f},{P(*q)[1]:.3f}" for q in quad)
                g.append(f'<polygon points="{pts}" fill="{fill}" stroke="{fill}" stroke-width="{0.7 * w:.4f}"/>')
                if edge != "none":
                    if lines is None:
                        g.append(f'<polygon points="{pts}" fill="none" stroke="{edge}" stroke-width="{sw * w:.4f}"/>')
                    else:
                        dd = " ".join(f"M{P(*a)[0]:.3f},{P(*a)[1]:.3f} L{P(*b)[0]:.3f},{P(*b)[1]:.3f}" for a, b in lines)
                        g.append(f'<path d="{dd}" fill="none" stroke="{edge}" stroke-width="{sw * w:.4f}" stroke-linecap="round"/>')
            elif it[0] == "path":
                _, d, fill, edge, sw, *op = it
                opa = f' stroke-opacity="{op[0]}"' if op else ""
                stroke = f'stroke="{edge}" stroke-width="{sw * w:.4f}"' if edge != "none" else f'stroke="{fill}" stroke-width="{0.5 * w:.4f}"'
                g.append(f'<path d="{d}" fill="{fill}" fill-rule="evenodd" {stroke}{opa}/>')
        g.append('</g></g>')
        return g

    o += emit(B["floor"], "L-floor") + emit(B["walls"], "L-walls") + emit(B["roof"], "L-roof")

    o.append('<g id="north">')
    n0, n1 = B["north"]
    vx, vy = n1[0] - n0[0], n1[1] - n0[1]
    L = math.hypot(vx, vy) or 1
    vx, vy = vx / L, vy / L
    ax0, ay0 = 110, 230
    ax1, ay1 = ax0 + vx * 46, ay0 + vy * 46
    hx, hy = -vy, vx
    o.append(f'<line x1="{ax0}" y1="{ay0}" x2="{ax1:.1f}" y2="{ay1:.1f}" stroke="{T["ink"]}" stroke-width="1.6"/>')
    o.append(f'<polygon points="{ax1 + vx * 10:.1f},{ay1 + vy * 10:.1f} {ax1 + hx * 5:.1f},{ay1 + hy * 5:.1f} {ax1 - hx * 5:.1f},{ay1 - hy * 5:.1f}" fill="{T["accent"]}" stroke="{T["ink"]}" stroke-width="1"/>')
    o.append(f'<text x="{ax1 + vx * 26:.1f}" y="{ay1 + vy * 26 + 5:.1f}" {SANS} font-size="14" font-weight="800" text-anchor="middle" fill="{T["ink"]}">N</text>')
    o.append('</g>')

    callouts = [
        ("roof", "ROOF", [f'slab {fi(H["roof"])} · overhang {fi(H["overhang"])}', f'top +{fi(H["wall"] + H["roof"])}']),
        ("walls", "WALLS", [f'exterior {round(S["ext_t"] * 12)}" · partitions {round(S["int_t"] * 12)}"',
                            f'height {fi(H["wall"])} · ±0\'-0" to +{fi(H["wall"])}']),
        ("floor", "FLOOR", [f'slab {fi(H["slab"])} · finished floor ±0\'-0"',
                            f'net area {S["net"]:,.0f} sq ft · {S["rooms"]} rooms']),
    ]
    used_y = []
    for key, name, lines in callouts:
        axp, ayp = tf(B["anchors"][key])
        ly = ayp
        for uy in used_y:
            if abs(ly - uy) < 90:
                ly = uy + 90
        used_y.append(ly)
        o.append(f'<g class="callout" id="c-{key}">')
        o.append(f'<polyline pathLength="1" class="leader" points="70,{ly + 6:.1f} 250,{ly + 6:.1f} {axp:.1f},{ayp:.1f}" fill="none" stroke="{T["ink"]}" stroke-width="1"/>')
        o.append(f'<circle class="dot" cx="{axp:.1f}" cy="{ayp:.1f}" r="3.2" fill="{T["ink"]}"/>')
        o.append(f'<text class="ctext" x="70" y="{ly:.1f}" {SANS} font-size="15" font-weight="800" letter-spacing="1.6" fill="{T["ink"]}">{name}</text>')
        for i, ln in enumerate(lines):
            o.append(f'<text class="ctext" x="70" y="{ly + 26 + i * 18:.1f}" {SANS} font-size="12.5" font-weight="500" fill="{T["mute"]}">{ln}</text>')
        o.append('</g>')

    y0 = 985
    o.append(f'<rect id="rule2" x="70" y="{y0}" width="940" height="1.5" fill="{T["rule"]}"/>')
    o.append(f'<text id="title" x="70" y="{y0 + 62}" {SERIF} font-size="44" font-weight="600" fill="{T["ink"]}">Exploded axonometric</text>')
    desc = (f'Roof, walls and floor pulled apart · orthographic, from the south turned '
            f'{abs(V["azimuth"]):g}° {"east" if V["azimuth"] >= 0 else "west"}, {V["elevation"]:g}° above the horizon')
    o.append(f'<text id="desc" x="70" y="{y0 + 96}" {SANS} font-size="15" font-weight="500" fill="{T["mute"]}">{desc}</text>')
    zs = [z for z in ("night", "day", "wet", "circ") if S["zone_area"].get(z, 0) > 0.5]
    items = [(ZONE_LABEL[z], T["zones"][z], S["zone_area"][z]) for z in zs]
    items += [(nm, T["zones"]["outdoor"], a) for nm, a in S["outdoor"] if a > 0.5]
    for i, (lab, col, a) in enumerate(items):
        cx = 70 + (i % 2) * 480
        yy = y0 + 140 + (i // 2) * 38
        o.append('<g class="leg">')
        o.append(f'<rect x="{cx}" y="{yy - 16}" width="34" height="22" rx="3" fill="{col}" stroke="{T["ink"]}" stroke-width="1"/>')
        o.append(f'<text x="{cx + 50}" y="{yy}" {SANS} font-size="16" font-weight="600" fill="{T["ink"]}">{lab}</text>')
        o.append(f'<text x="{cx + 420}" y="{yy}" {SANS} font-size="16" font-weight="800" text-anchor="end" fill="{T["ink"]}"><tspan class="num" data-v="{a:.0f}">{a:,.0f}</tspan> sq ft</text>')
        o.append('</g>')
    yy = y0 + 140 + ((len(items) + 1) // 2) * 38 + 6
    ow, od = B["overall"]
    parts = [f'Net floor area {S["net"]:,.0f} sq ft', f'gross {S["gross"]:,.0f} sq ft',
             f'overall {fi(ow)} × {fi(od)}', f'{S["n_win"]} windows']
    if S["n_sl"]:
        parts.append(f'{S["n_sl"]} sliding door' + ("s" if S["n_sl"] > 1 else ""))
    parts.append(f'{S["n_door"]} doors')
    o.append(f'<text id="summary" x="70" y="{yy}" {SANS} font-size="13" font-weight="500" fill="{T["mute"]}">{" · ".join(parts)} (glass highlighted)</text>')
    fy = PH - 70
    o.append('<g id="foot">')
    o.append(f'<rect x="70" y="{fy - 30}" width="940" height="1.5" fill="{T["rule"]}"/>')
    o.append(f'<text x="70" y="{fy}" {SANS} font-size="13" font-weight="600" letter-spacing="1" fill="{T["mute"]}">/axon · drawn in code from {plan.get("source", "plan")}</text>')
    o.append(f'<text x="1010" y="{fy}" {SANS} font-size="13" font-weight="800" letter-spacing="1" text-anchor="end" fill="{T["ink"]}">{plan.get("credit", "The Architecture Grind")}</text>')
    o.append('</g>')
    o.append('</svg>')
    return "\n".join(o), S


def animate_html(svg, theme="light", input_img=None, input_name="floor-plan.jpg", cmd="/axon"):
    """Self-contained HTML that replays the build tier by tier - made for screen recording."""
    import base64, mimetypes, os
    T = THEMES[theme]
    img_tag = ""
    if input_img and os.path.exists(input_img):
        mime = mimetypes.guess_type(input_img)[0] or "image/png"
        b64 = base64.b64encode(open(input_img, "rb").read()).decode()
        img_tag = f'<img src="data:{mime};base64,{b64}" alt="input plan">'
    fonts = ""
    for fam in (T.get("sans", SANS_DEFAULT), T.get("serif", SERIF_DEFAULT)):
        fn = fam.replace(" ", "") + ".ttf"
        for d in (os.path.expanduser("~/.fonts"), os.path.dirname(os.path.abspath(__file__))):
            fp = os.path.join(d, fn)
            if os.path.exists(fp):
                fb = base64.b64encode(open(fp, "rb").read()).decode()
                fonts += f"@font-face{{font-family:'{fam}';src:url(data:font/ttf;base64,{fb}) format('truetype');font-weight:100 900}}\n"
                break
    return HTML_TEMPLATE.replace("%%FONTS%%", fonts).replace("%%SVG%%", svg).replace("%%IMG%%", img_tag) \
        .replace("%%NAME%%", input_name).replace("%%CMD%%", cmd) \
        .replace("%%BG%%", T["bg"]).replace("%%INK%%", T["ink"]).replace("%%ACC%%", T["accent"]) \
        .replace("%%MUTE%%", T["mute"])


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>/axon - exploded axonometric build</title>
<style>
%%FONTS%%
  html,body{margin:0;height:100%;background:#151515;overflow:hidden;font-family:Manrope,Helvetica,Arial,sans-serif}
  #stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
  #sheet{position:relative;height:96vh;aspect-ratio:1080/1350;max-width:96vw;background:%%BG%%;
         box-shadow:0 30px 80px rgba(0,0,0,.45);border-radius:6px;overflow:hidden}
  #sheet svg{position:absolute;inset:0;width:100%;height:100%}
  #intro{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3.2%;z-index:5}
  #cmdbar{width:78%;display:flex;align-items:center;gap:1.4vh;padding:2.1vh 2.4vh;border:1.5px solid %%INK%%;border-radius:1.2vh;
          background:#fff;color:#2A2A2A;font-size:2.2vh;font-weight:600;box-shadow:0 1vh 3vh rgba(0,0,0,.08)}
  #cmdbar .chev{color:%%ACC%%;font-weight:800}
  #typed .cmd{background:%%ACC%%;color:#2A2A2A;padding:.2vh .8vh;border-radius:.6vh;font-weight:800}
  #typed .file{color:#6E6A63}
  #caret{display:inline-block;width:.25vh;height:2.6vh;background:#2A2A2A;animation:blink 1s steps(1) infinite}
  @keyframes blink{50%{opacity:0}}
  #card{width:78%;opacity:0;transform:translateY(2vh);border:1.5px solid %%INK%%;border-radius:1.2vh;background:#fff;overflow:hidden}
  #card img{display:block;width:100%}
  #card .lab{display:flex;justify-content:space-between;padding:1.2vh 1.8vh;font-size:1.5vh;font-weight:700;letter-spacing:.15em;color:#2A2A2A;
             border-top:1.5px solid %%INK%%;text-transform:uppercase}
  #status{font-size:1.6vh;font-weight:700;letter-spacing:.18em;color:%%MUTE%%;text-transform:uppercase;opacity:0;height:2vh}
  #hint{position:fixed;left:50%;bottom:1.2vh;transform:translateX(-50%);color:#8a857d;font-size:12px;letter-spacing:.12em;
        text-transform:uppercase;transition:opacity .4s}
  body.running #hint{opacity:0}
  #wl-faces > *{opacity:0}
  #hdr,#guides line,#L-floor,#L-walls,#L-roof,#north,.callout .ctext,.callout .dot,#rule2,#title,#desc,.leg,#summary,#foot{opacity:0}
</style></head>
<body>
<div id="stage"><div id="sheet">
  %%SVG%%
  <div id="intro">
    <div id="cmdbar"><span class="chev">&rsaquo;</span><span id="typed"></span><span id="caret"></span></div>
    <div id="card">%%IMG%%<div class="lab"><span>Input</span><span>%%NAME%%</span></div></div>
    <div id="status"></div>
  </div>
</div></div>
<div id="hint">Space / click to run  ·  R to reset</div>
<script>
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const E='cubic-bezier(.2,.8,.2,1)';
let running=false, runId=0;
const HIDE=['#hdr','#guides line','#L-floor','#fl-zones .zone','#fl-walls','#fl-furn','#L-walls','#wl-top','#L-roof','#north',
            '.callout .ctext','.callout .dot','#rule2','#title','#desc','.leg','#summary','#foot'];
function reset(){
  runId++; running=false; document.body.classList.remove('running');
  document.getAnimations().forEach(a=>a.cancel());
  HIDE.forEach(s=>$$(s).forEach(e=>e.style.opacity=0));
  $$('#wl-faces > *').forEach(e=>e.style.opacity=0);
  $$('.leader').forEach(e=>{e.style.strokeDasharray='1';e.style.strokeDashoffset='1'});
  $('#title').textContent='';
  $$('.num').forEach(n=>n.textContent='0');
  $('#typed').innerHTML=''; $('#status').textContent=''; $('#status').style.opacity=0;
  const i=$('#intro'); i.style.opacity=1; i.style.display='flex';
  $('#card').style.opacity=0; $('#card').style.transform='translateY(2vh)';
}
function show(el,from,dur=600,delay=0){
  if(!el) return; return el.animate([{opacity:0,...from},{opacity:1,transform:'translate(0,0)'}],
    {duration:dur,delay,easing:E,fill:'forwards'}).finished.then(()=>{el.style.opacity=1});
}
async function typeHTML(target, parts, speed=55, id){
  for(const [cls,txt] of parts){
    const span=document.createElement('span'); if(cls) span.className=cls; target.appendChild(span);
    for(const ch of txt){ if(id!==runId) return; span.textContent+=ch; await sleep(speed); }
  }
}
async function status(t){ const s=$('#status'); s.textContent=t; s.style.opacity=1; }
async function run(){
  if(running) return; reset(); running=true; const id=runId; document.body.classList.add('running');
  const ok=()=>id===runId;
  await sleep(500);
  await typeHTML($('#typed'),[['cmd','%%CMD%%'],[null,' '],['file','%%NAME%%']],70,id); if(!ok())return;
  await sleep(350);
  $('#card').animate([{opacity:0,transform:'translateY(2vh)'},{opacity:1,transform:'translateY(0)'}],{duration:600,easing:E,fill:'forwards'});
  await sleep(700); status('Reading plan · scaling to feet'); await sleep(1100);
  if(!ok())return; status('Walls · openings · rooms'); await sleep(1000);
  if(!ok())return;
  await $('#intro').animate([{opacity:1},{opacity:0,transform:'scale(.97)'}],{duration:500,easing:E,fill:'forwards'}).finished;
  $('#intro').style.display='none'; if(!ok())return;
  show($('#hdr'),{transform:'translate(0,-12px)'},600);
  await sleep(300);
  show($('#L-floor'),{transform:'translate(0,40px)'},900);
  $$('.g-lo').forEach((g,i)=>show(g,{},500,500+i*80));
  await sleep(700);
  for(const z of ['night','wet','day','circ']){
    const els=$$('#fl-zones .z-'+z); els.forEach((e,i)=>show(e,{},450,i*90));
    if(els.length) await sleep(380);
  }
  show($('#fl-walls'),{},500); await sleep(200);
  show($('#fl-furn'),{},600); await sleep(500);
  if(!ok())return;
  $('#L-walls').style.opacity=1;
  $('#L-walls').animate([{transform:'translate(0,70px)'},{transform:'translate(0,0)'}],{duration:2200,easing:E,fill:'forwards'});
  const faces=$$('#wl-faces > *'), total=1900;
  faces.forEach((f,i)=>f.animate([{opacity:0},{opacity:1}],{duration:140,delay:i/faces.length*total,fill:'forwards'}));
  await sleep(total+100);
  show($('#wl-top'),{},500); await sleep(450);
  $$('.g-hi').forEach((g,i)=>show(g,{},500,i*80));
  if(!ok())return;
  show($('#L-roof'),{transform:'translate(0,-60px)'},1000); await sleep(1000);
  show($('#north'),{transform:'translate(0,-6px)'},500); await sleep(300);
  for(const k of ['floor','walls','roof']){
    const c=$('#c-'+k); if(!c) continue;
    c.querySelector('.leader').animate([{strokeDashoffset:1},{strokeDashoffset:0}],{duration:550,easing:E,fill:'forwards'});
    await sleep(380); show(c.querySelector('.dot'),{},250);
    c.querySelectorAll('.ctext').forEach((t,i)=>show(t,{transform:'translate(-8px,0)'},450,i*110));
    await sleep(350);
  }
  if(!ok())return;
  show($('#rule2'),{},400); await sleep(250);
  const tt=$('#title'); tt.style.opacity=1; for(const ch of 'Exploded axonometric'){ if(!ok())return; tt.textContent+=ch; await sleep(40); }
  show($('#desc'),{transform:'translate(0,6px)'},500); await sleep(350);
  $$('.leg').forEach((l,i)=>{ show(l,{transform:'translate(0,8px)'},500,i*140);
    const n=l.querySelector('.num'), v=+n.dataset.v, t0=performance.now()+i*140;
    const tick=t=>{ const p=Math.min(1,Math.max(0,(t-t0)/900)); n.textContent=Math.round(v*(1-Math.pow(1-p,3))).toLocaleString();
      if(p<1&&ok()) requestAnimationFrame(tick)}; requestAnimationFrame(tick); });
  await sleep(900); show($('#summary'),{},500); await sleep(300); show($('#foot'),{},600);
  await sleep(800); running=false;
}
document.addEventListener('keydown',e=>{ if(e.code==='Space'){e.preventDefault(); run();} if(e.key==='r'||e.key==='R') reset(); });
document.addEventListener('click',run);
reset();
if(new URLSearchParams(location.search).has('autoplay')) setTimeout(run,600);
</script>
</body></html>
"""


if __name__ == "__main__":
    import os
    args = sys.argv[1:]
    theme, html_out, inp, style_path = "light", None, None, None
    for flag in ("--theme", "--html", "--input", "--style"):
        if flag in args:
            i = args.index(flag); val = args[i + 1]; del args[i:i + 2]
            if flag == "--theme": theme = val
            elif flag == "--html": html_out = val
            elif flag == "--style": style_path = val
            else: inp = val
    plan = json.load(open(args[0]))
    if style_path:
        st = json.load(open(style_path))
        theme = apply_style(st)
        if st.get("credit"):
            plan["credit"] = st["credit"]
    svg, S = render(plan, theme)
    open(args[1], "w").write(svg)
    if html_out:
        name = plan.get("input_name") or (os.path.basename(inp) if inp else "floor-plan.jpg")
        open(html_out, "w").write(animate_html(svg, theme, inp, name))
        print("wrote", html_out)
    print(f"wrote {args[1]} | net {S['net']:.0f} sf, gross {S['gross']:.0f} sf, zones "
          + ", ".join(f"{k}={v:.0f}" for k, v in S["zone_area"].items()))
```