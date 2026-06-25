# Project rules for Claude Code

## Commits

After completing a coherent unit of work (a feature, fix, or refactor) and
verifying it works (smoke test or test run passes), commit the changes
without asking. Use a clear conventional commit message — what changed and
why. Do not ask "want me to commit?" — just commit.

This does **not** authorize pushing to remote. Always ask before `git push`.

This does **not** authorize destructive operations (force push, branch
deletion, history rewrites). Always ask first.

Stage with explicit file paths (`git add <files>`) or `git add -A` after
reviewing `git status` — do not blindly run `git add .`.

## Logs / debug output

Local mirror files (`punchlist/wp-*.md`) and `data/` caches are gitignored
intentionally — don't commit them or suggest tracking them.
