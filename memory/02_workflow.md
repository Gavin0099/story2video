# Tech Stack

## Repo Facts

- Python 3.13 runs the `s2v` CLI. Episode v1 JSON is the source of content and SQLite stores revision, hash, state, and audit events.
- Node 22 checks the TypeScript and Remotion scaffold under `video/`.
- GitHub Actions runs Python and TypeScript checks. The pinned AI Governance Framework submodule supports development hooks and governance checks.
- M0 uses local fixtures. Rendering and YouTube publishing belong to later milestones in `PLAN.md`.
