---
name: actions-optimiser
description: Use when the user wants to optimise or review a GitHub Actions workflow file (.github/workflows/*.yml), find real-world examples of how a specific action like `hashicorp/setup-terraform` is used in other repos, or compare their workflow against community patterns. Triggers on "optimise this workflow", "how do others use <action>", "review my GitHub Actions", "find examples of <action>". Not for non-GitHub CI (CircleCI, GitLab CI, etc.).
version: 0.2.0
---

# GitHub Actions Optimiser

Mine real-world usage of a specific GitHub Action across public repos to inform optimisations to a workflow file.

## The technique

When a workflow uses an action like `uses: hashicorp/setup-terraform@v3`, search public repos for working examples and decode them in parallel:

### 1. Find candidate workflows

```bash
gh search code "setup-terraform path:.github/workflows" --limit 20
```

### 2. Pull at least 5 in parallel and decode

The contents API returns base64-encoded YAML — decode in one pipeline:

```bash
gh api repos/Sofiane-Truman/cloud-foundation-fabric/contents/.github/workflows/linting.yml \
  | jq -r '.content' | base64 -d
```

Run several of these concurrently (one per candidate repo) so a survey takes one round-trip, not five.

### 3. Identify patterns worth borrowing

Look for: non-default inputs that recur across repos, caching setups, matrix patterns, version pins, permissions blocks, conditional steps. Single-occurrence quirks are noise; patterns repeated across 3+ unrelated repos are signal.

### 4. Apply

Edit the user's workflow file to incorporate the patterns. Cite the source repo for any non-trivial change so the user can verify context.
