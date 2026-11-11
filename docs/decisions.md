# Decisions

Agents may add entries with status `proposed`. Only a human changes a status. The statuses are:

- `proposed`: suggested, not decided. Nobody relies on it. A slice that depends on it raises a flag, the same as an open Unknown.
- `accepted`: decided. Agents follow it. Every accepted entry names what would confirm or overturn it.
- `superseded by L-xxx`: replaced by a newer entry. Agents follow the newer one.
- `promoted`: now an invariant in `AGENTS.md`. Agents follow the invariant; this row records why it exists.

The log is append-only except for the Status cell, which a human may change. To change a decision itself, add a new entry and set the old one to `superseded by` it.

| ID | Status | Decision | Why | Confirm or overturn when | Date |
|---|---|---|---|---|---|
| L-001 | accepted | Slices use stable IDs: `- [ ] <id> \| <type> \| <label>`, the format the deterministic scripts already parse | — | A slice needs information the declaration line and body fields can't hold, or the scripts need a different format | 2026-11-09 |
| L-002 | accepted | Two slice types (execution, review). Review is widened to allow commands, read-only queries and disposable environments; there is no separate learning type | — | A slice first needs throwaway code (a spike) to answer its question | 2026-11-09 |
| L-003 | accepted | The orientation slice (S-0000) is how RAES is applied to an existing repo. It stands in for the planned `raes-discover` CLI | — | Orientation proves too manual to repeat across repos | 2026-11-09 |
| L-004 | accepted | The pipeline file is frozen during a slice. `accept_slice.py` ticks the checkbox, and the handoff note is written after acceptance (or after a blocked result) | — | Handoff notes written after acceptance prove unreliable | 2026-11-09 |
| L-005 | accepted | `allowed_paths` (globs the scripts check) is a separate body line from `scope` (prose for people) | — | In practice, scope and allowed_paths keep disagreeing, or a slice needs path rules that globs can't express | 2026-11-09 |
| L-006 | accepted | `docs/decisions.md` is the single canonical decision log for the kit, keeping L- numbering. L-001 to L-005 move here from `README.md` in a follow-up execution slice (S-0002) | Two logs would disagree over time; the README is part of the shipped kit, so moving them is a kit change | Adopters need the kit's design decisions inside the release archive (`docs/` is export-ignored) | 2026-11-10 |
| L-007 | accepted | The scripts require Python 3.10 or later | `accept_slice.py:18` evaluates `str \| os.PathLike[str]` at module load, which fails before 3.10 | An adopter needs an older Python, or the scripts start using features from a later version | 2026-11-10 |
| L-008 | accepted | S-0000 (orientation) runs outside the scripted flow: no preflight, baseline or inspection | Preflight requires `AGENTS.md`, `docs/pipeline.md` and `docs/decisions.md`, which S-0000 creates; as a review slice it would also be blocked at inspection for writing them. Relates to L-003 | The planned `raes-discover`, or a setup skill, makes orientation scriptable | 2026-11-10 |
| L-009 | accepted | Decision statuses are `proposed`, `accepted`, `superseded by L-xxx` and `promoted`; `provisional` is dropped. Every `accepted` entry names what would confirm or overturn it. A human may change an entry's Status cell; every other cell stays append-only | A status should change what someone does. `provisional` differed from `accepted` only by a required cell, which the Confirm or overturn column already covers. Changing the Status cell lets the log show at a glance which entries need a human | A status with its own agent behavior is needed, for example decisions an agent must re-check at every slice | 2026-11-10 |
| L-010 | proposed | In the decision log, "append-only" means no existing entry is edited or deleted, except that a human may change its Status cell. Adding new entries is always allowed | The log says "append-only" without defining it. Read literally, it could forbid adding an entry anywhere but the end, or seem to conflict with L-009's Status-cell edits | An entry needs a correction other than its status, or the log needs a way to retire an entry other than `superseded by` | 2026-11-10 |
