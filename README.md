# Architecture Grind Skills Library

Original skills for architecture workflows, organized as Claude Code plugins.

## Layout
- `.claude-plugin/marketplace.json` — the catalog Claude Code reads
- `plugins/<category>/skills/<skill>/SKILL.md` — one folder per skill
- `build_skill_zips.py` — run it to generate one upload-ready zip per skill in `dist/skills/`. The repo ships with a zip for every skill (Claude app: Settings > Skills > Upload)

## For Claude Code users (after you host this repo, e.g. on GitHub)
    claude plugin marketplace add <your-github-user>/<repo>
    claude plugin install design@architecture-grind

## Adding a skill
1. Create `plugins/<category>/skills/<name>/SKILL.md` (folder name = `name:` in frontmatter).
2. Run `python3 build_skill_zips.py` to make its upload zip.
3. Add the plugin (if new) to `.claude-plugin/marketplace.json`.

## Status
v0.2: 101 skills + 36 commands across 4 plugins (design, code-zoning, documents-construction, business).

Skills work in the Claude app (zip upload) and Claude Code. Commands (`plugins/*/commands/`) work in Claude Code only.

These are drafts. Read each against your own practice before publishing; none have been tested on real projects. Code and life-safety skills are written to use only user-supplied or officially sourced text and to state they are review aids for a licensed professional.
