---
name: resale-vs-face
description: "Resale vs face value on Ticker: how the lowest resale price of each event compares with face value on the primary market, above or below, as price context. Use when the user asks how resale prices compare with face value."
---

# Resale vs face value

**Plan:** Max

**Usual cost:** 1 or 2 requests (screener runs): one per direction. `list_screen_columns` is free.

For each event, the lowest resale price with fees next to face value, the lowest price the primary market still lists with fees. Resale can sit above face value or below it; this skill reports either direction the same way, as context for the event's prices. The two prices can cover different seats or restrictions, and neither says what a ticket holder paid.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 365 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| direction | both | above face, below face, or both | which of the two screens run |
| above by | 50% | 10 to 400% | `{"col": "ea.resale_to_primary_aip_ratio", "op": ">=", "val": <1 + above by / 100>}` |
| below by | 0% | 0 to 80% | `{"col": "ea.resale_to_primary_aip_ratio", "op": "<", "val": <1 - below by / 100>}` |
| face value floor | $10 all-in | $5 to $200 | `{"col": "ea.tm_lowest_aip_price_current", "op": ">=", "val": <face value floor>}`; a $0 or giveaway price breaks the comparison |
| rows | 20 | 5 to 30 | `limit` of each screen |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaves, always in the screen:

| App column | Leaf |
|---|---|
| Primary tickets, more than 0 | `{"col": "ea.tm_tickets_current", "op": ">", "val": 0}` |
| Priced as of, within a day | `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}` |
| Primary read, within 2 days | `{"col": "ea.tm_asof_at", "op": ">=", "val": {"days_ago": 2}}` |

Sort: soonest event first, `{"col": "ea.days_to_event", "dir": "asc"}`. The list follows the calendar, not the size of the difference.

## Steps

1. **Check the plan** with `list_screen_columns` `{}`. The answer is long (over 200 columns); you need only the rows for `ea.resale_to_primary_aip_ratio`, `ea.tm_lowest_aip_price_current` and `ea.tm_asof_at`. If any has `locked: true`, or a later screen answers that one of them "is locked on your plan", the account's plan does not read the primary market. Start the answer with this sentence, exactly as written, and stop:
   ```text
   Resale vs face compares resale with face value on the primary market, which the Max plan opens: https://findticker.com/plans. No screen on your plan makes this comparison.
   ```
   That sentence is the whole answer: call no other tool, and show no primary number.
   Done when you know the plan reads the primary market, or you have written the sentence and stopped.

2. **Read the parameters** from the user's words ("in Chicago", "under face value", "at least double", "NBA only", "top 10"); keep the default for the rest. "Double" is above by 100%. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Run each screen** the direction asks for with `screen_events`, one call per direction, every value written out as a number (above by 50%: 1.5; below by 0%: 1):
   ```json
   {"predicate": {"all": [<the fixed leaves>, <the parameter leaves>, <the above by or the below by leaf>]},
    "sort": {"col": "ea.days_to_event", "dir": "asc"},
    "columns": ["e.event_name", "e.local_date", "v.city", "ea.lowest_aip_price_current",
                "ea.tm_lowest_aip_price_current", "ea.resale_to_primary_aip_ratio",
                "ea.tm_tickets_current", "ea.last_price_snapshot_date", "ea.tm_asof_at"],
    "count": true, "diagnostics": true, "limit": <rows>}
   ```
   Use the server's eligible results and coverage diagnostics. Add no eligibility filter of your own.
   Done when every screen the direction asks for is back.

4. **Read the counts.** For each screen, `diagnostics.root.passed` is how many events match (`total` stops at 1,000). In `diagnostics.legs`, the leg on `ea.tm_asof_at` has `passed`: how many events had a fresh face value reading, so how many the screen could look at. If `diagnostics.status` is `unavailable`, call the same screen once more with `"limit": 1`, `"columns": ["e.event_name"]` and `"diagnostics": true`. If it is unavailable again, give `total` ("1,000 or more" when `countCapped` is true) and say the coverage count was not available on this run.
   Done when you hold the match count of each screen and the coverage count.

5. **Report.** First line, the values used: "Values: city every city, category every category, days to event 0 to 365, direction both, above by 50%, below by 0%, face value floor $10, rows 20." Then one short section per direction that ran, headed "Resale above face value" or "Resale below face value". Each opens with its count ("412 events match, of 21,600 with a fresh face value reading") and holds a table in date order: event (linked), date, city, resale lowest all-in, face value all-in, resale vs face, primary tickets. Resale vs face is the ratio as a percent difference: (ratio minus 1) times 100, written "+35%" or "-20%". Close with the time of the numbers: resale priced on the `last_price_snapshot_date` values, face value read between the earliest and the latest `tm_asof_at` in the tables.
   Done when every row is in a table and the answer says when each side was read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- Both prices are all-in: the price with fees. Face value here means the lowest ticket the primary market lists, which can be a child or restricted-view ticket; the tools do not say which.
- Write the difference as a percent ("resale vs face +35%"). Do not write it as a multiple of face value, do not rank events by the size of the difference, and do not say which market is the better deal.
- Say the primary market and resale. Describe each price by market, not by source code, and do not guess provider names. Never write "sold" or "tickets sold".
- To follow these events as alerts, the `build-view` skill saves the fixed leaves, the parameter leaves and one direction leaf as a View.
- Explain a plan requirement when it blocks the task; avoid unsolicited plan recommendations.

## Example

User: "How do resale prices compare with face value for NBA games in Los Angeles?"

`list_screen_columns` shows the primary columns open; two screens, one per direction. Answer: "Values: city Los Angeles, Inglewood, Anaheim, Pasadena, category NBA, days to event 0 to 365, direction both, above by 50%, below by 0%, face value floor $10, rows 20." Then "Resale above face value: 18 events match, of 140 with a fresh face value reading", a table with rows such as "Celtics at Lakers, 2026-11-20, resale $212 all-in, face value $131.40 all-in, resale vs face +61%, 846 primary tickets", then "Resale below face value: 27 events match", its table, and the two read times.
