---
name: actions-debugger
description: This skill should be used when the user asks to "check CI/CD logs", "view workflow run", "debug GitHub Actions failure", "fetch workflow logs", "why did my workflow fail", "check pipeline status", or shares a GitHub Actions run URL. Provides guidance for fetching and debugging GitHub Actions workflow logs via the gh CLI.
version: 0.1.0
allowed-tools: Read, Bash(gh:*)
---

# GitHub Workflow Log Debugger

GitHub workflows in `.github/workflows/` define critical CI/CD steps to build, test, and deploy the project. When they fail, diagnose issues using the `gh` CLI (pre-installed and pre-authenticated).

When an engineer shares a URL like `https://github.com/$REPO/actions/runs/$RUN_ID/job/$JOB_ID`, view the log with:

    gh run view -R $REPO --job $JOB_ID --log

## Step 1: List Latest Runs

A run starts when a new commit is pushed, but it can take several seconds to appear and minutes to complete.

    GH_PAGER=cat gh run ls

Doc: `gh run ls --help`

Wait for a workflow to complete:

    gh run watch $RUN_ID --exit-status

## Step 2: Verify Latest Commit Corresponds to the Latest Run

    gh run view $RUN_ID --json headSha -q '.headSha[:7]'

Compare with the local HEAD:

    git describe --always

If they differ, warn the user that the current change has not been pushed.

## Step 3: Debug Errors

Zoom into failed runs:

    gh run view $RUN_ID --log-failed

Doc: `gh run view --help`

## Step 4: Plan and Fix the Issue

Use AskUserQuestion for any clarifications and whether to `git push` to kick off another workflow iteration.

## Workflow Syntax Errors

Use `actionlint` to debug broken workflow YAML.
