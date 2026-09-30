---
name: momentum
description: Momentum screen on Ticker: events whose weekly price move is unusual next to their peers while tickets leave faster than before. Use when a broker asks what is breaking out or has momentum.
---

# Momentum

**Plan:** Pro

**Usual cost:** 2 requests: the plan check and one screener run.

Events whose price moved this week far more than events of the same kind at the same distance from the date, while resale tickets started leaving faster over the last three days than over the two weeks before. Two signals agree: price and supply.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Leaf it sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 365 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| price score | 2 | 1 to 6 | `{"col": "ea.price_self_z_7d_xs_z_subcat_tte", "op": ">=", "val": <price score>}` |
| pace score | -1 | -6 to 0 | `{"col": "ea.pace_z_3d_vs_14d_xs_z_subcat_tte", "op": "<=", "val": <pace score>}` |
| rows | 20 | 5 to 50 | `limit` |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaves, always in the screen:

| App column | Leaf |
|---|---|
| Priced as of, within a day | `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}` |

Sort: Price z (peer), highest first: `{"col": "ea.price_self_z_7d_xs_z_subcat_tte", "dir": "desc"}`.

## Steps

1. **Check the plan** with `list_views` `{"limit": 1}`. `views_cap` 0 means the Free plan. On Free, start the answer with this sentence, exactly as written:
   ```text
   Momentum is a Pro skill: https://findticker.com/plans. Here is last-week squeeze, the closest skill on your plan.
   ```
   Then load the `last-week-squeeze` skill and run it with this request's city, category and rows (if it is not installed, stop here). The plan sentence stays the first line of the whole answer, above the values line of the skill you hand over to.
   Done when you know the plan is Pro or higher, or you have handed over.

2. **Read the parameters** from the user's words ("in Boston", "a price score of 3", "next two weeks", "top 10"); keep the default for the rest. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Run the screen** with `screen_events`:
   ```json
   {"predicate": {"all": [<every leaf>]},
    "sort": {"col": "ea.price_self_z_7d_xs_z_subcat_tte", "dir": "desc"},
    "columns": ["e.event_name", "e.local_date", "v.city", "ea.median_price_current",
                "ea.median_price_pct_7d", "ea.price_self_z_7d_xs_z_subcat_tte",
                "ea.pace_z_3d_vs_14d_xs_z_subcat_tte", "ea.peer_n_subcat_tte",
                "ea.tickets_current", "ea.last_price_snapshot_date"],
    "count": true, "diagnostics": true, "limit": <rows>}
   ```
   The server applies its own floor (at least 25 listings and a $40 median). Add no floor of your own.
   Done when the page is back.

4. **Read the counts.** `diagnostics.root.passed` is how many events match (`total` stops at 1,000). `diagnostics.rows_evaluated` is how many events the screen looked at. If `diagnostics.status` is `unavailable` (it has a 6-second budget), call the same screen once more with `"limit": 1`, `"columns": ["e.event_name"]` and `"diagnostics": true`. If it is unavailable again, give `total`.
   Done when you hold both counts.

5. **Report.** First line, the values used: "Values: city every city, category every category, days to event 0 to 365, price score 2, pace score -1, rows 20." Then one sentence names the screen in the app's words, with the values used: "Price z (peer) 2 or more, Pace z (peer) -1 or less". Then the counts, then a table of the rows: event (linked), date, city, Median, Median 7d, Price z (peer), Pace z (peer), Tickets. Under the table, two lines: "Price z (peer): how unusual this week's price move is next to events of the same genre or league at the same distance from the date; 2 is unusual, and the score stops at 12." "Pace z (peer): whether tickets started leaving faster over the last 3 days than over the 2 weeks before, against the same peers; negative is faster." Close with the time of the numbers (the `last_price_snapshot_date` values).
   Done when every row is in the table and the answer says when its numbers were read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- A null score means fewer than 30 peers: the row can not be ranked, and the screen leaves it out.
- Name no marketplace. Never write "sold" or "tickets sold".
- To get these events as alerts, the `build-view` skill saves this screen as a View.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "What has real momentum in the NBA right now?"

`list_views` shows a cap of 25. One screen. Answer: "Values: city every city, category NBA, days to event 0 to 365, price score 2, pace score -1, rows 20. Price z (peer) 2 or more, Pace z (peer) -1 or less: 14 events match, of 64,600 screened." Then the rows, the explanation, and "Prices read 2026-09-29."
