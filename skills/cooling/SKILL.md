---
name: cooling
description: "Cooling events on Ticker: median price falling, resale tickets growing, the box office still holding most of the room. Use when the user asks what is cooling off or which on-sales are soft."
---

# Cooling

**Plan:** Max

**Usual cost:** 1 request (one screener run). `list_screen_columns` is free.

Events where the median resale price fell this week, more resale tickets came on sale, and the primary market (the box office) still has more than half the room to sell. Supply is ahead of demand on both sides: a list of events to stay out of, or to buy late.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Leaf it sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 365 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| median fall | 10% | 5 to 50% | `{"col": "ea.median_price_pct_7d", "op": "between", "val": [-90, -<median fall>]}` |
| primary remaining over | 50% | 20 to 90% | `{"col": "ea.tm_percent_remaining", "op": "between", "val": [<primary remaining over>, 100]}` |
| rows | 20 | 5 to 50 | `limit` |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaves, always in the screen:

| App column | Leaf |
|---|---|
| Tickets Δ7d, growing | `{"col": "ea.tickets_delta_7d", "op": ">", "val": 0}` |
| Priced as of, within a day | `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}` |
| Primary read, within 2 days | `{"col": "ea.tm_asof_at", "op": ">=", "val": {"days_ago": 2}}` |

Sort: Median 7d, steepest fall first: `{"col": "ea.median_price_pct_7d", "dir": "asc"}`.

## Steps

1. **Check the plan** with `list_screen_columns` `{}`. The answer is long (over 200 columns); you need only the rows for `ea.tm_percent_remaining` and `ea.tm_asof_at`. If either has `locked: true`, or a later screen answers that one of them "is locked on your plan", the account's plan does not read the primary market. Start the answer with this sentence, exactly as written:
   ```text
   Cooling reads the primary market, which the Max plan opens: https://findticker.com/plans. Here is price drop, the closest screen on your plan.
   ```
   Then load the `price-drop` skill and run it with this request's city, category, days to event and rows (if it is not installed, stop here). The plan sentence stays the first line of the whole answer, above the values line of the skill you hand over to. Show no primary number: never guess one and never take one from the web.
   Done when you know the plan reads the primary market, or you have handed over to `price-drop`.

2. **Read the parameters** from the user's words ("in Boston", "over 15 percent", "next two weeks", "top 10"); keep the default for the rest. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Run the screen** with `screen_events`:
   ```json
   {"predicate": {"all": [<every leaf>]},
    "sort": {"col": "ea.median_price_pct_7d", "dir": "asc"},
    "columns": ["e.event_name", "e.local_date", "v.city", "ea.median_price_current",
                "ea.median_price_pct_7d", "ea.lowest_price_current", "ea.tm_percent_remaining",
                "ea.tickets_current", "ea.tickets_delta_7d", "ea.last_price_snapshot_date",
                "ea.tm_asof_at"],
    "count": true, "diagnostics": true, "limit": <rows>}
   ```
   The server applies its own floor (at least 25 listings and a $40 median). Add no floor of your own.
   Done when the page is back.

4. **Read the counts.** `diagnostics.root.passed` is how many events match (`total` stops at 1,000). In `diagnostics.legs`, the leg on `ea.tm_asof_at` has `passed`: how many events had a fresh primary reading, so how many this screen could look at. Primary data covers only part of the events; say so with that number. If `diagnostics.status` is `unavailable` (it has a 6-second budget), call the same screen once more with `"limit": 1`, `"columns": ["e.event_name"]` and `"diagnostics": true`. If it is unavailable again, give `total` ("1,000 or more" when `countCapped` is true) and say the coverage count was not available on this run.
   Done when you hold the match count and the primary coverage count.

5. **Report.** First line, the values used: "Values: city every city, category every category, days to event 0 to 365, median fall 10%, primary remaining over 50%, rows 20." Then one sentence names the screen in the app's words, with the values used: "Median 7d down more than 10%, Tickets Δ7d up, Primary remaining over 50%". Then the counts ("230 events match, of 21,645 with a fresh primary reading"), then a table of the rows: event (linked), date, city, Median, Median 7d, Lowest, Primary remaining, Tickets, Tickets Δ7d. Close with the time of the numbers: resale priced on the `last_price_snapshot_date` values, primary read between the earliest and the latest `tm_asof_at` on the page.
   Done when every row is in the table and the answer says when each side was read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- Say the primary market and resale. Name no marketplace.
- A fall steeper than 90% in a week is a data break, and Primary remaining above 100 is a wrong capacity figure: the leaves leave both out.
- Never write "sold", "unsold" or "tickets sold": say "Primary remaining 64%".
- To get these events as alerts, the `build-view` skill saves this screen as a View.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Which concerts are going soft, with the box office still over 60 percent full of tickets?"

`list_screen_columns` shows the primary columns open. One screen. Answer: "Values: city every city, category concerts (14, 15, 17, 18, 20, 52, 74), days to event 0 to 365, median fall 10%, primary remaining over 60%, rows 20. Median 7d down more than 10%, Tickets Δ7d up, Primary remaining over 60%: 58 events match, of 21,600 with a fresh primary reading." Then the rows, then "Resale priced 2026-09-29; primary read 2026-09-28 06:10 to 2026-09-29 21:40 UTC."
