# Ticker skills

Research events, compare ticket prices and monitor the ticket market with the [Ticker](https://findticker.com) tools. Use these workflows to plan a visit, compare tour dates, follow demand indicators, review pricing or track listed inventory.

Each skill is a folder with a `SKILL.md` in the [Agent Skills](https://agentskills.io) format. Install the skills you want, or all 24. The Ticker tools enforce your account's plan and permissions.

## Skills

| Plan | Skill | What it does |
|---|---|---|
| Free | `city-under-price` | Events in one city on Ticker, in a date window, that a buyer can get into under a price, fees included |
| Free | `last-week-squeeze` | Last-week squeeze on Ticker: events in their final week where resale listings are being absorbed and the lowest price is climbing |
| Free | `numbers` | Understand Ticker's readings: price bases, observation times, and what taken, absorbed and Gone mean |
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
| Ultra | `hot-and-concentrated` | Hot events on Ticker with seller concentration: the hot-events screen, then each event's seller concentration |
| Ultra | `market-sweep` | Market sweep on Ticker: the screens of the lower plans run over the whole market at once, and the events several screens flag, ranked |
| Ultra | `performer-concentration` | Seller concentration across one act's upcoming dates on Ticker: how listed inventory is distributed among sellers on each date |
| Ultra | `seller-moves` | Seller moves on Ticker: changes in resale listings attributed to each seller over a window you pick |
| Ultra | `watchlist-sellers` | Seller concentration across your watched events on Ticker: how listed inventory is distributed among sellers for the events you watch |
| Ultra | `who-holds-the-inventory` | Who holds one event's resale inventory on Ticker: how many sellers, the largest one's share, and how that moved |

Each skill lists its parameters and reports the values used. Ask in plain words, such as "concerts in Boston this month under $100 including fees" or "compare prices across these tour dates". You can change the screen's parameters within its documented ranges.

## Install

Connect the Ticker MCP server at `https://api.findticker.com/mcp` and sign in with your Ticker account. No API key is needed for this connection.

### Claude Code

```sh
claude plugin marketplace add FindTicker/ticker-skills
claude plugin install ticker@ticker
```

This installs the skills and Ticker MCP connection. Run `/mcp` to sign in. Skills appear as `ticker:price-drop`, `ticker:pre-purchase-check` and the other names above.

### Claude

Follow the [Claude setup guide](https://findticker.com/docs/mcp/claude) to connect Ticker. For plugin installation, add `FindTicker/ticker-skills` as a marketplace in your app's plugin settings where supported, then install `ticker` and connect your account.

### Codex, Cursor, GitHub Copilot, Gemini CLI and other compatible apps

```sh
npx skills add FindTicker/ticker-skills
```

Choose the skills and apps in the installer, then add the Ticker MCP server in your app's MCP settings.

### ChatGPT

Connect Ticker using the [ChatGPT setup guide](https://findticker.com/docs/mcp/chatgpt). Ticker's tools work through the connection; these skill files require a client that supports Agent Skills.

[Connection and installation guides](https://findticker.com/docs/skills) cover the supported apps.

## Reading the results

Quote the reading time and price basis alongside values. Primary and resale prices can refer to different seats or restrictions. A listing that disappeared may have sold or been withdrawn; it is not a confirmed sale. Concentration describes observed listings, not seller identity or intent.

Examples illustrate the workflow. Use the tool's current response for values, availability and plan access. Ticker helps you compare observations; it does not guarantee future prices or purchase outcomes.

## License

Source-available for use with a Ticker account. See [LICENSE.md](LICENSE.md).
