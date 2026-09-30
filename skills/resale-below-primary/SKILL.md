---
name: resale-below-primary
description: "Resale below primary on Ticker: events where the lowest resale all-in is under the box office's lowest all-in, box office still selling. Use when resale beats face value."
---

# Resale below primary

**Plan:** Max

**Usual cost:** 3 requests (screener runs): one count, and a list of one or two pages. `list_screen_columns` is free.

Events where the cheapest resale ticket, fees included, costs less than the cheapest ticket the primary market (the box office) still sells, fees included. Resale undercuts the box office: a buyer should not pay the primary price, and a holder of primary tickets is under water.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 365 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| under by | 0% | 0 to 80% | the match multiplier M = 1 minus (under by / 100) |
| primary floor | $10 all-in | $5 to $200 | `{"col": "ea.tm_lowest_aip_price_current", "op": ">=", "val": <primary floor>}`; a $0 or giveaway primary price breaks the comparison |
| rows | 20 | 5 to 30 | how many ranked events the answer shows |

League and genre ids: NFL 1, MLB 2, NBA 3, NHL 4, NCAA football 5, NCAA basketball 6, soccer 34, MLS 87, WNBA 83, country 14, hip hop 15, pop 17, rock 18, R&B 20, Latin 52, alternative 74, comedy 11, musical 23, Broadway 64, family 10.

Fixed leaves, always in the screen:

| App column | Leaf |
|---|---|
| Primary tickets, more than 0 | `{"col": "ea.tm_tickets_current", "op": ">", "val": 0}` |
| Priced as of, within a day | `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}` |
| Primary read, within 2 days | `{"col": "ea.tm_asof_at", "op": ">=", "val": {"days_ago": 2}}` |

Price steps, in dollars: 20, 25, 30, 40, 50, 60, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 750, 1000, 1250, 1500, 2000, 2500, 3000.

**Why steps.** The screener compares a column with a number, never with a second column. So this skill compares Lowest all-in with the primary lowest all-in in steps. The step leg for a multiplier M is an `any` with one group per step S:

```json
{"any": [
  {"all": [{"col": "ea.tm_lowest_aip_price_current", "op": ">=", "val": 20},
           {"col": "ea.lowest_aip_price_current", "op": "<", "val": <M x 20>}]},
  ... one group like this for each step, in the order above ...
]}
```

An event passes when some step S sits between its two prices: primary all-in at or over S, resale all-in under M times S. Every event that passes has resale under M times primary. Some events close to the line pass no step, so the count of the match leg is a floor: write "at least". The match leg uses the multiplier M of the parameters; the list leg uses a stricter one (the list multiplier is 0.3, or M when that is smaller), so the list holds the biggest gaps in one or two pages.

## Steps

1. **Check the plan** with `list_screen_columns` `{}`. The answer is long (over 200 columns); you need only the rows for `ea.tm_lowest_aip_price_current`, `ea.tm_tickets_current` and `ea.tm_asof_at`. If any has `locked: true`, or a later screen answers that one of them "is locked on your plan", the account's plan does not read the primary market. Start the answer with this sentence, exactly as written, and stop:
   ```text
   Resale below primary compares resale with the primary market, which the Max plan opens: https://findticker.com/plans. No screen on your plan makes this comparison.
   ```
   That sentence is the whole answer: call no other tool, and show no primary number.
   Done when you know the plan reads the primary market, or you have written the sentence and stopped.

2. **Read the parameters** from the user's words ("in Chicago", "at least double", "NBA only", "top 10"); keep the default for the rest. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Build the two step legs**, the match leg and the list leg, one group per step, every value written out as a number (for S = 25 and M = 1: 25; for M = 0.3: 7.5).
   Done when you hold both legs.

4. **Count** with `screen_events`: `{"predicate": {"all": [<the fixed leaves>, <the parameter leaves>, <match leg>]}, "count": true, "diagnostics": true, "limit": 1, "columns": ["e.event_name"]}`. `diagnostics.root.passed` is the match count (a floor). In `diagnostics.legs`, the leg on `ea.tm_asof_at` has `passed`: how many events had a fresh primary reading, so how many this screen could look at. If `diagnostics.status` is `unavailable` (it has a 6-second budget), call the same count once more. If it is unavailable again, give `total` ("1,000 or more" when `countCapped` is true) and say the coverage count was not available on this run.
   Done when you hold both counts.

5. **List** with `screen_events`: `{"predicate": {"all": [<the fixed leaves>, <the parameter leaves>, <list leg>]}, "limit": 60, "columns": ["e.event_name", "e.local_date", "ea.lowest_aip_price_current", "ea.tm_lowest_aip_price_current", "ea.tm_tickets_current", "ea.last_price_snapshot_date", "ea.tm_asof_at"]}`. If 60 rows came back, or `meta.truncated` is true, call once more with `"page": 2`. Never a third page.
   Done when you hold every row of the list leg, or two pages of it.

6. **Rank.** For each row, the gap is how far resale sits under primary: 1 minus resale all-in divided by primary all-in, as a percent, and the dollar gap is the difference. Sort by the gap, biggest first, and keep as many as "rows".
   Done when you hold the top rows with both gaps.

7. **Report.** First line, the values used: "Values: city every city, category every category, days to event 0 to 365, under by 0%, primary floor $10, rows 20." Then one sentence names the screen: "Lowest all-in under the primary lowest all-in by <under by> or more, primary still has tickets". Then: "At least N events match, of C with a fresh primary reading. The list below ranks the events where resale is under <list multiplier x 100>% of primary." Then the table: event (linked), date, resale lowest all-in, primary lowest all-in, percent under, dollar gap, primary tickets. Close with the time of the numbers: resale priced on the `last_price_snapshot_date` values, primary read between the earliest and the latest `tm_asof_at` in the table. Add one line on the method: "The screener can not compare two columns, so Ticker compared the prices in steps; the count is a floor."
   Done when the ranked rows are in the table and the answer says when each side was read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- Both prices are all-in: what a buyer pays with fees.
- A high lowest primary price often means the box office has only its dearest seats left; say "the lowest ticket the box office lists".
- Say the primary market and resale. Name no marketplace. Never write "sold" or "tickets sold".
- To get these events as alerts, the `build-view` skill saves the fixed leaves, the parameter leaves and the match leg as a View.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Where is resale cheaper than the box office in Los Angeles?"

`list_screen_columns` shows the primary columns open; one count, one or two list pages. Answer: "Values: city Los Angeles, Inglewood, Anaheim, Pasadena, category every category, days to event 0 to 365, under by 0%, primary floor $10, rows 20. At least 214 events match, of 1,480 with a fresh primary reading. Ranked, where resale is under 30% of primary:" then rows such as "Usher and Chris Brown, resale $48 all-in against primary $307.53, 84% under, $260 gap, 251 primary tickets", then the two read times and the method line.
