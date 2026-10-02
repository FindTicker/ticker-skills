---
name: last-week-squeeze
description: "Last-week squeeze on Ticker: events in their final week where resale listings are being absorbed and the lowest price is climbing. Use for late demand, events heating up near the date, or a squeeze."
---

# Last-week squeeze

**Plan:** Free

**Usual cost:** 1 request (one screener run).

Events a week or less from the date where at least half of the resale market emptied out over the last 7 days and the cheapest ticket got dearer. Late demand is eating the supply: the get-in price is still moving up.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Leaf it sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 7 | 0 to 14 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| absorption | 0.5 | 0.2 to 0.9 | `{"col": "ea.absorption_rate_7d", "op": ">=", "val": <absorption>}` |
| lowest rise | 10% | 5 to 100% | `{"col": "ea.lowest_price_pct_7d", "op": ">", "val": <lowest rise>}` |
| rows | 20 | 5 to 50 | `limit` |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaf, always in the screen: Priced as of, within a day: `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}`.

## Steps

1. **Read the parameters** from the user's words ("in Nashville", "absorption over 0.7", "next 10 days", "top 10"); keep the default for the rest. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range ("Days to event takes 0 to 14.") and ask for a value inside it.
   Done when every parameter has a value inside its range.

2. **Run the screen** with `screen_events`:
   ```json
   {"predicate": {"all": [<every leaf>]},
    "sort": {"col": "ea.lowest_price_pct_7d", "dir": "desc"},
    "columns": ["e.event_name", "e.local_date", "v.city", "ea.days_to_event",
                "ea.lowest_price_current", "ea.lowest_price_pct_7d", "ea.median_price_current",
                "ea.absorption_rate_7d", "ea.tickets_current", "ea.last_price_snapshot_date"],
    "count": true, "diagnostics": true, "limit": <rows>}
   ```
   The server adds `absorption_data_quality` and `absorption_grain` to each row, and applies its own floor (at least 25 listings and a $40 median). Add no floor of your own.
   Done when the page is back.

3. **Read the counts.** `diagnostics.root.passed` is how many events match; `total` stops at 1,000, so prefer `root.passed`. `diagnostics.rows_evaluated` is how many events the screen looked at. If `diagnostics.status` is `unavailable` (it has a 6-second budget), call the same screen once more with `"limit": 1`, `"columns": ["e.event_name"]` and `"diagnostics": true`. If it is unavailable again, give `total`.
   Done when you hold both counts.

4. **Report.** First line, the values used (a skill of a higher plan that handed over to this one puts its plan sentence above it): "Values: city every city, category every category, days to event 0 to 7, absorption 0.5, lowest rise 10%, rows 20." Then one sentence names the screen in the app's words, with the values used: "7 days or less to go, Absorption rate 7d 0.5 or more, Lowest %Δ7d up more than 10%". Then the counts, then a table of the rows: event (linked), date, days to go, Lowest, Lowest %Δ7d, Median, Absorption rate 7d, Tickets. Under the table: "Absorbed means listings that left the resale market: a sale, a withdrawal or an expiry count the same." Close with the time of the numbers (the `last_price_snapshot_date` values).
   Done when every row is in the table and the answer says when its prices were read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- An `absorption_data_quality` under 0.5 is a weak reading: mark those rows "(weak reading)".
- Prices are resale list prices before fees. Name no marketplace. Never write "sold" or "tickets sold".
- Only when the user asks for alerts on this screen, or for the primary market (the box office), say in one sentence which plan opens it: saved Views that alert start on the Pro plan, and screens that read the primary market start on the Max plan (https://findticker.com/plans). Then answer with what this screen gives. Do not offer either unasked.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Which NFL games this week are heating up?"

One screen. Answer: "Values: city every city, category NFL, days to event 0 to 7, absorption 0.5, lowest rise 10%, rows 20. 7 days or less to go, Absorption rate 7d 0.5 or more, Lowest %Δ7d up more than 10%: 6 events match, of 64,600 screened." Then the rows, the absorption line, and "Prices read 2026-09-29."
