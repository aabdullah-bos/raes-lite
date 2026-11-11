# Decisions

Append-only. Agents may add entries with status `proposed`. Only a human sets an entry to `accepted`, or promotes it to an invariant in `AGENTS.md`. To change a decision, add a new entry that supersedes the old one; don't edit it.

L-001 to L-005 are still recorded in `README.md` until slice S-0002 moves them here.

| ID | Status | Decision | Why | Confirm or overturn when | Date |
|---|---|---|---|---|---|
| L-006 | proposed | `docs/decisions.md` is the single canonical decision log for the kit, keeping L- numbering. L-001 to L-005 move here from `README.md` in a follow-up execution slice (S-0002) | Two logs would disagree over time; the README is part of the shipped kit, so moving them is a kit change | Adopters need the kit's design decisions inside the release archive (`docs/` is export-ignored) | 2026-11-10 |
| L-007 | proposed | The scripts require Python 3.10 or later | `accept_slice.py:18` evaluates `str \| os.PathLike[str]` at module load, which fails before 3.10 | An adopter needs an older Python, or the scripts start using features from a later version | 2026-11-10 |
| L-008 | proposed | S-0000 (orientation) runs outside the scripted flow: no preflight, baseline or inspection | Preflight requires `AGENTS.md`, `docs/pipeline.md` and `docs/decisions.md`, which S-0000 creates; as a review slice it would also be blocked at inspection for writing them. Relates to L-003 | The planned `raes-discover`, or a setup skill, makes orientation scriptable | 2026-11-10 |
