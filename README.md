https://code.visualstudio.com/docs/copilot/customization/agent-skills

## Usage

```
npx skills add kaihendry/skills
```

To add skills from this repository to Claude Code:

```
/plugin marketplace add kaihendry/skills
```

## Available Skills

- **actions-debugger** - Debug GitHub Actions workflow failures by fetching and analysing CI/CD logs via the gh CLI
- **actions-optimiser** - Gather real-world usage context for GitHub Actions and recommend workflow improvements
- **actions-updater** - Update GitHub Actions in workflow files to their latest released versions
- **meteoblue-weather** - Get weather forecasts and meteogram images for one or more places using the Meteoblue API (requires `METEOBLUE_API_KEY`)
- **uk-highways-agency** - Check planned road closures and roadworks on England's Strategic Road Network via National Highways open data (optional: `NATIONAL_HIGHWAYS_KEY` from https://developer.data.nationalhighways.co.uk/profile for richer data)

https://github.com/anthropics/claude-code/issues/9716
