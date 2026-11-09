# Build snippets (IronPython inside Revit, via execute_revit_code)

`doc` is the project document. `DB` is `Autodesk.Revit.DB`. Each call is a fresh namespace - re-fetch `fd` and `view` at the top of every call. No transaction is opened for you.

## Open the template and get handles

```python
import System
p = r"C:\ProgramData\Autodesk\RVT 2027\Family Templates\English-Imperial\Titleblocks\E1 - 42 x 30.rft"
fd = doc.Application.NewFamilyDocument(p)        # first call only

# every later call:
fd = [d for d in doc.Application.Documents if d.IsFamilyDocument][0]
ln0 = DB.FilteredElementCollector(fd).OfClass(DB.CurveElement).FirstElement()
view = fd.GetElement(ln0.OwnerViewId)            # the Sheet view (fd.ActiveView is None)
```

If several family documents are open, match on `d.Title` or `d.PathName` instead of taking `[0]`.

## Inventory without flooding the output

```python
from collections import Counter
cnt = Counter()
for c in DB.FilteredElementCollector(fd).WhereElementIsNotElementType().ToElements():
    cnt[(c.Category.Name if c.Category else 'None', c.GetType().Name)] += 1
for k, v in cnt.most_common(15): print(k, v)
```

## Units and helpers

Revit internal units are feet. Work in inches and convert in one place.

```python
I = lambda v: v/12.0
P = lambda x, y: DB.XYZ(I(x), I(y), 0)

cats = fd.Settings.Categories.get_Item(DB.BuiltInCategory.OST_Lines)
gs = {sc.Name: sc.GetGraphicsStyle(DB.GraphicsStyleType.Projection) for sc in cats.SubCategories}
WIDE, MED, THIN = gs['<Wide Lines>'], gs['<Medium Lines>'], gs['<Thin Lines>']

def line(x0, y0, x1, y1, style):
    d = fd.FamilyCreate.NewDetailCurve(view, DB.Line.CreateBound(P(x0, y0), P(x1, y1)))
    d.LineStyle = style
```

## Layout pattern (parametrize everything)

```python
L, R, B, T = 1.0, 41.5, 0.5, 29.5          # border: left, right, bottom, top (inches)
X0, X1 = 37.5, 41.5                         # strip left/right edges
# boundaries bottom-up; assert they sum to the usable height before drawing
rows = [("SHEET NUMBER", 2.5), ("SHEET TITLE", 3.0), ...]
y = B
for title, h in rows:
    ...                                     # draw divider at y+h, text at top-left of cell
    y += h
assert abs(y - T) < 1e-6
```

Draw the border and strip edge in WIDE, section dividers in MED, cell lines in THIN. Keep the template's 4-line sheet-size outline untouched.

## Line colors (templates can ship a colored Wide Lines)

```python
for sc in cats.SubCategories:
    if sc.Name in ('<Wide Lines>', '<Medium Lines>', '<Thin Lines>'):
        sc.LineColor = DB.Color(0, 0, 0)
```

## Text styles and text notes

```python
BP = DB.BuiltInParameter
base = [t for t in DB.FilteredElementCollector(fd).OfClass(DB.TextNoteType).ToElements()
        if t.get_Parameter(BP.SYMBOL_NAME_PARAM).AsString() == 'Text Note 1'][0]

def mk(name, size_in, bold=False, font="Arial"):
    nt = base.Duplicate(name)
    nt.get_Parameter(BP.TEXT_FONT).Set(font)
    nt.get_Parameter(BP.TEXT_SIZE).Set(I(size_in))        # paper-space height
    nt.get_Parameter(BP.TEXT_STYLE_BOLD).Set(1 if bold else 0)
    nt.get_Parameter(BP.TEXT_WIDTH_SCALE).Set(1.0)
    nt.get_Parameter(BP.TEXT_BACKGROUND).Set(1)           # transparent
    return nt

def txt(x, y, s, nt, align=DB.HorizontalTextAlignment.Left):
    o = DB.TextNoteOptions(nt.Id)
    o.HorizontalAlignment = align
    o.VerticalAlignment = DB.VerticalTextAlignment.Top    # (x, y) = top-left for Left align
    return DB.TextNote.Create(fd, view.Id, P(x, y), s, o)
```

Field title: `txt(cell_x + 0.1, cell_top - 0.08, "PROJECT NAME", label_type)`.

## Vector logo from traced points

```python
s = 2.0 / 1150.0                          # inches per source pixel (logo height / pixel height)
def Q(px, py):                            # pixel -> feet; flip Y; (cx, top) = logo placement in inches
    return DB.XYZ((cx + (px - px0) * s) / 12.0, (top - (py - py0) * s) / 12.0, 0)
def Ln(a, b):    return DB.Line.CreateBound(Q(*a), Q(*b))
def Arc(a, m, b): return DB.Arc.Create(Q(*a), Q(*b), Q(*m))   # start, END, then a point on the arc
def loop(curves):
    cl = DB.CurveLoop()
    for c in curves: cl.Append(c)         # curves must be head-to-tail and closed
    return cl

frt = DB.FilteredElementCollector(fd).OfClass(DB.FilledRegionType).FirstElement()
ft = frt.Duplicate("Solid Black")
solid = [f for f in DB.FilteredElementCollector(fd).OfClass(DB.FillPatternElement).ToElements()
         if f.GetFillPattern().IsSolidFill][0]
ft.ForegroundPatternId = solid.Id
ft.ForegroundPatternColor = DB.Color(0, 0, 0)
DB.FilledRegion.Create(fd, ft.Id, view.Id, [loop(curves)])
```

Note the argument order of `Arc.Create(start, end, midpoint)`. Make rounded corners and curves with 3-point arcs. One closed loop per solid shape; a hole is an extra loop inside it.

## Preview to PNG and look at it

```python
import os
import System
from System.Collections.Generic import List
o = DB.ImageExportOptions()
o.ExportRange = DB.ExportRange.SetOfViews
o.SetViewsAndSheets(List[DB.ElementId]([view.Id]))
o.FilePath = r"<folder>\tb_preview"
o.HLRandWFViewsFileType = DB.ImageFileType.PNG
o.ImageResolution = DB.ImageResolution.DPI_150
o.ZoomType = DB.ZoomFitType.FitToPage
o.PixelSize = 3000
fd.ExportImage(o)
print([f for f in os.listdir(r"<folder>") if 'tb_preview' in f])
```

Read the PNG with the Read tool (the filename gets the view name appended). Delete it afterward. Use `doc.ExportImage` with a sheet id the same way to preview a title block on a project sheet.

## Fixing existing geometry

Find by geometry, delete, recreate:

```python
for c in DB.FilteredElementCollector(fd).OfClass(DB.CurveElement).ToElements():
    g = c.GeometryCurve
    p0, p1 = g.GetEndPoint(0), g.GetEndPoint(1)
    if abs(p0.X*12 - 38.4) < 0.01 and abs(p0.X - p1.X) < 1e-6:     # a vertical line at x = 38.4"
        style = c.LineStyle
        fd.Delete(c.Id)
```

## Save

```python
fd.SaveAs(r"<folder>\<Name>.rfa")         # throws if the file exists and overwrite is not set
```

## Load into a project (after the user confirms)

```python
doc.LoadFamily(r"<folder>\<Name>.rfa")    # in the project document, not the family document
```

## Things that do not exist in the API (do not try to work around them)

- Creating **Label** elements (the parameter-driven text fields) in a family.
- Creating a **Revision Schedule** element in a title block.
- Inserting raster images into a family.
Hand these to the user with the checklist in SKILL.md.
