---
name: market-sweep
description: Market sweep on Ticker: the screens of the lower plans run over the whole market at once, and the events several screens flag, ranked. Use when a broker asks for the day's full market read.
---

# Market sweep

**Plan:** Ultra

**Usual cost:** 8 requests: the plan check and seven screener runs.

Seven screens at once over the whole market, and one ranked list: the events that the most screens flag. Heat screens: hot events, primary gone and rising, last-week squeeze, momentum, interest rising. Cold screens: price drop, cooling. An event that three heat screens flag is a stronger call than one that one screen flags.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities | the `v.city` leaf, added to every screen |
| category | every category | a league or genre id, or an act or team name | the category leaf, added to every screen |
| rows per screen | 25 | 10 to 50 | the `limit` of each screen |
| rows | 20 | 5 to 30 | how many ranked events the answer shows |

Each screen runs with its own skill's defaults. The thresholds live in those skills, not here.

## Steps

1. **Check the plan first**, before any other tool, with `list_views` `{"limit": 1}`. `views_cap` null means no cap: the Ultra plan. A number means a lower plan: start the answer with this sentence, exactly as written:
   ```text
   Market sweep runs seven screens in one answer, which the Ultra plan opens: https://findticker.com/plans. Here is hot events, the closest skill on your plan.
   ```
   Then load the `hot-events` skill and run it with this request's city and category (if it is not installed, stop here). The plan sentence stays the first line of the whole answer, above the values line of the skill you hand over to.
   Done when you know the plan is Ultra, or you have handed over.

2. **Read the parameters** from the user's words ("in Texas cities", "NFL only"); keep the default for the rest. A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Run the seven screens.** For each of `hot-events`, `primary-gone-and-rising`, `last-week-squeeze`, `momentum`, `interest-rising`, `price-drop` and `cooling`: load the skill, take the leaves of its Parameters and fixed tables at their defaults, add this request's city and category leaves, and call `screen_events` once with its sort, `"limit": <rows per screen>`, `"count": true` and the columns `["e.event_name", "e.local_date", "v.city", "ea.median_price_current", "ea.median_price_pct_7d", "ea.last_price_snapshot_date"]`. Skip each skill's own plan check and report step. A skill that is not installed is skipped; say which.
   Done when you hold seven pages, or fewer with the skipped ones named.

4. **Rank.** Count, for each `event_id`, how many heat screens and how many cold screens returned it. Rank by heat screens, then by Median 7d. An event on both a heat and a cold screen is mixed: list it apart.
   Done when you hold the ranked events.

5. **Report.** First line, the values used: "Values: city every city, category every category, rows per screen 25, rows 20." Then one line per screen with its match count (`total`; "1,000 or more" when `countCapped`). Then the ranked table: event (linked), date, city, Median, Median 7d, the screens that flagged it. Then the mixed events, then the top cold events. Close with the time of the numbers (the `last_price_snapshot_date` values).
   Done when the ranked table and the counts are in the answer.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- A screen's page is its top rows, not every match: say "in the top 25 of" beside each count.
- Say the primary market and resale. Name no marketplace. Never write "sold", "sold out" or "tickets sold".
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Give me the full read of the market today."

`list_views` shows no cap; seven screens. Answer: "Values: city every city, category every category, rows per screen 25, rows 20." Then the seven counts, then "Flagged by three heat screens: Steelers at Browns (hot events, primary gone and rising, last-week squeeze)." and the rest of the table.
