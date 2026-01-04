---
name: Github Workflow Debugger
allowed-tools: "Read,Bash(gh:*)"
description: How to fix Github's CI/CD with the gh cli
author: "Kai Hendry <hendry@iki.fi>"
license: "MIT"
---

Github worklows found in `.github/workflows/` are critical CI/CD steps to build
/ test / deploy the project and they should not fail.

Since the repository might be private, the best way to view Github managed
workflows is via the Github cli, which should be pre-installed and available as
`gh`.

# Listing latest runs

A run should start from the moment a new commit is pushed, but in practice it
can take several seconds and again you need to wait until a workflow is run to
get a complete picture (often minutes!).

    GH_PAGER=cat gh run ls

Doc: `gh run ls --help`

# Failed runs

To zoom into failed runs:

    gh run view 20383733266 --log-failed

Doc: `gh run view --help`
