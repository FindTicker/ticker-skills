---
name: city-under-price
description: Events in one city on Ticker, in a date window, that a buyer can get into under a price, fees included. Use when the user asks what is on in a city this weekend or this month under a budget.
---

# City under a price

**Plan:** Free

**Usual cost:** 1 request (one screener run).

Every event in one city, inside a date window, whose cheapest resale ticket costs no more than the user's price with fees included. The cheapest ways in come first.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Leaf it sets |
|---|---|---|---|
| city | none: ask for one | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark; Chicago also Rosemont, Evanston) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| days to event | 0 to 30 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| price cap | $75 all-in | $10 to $1,000 | `{"col": "ea.lowest_aip_price_current", "op": "<=", "val": <price cap>}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| rows | 20 | 5 to 50 | `limit` |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaf, always in the screen: Priced as of, within a day: `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}`.

"This weekend" is counted from today: on a Monday it is days 4 to 6. Count it from the date the user gives, or ask.

## Steps

1. **Read the parameters** from the user's words ("in Austin", "under $50", "this weekend", "only comedy"); keep the default for the rest. With no city, ask for one and stop. A value outside its range: do not run; say the range ("The price cap takes $10 to $1,000.") and ask for a value inside it.
   Done when every parameter has a value inside its range.

2. **Run the screen** with `screen_events`:
   ```json
   {"predicate": {"all": [<every leaf>]},
    "sort": {"col": "ea.lowest_aip_price_current", "dir": "asc"},
    "columns": ["e.event_name", "e.local_date", "v.venue_name", "ea.lowest_aip_price_current",
                "ea.lowest_price_current", "ea.median_price_current", "ea.listings_current",
                "ea.last_price_snapshot_date"],
    "count": true, "diagnostics": true, "limit": <rows>}
   ```
   The server applies its own floor (at least 25 listings and a $40 median). Add no floor of your own.
   Done when the page is back.

3. **Read the counts.** `diagnostics.root.passed` is how many events match (`total` stops at 1,000). If `diagnostics.status` is `unavailable`, use `total`.
   Done when you hold the match count.

4. **Report.** First line, the values used (a skill of a higher plan that handed over to this one puts its plan sentence above it): "Values: city Austin, days to event 0 to 30, price cap $75 all-in, category every category, rows 20." Then the count ("131 events match"), then a table of the rows: event (linked), date, venue, Lowest all-in, Lowest before fees, Median. Close with the time of the numbers (the `last_price_snapshot_date` values).
   Done when every row is in the table and the answer says when its prices were read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- Lowest all-in is what a buyer pays at checkout with fees; say "all-in" beside it. The other prices are before fees.
- Small events with fewer than 25 listings are left out by the server's floor; say so if the user asks why a small show is missing.
- Name no marketplace. Never write "sold".
- Only when the user asks for alerts, or for the box office's own prices, say in one sentence which plan opens it: saved Views that alert start on the Pro plan, and the primary market's prices start on the Max plan (https://findticker.com/plans). Do not offer either unasked.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "What can I see in Chicago in the next two weeks for under 40 bucks?"

Values: city Chicago, Rosemont, Evanston; days to event 0 to 14; price cap $40. One screen. Answer: "Values: city Chicago, Rosemont, Evanston, days to event 0 to 14, price cap $40 all-in, category every category, rows 20. 38 events match." Then the table, cheapest first, then "Prices read 2026-09-29."
