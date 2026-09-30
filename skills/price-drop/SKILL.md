---
name: price-drop
description: Price-drop screen on Ticker: events whose median price fell over the week while resale tickets pile up. Use when the user asks what is getting cheaper, where prices are falling, or where to buy low.
---

# Price drop

**Plan:** Free

**Usual cost:** 1 request (one screener run).

Events whose median resale price fell this week while more resale tickets came on sale. Sellers are adding supply into a softer market: a buyer's list, and a warning for anyone holding tickets.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Leaf it sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 365 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| median fall | 10% | 5 to 50% | `{"col": "ea.median_price_pct_7d", "op": "between", "val": [-90, -<median fall>]}` |
| rows | 20 | 5 to 50 | `limit` |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaves, always in the screen:

| App column | Leaf |
|---|---|
| Tickets Δ7d, growing | `{"col": "ea.tickets_delta_7d", "op": ">", "val": 0}` |
| Priced as of, within a day | `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}` |

A fall steeper than 90% in a week is a data break (a week-old median in the thousands), so the median leaf stops at -90.

## Steps

1. **Read the parameters** from the user's words ("in Boston", "over 15 percent", "next two weeks", "top 10"); keep the default for the rest. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range ("Median fall takes 5 to 50 percent.") and ask for a value inside it.
   Done when every parameter has a value inside its range.

2. **Run the screen** with `screen_events`:
   ```json
   {"predicate": {"all": [<every leaf>]},
    "sort": {"col": "ea.median_price_pct_7d", "dir": "asc"},
    "columns": ["e.event_name", "e.local_date", "v.city", "ea.median_price_current",
                "ea.median_price_pct_7d", "ea.lowest_price_current", "ea.tickets_current",
                "ea.tickets_delta_7d", "ea.last_price_snapshot_date"],
    "count": true, "diagnostics": true, "limit": <rows>}
   ```
   The server applies its own floor (at least 25 listings and a $40 median) and drops stale rows. Add no floor of your own.
   Done when the page is back.

3. **Read the counts.** `diagnostics.root.passed` is how many events match; `total` stops at 1,000, so prefer `root.passed`. `diagnostics.rows_evaluated` is how many events the screen looked at after the server's gates. If `diagnostics.status` is `unavailable` (it has a 6-second budget), call the same screen once more with `"limit": 1`, `"columns": ["e.event_name"]` and `"diagnostics": true`. If it is unavailable again, give `total` ("1,000 or more" when `countCapped` is true).
   Done when you hold the match count and the count looked at.

4. **Report.** First line, the values used (a skill of a higher plan that handed over to this one puts its plan sentence above it): "Values: city every city, category every category, days to event 0 to 365, median fall 10%, rows 20." Then one sentence names the screen in the app's words, with the values used: "Median 7d down more than 10%, Tickets Δ7d up". Then the counts ("3,804 events match, of 64,612 screened"), then a table of the rows: event (linked), date, city, Median, Median 7d, Lowest, Tickets, Tickets Δ7d. Close with the time of the numbers: the `last_price_snapshot_date` values on the rows ("priced 2026-09-28 and 2026-09-29").
   Done when every row is in the table and the answer says when its prices were read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row. Every row carries `event_id` and `event_url`; never search again to find them.
- Prices are resale list prices before fees. Tickets is resale tickets on sale, not the box office's stock.
- Name no marketplace. Never write "sold" or "tickets sold": a ticket that left the market may have been withdrawn.
- Only when the user asks for alerts on this screen, or for the primary market (the box office), say in one sentence which plan opens it: saved Views that alert start on the Pro plan, and screens that read the primary market start on the Max plan (https://findticker.com/plans). Then answer with what this screen gives. Do not offer either unasked.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "What's getting cheaper in Chicago this month, down at least 20 percent?"

One screen. Answer: "Values: city Chicago, Rosemont, Evanston, category every category, days to event 0 to 30, median fall 20%, rows 20. Median 7d down more than 20% while Tickets Δ7d went up: 41 events match, of 2,310 screened." Then the table, then "Prices read 2026-09-29."
