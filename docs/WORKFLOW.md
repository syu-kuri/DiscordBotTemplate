# Development Workflow

Design happens in [DESIGN.md](../DESIGN.md). This document covers how work actually gets done and shipped: branching, commits, review, and versioning.

## Roles

- **Design** (architecture, scope, config schema): Claude, recorded in `DESIGN.md`.
- **Implementation**: Codex, working from `implementation`-labeled issues that each cite a `DESIGN.md` section.
- **Review**: Claude runs `/code-review` on every PR before merge (correctness, duplication, drift from `DESIGN.md`).
- **Merge decision**: repo owner.

## Branching

- `main` is always releasable. No long-lived `develop`/`staging` branch — this project is small enough that trunk-based development is simpler.
- One short-lived branch per issue, cut from the latest `main`: `issue-<number>-<slug>`, e.g. `issue-1-config-loading`.
- Branch is deleted after merge.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`. This keeps the changelog and version bumps easy to derive from history.

## Pull Requests

1. Open a PR from the issue branch into `main`, with `Closes #<issue-number>` in the description.
2. CI (`.github/workflows/ci.yml`: `ruff check .` + `pytest`) must pass — enforced by branch protection.
3. Claude reviews with `/code-review` and reports findings; address them or explicitly note why not.
4. Squash-merge into `main` (one commit per issue, using the PR title as the commit message — keep it in Conventional Commits form).
5. Delete the branch.

`main` is protected: no direct pushes, and the CI status check must pass before merging.

## Order of Work

Following the dependency graph already recorded on issues #1–#12:

1. **Wave 1** (parallelizable, no dependencies): #1 config, #2 i18n, #3 logging, #4 embeds, #5 checks
2. **Wave 2**: #6 bot core (depends on #1, #2, #3)
3. **Wave 3** (parallelizable): #7 general, #8 moderation, #9 welcome, #10 admin, #11 error_handler (all depend on #6, plus their listed utils)
4. **Wave 4**: #12 tests (depends on #1, #2) — replaces `tests/test_smoke.py`, which exists only to keep CI green until then

## Versioning

SemVer (`vMAJOR.MINOR.PATCH`), tagged on `main` and published as a GitHub Release. `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/).

- **`0.1.0`**: all of issues #1–#12 merged — the template has the full standard feature set described in `DESIGN.md` and runs end-to-end.
- **`0.x.y`** (pre-1.0): patch releases for fixes, minor releases for small additions, while the template is still being shaken out.
- **`1.0.0`**: once the template has been used to actually stand up a server and been stable for a while — a judgment call by the repo owner, not an automatic trigger.

## Progress Tracking

All 12 MVP issues are attached to the `v0.1.0 - MVP` milestone; the milestone's progress bar is the source of truth for "how much of the MVP is done."
