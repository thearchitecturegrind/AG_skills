---
name: "elevation-section"
description: "Turn an uploaded floor plan into a front elevation and a building section (imperial) in the /axon brand style, with an animated build page. Reuses the /axon plan JSON. Supports custom style blocks."
---

# Front Elevation + Section from a Floor Plan (/elevation)

The user uploads a floor plan. You draw two orthographic views on one sheet, at the same scale, in an architectural drawing style:

- **Front elevation:** brick walls hatched in running bond over a coursed stone base with a stone water table, stone head courses and projecting sills, fixed windows in dark frames with light-blue glass and reflections, detailed doors (frame, glazed lite, raised panels, lever, stone step) and sliders (two panels, interlock handle, tracks), porch posts, a layered roof fascia, cast shadows under the roof and sills (deeper where a wall sits back under a porch roof), heavier line weights on the nearest plane, an earth band, trees behind and shrubs in front.
- **Building section:** poché cut with brick hatch above and stone hatch below on exterior walls, concrete hatch on slab and footings, roof build-up lines, light-blue glazing with frames and interior sills, interior wall faces with skirting, and rooms furnished and planted (beds, nightstands, wardrobe, sofa, coffee table, TV unit, dining set, kitchen run, bath, laundry, pendant lights, figures, potted palms and ficus).
- Level markers (T.O. roof, B.O. roof, F.F.), overall dimension, key plan with the cut line and front marker, graphic scale bar, legend and title block. Everything is in feet and inches.

It uses the **same plan JSON as the `exploded-axon` skill** plus the keys `front`, `section` and `heights.base`. If the user already ran /axon on this plan, reuse that `plan.json`.

Every run produces:
- **elevation.png** and **elevation.svg** (editable in Illustrator, Figma or Affinity): the static sheet.
- **elevation-build.html**: an animated build made for screen recording, in the /axon template. A command bar types `/elevation floor-plan.jpg`, the input plan card appears, then the ground and earth band draw, trees fade in, the stone base and brick walls rise face by face, windows and doors pop in, the roof drops, shrubs grow, levels and the dimension draw, the key-plan cut line draws, the section's far walls fade in, foundations, slab, cut walls and roof build, the furnished rooms come up, and the title and legend finish. Space or click runs it, R resets.

## 1. Ask first (one AskUserQuestion call, only for what the plan and conversation don't answer)
1. **Style reference.** Default style (warm off-white, charcoal, yellow accent, Manrope + STIX Two Text), upload a reference image, or paste a style block. Style blocks use the `exploded-axon` schema (sections 2a/2b there) plus optional `brick`, `stone`, `glass`, `frame`, `plant` and `shade` colors.
2. **Scale:** if there's no overall dimension string or scale bar, ask for one overall dimension.
3. **Front:** which plan side is the front? Default: the side with the entry or porch.
4. **Section cut:** where to cut and which way to look. Suggest one: a cut that crosses the most rooms and passes through doors or windows. Default: a cut across the long side through the bedrooms and living, looking toward the plan top.
5. **Levels and materials:** B.O. roof (default 9'-0") and T.O. roof (default 10'-6"), stone base height (default 2'-6"), grade below finished floor (default 8"). Brick over stone is the default; ask only if the user wants other materials.
6. **North and sheet text:** is plan-up north? Project name, subtitle, sheet number.

If the user isn't around, use the defaults and list them in your reply.

## 2. Setup (once per session)
```bash
pip install --break-system-packages -q shapely
mkdir -p ~/.fonts && cd ~/.fonts && \
curl -sSLf -o Manrope.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf" && \
curl -sSLf -o STIXTwoText.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/stixtwotext/STIXTwoText%5Bwght%5D.ttf" && fc-cache -f
```
Write the script in section 6 to `elev_section.py` exactly as given. `rsvg-convert` exports the PNG.

## 3. Transcribe the plan to JSON
Follow section 4 of the `exploded-axon` skill: feet, origin at the top-left outer corner, x right, **y down**; `footprint` = outer face of the enclosed building; `walls` = axis-aligned centerlines with `t` (exterior 0.75, interior 0.42); `openings` with `window` / `door` / `slider` and optional `sill` / `head`; `rooms` with names and zones (room names pick the furniture: bed, living, dining, kitchen, bath, laundry); `outdoor` with `"covered": true` for porches under the roof. Measuring tip: threshold the image (`gray < 80`) and scan along each wall's centerline with numpy; the light gaps are the openings. Then add:

```json
"front": "bottom",                                   // plan side the elevation is drawn from: bottom | top | left | right
"section": {"axis": "y", "at": 10.5, "look": "top", "label": "A"},
                                                     // axis "y": cut runs left-right at y = at (ft from the plan top)
                                                     // axis "x": cut runs top-bottom at x = at (ft from the plan left)
                                                     // look: the plan side you look toward (must be perpendicular to the cut)
"heights": {"wall": 9, "roof": 1.5, "base": 2.5, "grade": 0.67, "slab": 1, "sill": 3, "head": 7, "overhang": 1.5}
                                                     // wall = B.O. roof level, wall + roof = T.O. roof level, base = stone base height
```
Keep the cut at least 6" away from any wall that runs parallel to it, or the section shows a wall face sliced lengthwise.

## 4. Render and check
Copy the uploaded plan next to the script as `floor-plan.jpg` (or `.png`); the build page shows it as the input card.
```bash
python3 elev_section.py plan.json elevation.svg --html elevation-build.html --input floor-plan.jpg   # add --style style.json or --theme dark
rsvg-convert -w 2160 elevation.svg -o elevation.png
```
**Always open the PNG and check it before delivering, including zoomed crops of both views** (crop the 2160 px PNG with Pillow):
- Elevation: every front window, door and slider is where the plan shows it (count them against the summary line). Brick hatch, stone base, frames, shadows under the roof and sills all read. Faces farther back read as a darker tone with lighter line weight.
- Section: the cut walls match the walls the cut line crosses in the plan, door openings show a header only, the room names suit the furniture shown, and nothing collides with a window.
- Levels read T.O. roof +10'-6" and B.O. roof +9'-0" (or the values the user gave).
- The key plan's cut line and front marker match what you intended.

Optionally screenshot the build page with Playwright and headless Chrome (`?autoplay`, wait ~25 s) to confirm the animation ends on the full sheet with no console errors. Fix the JSON and re-render until it's right.

## 5. Deliver
- Publish `elevation-build.html` as an artifact (title: "/elevation - elevation + section build"). To screen-record it, open it, go full screen, start recording, then press Space.
- Send `elevation.png` and `elevation.svg` with SendUserFile.
- In your reply, list the assumptions you made (scale, front, cut location, levels, base height, sills, roof, materials, style).

**Limits:** orthogonal walls only, flat slab roof only (pitched roofs aren't supported yet), single-story only, one section per sheet. The furniture and planting are generic symbols chosen by room name, not the plan's own furniture. Ceiling heights, footings and roof build-ups are simplified.

## 6. Script: elev_section.py
```python
#!/usr/bin/env python3
"""
elev_section.py - Front elevation + building section from a floor-plan JSON (same schema as /axon).
Architectural drawing style: line-weight hierarchy, brick hatch over a coursed stone base, fixed light-blue
glazing in frames, roof / sill shadows, earth band, trees + shrubs, furnished and planted section.
Imperial units. Default style: charcoal + yellow accent, STIX Two Text + Manrope.

Usage:
    python3 elev_section.py plan.json out.svg [--theme light|dark] [--style style.json] [--html build.html --input plan.jpg]
    rsvg-convert -w 2160 out.svg -o out.png
Plan coords in FEET, x right / y DOWN. Extra keys vs /axon:
    "front":   "bottom" | "top" | "left" | "right"      plan side the elevation is drawn from
    "section": {"axis": "y"|"x", "at": ft, "look": "top"|"bottom"|"left"|"right", "label": "A"}
    "heights": {"wall": 9, "roof": 1.5, "base": 2.5, "grade": 0.67, "slab": 1, "sill": 3, "head": 7, "overhang": 1.5}
               wall = B.O. roof level, wall + roof = T.O. roof level, base = stone base height
"""
import json, math, sys, os, base64, mimetypes, copy, random
from shapely.geometry import LineString, Polygon, box, Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

_LIGHT = dict(
    bg="#F5F3EE", ink="#2A2A2A", mute="#6E6A63", rule="#2A2A2A", poche="#2A2A2A", edge="#2A2A2A",
    guide="#8A857D", accent="#F2C230", face_s="#FFFFFF", slab_s="#D9D5CD", slab_e="#C8C3BA",
    brick="#E8E0D3", brick_far="#D8CFC0", brick_line="#6F685C",
    stone=("#D2CCC1", "#C6BFB3", "#DAD5CB"), stone_line="#5E5850",
    glass="#BCDCEE", glass_hi="#E7F4FB", glass_deep="#8DBFDC", frame="#33373B",
    plaster="#F1EDE5", plaster_deep="#DCD6CA", floor="#BDB6A8", wood="#D8CAB0", wood_dark="#A8977A",
    fabric="#CFC8BB", fabric_dark="#A59E90", plant="#8E9A88", plant_dark="#5B6757", shade="#F2C230",
    person="#3A3A3A", skin="#E0D6C6", earth_dot="#4A4640", tree=("#E0E0DA", "#D3D3CB", "#C4C4BB", "#B3B3A9"),
    trunk="#7C766C", furn_fill="#EFEBE2",
    zones=dict(day="#F7D774", night="#D9D5CD", wet="#AFA99F", circ="#FBEDBC", outdoor="#ECE8E1"))
THEMES = {"light": _LIGHT}
THEMES["dark"] = {**_LIGHT, **dict(
    bg="#1E1E1E", ink="#F1EEE7", mute="#A8A39A", rule="#F1EEE7", poche="#F2C230", edge="#0F0F0F",
    guide="#77736C", face_s="#3A3A3A", slab_s="#2B2B2B", slab_e="#242424",
    brick="#4A4640", brick_far="#3C3935", brick_line="#8A857D",
    stone=("#5A564F", "#4E4B45", "#625E57"), stone_line="#1F1D1A",
    glass="#5E87A0", glass_hi="#9CC4DA", glass_deep="#3E6178", frame="#0F0F0F",
    plaster="#3A3835", plaster_deep="#2E2C29", floor="#555049", wood="#6A5F4E", wood_dark="#4F4638",
    fabric="#5A564F", fabric_dark="#45423C", plant="#6C7A66", plant_dark="#46543F",
    person="#CFC9BD", skin="#B9AE9C", earth_dot="#CFC9BD", tree=("#4A4A46", "#40403C", "#363633", "#2C2C2A"),
    trunk="#5A564F", furn_fill="#44413C",
    zones=dict(day="#C99E22", night="#6B6862", wet="#55524D", circ="#8C7A44", outdoor="#3C3C3C"))}
SANS_DEFAULT, SERIF_DEFAULT = "Manrope", "STIX Two Text"


def hexshade(c, f):
    c = c.lstrip("#")
    return "#%02X%02X%02X" % tuple(min(255, int(int(c[i:i + 2], 16) * f)) for i in (0, 2, 4))


def apply_style(style):
    t = copy.deepcopy(THEMES["light"])
    for k in ("bg", "ink", "mute", "accent", "glass", "guide", "frame", "brick", "plant", "shade"):
        if k in style:
            t[k] = style[k]
    if "ink" in style:
        t["rule"] = t["edge"] = t["poche"] = style["ink"]
    if "edge" in style:
        t["edge"] = style["edge"]
    if "glass" in style:
        t["glass_hi"], t["glass_deep"] = hexshade(style["glass"], 1.12), hexshade(style["glass"], 0.8)
    if "brick" in style:
        t["brick_far"] = hexshade(style["brick"], 0.93)
    if "stone" in style:
        t["stone"] = (style["stone"], hexshade(style["stone"], 0.94), hexshade(style["stone"], 1.04))
    if "surface" in style:
        sf = style["surface"]
        t.update(face_s=sf, slab_s=hexshade(sf, .85), slab_e=hexshade(sf, .76))
    for z, c in style.get("zones", {}).items():
        t["zones"][z] = c
    t["sans"] = style.get("fonts", {}).get("sans", SANS_DEFAULT)
    t["serif"] = style.get("fonts", {}).get("serif", SERIF_DEFAULT)
    THEMES["custom"] = t
    return "custom"


def fi(v, sign=False):
    neg = v < 0
    inches = round(abs(v) * 12)
    s = f"{inches // 12}'-{inches % 12}\""
    if neg: return "-" + s
    if sign: return ("±" if inches == 0 else "+") + s
    return s


# ------------------------------------------------------------------ view geometry
AX = {
    "S": (lambda x, y: x, lambda x, y: y, (0, 1)),
    "N": (lambda x, y: -x, lambda x, y: -y, (0, -1)),
    "E": (lambda x, y: -y, lambda x, y: x, (1, 0)),
    "W": (lambda x, y: y, lambda x, y: -x, (-1, 0)),
}
SIDE = {"bottom": "S", "top": "N", "right": "E", "left": "W"}
OPP = {"S": "N", "N": "S", "E": "W", "W": "E"}


def compass(letter, north_deg):
    idx = {"N": 0, "E": 1, "S": 2, "W": 3}[letter]
    return ["north", "east", "south", "west"][(idx - round(north_deg / 90)) % 4]


def rect_poly(r):
    x1, y1, x2, y2 = r
    return box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))


def polys(g):
    if g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    return [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]


def lines(g):
    if g.is_empty: return []
    if g.geom_type == "LineString": return [g]
    out = []
    for p in getattr(g, "geoms", []):
        out += lines(p)
    return out


def facing(poly, side):
    u, nr, v = AX[side]
    poly = orient(poly, 1.0)
    out = []
    for ring in [poly.exterior] + list(poly.interiors):
        pts = list(ring.coords)
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy)
            if L < 1e-6: continue
            nx, ny = dy / L, -dx / L
            if nx * v[0] + ny * v[1] > 0.99:
                a, b = sorted((u(x1, y1), u(x2, y2)))
                out.append((a, b, nr(x1, y1)))
    out.sort(key=lambda f: (round(f[2], 3), f[0]))
    merged = []
    for f in out:
        if merged and abs(merged[-1][2] - f[2]) < 1e-3 and f[0] <= merged[-1][1] + 1e-3:
            merged[-1] = (merged[-1][0], max(merged[-1][1], f[1]), merged[-1][2])
        else:
            merged.append(f)
    return merged


def geometry(plan):
    H = dict(wall=9, slab=1, roof=1.5, overhang=1.5, sill=3, head=7, grade=0.67, base=2.5)
    H.update(plan.get("heights", {}))
    foot = Polygon(plan["footprint"])
    walls = [(LineString([tuple(w["a"]), tuple(w["b"])]), w.get("t", 0.5)) for w in plan["walls"]]
    walls_u = unary_union([ls.buffer(t / 2, cap_style="square", join_style="mitre") for ls, t in walls])
    ops = []
    for o in plan.get("openings", []):
        ls = LineString([tuple(o["a"]), tuple(o["b"])])
        host = max(walls, key=lambda w: w[0].buffer(0.05).intersection(ls).length)
        t = host[1]
        typ = o.get("type", "window")
        sill = o.get("sill", 0 if typ in ("door", "slider") else H["sill"])
        head = o.get("head", H["head"])
        rect = ls.buffer(t / 2 + 0.02, cap_style="flat")
        ops.append(dict(type=typ, ls=ls, t=t, sill=sill, head=head, rect=rect, piece=walls_u.intersection(rect)))
    ops_u = unary_union([o["rect"] for o in ops]) if ops else Polygon()
    solid = walls_u.difference(ops_u)
    outs = [(rect_poly(o["rect"]) if "rect" in o else Polygon(o["poly"]), o) for o in plan.get("outdoor", [])]
    covered = unary_union([foot] + [p for p, o in outs if o.get("covered")])
    roof = covered.buffer(H["overhang"], join_style="mitre")
    rooms = []
    for r in plan.get("rooms", []):
        rp = (rect_poly(r["rect"]) if "rect" in r else Polygon(r["poly"])).intersection(foot).difference(walls_u)
        rooms.append((r, rp))
    return dict(H=H, foot=foot, walls=walls, walls_u=walls_u, ops=ops, solid=solid, outs=outs, roof=roof, rooms=rooms)


def elevation(G, side):
    H, (u, nr, v) = G["H"], AX[side]
    it = []
    fac = facing(G["foot"], side)
    nearest = max(f[2] for f in fac)
    gz, base, wall = -H["grade"], H["base"], H["wall"]
    roof_f = facing(G["roof"], side)
    for a, b, d in fac:
        near = abs(d - nearest) < 0.05
        it.append(dict(k="base", u0=a, u1=b, z0=gz, z1=base, d=d, near=near, wt=True))
        cuts = sorted({a, b} | {x for ra, rb, rd in roof_f for x in (ra, rb) if a + 0.05 < x < b - 0.05})
        sh = []
        for s0, s1 in zip(cuts[:-1], cuts[1:]):
            m = (s0 + s1) / 2
            ds = [rd for ra, rb, rd in roof_f if ra <= m <= rb]
            setback = max(0, (max(ds) if ds else d) - d)
            sh.append((s0, s1, min(wall * 0.72, 1.1 + 0.45 * setback)))
        it.append(dict(k="face", u0=a, u1=b, z0=base, z1=wall, d=d + 0.0005, near=near, shadows=sh))
    for p, o in G["outs"]:
        for q in polys(p.difference(G["foot"])):
            for a, b, d in facing(q, side):
                it.append(dict(k="base", u0=a, u1=b, z0=gz, z1=-0.35, d=d, near=False, wt=False))
        if o.get("covered"):
            c = p.centroid
            for x, y in list(p.exterior.coords)[:-1]:
                if G["foot"].distance(Point(x, y)) > 0.3:
                    px, py = x + 0.25 * math.copysign(1, c.x - x), y + 0.25 * math.copysign(1, c.y - y)
                    it.append(dict(k="post", u0=u(px, py) - 0.25, u1=u(px, py) + 0.25, z0=-0.35, z1=wall, d=nr(px, py) + 0.25))
    n_open = {"window": 0, "door": 0, "slider": 0}
    for o in G["ops"]:
        (ax, ay), (bx, by) = list(o["ls"].coords)
        mx, my = (ax + bx) / 2, (ay + by) / 2
        off = o["t"] / 2 + 0.15
        pout, pin = Point(mx + v[0] * off, my + v[1] * off), Point(mx - v[0] * off, my - v[1] * off)
        if not G["foot"].contains(pout) and G["foot"].contains(pin):
            a, b = sorted((u(ax, ay), u(bx, by)))
            it.append(dict(k=o["type"], u0=a, u1=b, z0=o["sill"], z1=o["head"], d=nr(mx, my) + o["t"] / 2 + 0.001))
            n_open[o["type"]] += 1
    for a, b, d in roof_f:
        it.append(dict(k="roof", u0=a, u1=b, z0=wall, z1=wall + H["roof"], d=d))
    it.sort(key=lambda e: e["d"])
    fu = [u(x, y) for x, y in G["foot"].exterior.coords]
    return dict(items=it, foot_u=(min(fu), max(fu)), n_open=n_open)


def section(G, sec):
    H = G["H"]
    look = SIDE[sec.get("look", "top")]
    side = OPP[look]
    u, nr, v = AX[side]
    at, big = sec["at"], 2000
    if sec.get("axis", "y") == "y":
        line, cd = LineString([(-big, at), (big, at)]), nr(0, at)
    else:
        line, cd = LineString([(at, -big), (at, big)]), nr(at, 0)

    def segs(g):
        out = []
        for ls in lines(g.intersection(line)):
            cs = list(ls.coords)
            a, b = sorted((u(*cs[0]), u(*cs[-1])))
            if b - a > 0.02: out.append((a, b))
        return out

    wall = H["wall"]
    beyond, cut, rooms = [], [], []
    surf = unary_union([G["solid"]] + [o["piece"] for o in G["ops"] if o["type"] == "window"])
    for p in polys(surf):
        for a, b, d in facing(p, side):
            if d < cd - 0.01:
                beyond.append(dict(k="beyond", u0=a, u1=b, z0=0, z1=wall, d=d, skirt=True))
    for o in G["ops"]:
        for p in polys(o["piece"]):
            for a, b, d in facing(p, side):
                if d < cd - 0.01:
                    if o["type"] == "window" and b - a > 0.9:
                        beyond.append(dict(k="bglass", u0=a, u1=b, z0=o["sill"], z1=o["head"], d=d + 0.001))
                    if o["type"] == "door" and b - a > 1.0:
                        beyond.append(dict(k="bdoor", u0=a, u1=b, z0=0, z1=o["head"], d=d + 0.001))
                    if o["type"] == "slider" and b - a > 1.0:
                        beyond.append(dict(k="bslide", u0=a, u1=b, z0=0, z1=o["head"], d=d + 0.001))
                    if o["type"] in ("door", "slider") and o["head"] < wall:
                        beyond.append(dict(k="beyond", u0=a, u1=b, z0=o["head"], z1=wall, d=d))
    beyond.sort(key=lambda e: e["d"])
    for a, b in segs(G["foot"]):
        cut.append(dict(k="cut", u0=a, u1=b, z0=-H["slab"], z1=0, part="slab"))
    for p, o in G["outs"]:
        for a, b in segs(p.difference(G["foot"])):
            cut.append(dict(k="cut", u0=a, u1=b, z0=-H["slab"], z1=-0.35, part="slab"))
    for a, b in segs(G["walls_u"]):
        if b - a >= 0.6:   # exterior wall: foundation stem + footing
            cut.append(dict(k="cut", u0=a, u1=b, z0=-1.75, z1=-H["slab"], part="found", ext=True))
            cut.append(dict(k="cut", u0=a - 0.7, u1=b + 0.7, z0=-2.75, z1=-1.75, part="found", ext=True))
    for a, b in segs(G["solid"]):
        cut.append(dict(k="cut", u0=a, u1=b, z0=0, z1=wall, part="wall", ext=(b - a) >= 0.6))
    ucen = (min(s[0] for s in segs(G["foot"])) + max(s[1] for s in segs(G["foot"]))) / 2
    for o in G["ops"]:
        for a, b in segs(o["piece"]):
            ext = (b - a) >= 0.6
            if o["sill"] > 0: cut.append(dict(k="cut", u0=a, u1=b, z0=0, z1=o["sill"], part="wall", ext=ext))
            if o["head"] < wall: cut.append(dict(k="cut", u0=a, u1=b, z0=o["head"], z1=wall, part="wall", ext=ext))
            if o["type"] in ("window", "slider") and ext:
                m = (a + b) / 2
                cut.append(dict(k="cglass", u0=m - 0.08, u1=m + 0.08, z0=o["sill"], z1=o["head"], part="wall",
                                inward=1 if m < ucen else -1, wa=a, wb=b))
    for a, b in segs(G["roof"]):
        cut.append(dict(k="cut", u0=a, u1=b, z0=wall, z1=wall + H["roof"], part="roof"))
    for r, rp in G["rooms"]:
        ss = segs(rp)
        if ss:
            a, b = max(ss, key=lambda s: s[1] - s[0])
            rooms.append(dict(name=r.get("name", "Room"), u0=a, u1=b, zone=r.get("zone", "day")))
    fs = segs(G["foot"])
    return dict(beyond=beyond, cut=cut, rooms=rooms, side=side, look=look, line=line,
                foot_u=(min(s[0] for s in fs), max(s[1] for s in fs)))


# ------------------------------------------------------------------ drawing context
class Ctx:
    def __init__(s, X, Y, sc, T):
        s.X, s.Y, s.sc, s.T = X, Y, sc, T

    def r(s, u0, u1, z0, z1, fill="none", stroke=None, sw=0.0, op=None, rx=0, extra=""):
        x0, x1 = sorted((s.X(u0), s.X(u1)))
        y0, y1 = sorted((s.Y(z0), s.Y(z1)))
        a = f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="{fill}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
        if op is not None: a += f' fill-opacity="{op}"'
        if rx: a += f' rx="{rx}"'
        return a + f'{extra}/>'

    def ln(s, u0, z0, u1, z1, stroke, sw=0.8, op=None, dash=None, cap="round"):
        a = (f'<line x1="{s.X(u0):.2f}" y1="{s.Y(z0):.2f}" x2="{s.X(u1):.2f}" y2="{s.Y(z1):.2f}" '
             f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"')
        if op is not None: a += f' stroke-opacity="{op}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        return a + "/>"

    def ci(s, u, z, rft, fill, stroke=None, sw=0, op=None):
        a = f'<circle cx="{s.X(u):.2f}" cy="{s.Y(z):.2f}" r="{rft * s.sc:.2f}" fill="{fill}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
        if op is not None: a += f' fill-opacity="{op}"'
        return a + "/>"

    def pg(s, pts, fill, stroke=None, sw=0.8, op=None):
        p = " ".join(f"{s.X(u):.2f},{s.Y(z):.2f}" for u, z in pts)
        a = f'<polygon points="{p}" fill="{fill}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
        if op is not None: a += f' fill-opacity="{op}"'
        return a + "/>"

    def pth(s, d, fill="none", stroke=None, sw=0.8, op=None, sop=None):
        a = f'<path d="{d}" fill="{fill}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
        if op is not None: a += f' fill-opacity="{op}"'
        if sop is not None: a += f' stroke-opacity="{sop}"'
        return a + "/>"

    def P(s, u, z):
        return f"{s.X(u):.2f},{s.Y(z):.2f}"


def leaf(c, bu, bz, ang, length, width, fill, stroke, vein=True):
    a = math.radians(ang)
    tu, tz = bu + length * math.cos(a), bz + length * math.sin(a)
    mu, mz = (bu + tu) / 2, (bz + tz) / 2
    pu, pz = -math.sin(a), math.cos(a)
    d = (f"M{c.P(bu, bz)} Q{c.P(mu + pu * width, mz + pz * width)} {c.P(tu, tz)} "
         f"Q{c.P(mu - pu * width, mz - pz * width)} {c.P(bu, bz)} Z")
    out = c.pth(d, fill, stroke, 0.45)
    if vein: out += c.ln(bu, bz, tu, tz, stroke, 0.35, 0.7)
    return out


def streaks(c, u0, u1, z0, z1, spec=((0.10, 0.22, 0.5), (0.27, 0.31, 0.32))):
    out = ""
    w, h = u1 - u0, z1 - z0
    sl = h * 0.62
    bx = box(u0, z0, u1, z1)
    for a, b, op in spec:
        p = Polygon([(u0 + a * w + sl, z1), (u0 + b * w + sl, z1), (u0 + b * w, z0), (u0 + a * w, z0)]).intersection(bx)
        for q in polys(p):
            out += c.pg(list(q.exterior.coords), "#FFFFFF", None, op=op)
    return out


# ------------------------------------------------------------------ elevation parts
def glass_pane(c, u0, u1, z0, z1, shadow=True):
    T = c.T
    s = c.r(u0, u1, z0, z1, "url(#gGlass)", T["edge"], 0.5)
    s += streaks(c, u0, u1, z0, z1)
    if shadow:
        s += c.r(u0, u1, z1 - min(0.7, (z1 - z0) * 0.22), z1, "url(#gShadowTop)", extra=' opacity="0.8"')
        s += c.r(u0, u0 + min(0.32, (u1 - u0) * 0.2), z0, z1, "url(#gShadowLeft)", extra=' opacity="0.8"')
    return s


def d_window(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    w, h = u1 - u0, z1 - z0
    ft, mw = 0.2, 0.14
    s = c.r(u0 - 0.35, u1 + 0.35, z1, z1 + 0.5, T["stone"][2], T["stone_line"], 0.9)             # stone head course
    s += c.r(u0 - 0.35, u1 + 0.35, z1 + 0.5, z1 + 0.62, "url(#gShadowBelow)", extra=' opacity="0.0"')
    s += c.r(u0 - 0.22, u1 + 0.22, z0 - 1.05, z0 - 0.3, "url(#gShadowTop)", extra=' opacity="0.75"')  # cast shadow under sill
    s += c.r(u0 - 0.22, u1 + 0.22, z0 - 0.3, z0, T["stone"][1], T["stone_line"], 1.0)             # projecting sill
    s += c.ln(u0 - 0.22, z0 - 0.12, u1 + 0.22, z0 - 0.12, T["stone_line"], 0.4, 0.6)
    s += c.r(u0, u1, z0, z1, T["frame"], T["edge"], 1.3)                                         # frame
    n = 1 if w < 3.4 else 2 if w < 6.4 else 3
    iw = w - 2 * ft
    pw = (iw - (n - 1) * mw) / n
    rail = h >= 3.8
    for i in range(n):
        pu0 = u0 + ft + i * (pw + mw)
        if rail:
            rz = z1 - 1.15
            s += glass_pane(c, pu0, pu0 + pw, z0 + ft, rz - 0.06, shadow=False)
            s += glass_pane(c, pu0, pu0 + pw, rz + 0.06, z1 - ft)
        else:
            s += glass_pane(c, pu0, pu0 + pw, z0 + ft, z1 - ft)
    s += c.r(u0, u1, z0, z1, "none", T["edge"], 1.3)
    return s


def d_door(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    w = u1 - u0
    ft = 0.22
    s = c.r(u0 - 0.4, u1 + 0.4, -0.4, 0.0, T["stone"][1], T["stone_line"], 1.0)               # stone step
    s += c.r(u0 - 0.35, u1 + 0.35, z1, z1 + 0.5, T["stone"][2], T["stone_line"], 0.9)
    s += c.r(u0, u1, z0, z1, T["frame"], T["edge"], 1.3)
    s += c.r(u0 + ft, u1 - ft, z0 + 0.04, z1 - ft, T["wood"], T["edge"], 0.9)
    lite_z0 = z1 - ft - 2.35
    s += glass_pane(c, u0 + ft + 0.28, u1 - ft - 0.28, lite_z0, z1 - ft - 0.28)
    colw = (w - 2 * ft - 0.84 - 0.2) / 2
    for i in range(2):
        a = u0 + ft + 0.42 + i * (colw + 0.2)
        for zz0, zz1 in ((0.45, 1.85), (2.1, lite_z0 - 0.3)):
            s += c.r(a, a + colw, zz0, zz1, T["wood_dark"], T["edge"], 0.6, op=0.35)
            s += c.ln(a, zz1, a + colw, zz1, "#FFFFFF", 0.7, 0.7)
            s += c.ln(a, zz0, a, zz1, "#FFFFFF", 0.7, 0.5)
    s += c.r(u0 + ft, u1 - ft, z1 - ft - 0.5, z1 - ft, "url(#gShadowTop)", extra=' opacity="0.7"')
    s += c.r(u1 - ft - 0.5, u1 - ft - 0.05, 3.0, 3.12, T["frame"], None)                          # lever
    s += c.ci(u1 - ft - 0.3, 3.06, 0.11, T["frame"])
    s += c.r(u0, u1, z0, z1, "none", T["edge"], 1.3)
    return s


def d_slider(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    w = u1 - u0
    ft = 0.2
    s = c.r(u0 - 0.4, u1 + 0.4, -0.4, 0.0, T["stone"][1], T["stone_line"], 1.0)
    s += c.r(u0 - 0.35, u1 + 0.35, z1, z1 + 0.5, T["stone"][2], T["stone_line"], 0.9)
    s += c.r(u0, u1, z0, z1, T["frame"], T["edge"], 1.4)
    pw = (w - 2 * ft + 0.3) / 2
    pans = [(u0 + ft, u0 + ft + pw), (u1 - ft - pw, u1 - ft)]
    for i, (a, b) in enumerate(pans):
        s += c.r(a, b, z0 + 0.12, z1 - 0.12, T["frame"], T["edge"], 1.0 if i else 0.8)
        s += glass_pane(c, a + 0.14, b - 0.14, z0 + 0.26, z1 - 0.26, shadow=(i == 0))
    mid = (pans[0][1] + pans[1][0]) / 2
    s += c.r(mid - 0.05, mid + 0.05, 3.0, 4.4, T["plaster"], T["edge"], 0.6)                       # interlock handle
    s += c.ln(u0 + ft, z0 + 0.1, u1 - ft, z0 + 0.1, T["edge"], 1.0)
    s += c.ln(u0 + ft, z1 - 0.1, u1 - ft, z1 - 0.1, T["edge"], 1.0)
    s += c.r(u0, u1, z0, z1, "none", T["edge"], 1.4)
    return s


def d_post(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    s = c.r(u0, u1, z0 + 0.15, z1 - 0.18, "url(#gColumn)", T["edge"], 1.1)
    s += c.r(u0 - 0.2, u1 + 0.2, z0, z0 + 0.15, T["stone"][1], T["stone_line"], 0.9)
    s += c.r(u0 - 0.2, u1 + 0.2, z1 - 0.18, z1, T["frame"], T["edge"], 0.9)
    return s


def d_base(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    rng = random.Random(f"base{u0:.2f}{u1:.2f}{z1:.2f}")
    s = ""
    z = z0
    courses = []
    while z < z1 - 0.05:
        hh = min(rng.uniform(0.5, 0.85), z1 - z)
        if z1 - (z + hh) < 0.3: hh = z1 - z
        courses.append((z, z + hh))
        z += hh
    for cz0, cz1 in courses:
        cur = u0
        first = rng.uniform(0.5, 1.7)
        while cur < u1 - 0.02:
            L = first if cur == u0 else rng.uniform(1.0, 2.4)
            nxt = min(u1, cur + L)
            if u1 - nxt < 0.6: nxt = u1
            s += c.r(cur, nxt, cz0, cz1, rng.choice(T["stone"]), T["stone_line"], 0.5)
            cur = nxt
    s += c.r(u0, u1, z1 - 0.5, z1, "url(#gShadowTop)", extra=' opacity="0.0"')
    s += c.r(u0, u1, z0, z1, "none", T["edge"], 2.0 if e["near"] else 1.2)
    if e.get("wt"):
        s += c.r(u0 - 0.07, u1 + 0.07, z1, z1 + 0.2, T["stone"][2], T["edge"], 1.1)
        s += c.r(u0, u1, z1 - 0.55, z1, "url(#gShadowTop)", extra=' opacity="0.0"')
    return s


def d_face(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    s = c.r(u0, u1, z0, z1, T["brick"] if e["near"] else T["brick_far"])
    s += c.r(u0, u1, z0, z1, "url(#pBrickE)")
    for a, b, sh in e["shadows"]:
        s += c.r(a, b, z1 - sh, z1, "url(#gShadowTop)")
    s += c.r(u0, u1, z0, z1, "none", T["edge"], 2.0 if e["near"] else 1.2)
    return s


def d_roof(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    s = c.r(u0, u1, z0, z1, "url(#gFascia)", T["edge"], 2.2)
    s += c.r(u0, u1, z1 - 0.22, z1, T["frame"], T["edge"], 0.8)
    s += c.ln(u0, z0 + 0.28, u1, z0 + 0.28, T["edge"], 0.5, 0.55)
    return s


# ------------------------------------------------------------------ entourage
def shrub(c, u, zg, w, h, seed, kind):
    T = c.T
    rng = random.Random(f"shrub{seed}")
    s = ""
    if kind == "bush":
        for _ in range(9):
            uu, zz = u + rng.uniform(-w * .38, w * .38), zg + rng.uniform(h * .3, h * .62)
            s += c.ci(uu, zz, rng.uniform(.28, .5) * h * .7, T["plant"] if rng.random() < .6 else T["plant_dark"], T["edge"], 0.4, 0.92)
        for _ in range(16):
            s += c.ci(u + rng.uniform(-w * .4, w * .4), zg + rng.uniform(h * .15, h * .8), 0.05, T["edge"], None, 0, 0.35)
    else:
        for _ in range(16):
            bu = u + rng.uniform(-w / 2, w / 2)
            ang = rng.uniform(55, 125) + (bu - u) * 8
            s += leaf(c, bu, zg, ang, rng.uniform(.65, 1) * h, 0.13, T["plant"] if rng.random() < .5 else T["plant_dark"], T["edge"], False)
    return s


def tree(c, u, zg, ztop, rad, seed):
    T = c.T
    rng = random.Random(f"tree{seed}")
    zc = ztop - rad
    s = c.pg([(u - 0.28, zg), (u + 0.28, zg), (u + 0.1, zc), (u - 0.1, zc)], T["trunk"], None)
    for ang in (-35, 40, 15):
        a = math.radians(90 + ang)
        s += c.ln(u, zc - rad * .55, u + math.cos(a) * rad * .7, zc - rad * .55 + math.sin(a) * rad * .7, T["trunk"], 2.0)
    pts = []
    for _ in range(20):
        t = rng.uniform(0, 2 * math.pi)
        rr = rad * math.sqrt(rng.random()) * 0.78
        pts.append((u + math.cos(t) * rr * 1.1, zc + math.sin(t) * rr * 0.9, rng.uniform(.38, .62) * rad))
    pts.sort(key=lambda p: -p[1])
    for k, (pu, pz, pr) in enumerate(pts):
        shade = T["tree"][0] if pz > zc else T["tree"][1] if pz > zc - rad * .35 else T["tree"][2]
        s += c.ci(pu, pz, pr, shade, None, 0, 0.96)
    for _ in range(10):
        s += c.ci(u + rng.uniform(-rad * .8, rad * .7), zc - rng.uniform(0, rad * .8), rng.uniform(.25, .45) * rad * .55, T["tree"][3], None, 0, 0.55)
    for _ in range(45):
        s += c.ci(u + rng.uniform(-rad * 1.0, rad * 1.0), zc + rng.uniform(-rad * .9, rad * .8), 0.045, T["edge"], None, 0, 0.28)
    return s


def trees_for(lo, hi, zg, seed):
    L = hi - lo
    spec = [(lo - 1.4, 14.4, 3.3), (lo + L * 0.31, 15.8, 4.2), (lo + L * 0.64, 14.6, 3.6), (hi + 0.2, 15.2, 3.3)]
    return [dict(u=u, ztop=zt, rad=r, seed=f"{seed}{i}") for i, (u, zt, r) in enumerate(spec)]


# ------------------------------------------------------------------ interior: furniture, plants, people
def fshadow(c, u0, u1):
    return c.r(u0 - 0.1, u1 + 0.1, 0, 0.1, c.T["ink"], None, 0, op=0.16)


def pot(c, u, w=0.9, h=1.0, fill=None):
    T = c.T
    s = c.pg([(u - w / 2, 0), (u + w / 2, 0), (u + w / 2 + 0.1, h), (u - w / 2 - 0.1, h)], fill or T["fabric"], T["edge"], 0.7)
    return s + c.r(u - w / 2 - 0.13, u + w / 2 + 0.13, h, h + 0.12, fill or T["fabric"], T["edge"], 0.7)


def plant_tall(c, u, h, seed):
    T = c.T
    rng = random.Random(f"pt{seed}")
    s = fshadow(c, u - 0.5, u + 0.5) + c.ln(u, 1.1, u + 0.1, h * 0.82, T["plant_dark"], 1.2)
    for i in range(18):
        bz = rng.uniform(1.8, h * 0.9)
        bu = u + 0.1 * (bz / h)
        ang = rng.uniform(10, 75) if rng.random() < .5 else rng.uniform(105, 170)
        s += leaf(c, bu, bz, ang, rng.uniform(.8, 1.45), rng.uniform(.28, .46), T["plant"] if i % 3 else T["plant_dark"], T["edge"])
    return s + pot(c, u)


def plant_palm(c, u, h, seed):
    T = c.T
    rng = random.Random(f"pp{seed}")
    s = fshadow(c, u - 0.5, u + 0.5) + c.ln(u, 1.1, u, h * 0.7, T["plant_dark"], 1.4)
    for i in range(11):
        ang = 100 + (i - 5) * 15 + rng.uniform(-6, 6)
        s += leaf(c, u, h * 0.7 + rng.uniform(-.2, .2), ang, rng.uniform(1.9, 2.8), 0.17, T["plant"] if i % 2 else T["plant_dark"], T["edge"])
    return s + pot(c, u, 1.0, 1.1)


def plant_snake(c, u, seed, h=3.4):
    T = c.T
    rng = random.Random(f"sn{seed}")
    s = fshadow(c, u - 0.4, u + 0.4)
    for i in range(9):
        bu = u + (i - 4) * 0.08
        s += leaf(c, bu, 0.95, 90 + (i - 4) * 6 + rng.uniform(-3, 3), rng.uniform(.65, 1) * h, 0.15, T["plant"] if i % 2 else T["plant_dark"], T["edge"])
    return s + pot(c, u, 0.8, 0.95, T["wood"])


def plant_small(c, u, z, seed):
    T = c.T
    rng = random.Random(f"ps{seed}")
    s = c.pg([(u - .17, z), (u + .17, z), (u + .21, z + .34), (u - .21, z + .34)], T["fabric"], T["edge"], 0.6)
    for i in range(7):
        s += leaf(c, u, z + .32, 90 + (i - 3) * 22 + rng.uniform(-6, 6), rng.uniform(.4, .75), .12, T["plant"] if i % 2 else T["plant_dark"], T["edge"], False)
    return s


def plant_hang(c, u, zc, seed):
    T = c.T
    rng = random.Random(f"ph{seed}")
    zp = 6.7
    s = c.ln(u, zc, u, zp + .42, T["edge"], 0.6)
    s += c.pg([(u - .3, zp + .42), (u + .3, zp + .42), (u + .17, zp), (u - .17, zp)], T["fabric"], T["edge"], 0.7)
    for i in range(7):
        bu = u + rng.uniform(-.2, .2)
        ln = rng.uniform(1.0, 2.4)
        d = f"M{c.P(bu, zp + .3)} Q{c.P(bu + rng.uniform(-.5, .5), zp - ln * .5)} {c.P(bu + rng.uniform(-.35, .35), zp - ln)}"
        s += c.pth(d, "none", T["plant_dark"], 0.9)
        for j in range(4):
            s += leaf(c, bu + rng.uniform(-.2, .2), zp - ln * (j + 1) / 5, rng.choice((20, 160, 200, 340)), .3, .09, T["plant"], T["edge"], False)
    for _ in range(5):
        s += leaf(c, u + rng.uniform(-.2, .2), zp + .4, rng.uniform(40, 140), rng.uniform(.4, .65), .12, T["plant"], T["edge"], False)
    return s


def pendant(c, u, wall, length=2.6, w=0.9):
    T = c.T
    zt = wall - length
    s = c.ln(u, wall, u, zt + 0.5, T["edge"], 0.6)
    s += c.pth(f"M{c.P(u - w / 2, zt)} Q{c.P(u - w / 2, zt + .5)} {c.P(u, zt + .52)} Q{c.P(u + w / 2, zt + .5)} {c.P(u + w / 2, zt)} Z", T["shade"], T["edge"], 0.7)
    s += c.r(u - w / 2 + .1, u + w / 2 - .1, zt - .05, zt, "#FFFFFF", None, 0, op=0.9)
    return s


def person(c, u, seed, h=5.75):
    T = c.T
    rng = random.Random(f"pe{seed}")
    cloth = rng.choice((T["person"], T["fabric_dark"], T["wood_dark"], "#4A5560"))
    s = c.r(u - .4, u + .4, 0, .08, T["ink"], None, 0, op=0.18)
    s += c.r(u - .27, u - .04, 0.05, 3.0, T["person"], None)
    s += c.r(u + .04, u + .27, 0.05, 3.0, T["person"], None)
    s += c.pth(f"M{c.P(u - .42, 3.15)} L{c.P(u - .36, 4.95)} Q{c.P(u, 5.12)} {c.P(u + .36, 4.95)} L{c.P(u + .42, 3.15)} Z", cloth, None)
    s += c.pth(f"M{c.P(u - .42, 4.9)} L{c.P(u - .58, 3.4)} L{c.P(u - .47, 3.35)} L{c.P(u - .3, 4.7)} Z", cloth, None)
    s += c.pth(f"M{c.P(u + .42, 4.9)} L{c.P(u + .58, 3.4)} L{c.P(u + .47, 3.35)} L{c.P(u + .3, 4.7)} Z", cloth, None)
    s += c.r(u - .07, u + .07, 4.95, 5.2, T["skin"], None)
    s += c.ci(u, h - .33, .27, T["skin"], T["edge"], 0.5)
    s += c.pth(f"M{c.P(u - .28, h - .25)} Q{c.P(u, h + .12)} {c.P(u + .28, h - .25)} Q{c.P(u, h - .05)} {c.P(u - .28, h - .25)}", T["person"], None)
    return s


def bed(c, u0, seed=0):
    T = c.T
    w = 5.6
    s = fshadow(c, u0, u0 + w)
    s += c.r(u0 - 0.05, u0 + w + 0.05, 0.55, 3.5, T["wood_dark"], T["edge"], 0.8)
    for i in range(3):
        s += c.r(u0 + 0.25 + i * (w - 0.5) / 3, u0 + 0.25 + (i + 1) * (w - 0.5) / 3 - 0.08, 1.9, 3.25, T["wood"], T["edge"], 0.5, op=0.7)
    s += c.r(u0, u0 + w, 0.35, 1.0, T["wood_dark"], T["edge"], 0.8)
    s += c.r(u0 + 0.1, u0 + w - 0.1, 1.0, 1.85, "#F6F3EC", T["edge"], 0.8, rx=2)
    s += c.r(u0 + 0.1, u0 + w - 0.1, 1.0, 1.4, T["fabric_dark"], T["edge"], 0.6, op=0.65)
    s += c.ln(u0 + 0.1, 1.4, u0 + w - 0.1, 1.4, T["edge"], 0.6)
    s += c.r(u0 + 0.35, u0 + 2.65, 1.85, 2.5, "#FFFFFF", T["edge"], 0.8, rx=5)
    s += c.r(u0 + 2.95, u0 + 5.25, 1.85, 2.5, "#FFFFFF", T["edge"], 0.8, rx=5)
    s += c.r(u0 + 0.12, u0 + 0.3, 0, 0.35, T["wood_dark"], T["edge"], 0.6)
    s += c.r(u0 + w - 0.3, u0 + w - 0.12, 0, 0.35, T["wood_dark"], T["edge"], 0.6)
    return s


def nightstand(c, u0, lamp=True):
    T = c.T
    s = fshadow(c, u0, u0 + 1.4)
    s += c.r(u0, u0 + 1.4, 0.2, 1.75, T["wood"], T["edge"], 0.8)
    s += c.ln(u0, 1.0, u0 + 1.4, 1.0, T["edge"], 0.6)
    s += c.ci(u0 + 0.7, 1.38, 0.05, T["edge"]) + c.ci(u0 + 0.7, 0.6, 0.05, T["edge"])
    s += c.r(u0 + 0.1, u0 + 0.2, 0, 0.2, T["wood_dark"], T["edge"], 0.5) + c.r(u0 + 1.2, u0 + 1.3, 0, 0.2, T["wood_dark"], T["edge"], 0.5)
    if lamp:
        s += c.r(u0 + 0.62, u0 + 0.78, 1.75, 2.35, T["edge"], None)
        s += c.pg([(u0 + .35, 2.3), (u0 + 1.05, 2.3), (u0 + .92, 2.95), (u0 + .48, 2.95)], T["shade"], T["edge"], 0.7, op=0.92)
    return s


def wardrobe(c, u0, w=3.2):
    T = c.T
    s = fshadow(c, u0, u0 + w) + c.r(u0, u0 + w, 0.1, 7.0, T["wood"], T["edge"], 0.9)
    s += c.ln(u0 + w / 2, 0.1, u0 + w / 2, 7.0, T["edge"], 0.7)
    s += c.r(u0 + w / 2 - .22, u0 + w / 2 - .17, 3.0, 4.2, T["edge"], None) + c.r(u0 + w / 2 + .17, u0 + w / 2 + .22, 3.0, 4.2, T["edge"], None)
    s += c.r(u0 + 0.12, u0 + w - 0.12, 0.1, 0.3, T["wood_dark"], T["edge"], 0.5)
    s += c.r(u0 - .05, u0 + w + .05, 7.0, 7.12, T["wood_dark"], T["edge"], 0.7)
    return s


def sofa(c, u0, w=6.8):
    T = c.T
    s = fshadow(c, u0, u0 + w)
    s += c.r(u0 + 0.5, u0 + w - 0.5, 0.45, 2.95, T["fabric"], T["edge"], 0.9, rx=3)
    cw = (w - 1.4) / 3
    for i in range(3):
        s += c.r(u0 + 0.7 + i * cw, u0 + 0.7 + (i + 1) * cw - 0.05, 1.55, 2.8, T["fabric"], T["edge"], 0.7, rx=4)
        s += c.r(u0 + 0.7 + i * cw, u0 + 0.7 + (i + 1) * cw - 0.05, 0.7, 1.5, T["fabric_dark"], T["edge"], 0.7, op=0.55, rx=3)
    s += c.r(u0, u0 + 0.62, 0.45, 2.15, T["fabric"], T["edge"], 0.9, rx=4)
    s += c.r(u0 + w - 0.62, u0 + w, 0.45, 2.15, T["fabric"], T["edge"], 0.9, rx=4)
    s += c.r(u0 + 0.55, u0 + w - 0.55, 0.45, 0.62, T["fabric_dark"], T["edge"], 0.6, op=0.6)
    s += c.pg([(u0 + 1.0, 1.55), (u0 + 1.8, 1.55), (u0 + 1.75, 2.4), (u0 + 1.05, 2.4)], T["shade"], T["edge"], 0.7, op=0.9)
    for uu in (u0 + 0.2, u0 + w - 0.35):
        s += c.r(uu, uu + 0.15, 0, 0.45, T["wood_dark"], T["edge"], 0.5)
    return s


def coffee_table(c, uc, w=3.2):
    T = c.T
    u0 = uc - w / 2
    s = fshadow(c, u0, u0 + w) + c.r(u0, u0 + w, 1.3, 1.46, T["wood"], T["edge"], 0.8)
    s += c.r(u0 + 0.25, u0 + 0.36, 0, 1.3, T["wood_dark"], T["edge"], 0.6) + c.r(u0 + w - 0.36, u0 + w - 0.25, 0, 1.3, T["wood_dark"], T["edge"], 0.6)
    s += c.r(u0 + 0.36, u0 + w - 0.36, 0.45, 0.55, T["wood_dark"], T["edge"], 0.5)
    s += c.r(u0 + 0.5, u0 + 1.2, 1.46, 1.62, T["fabric_dark"], T["edge"], 0.5) + c.r(u0 + 0.58, u0 + 1.12, 1.62, 1.76, "#FFFFFF", T["edge"], 0.5)
    s += c.pth(f"M{c.P(u0 + 2.3, 1.46)} Q{c.P(u0 + 2.05, 1.85)} {c.P(u0 + 2.2, 2.0)} L{c.P(u0 + 2.4, 2.0)} Q{c.P(u0 + 2.55, 1.85)} {c.P(u0 + 2.3, 1.46)} Z", T["glass"], T["edge"], 0.6)
    s += leaf(c, u0 + 2.3, 2.0, 70, .55, .1, T["plant"], T["edge"], False) + leaf(c, u0 + 2.3, 2.0, 115, .5, .1, T["plant_dark"], T["edge"], False)
    return s


def console_tv(c, u0, w=4.6):
    T = c.T
    s = fshadow(c, u0, u0 + w) + c.r(u0, u0 + w, 0.35, 1.7, T["wood"], T["edge"], 0.9)
    for i in range(3):
        x = u0 + i * w / 3
        s += c.r(x + .06, x + w / 3 - .06, 0.45, 1.6, "none", T["edge"], 0.5)
        s += c.r(x + w / 6 - .25, x + w / 6 + .25, 1.2, 1.26, T["edge"], None)
    for uu in (u0 + .2, u0 + w - .35):
        s += c.r(uu, uu + .15, 0, .35, T["wood_dark"], T["edge"], 0.5)
    s += c.r(u0 + w / 2 - 0.5, u0 + w / 2 + 0.5, 1.7, 1.85, T["edge"], None)
    s += c.r(u0 + .45, u0 + w - .45, 1.85, 4.2, T["edge"], T["edge"], 0.8)
    s += c.pg([(u0 + .6, 1.95), (u0 + 1.6, 1.95), (u0 + 2.7, 4.1), (u0 + 1.7, 4.1)], "#FFFFFF", None, op=0.1)
    return s


def dining(c, u0, w=6.0):
    T = c.T
    s = fshadow(c, u0 - .2, u0 + w + .2)
    for i in range(3):
        cu = u0 + .4 + i * (w - 1.3) / 2
        s += c.r(cu, cu + 1.3, 1.4, 1.54, T["wood_dark"], T["edge"], 0.7)
        s += c.r(cu + .08, cu + 1.22, 1.54, 3.05, T["wood"], T["edge"], 0.7, rx=2)
        for k in range(1, 4):
            s += c.ln(cu + .08, 1.54 + k * .36, cu + 1.22, 1.54 + k * .36, T["edge"], 0.4, 0.6)
        s += c.r(cu + .08, cu + .18, 0, 1.4, T["wood_dark"], T["edge"], 0.5) + c.r(cu + 1.12, cu + 1.22, 0, 1.4, T["wood_dark"], T["edge"], 0.5)
    s += c.r(u0, u0 + w, 2.45, 2.62, T["wood"], T["edge"], 0.9)
    s += c.r(u0 + .15, u0 + .28, 0, 2.45, T["wood_dark"], T["edge"], 0.6) + c.r(u0 + w - .28, u0 + w - .15, 0, 2.45, T["wood_dark"], T["edge"], 0.6)
    s += c.pth(f"M{c.P(u0 + w / 2 - .18, 2.62)} Q{c.P(u0 + w / 2 - .32, 3.0)} {c.P(u0 + w / 2 - .2, 3.2)} L{c.P(u0 + w / 2 + .2, 3.2)} Q{c.P(u0 + w / 2 + .32, 3.0)} {c.P(u0 + w / 2 + .18, 2.62)} Z", T["glass"], T["edge"], 0.6)
    s += leaf(c, u0 + w / 2, 3.2, 80, .7, .12, T["plant"], T["edge"], False) + leaf(c, u0 + w / 2, 3.2, 105, .6, .12, T["plant_dark"], T["edge"], False)
    return s


def kitchen(c, u0, w, wall):
    T = c.T
    s = fshadow(c, u0, u0 + w)
    cw = min(w - 3.2, 9.0)
    s += c.r(u0, u0 + cw, 0.3, 2.9, T["wood"], T["edge"], 0.9)
    n = max(2, int(cw // 1.5))
    for i in range(n):
        x = u0 + i * cw / n
        s += c.r(x + .05, x + cw / n - .05, 0.4, 2.8, "none", T["edge"], 0.5)
        s += c.r(x + cw / n / 2 - .2, x + cw / n / 2 + .2, 2.45, 2.5, T["edge"], None)
    s += c.r(u0, u0 + cw, 0, 0.3, T["edge"], None)
    s += c.r(u0 - .05, u0 + cw + .05, 2.9, 3.06, T["stone"][2], T["edge"], 0.8)
    s += c.r(u0, u0 + cw, 3.06, 4.5, T["plaster_deep"], None, 0, op=0.6)
    for k in range(1, 5):
        s += c.ln(u0, 3.06 + k * .36, u0 + cw, 3.06 + k * .36, T["edge"], 0.3, 0.5)
    s += c.r(u0, u0 + cw, 4.9, 7.1, T["wood"], T["edge"], 0.9)
    m = max(2, int(cw // 1.8))
    for i in range(m):
        x = u0 + i * cw / m
        s += c.r(x + .05, x + cw / m - .05, 5.0, 7.0, "none", T["edge"], 0.5)
        s += c.r(x + cw / m / 2 - .2, x + cw / m / 2 + .2, 5.15, 5.2, T["edge"], None)
    sc_u = u0 + cw * 0.6
    s += c.pth(f"M{c.P(sc_u - .45, 2.95)} Q{c.P(sc_u, 2.6)} {c.P(sc_u + .45, 2.95)}", "none", T["edge"], 0.8)
    s += c.pth(f"M{c.P(sc_u, 2.95)} L{c.P(sc_u, 3.7)} Q{c.P(sc_u + .1, 3.95)} {c.P(sc_u + .35, 3.85)}", "none", T["edge"], 1.1)
    s += plant_small(c, u0 + 0.8, 3.06, "k")
    fu = u0 + cw + 0.5
    if fu + 2.7 <= u0 + w:
        s += c.r(fu, fu + 2.7, 0.1, 6.2, "#E6E3DC", T["edge"], 0.9, rx=2)
        s += c.ln(fu, 4.4, fu + 2.7, 4.4, T["edge"], 0.7)
        s += c.r(fu + .22, fu + .3, 4.7, 5.7, T["edge"], None) + c.r(fu + .22, fu + .3, 2.8, 3.8, T["edge"], None)
    return s


def bath(c, u0, w):
    T = c.T
    s = fshadow(c, u0, u0 + w)
    vw = min(2.6, w * 0.4)
    s += c.r(u0 + .3, u0 + .3 + vw, 0.5, 2.7, T["wood"], T["edge"], 0.9)
    s += c.ln(u0 + .3 + vw / 2, .5, u0 + .3 + vw / 2, 2.7, T["edge"], 0.6)
    s += c.pth(f"M{c.P(u0 + .3, 2.7)} L{c.P(u0 + .3 + vw, 2.7)} L{c.P(u0 + .3 + vw - .2, 2.95)} L{c.P(u0 + .5, 2.95)} Z", "#FFFFFF", T["edge"], 0.7)
    s += c.r(u0 + .3 + vw / 2 - .07, u0 + .3 + vw / 2 + .07, 2.95, 3.25, T["edge"], None)
    s += c.r(u0 + .45, u0 + .15 + vw, 3.7, 6.7, "url(#gGlass)", T["edge"], 0.8) + streaks(c, u0 + .45, u0 + .15 + vw, 3.7, 6.7)
    tu = u0 + w - 2.6
    s += c.r(tu, tu + 0.9, 0.9, 2.5, "#FFFFFF", T["edge"], 0.8, rx=3)
    s += c.pth(f"M{c.P(tu + .9, 1.6)} Q{c.P(tu + 1.45, 1.55)} {c.P(tu + 1.4, 0.2)} L{c.P(tu + .95, 0.2)} Z", "#FFFFFF", T["edge"], 0.8)
    s += c.ln(tu + .1, 2.2, tu + .8, 2.2, T["edge"], 0.5)
    return s


def laundry(c, u0, w):
    T = c.T
    s = fshadow(c, u0, u0 + 5.0)
    for i in range(2):
        x = u0 + .3 + i * 2.5
        s += c.r(x, x + 2.3, 0.1, 3.5, "#ECE9E2", T["edge"], 0.9, rx=3)
        s += c.r(x + .15, x + 2.15, 3.1, 3.4, T["plaster_deep"], T["edge"], 0.5)
        s += c.ci(x + 1.15, 1.75, 0.8, T["glass"], T["edge"], 1.0)
        s += c.ci(x + 1.15, 1.75, 0.55, T["glass_deep"], T["edge"], 0.6, 0.55)
    s += c.r(u0 + .2, u0 + 5.0, 4.9, 5.05, T["wood"], T["edge"], 0.8)
    s += plant_small(c, u0 + 4.3, 5.05, "l")
    return s


def furnish(c, room, H, ctx):
    nm = room["name"].lower()
    u0, u1, w, zn = room["u0"], room["u1"], room["u1"] - room["u0"], room["zone"]
    wall = H["wall"]
    kind = ("bed" if "bed" in nm else "living" if ("living" in nm or "family" in nm) else "dining" if "dining" in nm
            else "kitchen" if "kitchen" in nm else "bath" if any(k in nm for k in ("bath", "toilet", "wc", "powder"))
            else "laundry" if ("laundry" in nm or "utility" in nm) else {"night": "bed", "day": "living", "wet": "bath"}.get(zn, "living"))
    s = c.r(u0, u1, wall - 1.0, wall, "url(#gShadowTop)", extra=' opacity="0.5"')
    s += c.r(u0, u1, 0, 0.13, c.T["floor"], c.T["edge"], 0.5)
    k = ctx["count"].setdefault(kind, 0)
    ctx["count"][kind] += 1
    mirror = k % 2 == 1
    if kind == "bed" and w >= 8:
        bu = (u1 - 1.0 - 1.5 - 5.6 - 1.5) if mirror else (u0 + 1.0 + 1.5)
        s += nightstand(c, bu - 1.5, lamp=not mirror)
        s += bed(c, bu, k)
        s += nightstand(c, bu + 5.6 + 0.1, lamp=mirror)
        far_u0 = (u0 + 0.5) if mirror else (u1 - 3.6)
        if w >= 12.6:
            s += wardrobe(c, far_u0, 3.2)
        else:
            s += plant_tall(c, far_u0 + 1.3, 5.2, f"b{k}")
        s += pendant(c, bu + 2.8, wall, 2.2, 0.8)
    elif kind == "living":
        sw = min(6.8, w * 0.46)
        s += sofa(c, u0 + 0.9, sw)
        s += coffee_table(c, u0 + 0.9 + sw / 2, 3.2)
        if w >= 13:
            s += console_tv(c, u1 - 5.0, 4.6)
            s += person(c, u1 - 1.3, "lp")
        if w >= 12:
            s += plant_palm(c, u0 + 0.9 + sw + 1.1, 6.0, "lv")
        s += pendant(c, u0 + 0.9 + sw / 2 - 1.0, wall, 2.8, 1.0) + pendant(c, u0 + 0.9 + sw / 2 + 1.0, wall, 2.3, 1.0)
    elif kind == "dining":
        tw = min(6.0, w * 0.6)
        s += dining(c, u0 + (w - tw) / 2, tw)
        s += pendant(c, u0 + w / 2 - 1.0, wall, 3.2, 1.0) + pendant(c, u0 + w / 2 + 1.0, wall, 3.2, 1.0)
        s += plant_tall(c, u1 - 1.0, 5.0, "dn")
    elif kind == "kitchen":
        s += kitchen(c, u0 + 0.3, w - 0.6, wall)
        s += pendant(c, u0 + w * 0.5, wall, 3.0, 0.9)
    elif kind == "bath":
        s += bath(c, u0, w)
    elif kind == "laundry":
        s += laundry(c, u0, w)
    else:
        s += plant_tall(c, u0 + w / 2, 5.0, "x")
    return s


# ------------------------------------------------------------------ interior wall faces beyond, cut parts
def d_beyond(c, e):
    T = c.T
    s = c.r(e["u0"], e["u1"], e["z0"], e["z1"], "url(#gPlaster)", T["edge"], 0.8)
    if e.get("skirt"):
        s += c.r(e["u0"], e["u1"], 0, 0.42, T["plaster_deep"], T["edge"], 0.5)
    return s


def d_bglass(c, e):
    T = c.T
    u0, u1, z0, z1 = e["u0"], e["u1"], e["z0"], e["z1"]
    w = u1 - u0
    ft, mw = 0.16, 0.12
    s = c.r(u0 - 0.15, u1 + 0.15, z0 - 0.14, z0, T["plaster"], T["edge"], 0.7)                    # interior sill board
    s += c.r(u0 - 0.08, u1 + 0.08, z0, z1 + 0.08, T["plaster_deep"], T["edge"], 0.6)               # casing
    s += c.r(u0, u1, z0, z1, T["frame"], T["edge"], 1.0)
    n = 1 if w < 3.4 else 2 if w < 6.4 else 3
    pw = (w - 2 * ft - (n - 1) * mw) / n
    for i in range(n):
        a = u0 + ft + i * (pw + mw)
        s += glass_pane(c, a, a + pw, z0 + ft, z1 - ft, shadow=False)
    return s


def d_bdoor(c, e):
    T = c.T
    u0, u1, z1 = e["u0"], e["u1"], e["z1"]
    w = u1 - u0
    s = c.r(u0 - 0.15, u1 + 0.15, 0, z1 + 0.15, T["plaster_deep"], T["edge"], 0.7)
    s += c.r(u0, u1, 0, z1, T["wood"], T["edge"], 1.0)
    cw = (w - 0.9) / 2
    for i in range(2):
        a = u0 + 0.3 + i * (cw + 0.3)
        for zz0, zz1 in ((0.4, 2.7), (3.0, 6.6)):
            s += c.r(a, a + cw, zz0, zz1, T["wood_dark"], T["edge"], 0.5, op=0.32)
    s += c.r(u1 - 0.5, u1 - 0.1, 3.0, 3.12, T["frame"], None) + c.ci(u1 - 0.32, 3.06, 0.1, T["frame"])
    return s


def d_bslide(c, e):
    T = c.T
    u0, u1, z1 = e["u0"], e["u1"], e["z1"]
    s = c.r(u0 - 0.1, u1 + 0.1, 0, z1 + 0.1, T["plaster_deep"], T["edge"], 0.7)
    s += c.r(u0, u1, 0, z1, T["frame"], T["edge"], 1.0)
    pw = (u1 - u0 - 0.4 + 0.3) / 2
    for a, b in ((u0 + 0.2, u0 + 0.2 + pw), (u1 - 0.2 - pw, u1 - 0.2)):
        s += c.r(a, b, 0.12, z1 - 0.12, T["frame"], T["edge"], 0.8) + glass_pane(c, a + 0.12, b - 0.12, 0.24, z1 - 0.24, shadow=False)
    return s


def d_cut(c, e):
    T = c.T
    u0, u1, z0, z1, part = e["u0"], e["u1"], e["z0"], e["z1"], e["part"]
    s = c.r(u0, u1, z0, z1, T["poche"], T["poche"], 1.0)
    if part == "wall" and e.get("ext"):
        base = c.base
        if z0 < base:
            s += c.r(u0, u1, z0, min(z1, base), "url(#pCutStone)")
        if z1 > base:
            s += c.r(u0, u1, max(z0, base), z1, "url(#pCutBrick)")
    elif part == "slab":
        s += c.r(u0, u1, z0, z1, "url(#pConc)") + c.ln(u0, -0.12, u1, -0.12, T["bg"], 0.6, 0.55)
    elif part == "found":
        s += c.r(u0, u1, z0, z1, "url(#pConc)")
    elif part == "roof":
        s += c.ln(u0, z1 - 0.2, u1, z1 - 0.2, T["bg"], 0.7, 0.6)
        s += c.ln(u0, z1 - 0.62, u1, z1 - 0.62, T["bg"], 0.5, 0.4, dash="3 2")
        s += c.ln(u0, z0 + 0.22, u1, z0 + 0.22, T["bg"], 0.6, 0.5)
    return s


def d_cglass(c, e):
    T = c.T
    u0, u1, z0, z1, d = e["u0"], e["u1"], e["z0"], e["z1"], e["inward"]
    s = c.r(u0, u1, z0, z1, T["glass"], T["edge"], 0.5)
    s += c.r(u0 - 0.1, u1 + 0.1, z0 - 0.04, z0 + 0.22, T["frame"], T["edge"], 0.5)
    s += c.r(u0 - 0.1, u1 + 0.1, z1 - 0.22, z1 + 0.04, T["frame"], T["edge"], 0.5)
    m = (u0 + u1) / 2
    ext_u0, ext_u1 = (e["wa"] - 0.25, m) if d > 0 else (m, e["wb"] + 0.25)
    s += c.pg([(ext_u0 if d > 0 else ext_u1, z0 - 0.26), (m, z0 - 0.02), (m, z0), (ext_u0 if d > 0 else ext_u1, z0 - 0.02)], T["stone"][1], T["stone_line"], 0.8)
    if d > 0:
        s += c.r(m, e["wb"] + 0.15, z0, z0 + 0.12, T["plaster"], T["edge"], 0.6)
    else:
        s += c.r(e["wa"] - 0.15, m, z0, z0 + 0.12, T["plaster"], T["edge"], 0.6)
    return s


def d_ent(c, e):
    if e["kind"] == "tree":
        return tree(c, e["u"], e["zg"], e["ztop"], e["rad"], e["seed"])
    return shrub(c, e["u"], e["zg"], e["w"], e["h"], e["seed"], e["kind"])


DRAW = dict(base=d_base, face=d_face, post=d_post, window=d_window, door=d_door, slider=d_slider, roof=d_roof,
            beyond=d_beyond, bglass=d_bglass, bdoor=d_bdoor, bslide=d_bslide, cut=d_cut, cglass=d_cglass,
            ent=d_ent, room=lambda c, e: e["html"])


def item(C, e):
    cx = (C.X(e["u0"]) + C.X(e["u1"])) / 2
    cls = f"it k-{e['k']}" + (f" p-{e['part']}" if e.get("part") else "")
    return f'<g class="{cls}" data-u="{cx:.1f}">{DRAW[e["k"]](C, e)}</g>'


# ------------------------------------------------------------------ defs
def make_defs(T, sc, yE0, x0):
    bw, bh = 0.67 * sc, 0.5 * sc
    d = ['<defs>']
    d.append(f'<pattern id="pBrickE" x="{x0:.2f}" y="{yE0:.2f}" width="{bw:.3f}" height="{bh:.3f}" patternUnits="userSpaceOnUse">'
             f'<path d="M0,0 H{bw:.3f} M0,{bh / 2:.3f} H{bw:.3f}" stroke="{T["brick_line"]}" stroke-width="0.42" stroke-opacity="0.62" fill="none"/>'
             f'<path d="M0,0 V{bh / 2:.3f} M{bw / 2:.3f},{bh / 2:.3f} V{bh:.3f}" stroke="{T["brick_line"]}" stroke-width="0.38" stroke-opacity="0.5" fill="none"/></pattern>')
    d.append(f'<pattern id="pCutBrick" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(0)">'
             f'<path d="M-1,6 L6,-1 M-1,1 L1,-1 M4,6 L6,4" stroke="{T["bg"]}" stroke-width="0.75" stroke-opacity="0.6" fill="none"/></pattern>')
    d.append(f'<pattern id="pCutStone" width="11" height="8" patternUnits="userSpaceOnUse">'
             f'<path d="M0,4 H11 M3,0 V4 M8,4 V8 M0,8 H11" stroke="{T["bg"]}" stroke-width="0.7" stroke-opacity="0.6" fill="none"/></pattern>')
    d.append(f'<pattern id="pConc" width="7" height="7" patternUnits="userSpaceOnUse">'
             f'<circle cx="1.5" cy="1.5" r="0.55" fill="{T["bg"]}" fill-opacity="0.55"/><circle cx="5" cy="4.4" r="0.45" fill="{T["bg"]}" fill-opacity="0.5"/>'
             f'<path d="M0,7 L2.5,4.5" stroke="{T["bg"]}" stroke-width="0.5" stroke-opacity="0.45"/></pattern>')
    rng = random.Random("earth")
    dots = "".join(f'<circle cx="{rng.uniform(0, 16):.1f}" cy="{rng.uniform(0, 14):.1f}" r="{rng.uniform(.4, .95):.2f}" fill="{T["earth_dot"]}" fill-opacity="{rng.uniform(.5, .9):.2f}"/>' for _ in range(16))
    d.append(f'<pattern id="pEarth" width="16" height="14" patternUnits="userSpaceOnUse">{dots}</pattern>')
    def lg(i, x2, y2, stops):
        return f'<linearGradient id="{i}" x1="0" y1="0" x2="{x2}" y2="{y2}">' + "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</linearGradient>'
    ink = T["ink"]
    d.append(lg("gGlass", 0, 1, [(0, T["glass_hi"], 1), (0.55, T["glass"], 1), (1, T["glass_deep"], 1)]))
    d.append(lg("gShadowTop", 0, 1, [(0, "#1B1B1B", 0.5), (0.45, "#1B1B1B", 0.2), (1, "#1B1B1B", 0)]))
    d.append(lg("gShadowBelow", 0, 1, [(0, "#1B1B1B", 0.3), (1, "#1B1B1B", 0)]))
    d.append(lg("gShadowLeft", 1, 0, [(0, "#1B1B1B", 0.38), (1, "#1B1B1B", 0)]))
    d.append(lg("gColumn", 1, 0, [(0, "#FAF8F3", 1), (0.45, T["slab_s"], 1), (1, hexshade(T["slab_e"], 0.7), 1)]))
    d.append(lg("gFascia", 0, 1, [(0, T["face_s"], 1), (0.5, T["slab_s"], 1), (1, T["slab_e"], 1)]))
    d.append(lg("gPlaster", 0, 1, [(0, hexshade(T["plaster"], 0.9), 1), (0.3, T["plaster"], 1), (1, hexshade(T["plaster"], 0.96), 1)]))
    d.append(lg("gEarthFade", 0, 1, [(0, T["bg"], 0.0), (0.55, T["bg"], 0.35), (1, T["bg"], 0.96)]))
    d.append('</defs>')
    return "".join(d)


# ------------------------------------------------------------------ render
def render(plan, theme="light"):
    T = THEMES[theme]
    G = geometry(plan)
    H = G["H"]
    north = plan.get("north", 0)
    fside = SIDE[plan.get("front", "bottom")]
    sec = plan.get("section") or {"axis": "y", "at": round(G["foot"].bounds[3] * 0.35, 1), "look": "top", "label": "A"}
    lab = sec.get("label", "A")
    E = elevation(G, fside)
    S = section(G, sec)
    SANS = 'font-family="%s, Helvetica, Arial, sans-serif"' % T.get("sans", SANS_DEFAULT)
    SERIF = 'font-family="\'%s\', Georgia, serif"' % T.get("serif", SERIF_DEFAULT)
    PW, PH = 1080, 1350
    DL, DR = 70, 790
    gz = -H["grade"]
    ED = 3.2

    def urange(items):
        return min(e["u0"] for e in items), max(e["u1"] for e in items)
    eu = urange(E["items"]); su = urange(S["cut"] + S["beyond"])
    same = fside == S["side"]
    span = max(eu[1] - eu[0], su[1] - su[0]) if not same else max(eu[1], su[1]) - min(eu[0], su[0])
    ztop = H["wall"] + H["roof"]
    TOP, HEAD = 118, 92
    AV = 965 - TOP
    per = ztop + H["grade"] + ED
    sc = min((DR - DL - 70) / span, (AV / 2 - (HEAD + 92) - 4) / per, 26.0)
    slack = max(0, AV - 2 * (HEAD + 92 + per * sc))

    def mkX(ur):
        lo, hi = (min(eu[0], su[0]), max(eu[1], su[1])) if same else ur
        off = DL + ((DR - DL) - (hi - lo) * sc) / 2
        return lambda uu: off + (uu - lo) * sc

    XE, XS = mkX(eu), mkX(su)
    yE0 = TOP + slack / 3 + HEAD + ztop * sc
    endE = yE0 + (H["grade"] + ED) * sc + 24 + 46 + 22
    yS0 = endE + slack / 3 + HEAD + ztop * sc
    YE = lambda z: yE0 - z * sc
    YS = lambda z: yS0 - z * sc
    cE, cS = Ctx(XE, YE, sc, T), Ctx(XS, YS, sc, T)
    cE.base = cS.base = H["base"]

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}">',
         make_defs(T, sc, yE0, XE(0)),
         f'<rect width="{PW}" height="{PH}" fill="{T["bg"]}"/>', '<g id="hdr">']
    title = f'{plan.get("project", "Project").upper()}  ·  {plan.get("subtitle", "").upper()}'.strip(" ·")
    o.append(f'<text x="70" y="88" {SANS} font-size="15" font-weight="700" letter-spacing="2.2" fill="{T["ink"]}">{title}</text>')
    o.append(f'<text x="1010" y="88" {SANS} font-size="15" font-weight="700" letter-spacing="2" text-anchor="end" fill="{T["ink"]}">{plan.get("sheet", "01 / 01")}</text>')
    o.append(f'<rect x="70" y="104" width="940" height="1.5" fill="{T["rule"]}"/>')
    o.append(f'<rect x="70" y="102" width="56" height="5" fill="{T["accent"]}"/>')
    o.append('</g>')

    # ---- entourage items
    ent_rng = random.Random("ent")
    efu = E["foot_u"]
    blockers = [(e["u0"], e["u1"]) for e in E["items"] if e["k"] in ("door", "slider")] + \
               [(e["u0"] - 0.6, e["u1"] + 0.6) for e in E["items"] if e["k"] == "post"]
    uu, i = efu[0] + 1.0, 0
    while uu < efu[1] - 1.0:
        w = ent_rng.uniform(2.4, 3.6)
        if not any(a - 1.4 < uu < b + 1.4 for a, b in blockers):
            E["items"].append(dict(k="ent", kind="bush" if i % 2 == 0 else "grass", u=uu, zg=gz, w=w, h=ent_rng.uniform(1.6, 2.5),
                                   seed=f"e{i}", u0=uu - w / 2, u1=uu + w / 2, d=1e6 + i))
            i += 1
        uu += ent_rng.uniform(5.5, 8.5)
    sfu = S["foot_u"]
    for j, (uc, kd) in enumerate(((sfu[0] - 1.1, "bush"), (sfu[0] - 3.1, "grass"), (sfu[1] + 1.1, "bush"), (sfu[1] + 3.2, "grass"))):
        S["beyond"].append(dict(k="ent", kind=kd, u=uc, zg=gz, w=2.8, h=2.2 + 0.3 * (j % 2), seed=f"s{j}", u0=uc - 1.4, u1=uc + 1.4, d=1e6 + j))
    E_trees = trees_for(eu[0], eu[1], gz, "E")
    S_trees = trees_for(su[0], su[1], gz, "S")

    def earth(C, gid):
        x0, x1 = 70, 1010
        gy, by = C.Y(gz), C.Y(gz - ED)
        s = [f'<g id="{gid}">']
        s.append(f'<rect x="{x0}" y="{gy:.1f}" width="{x1 - x0}" height="{by - gy:.1f}" fill="url(#pEarth)"/>')
        for k, (dz, a) in enumerate(((0.75, .55), (1.65, .38), (2.55, .22))):
            yy = C.Y(gz - dz)
            pts = " L".join(f"{x:.0f},{yy + 1.8 * math.sin(x / 38 + k * 1.7):.1f}" for x in range(x0, x1 + 1, 8))
            s.append(f'<path d="M{pts}" fill="none" stroke="{T["ink"]}" stroke-width="0.6" stroke-opacity="{a}"/>')
        s.append(f'<rect x="{x0}" y="{gy:.1f}" width="{x1 - x0}" height="{by - gy:.1f}" fill="url(#gEarthFade)"/>')
        s.append('</g>')
        return "".join(s)

    def ground(C, gid, ur):
        gy = C.Y(gz)
        return (f'<line id="{gid}" pathLength="1" class="draw" x1="70" y1="{gy:.1f}" x2="1010" y2="{gy:.1f}" '
                f'stroke="{T["ink"]}" stroke-width="3.2" stroke-linecap="square"/>')

    def trees(C, gid, lst):
        return [f'<g id="{gid}">'] + [f'<g class="ent">{tree(C, t["u"], t["zg"] if "zg" in t else gz, t["ztop"], t["rad"], t["seed"])}</g>' for t in lst] + ['</g>']

    def levels(C, ur, gid):
        lv = [("T.O. ROOF", H["wall"] + H["roof"]), ("B.O. ROOF", H["wall"]), ("F.F.", 0)]
        g = [f'<g id="{gid}">']
        for nm, z in lv:
            y = C.Y(z)
            g.append('<g class="lvl">')
            g.append(f'<line pathLength="1" class="draw" x1="{C.X(ur[1]) + 8:.1f}" y1="{y:.1f}" x2="{DR + 32}" y2="{y:.1f}" stroke="{T["guide"]}" stroke-width="0.9" stroke-dasharray="1"/>')
            g.append(f'<polygon class="lt" points="{DR + 32},{y:.1f} {DR + 40},{y - 7:.1f} {DR + 24},{y - 7:.1f}" fill="{T["accent"]}" stroke="{T["ink"]}" stroke-width="1"/>')
            g.append(f'<text class="lt" x="{DR + 48}" y="{y + 4:.1f}" {SANS} font-size="11.5" font-weight="800" letter-spacing="1" fill="{T["ink"]}">{nm} <tspan font-weight="500" fill="{T["mute"]}">{fi(z, True)}</tspan></text>')
            g.append('</g>')
        g.append('</g>')
        return g

    def tag(y, num, name, sub, gid):
        return [f'<g id="{gid}">',
                f'<circle cx="84" cy="{y - 5}" r="14" fill="none" stroke="{T["ink"]}" stroke-width="1.4"/>',
                f'<text x="84" y="{y}" {SANS} font-size="13" font-weight="800" text-anchor="middle" fill="{T["ink"]}">{num}</text>',
                f'<text x="110" y="{y - 1}" {SANS} font-size="15" font-weight="800" letter-spacing="1.6" fill="{T["ink"]}">{name}</text>',
                f'<text x="110" y="{y + 18}" {SANS} font-size="12.5" font-weight="500" fill="{T["mute"]}">{sub}</text>', '</g>']

    # ---------- FRONT ELEVATION
    o.append(earth(cE, "E-earth"))
    o += trees(cE, "E-trees", E_trees)
    o.append(ground(cE, "E-ground", E["foot_u"]))
    o.append('<g id="E-draw" stroke-linejoin="miter">')
    o += [item(cE, e) for e in sorted(E["items"], key=lambda e: e["d"])]
    o.append('</g>')
    o += levels(cE, eu, "E-levels")
    dy = YE(gz - ED) + 24
    a, b = E["foot_u"]
    o.append('<g id="E-dim">')
    o.append(f'<line pathLength="1" class="draw" x1="{XE(a):.1f}" y1="{dy:.1f}" x2="{XE(b):.1f}" y2="{dy:.1f}" stroke="{T["ink"]}" stroke-width="0.9"/>')
    for xx in (XE(a), XE(b)):
        o.append(f'<line class="tk" x1="{xx - 5:.1f}" y1="{dy + 5:.1f}" x2="{xx + 5:.1f}" y2="{dy - 5:.1f}" stroke="{T["ink"]}" stroke-width="1.6"/>')
        o.append(f'<line class="tk" x1="{xx:.1f}" y1="{dy - 10:.1f}" x2="{xx:.1f}" y2="{dy + 6:.1f}" stroke="{T["ink"]}" stroke-width="0.8"/>')
    o.append(f'<text class="tk" x="{(XE(a) + XE(b)) / 2:.1f}" y="{dy - 7:.1f}" {SANS} font-size="12" font-weight="700" text-anchor="middle" fill="{T["ink"]}">{fi(b - a)}</text>')
    o.append('</g>')
    fdir = compass(fside, north)
    o += tag(dy + 46, "1", "FRONT ELEVATION", f'{fdir.capitalize()} side · looking {compass(OPP[fside], north)} · brick over stone base', "E-label")

    # ---------- SECTION
    ctx = dict(count={})
    o.append(earth(cS, "S-earth"))
    o += trees(cS, "S-trees", S_trees)
    o.append(ground(cS, "S-ground", su))
    o.append('<g id="S-draw">')
    o += [item(cS, e) for e in sorted(S["beyond"], key=lambda e: e["d"])]
    for r in S["rooms"]:
        o.append(item(cS, dict(k="room", u0=r["u0"], u1=r["u1"], html=furnish(cS, r, H, ctx))))
    cuts = sorted(S["cut"], key=lambda e: ({"found": 0, "slab": 1, "wall": 2, "roof": 3}[e["part"]], e["k"] == "cglass", e["u0"]))
    o += [item(cS, e) for e in cuts]
    o.append('</g>')
    o += levels(cS, su, "S-levels")
    ldir = compass(S["look"], north)
    stag = YS(gz - ED) + 34
    o += tag(stag, "2", f"SECTION {lab}–{lab}", f'Cut {fi(sec["at"])} from plan {"top" if sec.get("axis", "y") == "y" else "left"} edge · looking {ldir}', "S-label")
    # graphic scale bar
    seg = 5 * sc
    bx0 = DR - 4 * seg
    o.append('<g id="scalebar">')
    for k in range(4):
        o.append(f'<rect x="{bx0 + k * seg:.1f}" y="{stag - 4:.1f}" width="{seg:.1f}" height="6" fill="{T["ink"] if k % 2 == 0 else T["bg"]}" stroke="{T["ink"]}" stroke-width="1"/>')
    for k in range(5):
        o.append(f'<text x="{bx0 + k * seg:.1f}" y="{stag - 10:.1f}" {SANS} font-size="10" font-weight="700" text-anchor="middle" fill="{T["ink"]}">{k * 5}</text>')
    o.append(f'<text x="{bx0 + 4 * seg + 8:.1f}" y="{stag + 2:.1f}" {SANS} font-size="10" font-weight="700" fill="{T["mute"]}">FT</text>')
    o.append('</g>')

    # ---------- TITLE BLOCK
    y0 = 985
    o.append(f'<rect id="rule2" x="70" y="{y0}" width="940" height="1.5" fill="{T["rule"]}"/>')
    o.append(f'<text id="title" x="70" y="{y0 + 62}" {SERIF} font-size="44" font-weight="600" fill="{T["ink"]}">Elevation + section</text>')
    o.append(f'<text id="desc" x="70" y="{y0 + 96}" {SANS} font-size="15" font-weight="500" fill="{T["mute"]}">Front ({fdir}) elevation and section {lab}–{lab} · orthographic, same scale</text>')
    legend = [("Cut · poché", T["poche"]), ("Brick", T["brick"]), ("Stone base", T["stone"][0]), ("Fixed glazing", T["glass"])]
    for i, (labt, col) in enumerate(legend):
        cx = 70 + (i % 2) * 260
        yy = y0 + 140 + (i // 2) * 38
        o.append('<g class="leg">')
        o.append(f'<rect x="{cx}" y="{yy - 16}" width="34" height="22" rx="3" fill="{col}" stroke="{T["ink"]}" stroke-width="1"/>')
        if labt == "Brick": o.append(f'<rect x="{cx}" y="{yy - 16}" width="34" height="22" rx="3" fill="url(#pBrickE)"/>')
        o.append(f'<text x="{cx + 48}" y="{yy}" {SANS} font-size="15" font-weight="600" fill="{T["ink"]}">{labt}</text>')
        o.append('</g>')
    # key plan
    fx0, fy0, fx1, fy1 = G["roof"].bounds
    kw, kh = 300, 165
    ks = min(kw / (fx1 - fx0 + 8), kh / (fy1 - fy0 + 6))
    kox = 1010 - (fx1 - fx0) * ks - 26
    koy = y0 + 22 + (kh - (fy1 - fy0) * ks) / 2
    KX = lambda x: kox + (x - fx0) * ks
    KY = lambda y: koy + (y - fy0) * ks
    o.append('<g id="key">')
    o.append(f'<text x="{kox:.1f}" y="{y0 + 16}" {SANS} font-size="10.5" font-weight="800" letter-spacing="1.6" fill="{T["mute"]}">KEY PLAN</text>')
    for p, oo in G["outs"]:
        for q in polys(p.difference(G["foot"])):
            d = "M" + " L".join(f"{KX(x):.1f},{KY(y):.1f}" for x, y in q.exterior.coords) + "Z"
            o.append(f'<path d="{d}" fill="{T["zones"]["outdoor"]}" stroke="{T["ink"]}" stroke-width="0.8" stroke-dasharray="3 2"/>')
    d = "M" + " L".join(f"{KX(x):.1f},{KY(y):.1f}" for x, y in G["foot"].exterior.coords) + "Z"
    o.append(f'<path d="{d}" fill="{T["face_s"]}" stroke="none"/>')
    for p in polys(G["solid"]):
        d = "".join("M" + " L".join(f"{KX(x):.2f},{KY(y):.2f}" for x, y in r.coords) + "Z" for r in [p.exterior] + list(p.interiors))
        o.append(f'<path d="{d}" fill="{T["poche"]}" fill-rule="evenodd" stroke="none"/>')
    fu, fnr, fv = AX[fside]
    bx0_, by0_, bx1_, by1_ = G["foot"].bounds
    cxm, cym = (bx0_ + bx1_) / 2, (by0_ + by1_) / 2
    ex = {"S": (cxm, by1_ + 3.2), "N": (cxm, by0_ - 3.2), "E": (bx1_ + 3.2, cym), "W": (bx0_ - 3.2, cym)}[fside]
    ax_, ay_ = KX(ex[0]), KY(ex[1])
    o.append(f'<g id="key-front"><polygon points="{ax_ - fv[0] * 2 - fv[1] * 9:.1f},{ay_ - fv[1] * 2 + fv[0] * 9:.1f} {ax_ - fv[0] * 2 + fv[1] * 9:.1f},{ay_ - fv[1] * 2 - fv[0] * 9:.1f} {ax_ - fv[0] * 13:.1f},{ay_ - fv[1] * 13:.1f}" fill="{T["accent"]}" stroke="{T["ink"]}" stroke-width="1"/>'
             f'<text x="{ax_ + fv[0] * 9:.1f}" y="{ay_ + fv[1] * 9 + 4:.1f}" {SANS} font-size="11" font-weight="800" text-anchor="middle" fill="{T["ink"]}">1</text></g>')
    if sec.get("axis", "y") == "y":
        p0, p1 = (bx0_ - 3.5, sec["at"]), (bx1_ + 3.5, sec["at"])
    else:
        p0, p1 = (sec["at"], by0_ - 3.5), (sec["at"], by1_ + 3.5)
    lv = AX[OPP[SIDE[sec.get("look", "top")]]][2]
    o.append(f'<line id="key-cut" pathLength="1" class="draw" x1="{KX(p0[0]):.1f}" y1="{KY(p0[1]):.1f}" x2="{KX(p1[0]):.1f}" y2="{KY(p1[1]):.1f}" stroke="{T["ink"]}" stroke-width="1.6" stroke-dasharray="1"/>')
    for px, py in (p0, p1):
        X_, Y_ = KX(px), KY(py)
        o.append(f'<g class="kb"><circle cx="{X_:.1f}" cy="{Y_:.1f}" r="8" fill="{T["accent"]}" stroke="{T["ink"]}" stroke-width="1.2"/>'
                 f'<text x="{X_:.1f}" y="{Y_ + 4:.1f}" {SANS} font-size="10" font-weight="800" text-anchor="middle" fill="{T["ink"]}">{lab}</text>'
                 f'<polygon points="{X_ - lv[0] * 9 - lv[1] * 5:.1f},{Y_ - lv[1] * 9 + lv[0] * 5:.1f} {X_ - lv[0] * 9 + lv[1] * 5:.1f},{Y_ - lv[1] * 9 - lv[0] * 5:.1f} {X_ - lv[0] * 16:.1f},{Y_ - lv[1] * 16:.1f}" fill="{T["ink"]}"/></g>')
    na = math.radians(north)
    nx, ny = math.sin(na), -math.cos(na)
    nX, nY = kox - 30, koy + 30
    o.append(f'<g class="kb"><line x1="{nX:.1f}" y1="{nY:.1f}" x2="{nX + nx * 22:.1f}" y2="{nY + ny * 22:.1f}" stroke="{T["ink"]}" stroke-width="1.4"/>'
             f'<polygon points="{nX + nx * 30:.1f},{nY + ny * 30:.1f} {nX + nx * 22 - ny * 4:.1f},{nY + ny * 22 + nx * 4:.1f} {nX + nx * 22 + ny * 4:.1f},{nY + ny * 22 - nx * 4:.1f}" fill="{T["accent"]}" stroke="{T["ink"]}" stroke-width="0.9"/>'
             f'<text x="{nX + nx * 42:.1f}" y="{nY + ny * 42 + 4:.1f}" {SANS} font-size="11" font-weight="800" text-anchor="middle" fill="{T["ink"]}">N</text></g>')
    o.append('</g>')
    ow, od = G["foot"].bounds[2] - G["foot"].bounds[0], G["foot"].bounds[3] - G["foot"].bounds[1]
    no = E["n_open"]
    parts = [f'Overall {fi(ow)} × {fi(od)}', f'B.O. roof {fi(H["wall"], True)}', f'T.O. roof {fi(H["wall"] + H["roof"], True)}',
             f'stone base {fi(H["base"])}', f'front: {no["window"]} fixed windows']
    if no["slider"]: parts.append(f'{no["slider"]} slider')
    if no["door"]: parts.append(f'{no["door"]} doors')
    o.append(f'<text id="summary" x="70" y="{y0 + 228}" {SANS} font-size="13" font-weight="500" fill="{T["mute"]}">{" · ".join(parts)}</text>')
    fy = PH - 70
    o.append('<g id="foot">')
    o.append(f'<rect x="70" y="{fy - 30}" width="940" height="1.5" fill="{T["rule"]}"/>')
    o.append(f'<text x="70" y="{fy}" {SANS} font-size="13" font-weight="600" letter-spacing="1" fill="{T["mute"]}">/elevation · drawn in code from {plan.get("source", "plan")}</text>')
    o.append(f'<text x="1010" y="{fy}" {SANS} font-size="13" font-weight="800" letter-spacing="1" text-anchor="end" fill="{T["ink"]}">{plan.get("credit", "The Architecture Grind")}</text>')
    o.append('</g></svg>')
    info = dict(scale=sc, n_open=no, cut_walls=sum(1 for c in S["cut"] if c["part"] == "wall"),
                rooms=[r["name"] for r in S["rooms"]], overall=(ow, od))
    return "\n".join(o), info


def animate_html(svg, theme="light", input_img=None, input_name="floor-plan.jpg", cmd="/elevation"):
    T = THEMES[theme]
    img_tag = ""
    if input_img and os.path.exists(input_img):
        mime = mimetypes.guess_type(input_img)[0] or "image/png"
        img_tag = f'<img src="data:{mime};base64,{base64.b64encode(open(input_img, "rb").read()).decode()}" alt="input plan">'
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
        .replace("%%BG%%", T["bg"]).replace("%%INK%%", T["ink"]).replace("%%ACC%%", T["accent"]).replace("%%MUTE%%", T["mute"])


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>/elevation - elevation + section build</title>
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
  .it,.ent{transform-box:fill-box;transform-origin:50% 100%}
  .k-roof{transform-origin:50% 0%}
  .p-slab,.p-roof,.p-found{transform-origin:0% 50%}
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
const HIDE=['#hdr','#E-ground','#E-earth','#E-trees .ent','#E-draw .it','#E-levels .lvl','#E-dim','#E-label',
            '#S-ground','#S-earth','#S-trees .ent','#S-draw .it','#S-levels .lvl','#S-label','#scalebar',
            '#key','#rule2','#title','#desc','.leg','#summary','#foot'];
const byU=els=>els.sort((a,b)=>(+a.dataset.u)-(+b.dataset.u));
function reset(){
  runId++; running=false; document.body.classList.remove('running');
  document.getAnimations().forEach(a=>a.cancel());
  HIDE.forEach(s=>$$(s).forEach(e=>e.style.opacity=0));
  $$('.draw').forEach(e=>{e.style.strokeDasharray='1';e.style.strokeDashoffset='1'});
  $('#title').textContent='';
  $('#typed').innerHTML=''; $('#status').textContent=''; $('#status').style.opacity=0;
  const i=$('#intro'); i.style.opacity=1; i.style.display='flex';
  $('#card').style.opacity=0; $('#card').style.transform='translateY(2vh)';
}
function show(el,from,dur=600,delay=0){
  if(!el) return Promise.resolve();
  return el.animate([{opacity:0,...from},{opacity:1,transform:'none'}],{duration:dur,delay,easing:E,fill:'forwards'})
    .finished.then(()=>{el.style.opacity=1});
}
function draw(el,dur=700,delay=0){ if(!el) return; el.style.opacity=1;
  el.animate([{strokeDashoffset:1},{strokeDashoffset:0}],{duration:dur,delay,easing:E,fill:'forwards'}); }
function rise(els,total,from){ els.forEach((e,i)=>show(e,from,520,i/Math.max(1,els.length)*total)); return sleep(total+300); }
async function typeHTML(target, parts, speed, id){
  for(const [cls,txt] of parts){
    const span=document.createElement('span'); if(cls) span.className=cls; target.appendChild(span);
    for(const ch of txt){ if(id!==runId) return; span.textContent+=ch; await sleep(speed); }
  }
}
function status(t){ const s=$('#status'); s.textContent=t; s.style.opacity=1; }
function levels(id){ $$(id+' .lvl').forEach((l,i)=>{ l.style.opacity=1; draw(l.querySelector('.draw'),600,i*140);
  l.querySelectorAll('.lt').forEach(t=>show(t,{transform:'translate(-6px,0)'},450,300+i*140)); }); }
async function run(){
  if(running) return; reset(); running=true; const id=runId; document.body.classList.add('running');
  const ok=()=>id===runId;
  await sleep(500);
  await typeHTML($('#typed'),[['cmd','%%CMD%%'],[null,' '],['file','%%NAME%%']],70,id); if(!ok())return;
  await sleep(350);
  $('#card').animate([{opacity:0,transform:'translateY(2vh)'},{opacity:1,transform:'translateY(0)'}],{duration:600,easing:E,fill:'forwards'});
  await sleep(700); status('Reading plan · scaling to feet'); await sleep(1100);
  if(!ok())return; status('Projecting front · cutting section'); await sleep(1000);
  if(!ok())return;
  await $('#intro').animate([{opacity:1},{opacity:0,transform:'scale(.97)'}],{duration:500,easing:E,fill:'forwards'}).finished;
  $('#intro').style.display='none'; if(!ok())return;
  show($('#hdr'),{transform:'translate(0,-12px)'},600); await sleep(250);
  // ELEVATION
  draw($('#E-ground'),800); show($('#E-earth'),{},900); await sleep(600);
  await rise($$('#E-trees .ent'),500,{transform:'translate(0,14px)'}); if(!ok())return;
  await rise(byU($$('#E-draw .k-base')),500,{transform:'scaleY(0)'});
  await rise(byU($$('#E-draw .k-face, #E-draw .k-post')),900,{transform:'scaleY(0)'}); if(!ok())return;
  await rise(byU($$('#E-draw .k-window, #E-draw .k-door, #E-draw .k-slider')),900,{transform:'scaleY(.2)'}); if(!ok())return;
  await rise($$('#E-draw .k-roof'),200,{transform:'translate(0,-40px)'});
  await rise(byU($$('#E-draw .k-ent')),500,{transform:'scaleY(.2)'});
  levels('#E-levels'); await sleep(500);
  const ed=$('#E-dim'); ed.style.opacity=1; draw(ed.querySelector('.draw'),600);
  ed.querySelectorAll('.tk').forEach((t,i)=>show(t,{},300,400+i*60));
  await sleep(500); show($('#E-label'),{transform:'translate(-8px,0)'},500); await sleep(600);
  if(!ok())return;
  // KEY PLAN + SECTION
  show($('#key'),{},500); $$('#key .kb').forEach(e=>e.style.opacity=0); draw($('#key-cut'),800);
  await sleep(600); $$('#key .kb').forEach((e,i)=>show(e,{transform:'scale(.6)'},400,i*120)); await sleep(500);
  draw($('#S-ground'),800); show($('#S-earth'),{},900); await sleep(600);
  await rise($$('#S-trees .ent'),500,{transform:'translate(0,14px)'}); if(!ok())return;
  await rise(byU($$('#S-draw .k-beyond, #S-draw .k-bglass, #S-draw .k-bdoor, #S-draw .k-bslide')),900,{}); if(!ok())return;
  await rise(byU($$('#S-draw .p-found')),300,{transform:'scaleX(0)'});
  await rise(byU($$('#S-draw .p-slab')),250,{transform:'scaleX(0)'});
  await rise(byU($$('#S-draw .p-wall')),900,{transform:'scaleY(0)'}); if(!ok())return;
  await rise(byU($$('#S-draw .p-roof')),250,{transform:'scaleX(0)'});
  await rise(byU($$('#S-draw .k-room')),1100,{transform:'translate(0,10px)'}); if(!ok())return;
  await rise(byU($$('#S-draw .k-ent')),500,{transform:'scaleY(.2)'});
  levels('#S-levels'); await sleep(600);
  show($('#S-label'),{transform:'translate(-8px,0)'},500); show($('#scalebar'),{},600); await sleep(700);
  if(!ok())return;
  // TITLE BLOCK
  show($('#rule2'),{},400); await sleep(250);
  const tt=$('#title'); tt.style.opacity=1; for(const ch of 'Elevation + section'){ if(!ok())return; tt.textContent+=ch; await sleep(40); }
  show($('#desc'),{transform:'translate(0,6px)'},500); await sleep(350);
  $$('.leg').forEach((l,i)=>show(l,{transform:'translate(0,8px)'},500,i*140));
  await sleep(800); show($('#summary'),{},500); await sleep(300); show($('#foot'),{},600);
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
        if st.get("credit"): plan["credit"] = st["credit"]
    svg, info = render(plan, theme)
    open(args[1], "w").write(svg)
    if html_out:
        name = plan.get("input_name") or (os.path.basename(inp) if inp else "floor-plan.jpg")
        open(html_out, "w").write(animate_html(svg, theme, inp, name))
        print("wrote", html_out)
    print(f"wrote {args[1]} | scale {info['scale']:.1f} px/ft | front openings {info['n_open']} | "
          f"cut wall pieces {info['cut_walls']} | section rooms {info['rooms']}")
```