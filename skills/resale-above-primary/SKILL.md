---
name: resale-above-primary
description: Resale above primary on Ticker: events where the lowest resale all-in price is far above the box office's while the box office still has tickets. Use for primary-to-resale spreads, markups or flips.
---

# Resale above primary

**Plan:** Max

**Usual cost:** 3 requests (screener runs): one count, and a list of one or two pages. `list_screen_columns` is free.

Events where the cheapest resale ticket, fees included, costs more than a multiple of the cheapest ticket the primary market (the box office) still sells, fees included. The box office still has tickets, so a buyer can get in at the lower price.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Sets |
|---|---|---|---|
| city | every city | city names; a metro takes all its cities (New York is also Brooklyn, Flushing, Elmont, Newark) | `{"col": "v.city", "op": "in", "val": [<cities>]}` |
| category | every category | a league or genre id (list below), or an act or team name | `{"col": "e.sub_category_id", "op": "in", "val": [<ids>]}`, or `{"col": "p.name", "op": "contains", "val": "<name>"}` |
| days to event | 0 to 365 | 0 to 365 | `{"col": "ea.days_to_event", "op": "between", "val": [<from>, <to>]}` |
| multiple | 1.5 times | 1.2 to 5 times | the match multiplier M of the step leg |
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
  {"all": [{"col": "ea.tm_lowest_aip_price_current", "op": "<=", "val": 20},
           {"col": "ea.lowest_aip_price_current", "op": ">=", "val": <M x 20>}]},
  ... one group like this for each step, in the order above ...
]}
```

An event passes when some step S sits between its two prices: primary all-in at or under S, resale all-in at or over M times S. Every event that passes has resale at M times primary or more. Some events close to the line pass no step, so the count of the match leg is a floor: write "at least". The match leg uses the multiplier M of the parameters; the list leg uses a stricter one (the list multiplier is 2.5, or the multiple when that is larger), so the list holds the biggest gaps in one or two pages.

## Steps

1. **Check the plan** with `list_screen_columns` `{}`. The answer is long (over 200 columns); you need only the rows for `ea.tm_lowest_aip_price_current`, `ea.tm_tickets_current` and `ea.tm_asof_at`. If any has `locked: true`, or a later screen answers that one of them "is locked on your plan", the account's plan does not read the primary market. Start the answer with this sentence, exactly as written, and stop:
   ```text
   Resale above primary compares resale with the primary market, which the Max plan opens: https://findticker.com/plans. No screen on your plan makes this comparison.
   ```
   That sentence is the whole answer: call no other tool, and show no primary number.
   Done when you know the plan reads the primary market, or you have written the sentence and stopped.

2. **Read the parameters** from the user's words ("in Chicago", "at least double", "NBA only", "top 10"); keep the default for the rest. Leave out the leaf of a parameter left at "every". A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Build the two step legs**, the match leg and the list leg, one group per step, every value written out as a number (for S = 25 and M = 1.5: 37.5).
   Done when you hold both legs.

4. **Count** with `screen_events`: `{"predicate": {"all": [<the fixed leaves>, <the parameter leaves>, <match leg>]}, "count": true, "diagnostics": true, "limit": 1, "columns": ["e.event_name"]}`. `diagnostics.root.passed` is the match count (a floor). In `diagnostics.legs`, the leg on `ea.tm_asof_at` has `passed`: how many events had a fresh primary reading, so how many this screen could look at. If `diagnostics.status` is `unavailable` (it has a 6-second budget), call the same count once more. If it is unavailable again, give `total` ("1,000 or more" when `countCapped` is true) and say the coverage count was not available on this run.
   Done when you hold both counts.

5. **List** with `screen_events`: `{"predicate": {"all": [<the fixed leaves>, <the parameter leaves>, <list leg>]}, "limit": 60, "columns": ["e.event_name", "e.local_date", "ea.lowest_aip_price_current", "ea.tm_lowest_aip_price_current", "ea.tm_tickets_current", "ea.last_price_snapshot_date", "ea.tm_asof_at"]}`. If 60 rows came back, or `meta.truncated` is true, call once more with `"page": 2`. Never a third page.
   Done when you hold every row of the list leg, or two pages of it.

6. **Rank.** For each row, the gap is resale all-in divided by primary all-in (`lowest_aip_price_current` / `tm_lowest_aip_price_current`), and the dollar gap is the difference. Sort by the gap, biggest first, and keep as many as "rows".
   Done when you hold the top rows with both gaps.

7. **Report.** First line, the values used: "Values: city every city, category every category, days to event 0 to 365, multiple 1.5, primary floor $10, rows 20." Then one sentence names the screen: "Lowest all-in more than <multiple> times the primary lowest all-in, primary still has tickets". Then: "At least N events match, of C with a fresh primary reading. The list below ranks the events where resale is <list multiplier> times primary or more." Then the table: event (linked), date, resale lowest all-in, primary lowest all-in, times, dollar gap, primary tickets. Close with the time of the numbers: resale priced on the `last_price_snapshot_date` values, primary read between the earliest and the latest `tm_asof_at` in the table. Add one line on the method: "The screener can not compare two columns, so Ticker compared the prices in steps; the count is a floor."
   Done when the ranked rows are in the table and the answer says when each side was read.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Link each event with the `event_url` on its row; never search again to find it.
- Both prices are all-in: what a buyer pays with fees.
- The lowest primary price can be a child or a restricted-view ticket; the tools do not say which, so say "the lowest ticket the box office lists".
- Say the primary market and resale. Name no marketplace. Never write "sold" or "tickets sold".
- To get these events as alerts, the `build-view` skill saves the fixed leaves, the parameter leaves and the match leg as a View.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "I'm looking for spreads on NFL games: where is resale at least double the box office, fees in?"

`list_screen_columns` shows the primary columns open; one count, one or two list pages. Answer: "Values: city every city, category NFL, days to event 0 to 365, multiple 2, primary floor $10, rows 20. At least 38 events match, of 21,600 with a fresh primary reading. Ranked, where resale is 2.5 times primary or more:" then rows such as "Bills at Chiefs, resale $310 all-in against primary $96.40, 3.2 times, $214 gap, 1,204 primary tickets", then the two read times and the method line.
