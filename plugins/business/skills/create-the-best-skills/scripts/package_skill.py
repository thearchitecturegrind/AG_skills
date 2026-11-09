#!/usr/bin/env python3
"""
Validate a skill folder and package it as an upload-ready zip.

Usage:
    python3 package_skill.py <skill_folder> [output_dir]

Output: <output_dir>/<skill-name>.zip, with the skill folder at the root of the zip
(the structure Claude's skill upload expects).

Errors stop packaging. Warnings are printed for review but do not block.
"""

import os
import re
import sys
import zipfile

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LEN = 64
MAX_DESCRIPTION_LEN = 1024

# Patterns that usually mean project-specific or secret content was left behind.
SUSPICIOUS_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "looks like an API key"),
    (re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.I),
     "looks like a hard-coded credential"),
    (re.compile(r"[A-Za-z]:\\{1,2}Users\\{1,2}[^\\\s]+", re.I), "looks like a personal Windows path"),
    (re.compile(r"/Users/[^/\s]+/"), "looks like a personal Mac path"),
    (re.compile(r"/mnt/user-data/uploads/[^\s)'\"]+"), "points at a specific uploaded file"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "contains an email address"),
]

# Files that should never ship inside a skill.
JUNK_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}
JUNK_SUFFIXES = (".pyc", ".log", ".tmp")


def fail(msg):
    print(f"ERROR: {msg}")


def warn(msg):
    print(f"WARNING: {msg}")


def parse_frontmatter(text):
    """Return (dict, body) from a SKILL.md, or (None, text) if no frontmatter."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    block = text[3:end].strip("\n")
    body = text[end + 4:]
    data = {}
    current_key = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            data[current_key] = m.group(2).strip()
        elif current_key and line.startswith((" ", "\t")):
            # Continuation of a folded multi-line value.
            data[current_key] = (data[current_key] + " " + line.strip()).strip()
    for k, v in data.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            data[k] = v[1:-1]
    return data, body


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    skill_dir = os.path.abspath(sys.argv[1].rstrip("/"))
    out_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.getcwd()
    folder_name = os.path.basename(skill_dir)
    errors = 0

    if not os.path.isdir(skill_dir):
        fail(f"'{skill_dir}' is not a folder.")
        sys.exit(1)

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        fail("SKILL.md is missing (the file name must be exactly SKILL.md).")
        sys.exit(1)

    with open(skill_md, encoding="utf-8") as f:
        text = f.read()

    fm, body = parse_frontmatter(text)
    if fm is None:
        fail("SKILL.md must start with frontmatter between two '---' lines.")
        sys.exit(1)

    # --- name ---
    name = fm.get("name", "")
    if not name:
        fail("Frontmatter is missing 'name'.")
        errors += 1
    else:
        if not NAME_PATTERN.match(name):
            fail(f"name '{name}' must be lowercase letters, numbers and single hyphens.")
            errors += 1
        if len(name) > MAX_NAME_LEN:
            fail(f"name is {len(name)} characters; keep it to {MAX_NAME_LEN} or fewer.")
            errors += 1
        if name != folder_name:
            fail(f"name '{name}' must match the folder name '{folder_name}'.")
            errors += 1

    # --- description ---
    desc = fm.get("description", "")
    if not desc:
        fail("Frontmatter is missing 'description'.")
        errors += 1
    else:
        if len(desc) > MAX_DESCRIPTION_LEN:
            fail(f"description is {len(desc)} characters; keep it to {MAX_DESCRIPTION_LEN} or fewer.")
            errors += 1
        if "<" in desc or ">" in desc:
            fail("description can't contain angle brackets (< or >).")
            errors += 1
        if len(desc) < 80:
            warn("description is very short; it may not trigger reliably. Say what it does AND when to use it.")

    if len(body.strip()) < 50:
        fail("SKILL.md has almost no instructions below the frontmatter.")
        errors += 1

    line_count = text.count("\n") + 1
    if line_count > 500:
        warn(f"SKILL.md is {line_count} lines; consider trimming (under ~500 is ideal).")

    # --- referenced files exist ---
    for ref in sorted(set(re.findall(r"\b((?:scripts|references|assets)/[\w./-]+)", text))):
        ref = ref.rstrip(".,)")
        if not os.path.exists(os.path.join(skill_dir, ref)):
            fail(f"SKILL.md references '{ref}', but that file isn't in the skill folder.")
            errors += 1

    # --- scan all files for leftovers and junk ---
    all_files = []
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in JUNK_NAMES]
        for fn in files:
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, skill_dir)
            if fn in JUNK_NAMES or fn.endswith(JUNK_SUFFIXES):
                warn(f"skipping junk file '{rel}'.")
                continue
            all_files.append((path, rel))
            if fn == "package_skill.py":
                continue  # this checker's own patterns would flag themselves
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
            except (UnicodeDecodeError, OSError):
                continue  # binary file (template, image) - not scanned
            for pattern, reason in SUSPICIOUS_PATTERNS:
                m = pattern.search(content)
                if m:
                    line_no = content[:m.start()].count("\n") + 1
                    warn(f"{rel} line {line_no} {reason}: '{m.group(0)[:60]}' - remove if project-specific.")

    if errors:
        print(f"\nNot packaged: {errors} error(s) to fix.")
        sys.exit(1)

    # --- package: folder at the zip root ---
    os.makedirs(out_dir, exist_ok=True)
    zip_path = os.path.join(out_dir, f"{folder_name}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, rel in all_files:
            zf.write(path, os.path.join(folder_name, rel))

    print(f"\nPackaged {len(all_files)} file(s) -> {zip_path}")
    for _, rel in all_files:
        print(f"  {folder_name}/{rel}")


if __name__ == "__main__":
    main()
