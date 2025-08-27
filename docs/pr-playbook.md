# PR & Release Playbook

We ship small, obvious changes fast. Every change carries its intent with it.

## When opening a PR
Include this header:
```
Why:
User job:
What changes:
Next best action (user):
Telemetry added/updated:
Doc impact:
```

Tag with exactly one area: `area:tools`, `area:knowledge`, or `area:blog`. Add `release-note` if user-visible.

## Content PRs (articles, posts)
State the capability, link to the tool, and include two failure modes. Add a screenshot of the hero section as rendered locally.

## Tool PRs
Prove the run path with one screenshot of inputs and one of outputs. Include the filled Idea record in the PR body for v0/v1.

## Migrations
Run locally. Dump schema diff in a comment if non-trivial. Avoid long index names; prefer `ka_stat_pub_idx`-style.

## Preview discipline
For knowledge, use `?preview=1` when verifying changes while unpublished; staff-only enforcement is in views. For blog and tools, preview via local dev server with the same assets as prod.

## Releasing
Squash-merge to `main`. Tag with `vYYYY.MM.DD-<short>`. Write a short release note that mentions any new tools, new capabilities, or significant content clusters. Link to the docs page if a new capability was introduced.

## Rollback
If revert is required, revert the merge commit and redeploy. For migrations, include a one-liner in the revert PR on how to reverse and repopulate any data.
