---
name: actions-optimiser
description: Steps for creating better Github actions by gathering context on how they are used
---

# Process

## 1. Search for how an action is used:

When a Github workflow .github/workflows/* is using action in the YAML such as:

    uses: hashicorp/setup-terraform@v3

You can use the pre-installed github cli to see how it is used by other repositories:

    gh search code "setup-terraform path:.github/workflows"

## 2. Viewing search results with context

Use the pattern /repos/{owner}/{repo}/contents/{path} to look up at least five of the results in parallel. For example:

    gh api repos/Sofiane-Truman/cloud-foundation-fabric/contents/.github/workflows/linting.yml | jq -r '.content' | base64 -d | less

## 3. Check with authorative usage

Given the earlier example of hashicorp/setup-terraform@v3, the canonical source
respository is https://github.com/hashicorp/setup-terraform. Study the README.md

## 4. Plan for optimisations

How can the Github workflow be better? Assume we want to use the latest version of the actions and
try keep to the defaults, though find & explore novel yet succinct usages from Github search.
