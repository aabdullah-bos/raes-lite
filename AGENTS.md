# AGENTS.md

Shared guidance for every AI coding agent working in this repository. This file is the single source of truth; provider-specific files (such as `CLAUDE.md`) import it and add only notes specific to that provider.

## Intent
raes-lite is the RAES Lite kit: plain files and a skill that run RAES slices inside the agent you already use.
Current work: make the kit safe to build with itself and to release by tag, starting with the problems found while setting it up.

## Repo map
- `README.md`: direction, principles, slice contract, and (for now) design decisions L-001 to L-005.
- `bootstrap-prompt.md`: the S-0000 (orientation) prompt adopters paste into their agent.
- `templates/`: the AGENTS, pipeline and decisions templates that adopters copy.
- `skills/raes-slice/`: **the product, under development.** `SKILL.md` plus `scripts/` (`preflight.py`, `inspect_result.py`, `accept_slice.py`; Python standard library plus `git` only). `tests/` holds the unittest suite and fixtures, and is left out of releases.
- `adapters/claude-code/`: CLAUDE template, settings example, install notes. `adapters/codex/`: a placeholder (metadata plus the original Codex skill, for reference).
- `.claude/skills/raes-slice/`: **pinned copy of the last release (see its `VERSION`), the tool that checks the work.** Never edit it during a slice. It is refreshed only after a release, as its own change.
- `.claude/settings.json`: shared deny rules.
- `.gitattributes`: sets what a release archive contains. Dev files (`AGENTS.md`, `CLAUDE.md`, `docs/`, `.claude/`, skill tests) are export-ignored.
- `docs/pipeline.md`, `docs/decisions.md`: this repo's slice backlog and its single canonical decision log (see L-006).
- Releases are git tags. There is no CI in the repo.

## Done means these checks pass
- `cd skills/raes-slice && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`

## Forbidden
- No `apply`, `destroy`, `import` or state-changing commands, and no write calls to cloud APIs. Applies go through CI or a human.
- No edits to `AGENTS.md`, or to intent and invariants anywhere. Propose changes in the handoff note.
- No edits to `.claude/skills/raes-slice/` or `.claude/settings.json` during a slice.
- No creating or moving git tags, and no pushing. Releases are a human step.

## Invariants
- None yet.

## Unknowns
- **U4: CI.** None in the repo. None yet: add after the need shows up in three slices.
- **U5: Release process.** Who tags, what must pass first, and when the pinned copy is refreshed. Settled by a release checklist from the human.
- **U6: Contract consumers.** Whether the slice format, lite artifact paths, script JSON input and output, script CLI flags and release archive contents are consumed only by the owner's repos or also by outside adopters. That decides how strict version bumps must be. Settled by the human.
- **U8: Linter or formatter.** None configured. None yet: add after the need shows up in three slices.

---

## RAES working rules (all agents)

### Always
- Read `AGENTS.md`, `docs/decisions.md` and the slice entry in `docs/pipeline.md` before acting.
- Define done as runnable checks before changing anything.
- Work exactly one slice, then stop.
- Propose decisions; don't promote them. You may append proposed entries to `docs/decisions.md`.
- Never mark a slice complete without the human's explicit confirmation.

### Scope
- Treat a slice's `scope:` and `out_of_scope:` lines as hard edges.
- Before touching anything outside the declared scope, stop and flag. Don't fix things on the side.
- If a slice declares no scope, state the scope you intend in one line before you start, and flag if the work grows beyond it.

### Flag (stop and ask) when any of these is true
1. The change would alter an invariant or a contract. For infra, that includes module inputs and outputs, naming and tag schemas, and launch configuration inputs.
2. The slice depends on an open Unknown.
3. There are two or more reasonable interpretations, and the choice affects a contract, data, cost, security or user-visible behavior.
4. A plan shows a destroy or replace, or touches IAM, networking, state or shared resources.
5. The work touches an environment or account outside the slice's scope, especially production.
6. The work needs a new dependency, provider or module source.
7. Sources disagree (docs vs. code, or one doc vs. another).
8. A required validation command is missing or can't run.

A flag says what you found, the options you see, and what you need from the human. Then wait.

### Stuck (stop and report) when any of these is true
- The same check has failed after 3 fix attempts.
- Progress needs a decision or information that isn't in the artifacts.
- The environment blocks the work (credentials, access, a missing service).

When stuck, stop trying. Write a handoff note in `docs/pipeline.md` that starts with `BLOCKED:` and lists what you tried, what failed, and what you need. Leave the slice unchecked.
