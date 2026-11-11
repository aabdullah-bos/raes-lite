# Pipeline

<!--
Slice format (one line per slice, under "## Slice Backlog"):
  - [ ] <stable-id> | <execution|review> | <label>
IDs are stable and never reused (for example S-0001). Use lowercase [x] for accepted slices.

Optional body lines, indented two spaces under the declaration:
  - scope: the edges the agent must stay inside
  - out_of_scope: what it must not touch
  - question: (review slices) the question this slice must answer with evidence
  - experiment: a falsifiable prediction, checked at the end of the slice
  - allowed_paths: comma-separated path globs the slice may change (checked at inspection)

A review slice may run commands, read-only queries and disposable local environments.
It may change only the decision log and its allowed_paths; anything else it creates is removed or kept outside the repo.
The pipeline file itself is not edited during a slice: acceptance ticks the checkbox, and the handoff note is written afterwards.
-->

## Slice Backlog

- [x] S-0000 | review | Orientation

  - scope: read-only inspection of the repo; draft the Repo map, Done checks and Unknowns for `AGENTS.md`; propose the next 2–3 slices
  - out_of_scope: any change to tracked code, infrastructure or config; any command that writes to a cloud account
  - question: what does this repo contain, how is it validated today, and what is still unknown?
  - experiment: the agent flags at least one Unknown rather than inventing a missing contract

- [x] S-0001 | execution | Remove Write deny rules from the Claude Code settings example

  - scope: delete the `Write(...)` entries from `adapters/claude-code/settings.example.json`, since `Edit(...)` rules already cover Write and `Write(...)` rules trigger a startup warning; adjust `adapters/claude-code/README.md` only if it mentions them
  - out_of_scope: `.claude/settings.json`, the pinned skill, every other deny rule, any other adapter
  - experiment: the example stays valid JSON, it has no `Write(` entries, and every rule that remains is unchanged (the only diff lines in the example are removals)
  - allowed_paths: adapters/claude-code/**

- [ ] S-0002 | execution | Move design decisions L-001 to L-005 into docs/decisions.md

  - scope: move the L-001 to L-005 rows from the README's Design decisions table into `docs/decisions.md` with their wording unchanged and their status unchanged except that `provisional` becomes `accepted` (L-009), and replace the README table with a link to the log. Map the README columns into the log's format (`ID | Status | Decision | Why | Confirm or overturn when | Date`): Revisit when becomes Confirm or overturn when, Why is left as "—", and Date is the date the decision first appeared in git history
  - out_of_scope: changing what any decision says, any status change other than `provisional` to `accepted`, L-006 and later entries, any other README section, templates
  - experiment: every L-001 to L-005 row appears exactly once in `docs/decisions.md`, none remain in `README.md`, and the test suite still passes
  - allowed_paths: README.md, docs/decisions.md

- [ ] S-0003 | execution | Skip gitignored files in the inspect_result.py snapshot

  - scope: `_file_snapshot` in `skills/raes-slice/scripts/inspect_result.py` currently walks every file with `rglob`; make it leave out gitignored paths, with a failing test written first
  - out_of_scope: the pinned copy in `.claude/skills/`, other scripts, the JSON output schema, how tracked and untracked (not ignored) files are reported
  - experiment: a new test that creates a gitignored file (for example `__pycache__/x.pyc`) between baseline and inspect fails before the change and passes after, and all existing tests keep passing
  - allowed_paths: skills/raes-slice/**

- [ ] S-0004 | execution | Put Status second in the decisions template

  - scope: reorder the table header and the example row in `templates/decisions.template.md` to `ID | Status | Decision | Why | Confirm or overturn when | Date`
  - out_of_scope: the explanatory text above the table, `docs/decisions.md`, every other template
  - experiment: the template has the new header, the example row has the same six values in the new order, and the test suite still passes
  - allowed_paths: templates/decisions.template.md

- [ ] S-0005 | execution | Define decision statuses in the kit

  - scope: apply L-009 to the shipped kit. In `templates/decisions.template.md`, replace the text above the table with the status definitions and the Status-cell editing rule from `docs/decisions.md`, and change the example row's status from `provisional` to `accepted`. In the README's Decision rights section, replace "Decisions can be provisional" with "Any decision can be overturned: record the evidence that would confirm or overturn it, then supersede it with a new entry"
  - out_of_scope: the table header and column order (S-0004), `docs/decisions.md`, every other README section, `AGENTS.template.md`, `SKILL.md`
  - experiment: no shipped file except git history uses `provisional` as a status, the template lists exactly the four statuses in L-009, and the test suite still passes
  - allowed_paths: templates/decisions.template.md, README.md

## Handoff Notes

### S-0000

Drafted `AGENTS.md`, `docs/pipeline.md` and `docs/decisions.md` for this repo. The human approved them with edits and renamed `AGENTS.draft.md` to `AGENTS.md`. This slice ran outside the scripts (no preflight, baseline or inspection) and was ticked by hand, as L-008 describes.

- Validation: preflight on a scratch copy returned `ready` and selected S-0000 as a review slice.
- Flags raised: the `Edit(AGENTS.md)` deny rule blocked writing `AGENTS.md`, so the agent wrote a draft for the human to rename. There were two decision logs, settled by L-006.
- Proposed decisions: L-006 (one canonical decision log), L-007 (Python 3.10 or later), L-008 (S-0000 runs outside the scripted flow).
- Experiment held: the agent raised Unknowns U1 to U8 instead of inventing contracts. U4, U5, U6 and U8 are still open.
- Next recommended slice: S-0001.

### S-0001

Removed `"Write(AGENTS.md)"`, the only `Write(` entry, from `adapters/claude-code/settings.example.json`. `adapters/claude-code/README.md` doesn't mention `Write(` rules, so it is unchanged.

- Validation: the example is valid JSON with no `Write(` entries (this failed before the edit). The remaining 11 deny rules match `HEAD` exactly. The unittest suite passes (64 tests). Inspection was `validated` with `in_scope`.
- Experiment held: the JSON stays valid and has no `Write(` entries, and the rules that remain are unchanged. `Write(AGENTS.md)` was the last entry, so the diff also shows the trailing comma coming off `Edit(AGENTS.md)`; the rule itself is unchanged.
- Flags raised:
  - The first acceptance attempt was blocked with `VALIDATION_STATE_STALE`. Running the pinned scripts without `PYTHONDONTWRITEBYTECODE=1` writes `.claude/skills/raes-slice/scripts/__pycache__/`, which is gitignored, and the snapshot picks it up. Rerunning inspection and acceptance with `PYTHONDONTWRITEBYTECODE=1` worked. Inspection still listed `__pycache__/inspect_result.cpython-312.pyc` as untracked. This is the problem S-0003 fixes. Until the pinned copy is refreshed, SKILL.md could tell agents to run the scripts with `PYTHONDONTWRITEBYTECODE=1`.
  - In `docs/decisions.md`, L-006 and L-007 have the status `accept`, but L-009's status list says `accepted`. A human needs to correct the Status cells.
- Proposed decisions: none.
- Next recommended slice: S-0003. It removes the bytecode problem behind the stale-state block above.
