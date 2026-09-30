---
name: interest-rising
description: "Interest rising on Ticker: events where shopper attention grew over the week and again today. Use when the user asks what people are starting to look at before prices move."
---

# Interest rising

**Plan:** Pro

**Usual cost:** 2 requests: the plan check and one screener run.

Events where Interest, the attention an event gets from shoppers, grew over the last 7 days and grew again over the last day. Attention often shows up before the price moves.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Leaf it sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 365 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| interest rise, 7 days | 500 | 100 to 20,000 | `{"col": "ea.interest_d7", "op": ">=", "val": <interest rise, 7 days>}` |
| interest rise, 1 day | above 0 | 0 to 10,000 | `{"col": "ea.interest_d1", "op": ">", "val": <interest rise, 1 day>}` |
| rows | 20 | 5 to 50 | `limit` |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaves, always in the screen:

| App column | Leaf |
|---|---|
| Interest read, within 2 days | `{"col": "ea.demand_asof_date", "op": ">=", "val": {"days_ago": 2}}` |
| Priced as of, within a day | `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}` |

Sort: Interest Δ7d, biggest rise first: `{"col": "ea.interest_d7", "dir": "desc"}`.

## Steps

1. **Check the plan** with `list_views` `{"limit": 1}`. `views_cap` 0 means the Free plan. On Free, start the answer with this sentence, exactly as written:
   ```text
   Interest rising is a Pro skill: https://findticker.com/plans. Here is last-week squeeze, the closest skill on your plan.
   ```
   Then load the `last-week-squeeze` skill and run it with this request's city, category and rows (if it is not installed, stop here). The plan sentence stays the first line of the whole answer, above the values line of the skill you hand over to.
   Done when you know the plan is Pro or higher, or you have handed over.

2. **Read the parameters** from the user's words ("in Boston", "a price score of 3", "next two weeks", "top 10"); keep the default for the rest. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Run the screen** with `screen_events`:
   ```json
   {"predicate": {"all": [<every leaf>]},
    "sort": {"col": "ea.interest_d7", "dir": "desc"},
    "columns": ["e.event_name", "e.local_date", "v.city", "ea.interest", "ea.interest_d1",
                "ea.interest_d7", "ea.sales", "ea.median_price_current", "ea.median_price_pct_7d",
                "ea.demand_asof_date", "ea.last_price_snapshot_date"],
    "count": true, "diagnostics": true, "limit": <rows>}
   ```
   The server applies its own floor (at least 25 listings and a $40 median). Add no floor of your own.
   Done when the page is back.

4. **Read the counts.** `diagnostics.root.passed` is how many events match (`total` stops at 1,000). `diagnostics.rows_evaluated` is how many events the screen looked at. If `diagnostics.status` is `unavailable` (it has a 6-second budget), call the same screen once more with `"limit": 1`, `"columns": ["e.event_name"]` and `"diagnostics": true`. If it is unavailable again, give `total`.
   Done when you hold both counts.

5. **Report.** First line, the values used: "Values: city every city, category every category, days to event 0 to 365, interest rise 7 days 500, interest rise 1 day above 0, rows 20." Then one sentence names the screen in the app's words, with the values used: "Interest Δ7d up 500 or more, Interest Δ1d up". Then the counts, then a table of the rows: event (linked), date, city, Interest, Interest Δ1d, Interest Δ7d, Sales, Median, Median 7d. Under the table: "Interest is a rolling level of shopper attention, not a count of people today; read the change as momentum." Close with the time of the numbers (the `last_price_snapshot_date` values).
   Done when every row is in the table and the answer says when its numbers were read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- A null score means fewer than 30 peers: the row can not be ranked, and the screen leaves it out.
- Name no marketplace. Never write "sold" or "tickets sold".
- To get these events as alerts, the `build-view` skill saves this screen as a View.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Which concerts are people suddenly looking at this week?"

`list_views` shows a cap of 25. One screen. Answer: "Values: city every city, category concerts (14, 15, 17, 18, 20, 52, 74), days to event 0 to 365, interest rise 7 days 500, interest rise 1 day above 0, rows 20. Interest Δ7d up 500 or more, Interest Δ1d up: 61 events match, of 64,600 screened." Then the rows, the explanation, and "Prices read 2026-09-29."
