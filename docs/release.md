# Release checklist

How a change to the kit goes from a slice to a tagged release, and then into the pinned copy that checks the next slices. This file is for developing the kit and is left out of releases.

Agents in this repo can't tag or push (see `.claude/settings.json`). The human does every step marked **(you)**.

## Versions

Tags use `vMAJOR.MINOR.PATCH`.

- **PATCH**: fixes and wording changes that don't change a contract.
- **MINOR**: additions that existing users don't have to act on, such as a new optional slice field or a new adapter.
- **MAJOR**: changes that existing users must act on. These are the contracts:
  - the slice declaration line and its body fields
  - the lite artifact paths (`AGENTS.md`, `docs/pipeline.md`, `docs/decisions.md`)
  - the scripts' JSON output and the `validation.json` they take as input
  - the scripts' command-line flags
  - what a release archive contains

How strict this needs to be depends on U6 in `AGENTS.md`: whether people outside your own repos use the kit.

## 1. Work slices (agent and you)

For each slice that goes into the release:

1. **(you)** Queue the slice in `docs/pipeline.md` on `main`. Never edit the pipeline during a slice.
2. **(you)** Create a branch:
   ```sh
   git switch main && git pull && git switch -c <slice-id>-<short-name>
   ```
3. **(agent)** Run `/raes-slice --dry-run`. Check that it picked the slice you meant, with the right scope.
4. **(agent)** Run `/raes-slice`. At the review gate, **(you)** read the diff and answer yes or no. After a yes, `accept_slice.py` ticks the slice and the agent writes the handoff note.
5. **(you)** Commit, push and open a PR. Merge it when you're satisfied.

## 2. Before tagging (you)

On an up-to-date `main`:

- [ ] Every slice meant for this release is ticked (`[x]`), and none has a handoff note starting with `BLOCKED:`.
- [ ] The done check passes:
  ```sh
  cd skills/raes-slice && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
  ```
- [ ] The working tree is clean (`git status`).
- [ ] The version number follows the rules above.
- [ ] If you want the README's install example to name the new version, update it now in its own commit.

## 3. Tag and publish (you)

```sh
git tag -a vX.Y.Z -m "<one-line summary>"
git push origin vX.Y.Z
git archive vX.Y.Z | tar -t
```

- [ ] The archive contains only the kit: `README.md`, `LICENSE`, `bootstrap-prompt.md`, `templates/`, `adapters/` and `skills/raes-slice/` without `tests/`. There should be no `AGENTS.md`, `CLAUDE.md`, `docs/` or `.claude/`. If anything is wrong, fix `.gitattributes` and tag a new PATCH version. Don't move an existing tag.
- [ ] Optional: `gh release create vX.Y.Z --notes "<what changed, which slices>"`.

## 4. Refresh the pinned copy (you, as its own change)

Until this step, slices are still checked by the previous release.

```sh
git switch main && git pull && git switch -c refresh-pinned-vX.Y.Z
T=$(mktemp -d)
git archive vX.Y.Z skills/raes-slice | tar -x -C "$T"
rm -rf .claude/skills/raes-slice
cp -R "$T/skills/raes-slice" .claude/skills/
echo vX.Y.Z > .claude/skills/raes-slice/VERSION
git add -A && git commit -m "Refresh pinned skill to vX.Y.Z"
git push -u origin HEAD
```

- [ ] With the new copy, preflight returns `ready`: `python3 .claude/skills/raes-slice/scripts/preflight.py --project-root .`
- [ ] Open a PR, review the diff (it should touch only `.claude/skills/raes-slice/`), and merge it.

Do this step yourself. The deny rules stop Claude's file-editing tools from changing `.claude/skills/`, but they don't stop shell commands such as `cp`.

## 5. Update the repos that use the kit (you, when you choose)

In each repo that has the kit installed, replace `.claude/skills/raes-slice/` from the new tag in the same way. Include the version in the commit message, so you always know which version each repo runs. Read the release notes first when the version is MINOR or MAJOR.
