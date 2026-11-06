# Ticker skills

Research events, follow ticket prices and demand, and read the resale market with the [Ticker](https://findticker.com) tools: price trends, tour dates side by side, resale vs face value, demand signals and listed inventory.

Each skill is a folder with a `SKILL.md` in the [Agent Skills](https://agentskills.io) format. Install the skills you want, or all 23. The Ticker tools enforce your account's plan and permissions.

## Skills

| Plan | Skill | What it does |
|---|---|---|
| Free | `city-under-price` | Events in one city on Ticker, in a date window, with a lowest resale price at or under a set price, fees included |
| Free | `event-check` | Event check on Ticker: one event's price trend, its sections and the market around it, with resale vs face value on Max |
| Free | `final-week-demand` | Final-week demand on Ticker: events in their last week where resale listings are being absorbed and the lowest price is rising |
| Free | `numbers` | Understand Ticker's readings: price bases, observation times, and what taken, absorbed and Gone mean |
| Free | `price-drop` | Price-drop screen on Ticker: events whose median price fell over the week while resale tickets pile up |
| Free | `sale-calendar` | On-sale and presale calendar on Ticker for one city or one act: the upcoming on-sale and presale dates in the coming days |
| Pro | `build-view` | Build a saved View on Ticker that alerts when events enter a screen, tested on today's market, at the right cadence |
| Pro | `interest-rising` | Interest rising on Ticker: events where shopper attention grew over the week and again today |
| Pro | `momentum` | Momentum screen on Ticker: events whose weekly price move is unusual next to their peers while tickets leave faster than before |
| Pro | `todays-moves` | Today's moves on Ticker: which events entered your saved Views and which watched events fired, since a time you pick |
| Pro | `tour-dates` | Two dates of one tour side by side on Ticker: price, trend, supply and how each moves against the rest of the tour |
| Pro | `watch-event` | Watch an event on Ticker with the alert the user wants: star it, arm triggers at the right thresholds, say where alerts go |
| Max | `cooling` | Cooling events on Ticker: median price falling, resale tickets growing, the primary market still holding most of the room |
| Max | `hot-events` | Hot events on Ticker: median price rising, little left on the primary market, resale tickets falling |
| Max | `resale-vs-face` | Resale vs face value on Ticker: how the lowest resale price of each event compares with face value on the primary market, above or below, as price context |
| Max | `seat-map-moves` | Seat map moves on Ticker: primary seats taken by section for one event, and how that changed over the last day |
| Max | `sold-through-and-rising` | Sold through and rising on Ticker: late demand, where the primary market has little left, resale listings are shrinking and the lowest resale price is climbing |
| Ultra | `hot-and-concentrated` | Hot events on Ticker with seller concentration: the hot-events screen, then each event's seller concentration |
| Ultra | `market-sweep` | Market sweep on Ticker: the screens of the lower plans run over the whole market at once, and the events several screens flag, ranked |
| Ultra | `performer-concentration` | Seller concentration across one act's upcoming dates on Ticker: how listed inventory is distributed among sellers on each date |
| Ultra | `seller-concentration` | Seller concentration for one event on Ticker: how much of its resale inventory the largest sellers hold, shown anonymously, and how that moved |
| Ultra | `seller-moves` | Seller moves on Ticker: changes in resale listings attributed to each seller over a window you pick |
| Ultra | `watchlist-sellers` | Seller concentration across your watched events on Ticker: how listed inventory is distributed among sellers for the events you watch |

### Renamed skills

Six skills have new names. The old names still work for existing installs and saved commands: each one is a short alias that runs the new skill, and your assistant will not pick an alias on its own.

| Old name | New name |
|---|---|
| `pre-purchase-check` | `event-check` |
| `last-week-squeeze` | `final-week-demand` |
| `primary-gone-and-rising` | `sold-through-and-rising` |
| `resale-above-primary` | `resale-vs-face` |
| `resale-below-primary` | `resale-vs-face` |
| `who-holds-the-inventory` | `seller-concentration` |

Each skill lists its parameters and reports the values used. Ask in plain words, such as "concerts in Boston this month under $100 including fees" or "compare prices across these tour dates". You can change the screen's parameters within its documented ranges.

## Install

Connect the Ticker MCP server at `https://api.findticker.com/mcp` and sign in with your Ticker account. No API key is needed for this connection.

### Claude Code

```sh
claude plugin marketplace add FindTicker/ticker-skills
claude plugin install ticker@ticker
```

This installs the skills and Ticker MCP connection. Run `/mcp` to sign in. Skills appear as `ticker:price-drop`, `ticker:event-check` and the other names above.

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

Examples illustrate the workflow. Use the tool's current response for values, availability and plan access. Ticker reports observed prices and listings; it does not predict future prices.

## License

Source-available for use with a Ticker account. See [LICENSE.md](LICENSE.md).
