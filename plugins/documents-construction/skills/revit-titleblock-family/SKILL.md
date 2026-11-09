---
name: revit-titleblock-family
description: Interview the user, then build or edit a Revit title block family (.rft/.rfa) through the pyRevit execute_code route - sheet size, border, title block strip or box, field titles, logo, text styles, line weights - preview it, save it, and hand off the few steps the Revit API cannot do (labels, revision schedule). Use whenever the user wants to create, make, rebuild, resize, restyle or fix a title block, sheet border, or sheet template in Revit, even if they only say "set up my sheet" or give a paper size like 24x36, 30x42 or A1. Also use for editing an existing title block family. Do not skip the interview - a title block built from a vague request is almost always rebuilt.
---

# Revit title block family builder

Builds a title block family from the Autodesk title block template, using the Revit connector's `execute_revit_code` tool (IronPython inside Revit). Everything the API can do is automated and visually verified. Two things the API cannot do - **Labels** and **Revision Schedules** - are handed to the user as a short manual checklist at the end.

Read `references/build-snippets.md` before writing any code. It has tested helpers and the gotchas.

## Phase 1 - Environment check (do first, silently)

1. `get_revit_status` - Revit must be running with the connector active. If not, offer `launch_revit`.
2. Via `execute_revit_code`, read `doc.Application.VersionNumber`, `doc.IsFamilyDocument`, `doc.Title`, and `doc.Application.FamilyTemplatePath`.
3. Find the title block templates: look in `<FamilyTemplatePath>\<language>\Titleblocks\` (Imperial: `English-Imperial`, Metric: `English`). Standard sizes ship as `.rft` files (A through E1, plus `New Size.rft` for anything custom). Pick the template closest to the requested sheet size; ISO sizes use the metric folder.
4. If the user wants a specific font, confirm it is installed (Windows font folders, including `%LOCALAPPDATA%\Microsoft\Windows\Fonts`). **Fonts are not embedded in an .rfa** - warn them that machines without the font will substitute another.

Ask nothing in this phase that you can discover yourself.

## Phase 2 - Interview

Ask the user for the items below. Group them into one message, mark which have defaults, and accept "use defaults". Never invent firm-specific content (names, addresses, standards) - use clearly labeled placeholders.

**Sheet**
- Sheet size and units (ARCH D 24x36, E1 30x42, ISO A1, custom...). Orientation (landscape is the norm).
- Margins / border offsets. Default: 1" binding edge on the left, 1/2" on the other three sides (metric: 25 mm / 12 mm).
- Border: single or double line; line weights.

**Title block layout**
- Where it sits: vertical strip on the right, horizontal strip along the bottom, or a box in the bottom-right corner. Width (strip) or height (bar).
- Order of sections, top to bottom (or left to right). Typical blocks: logo / firm info, consultant blocks (how many), revision table (how many rows), seal / signature box, key plan, north arrow, project info, drawn/checked, scale/date, sheet title, sheet number.
- Anything unusual: stamps ("not for construction"), phase or status box, graphic scale, issue-for block.

**Fields** - for each field the user wants, which parameter feeds it (see the mapping table below). Fields they do not specify get a generic title.

**Look**
- Font, and text heights for: field titles, section titles, firm name, sheet number, sheet title. Defaults: field titles 3/32", section titles 1/8" bold.
- Line weights (heavy border, medium section dividers, thin cell lines) and color (default all black).

**Logo**
- File type: SVG / DWG / PNG / JPG. Logo is best rebuilt as vector. See "Logo" below. Ask whether a raster logo is acceptable (it will need a manual Insert > Image step).

**Logistics**
- Revit version (you already know), save location and file name, whether to load into their open project.
- Do they have an existing title block, sample sheet or PDF to match? Ask them to share it - it removes the most guesswork.
- Firm shared-parameter file? If not, use built-in parameters and add custom ones only where needed.
- Editing an existing family instead? Get the path (or the loaded family name) and the list of changes; save as a copy (`_v2`) unless told to overwrite.

### Parameter mapping (give this to the user when they pick fields)

| Field | Label source | Notes |
|---|---|---|
| Sheet number | Sheet Number | |
| Sheet title | Sheet Name | |
| Scale | Scale | Shows "As indicated" when the sheet holds views at different scales |
| Date | Sheet Issue Date | Per sheet; Project Issue Date is per project |
| Drawn by / Checked by | Drawn By / Checked By | Sheet-level built-ins |
| Project name | Project Name | Project Information |
| Project number | Project Number | Project Information |
| Client | Client Name | Project Information |
| Address | Project Address | Project Information |
| Status / phase | Project Status | Project Information |
| Firm name | Organization Name | Project Information; or static text if it never changes |
| Consultant blocks | static text, or a custom label | Custom labels need a project/shared parameter bound to Sheets |
| Revisions | Revision Schedule element | Not a label - see manual steps |

## Phase 3 - Build

Confirm the plan back to the user in 5-8 lines (size, layout, section order and heights, fonts, anything defaulted) before building. Then:

1. **Open the template**: `doc.Application.NewFamilyDocument(<rft path>)`. This returns a family document that is *not* the UI-active one; fetch it with `[d for d in doc.Application.Documents if d.IsFamilyDocument][0]`.
2. **Inspect it** by counting categories, not by dumping elements (a template holds ~1,700 elements and the output will overflow). The template contains 4 detail lines forming the sheet-size outline - keep them.
3. **Layout math**: write down the strip/bar boundaries in inches, bottom-up, and check they sum to the usable height (or width) *before* drawing. Convert to feet (`/12`) only inside helper functions.
4. **Draw** in this order, one transaction each so a failure is easy to isolate: linework -> text styles and text notes -> logo filled regions.
5. **Preview**: export the sheet view to PNG (snippet in references), read the image, and fix what you see. Typical fixes: lines crossing a header, text too wide for its cell, color overrides from the template. Delete the preview PNG when done.
6. **Save**: `SaveAs` to the agreed path. Do not overwrite an existing file without asking.

Rules of thumb for layout:
- Field title text sits top-left of each cell, offset about 0.1" in and 0.08" down.
- Leave empty space in each cell for the label the user will place.
- Size the firm-name text so the longest line fits the strip width with margin; check in the preview.
- Heavy line = outer border and strip edge; medium = major section dividers; thin = cells.

## Logo

- **Vector rebuild (preferred, when the logo is geometric)**: read the logo image, estimate key vertices in pixel coordinates, convert to inches with one scale factor, and build each closed shape as a single `CurveLoop` of lines and 3-point arcs. Create a `FilledRegionType` with solid fill and black foreground, then `FilledRegion.Create`. Each shape needs its own closed loop; holes need a second loop inside the first. Verify in the preview and adjust vertices.
- **Raster**: the API cannot insert images into a family. Tell the user to use Insert > Image in the Family Editor and position it in the logo cell. Warn that drop shadows and off-white backgrounds in a JPG will print.
- **DWG/SVG**: DWG import is a manual Insert > Import CAD step (import as detail lines, not as a linked file). SVG is not supported by Revit - convert to DWG first.

## Phase 4 - Manual handoff (always give this checklist)

The Revit API cannot create these. Say so plainly, then list exactly what to click:

1. **Labels** - Annotate > Label, one per field cell, bound to the parameter from the mapping table. Set the label's text type to the same font/size as the title style.
2. **Revision schedule** - Annotate > Revision Schedule, placed over the drawn revision grid; set the grow direction and the number of rows.
3. **Raster logo** (only if applicable) - Insert > Image.
4. **Load and test** - Load into the Project and apply to a test sheet; check that every label fills, and the revision table grows correctly.

Offer to do the label placement through computer-use automation if the user does not want to click through it. Do not start that without being asked.

## Phase 5 - Load into the project (only after confirmation)

Loading a family into the user's project and changing title blocks on existing sheets are outward-facing changes to their model. Ask first. Then:
- Load with `doc.LoadFamily(path)` (use a load-options handler that overwrites parameter values if replacing a loaded version).
- Place or swap only on the sheets the user names; never batch-swap all sheets unprompted.
- Re-export the target sheet to PNG and check it.

## Editing an existing title block family

1. Open it (`doc.Application.OpenDocumentFile(path)`) or, if loaded in the project, `doc.EditFamily(symbol.Family)`.
2. Inventory it: detail lines (with endpoints), text notes (text, type, location), filled regions, labels (read-only - list them), images.
3. Preview it to PNG before changing anything.
4. Apply only the requested edits. Existing labels can be moved or restyled but not created.
5. `SaveAs` a copy unless told to overwrite; reload into the project only after confirmation.

## Common failure modes

- **Output too large**: dumping all elements in the template floods the response. Aggregate with a `Counter`.
- **`ElementId` ambiguity**: IronPython cannot pick a constructor for a plain int. Use `DB.ElementId(System.Int64(n))`.
- **`fd.ActiveView` is None**: the family doc is not UI-active. Get the sheet view from any template detail line's `OwnerViewId`.
- **`import System` fails silently, then `System` is undefined**: add `import System` and `from System.Collections.Generic import List` explicitly.
- **Blue or colored lines**: the template's line subcategories may carry a color; set `LineColor` on `<Wide Lines>`, `<Medium Lines>`, `<Thin Lines>`.
- **Element `.Name` raises AttributeError** for some types: use `get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()` or `getattr`.
- **Text wider than its cell**: check the preview; reduce size or shorten the title rather than overflowing.
- **Font missing**: Revit silently substitutes. Confirm installation in Phase 1.
- **Duplicate type names**: `Duplicate(name)` throws if the name exists; check or suffix.
