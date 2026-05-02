---
name: actions-updater
description: Use when the user wants to update, upgrade, or bump GitHub Actions in workflow files to their latest released versions, check for outdated actions, or run this as a Dependabot replacement for `package-ecosystem: "github-actions"`. Triggers on "update GitHub Actions", "bump actions versions", "check for action updates", "upgrade workflow actions", "find outdated actions". Only for GitHub Actions `uses:` pins — not npm, pip, or other ecosystems.
version: 0.2.0
---

# GitHub Actions Version Updater

Update GitHub Actions in workflow files to their latest released versions. Replaces Dependabot's `package-ecosystem: "github-actions"`.

## Step 1: Check for updates

Run the bundled script to parse all `uses:` lines and query each action's latest release:

```bash
uv run actions-updater/scripts/check_updates.py            # scans .github/workflows/
uv run actions-updater/scripts/check_updates.py path.yaml  # specific file(s)
```

The script parses workflow YAML, recursively extracts all `uses: owner/repo@version` entries (handles composite actions and matrix jobs), queries `gh release view --repo owner/repo` for each, and prints a comparison table. Skips local actions (`./...`) and Docker actions (`docker://...`). Requires authenticated `gh` CLI — unauthenticated calls hit a 60 req/hr GitHub limit and the script will fail noisily on rate-limited repos.

## Step 2: Update workflow files

For each action with an available update, edit the workflow file. **Pin policy, in priority order:**

1. **SHA pins (e.g. `@a1b2c3...`) — never auto-update.** Flag them and stop. SHAs are pinned for supply-chain reasons; bumping them silently defeats the purpose.
2. **Major-version pins (e.g. `@v3`) — update to the new major only** (e.g. `v4.2.1` released → write `@v4`). Don't pin to the patch version; the user opted into floating majors.
3. **Exact pins (e.g. `@v3.1.0`) — update to the full latest release tag.**

Note: some actions (e.g. `actions/checkout`) move major tags without cutting a GitHub release. The script handles that case but won't surface intermediate patches.

## Step 3: Summarise

Present a table of updates applied: action, old version, new version. Call out any SHA-pinned entries that were flagged and skipped.
