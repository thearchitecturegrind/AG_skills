#!/usr/bin/env python3
"""Make one upload-ready zip per skill (for Claude app > Settings > Skills > Upload).
Usage: python3 build_skill_zips.py        -> writes dist/skills/<skill>.zip
Each zip holds the skill folder at its root, which is what the uploader expects."""
import glob, os, zipfile
os.makedirs("dist/skills", exist_ok=True)
for d in sorted(glob.glob("plugins/*/skills/*/")):
    name = os.path.basename(d.rstrip("/"))
    with zipfile.ZipFile(f"dist/skills/{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(d):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.join(name, os.path.relpath(p, d)))
    print("built", name)
