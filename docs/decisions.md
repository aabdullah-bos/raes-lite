# Decisions

Agents may add entries with status `proposed`. Only a human changes a status. The statuses are:

- `proposed`: suggested, not decided. Nobody relies on it. A slice that depends on it raises a flag, the same as an open Unknown.
- `accepted`: decided. Agents follow it. Every accepted entry names what would confirm or overturn it.
- `superseded by L-xxx`: replaced by a newer entry. Agents follow the newer one.
- `promoted`: now an invariant in `AGENTS.md`. Agents follow the invariant; this row records why it exists.

The log is append-only except for the Status cell, which a human may change. To change a decision itself, add a new entry and set the old one to `superseded by` it.

L-001 to L-005 are still recorded in `README.md` until slice S-0002 moves them here.

| ID | Status | Decision | Why | Confirm or overturn when | Date |
|---|---|---|---|---|---|
| L-006 | accepted | `docs/decisions.md` is the single canonical decision log for the kit, keeping L- numbering. L-001 to L-005 move here from `README.md` in a follow-up execution slice (S-0002) | Two logs would disagree over time; the README is part of the shipped kit, so moving them is a kit change | Adopters need the kit's design decisions inside the release archive (`docs/` is export-ignored) | 2026-11-10 |
| L-007 | accepted | The scripts require Python 3.10 or later | `accept_slice.py:18` evaluates `str \| os.PathLike[str]` at module load, which fails before 3.10 | An adopter needs an older Python, or the scripts start using features from a later version | 2026-11-10 |
| L-008 | accepted | S-0000 (orientation) runs outside the scripted flow: no preflight, baseline or inspection | Preflight requires `AGENTS.md`, `docs/pipeline.md` and `docs/decisions.md`, which S-0000 creates; as a review slice it would also be blocked at inspection for writing them. Relates to L-003 | The planned `raes-discover`, or a setup skill, makes orientation scriptable | 2026-11-10 |
| L-009 | accepted | Decision statuses are `proposed`, `accepted`, `superseded by L-xxx` and `promoted`; `provisional` is dropped. Every `accepted` entry names what would confirm or overturn it. A human may change an entry's Status cell; every other cell stays append-only | A status should change what someone does. `provisional` differed from `accepted` only by a required cell, which the Confirm or overturn column already covers. Changing the Status cell lets the log show at a glance which entries need a human | A status with its own agent behavior is needed, for example decisions an agent must re-check at every slice | 2026-11-10 |
