# CLAUDE.md

@AGENTS.md

`AGENTS.md` (imported above) is the single source of truth. Keep shared guidance there, so that every agent reads the same rules.

## Notes specific to Claude Code
- This repository is the RAES Lite kit, and it is built using the kit itself. `.claude/skills/raes-slice/` is a pinned copy of the last release (see its `VERSION` file). It is the tool that checks your work. `skills/raes-slice/` is the version under development, which is the product. Never edit the pinned copy during a slice. It is refreshed only after a release, as its own change.
- To work a slice, run `/raes-slice`. To preview one without making changes, run `/raes-slice --dry-run`.
- `.claude/settings.json` (shared, committed) holds the deny rules. `.claude/settings.local.json` is personal, so don't commit it.
- To confirm `AGENTS.md` loaded, run `/memory`.
