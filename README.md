# Ticker skills

Skills that teach an AI assistant a broker's daily work with the [Ticker](https://findticker.com) tools: screens that give a list to act on today, one-event checks, alerts, and who holds the inventory. Each skill is one folder under `skills/` with a `SKILL.md` in the open [Agent Skills](https://agentskills.io) format, so the same files work in Claude, Codex, Cursor, GitHub Copilot, Gemini CLI and the other apps that read that format.

Install all 24. Your Ticker plan decides what the tools answer, not which skills you have: a skill of a higher plan than yours tells you which plan opens it and runs the closest skill your plan has.

| Plan | Skill | What it does |
|---|---|---|
| Free | `city-under-price` | Events in one city on Ticker, in a date window, that a buyer can get into under a price, fees included |
| Free | `last-week-squeeze` | Last-week squeeze on Ticker: events in their final week where resale listings are being absorbed and the lowest price is climbing |
| Free | `numbers` | How Ticker's numbers are made: sources, read times, and what taken, absorbed and Gone mean |
| Free | `pre-purchase-check` | Pre-purchase check on one event with Ticker: price trend, cheapest sections, primary against resale |
| Free | `price-drop` | Price-drop screen on Ticker: events whose median price fell over the week while resale tickets pile up |
| Free | `sale-calendar` | On-sale and presale calendar on Ticker for one city or one act: which events go on sale or open a presale in the coming days |
| Pro | `build-view` | Build a saved View on Ticker that alerts when events enter a screen, tested on today's market, at the right cadence |
| Pro | `interest-rising` | Interest rising on Ticker: events where shopper attention grew over the week and again today |
| Pro | `momentum` | Momentum screen on Ticker: events whose weekly price move is unusual next to their peers while tickets leave faster than before |
| Pro | `todays-moves` | Today's moves on Ticker: which events entered your saved Views and which watched events fired, since a time you pick |
| Pro | `tour-dates` | Two dates of one tour side by side on Ticker: price, trend, supply and how each moves against the rest of the tour |
| Pro | `watch-event` | Watch an event on Ticker with the alert the user wants: star it, arm triggers at the right thresholds, say where alerts go |
| Max | `cooling` | Cooling events on Ticker: median price falling, resale tickets growing, the box office still holding most of the room |
| Max | `hot-events` | Hot events on Ticker: median price rising, the box office almost empty, resale tickets falling |
| Max | `primary-gone-and-rising` | Primary gone and rising on Ticker: the box office nearly empty, resale tickets falling, the lowest price climbing |
| Max | `resale-above-primary` | Resale above primary on Ticker: events where the lowest resale all-in price is far above the box office's while the box office still has tickets |
| Max | `resale-below-primary` | Resale below primary on Ticker: events where the lowest resale all-in is under the box office's lowest all-in, box office still selling |
| Max | `seat-map-moves` | Seat map moves on Ticker: which sections of one event drained or filled at the box office over the last day |
| Ultra | `hot-and-concentrated` | Hot events on Ticker checked for who holds them: the hot-events screen, then each event's seller concentration |
| Ultra | `market-sweep` | Market sweep on Ticker: the screens of the lower plans run over the whole market at once, and the events several screens flag, ranked |
| Ultra | `performer-concentration` | Seller concentration across one act's upcoming dates on Ticker: which nights a few sellers control and which are spread out |
| Ultra | `seller-moves` | Seller moves on Ticker: which sellers of one event are unloading or loading tickets, hour by hour, over a window you pick |
| Ultra | `watchlist-sellers` | Seller concentration across your watched events on Ticker: which of the events you watch a few sellers control |
| Ultra | `who-holds-the-inventory` | Who holds one event's resale inventory on Ticker: how many sellers, the largest one's share, and how that moved |

Every skill has a Parameters table at the top of its file: a city, a category, days to the event, a threshold, how many rows. Ask in plain words ("hot events in Boston, median up over 15 percent") and the skill says back the values it used. A value outside its range is refused with the range.

## Install

Every skill works through the Ticker MCP server, `https://api.findticker.com/mcp`. You sign in with your Ticker account the first time. There is no key to paste.

### Claude Code

```
claude plugin marketplace add FindTicker/ticker-skills
claude plugin install ticker@ticker
```

That installs one plugin, `ticker`: all 24 skills and the Ticker server. Start Claude Code, run `/mcp`, and sign in to Ticker. The skills show as `ticker:price-drop`, `ticker:hot-events` and so on. Inside Claude Code, `/plugin marketplace add FindTicker/ticker-skills` and `/plugin install ticker@ticker` do the same.

### Claude (claude.ai and the desktop app)

Open Customize, Plugins, Add, Add marketplace, and enter `FindTicker/ticker-skills`. Add the `ticker` plugin, then open its Connectors tab, connect Ticker and sign in. The plugin also reaches Claude Code on the same account.

### Codex, Cursor, GitHub Copilot, Gemini CLI and others

```
npx skills add FindTicker/ticker-skills
```

The [skills CLI](https://github.com/vercel-labs/skills) asks which skills to install and for which apps. Then add the Ticker MCP server in that app's MCP settings.

### ChatGPT

ChatGPT has no way to install skills. Connect the Ticker MCP server instead, and the Ticker tools work on their own: https://docs.findticker.com/docs/connect

Every app, step by step: https://docs.findticker.com/docs/skills

## For maintainers

A skill's plan lives on the `**Plan:**` line of its `SKILL.md`. `scripts/bundles.py` reads those lines:

- `python3 scripts/bundles.py marketplace` writes `.claude-plugin/marketplace.json` (one plugin, every skill); `check` fails when that file and the skill folders disagree, or when a plan README names a skill outside its plan.
- `python3 scripts/bundles.py list <plan>` prints one plan's skills, and `table` the table above.
- `python3 scripts/bundles.py build` still writes a plugin ZIP and a skills-only ZIP per plan into `dist/`, each with a README of its own plan. Nothing links to them now. The same commit builds the same bytes.

How each app takes skills, and the per-plan design this replaced, is in [`docs/distribution.md`](docs/distribution.md).

## How the skills were tested

Each skill was run end to end by a real assistant against the real Ticker tools, from one user prompt, with only these skills installed, as a test account of each plan, before it was published here.

## License

Source-available: free to install and use with a Ticker account. See [`LICENSE.md`](LICENSE.md).
