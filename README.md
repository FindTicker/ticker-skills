# Ticker skills

Skills that teach an AI assistant how to do real work with the [Ticker](https://findticker.com) MCP tools: find underpriced events, check an event before buying, read a seat map, set up alerts, and more. Each skill is one folder under `skills/` with a `SKILL.md` in the open [Agent Skills](https://agentskills.io) format, so the same files work in Claude, Codex, Cursor, GitHub Copilot, Gemini CLI and the other clients that read that format.

The skills are free to read and install. The Ticker tools behind them follow your plan; a skill that needs more than the Pro plan says so in its first lines.

## The skills

| Skill | What it does | Plan |
|---|---|---|
| `ticker-underpriced-events` | Screens a city, date window or category for events whose price fell harder than their peers | Every plan |
| `ticker-pre-purchase-check` | Price trend, cheapest way in by section, primary against resale, open seats for one event | Pro; Max adds the primary market's prices by section |
| `ticker-seat-map-read` | Which sections drained or filled in the last 24 hours, and where seats just opened | Pro; Max adds each section's share taken |
| `ticker-watch-event` | Stars an event and arms the alerts you asked for, at the right thresholds | Every plan |
| `ticker-build-view` | Builds a saved View that alerts on a price drop or a listing collapse, tested on today's market | Every plan |
| `ticker-performer-demand` | Rank and trend, upcoming dates and hottest cities for one act or team | Every plan |
| `ticker-sale-calendar` | Presale and on-sale calendar for an act, a venue or a city | Every plan |
| `ticker-compare-events` | Two events, or two nights of one tour, side by side | Every plan |
| `ticker-broker-end-of-day` | What moved on your watchlist, what your Views caught, what to act on | Every plan |
| `ticker-sell-through` | Share of seats taken, primary against resale, pace against days to go | Max |
| `ticker-venue-guide` | A room's capacity, section names, where the get-in price sits, what is on next | Every plan |
| `ticker-numbers` | How Ticker's numbers are made: sources, read ages, and what taken, Gone and Not seen mean | Every plan |

## Install

Every skill needs the Ticker MCP server connected: `https://api.findticker.com/mcp`. You sign in with your Ticker account the first time; there is no key to paste.

**Claude Code** installs the skills and the MCP server together:

```
/plugin marketplace add FindTicker/ticker-skills
/plugin install ticker@ticker
```

Then run `/mcp` once to sign in to Ticker. The skills appear as `ticker:ticker-...`.

**Claude (claude.ai and the desktop app).** Zip this repository and upload it under Customize, Plugins, Add, Upload plugin; then connect Ticker from the plugin's Connectors tab. To add one skill alone, zip its folder (the folder itself at the top of the zip) and upload it under Customize, Skills, and add Ticker under Settings, Connectors, Add custom connector.

**Codex, Cursor, GitHub Copilot, Gemini CLI and other clients:**

```
npx skills add FindTicker/ticker-skills
npx skills add FindTicker/ticker-skills --skill ticker-pre-purchase-check
```

Then add the Ticker MCP server in that client's own MCP settings.

## How the skills were tested

Each skill was run end to end by a real assistant against the real Ticker tools, from a single user prompt, with only these skills installed. The transcripts are in [`evidence/`](evidence/), one folder per skill, with the method and the grades in [`evidence/README.md`](evidence/README.md). How each client takes a skill, and what "installed with the MCP" means in each, is in [`docs/distribution.md`](docs/distribution.md).
