---
name: tour-dates
description: "Two dates of one tour side by side on Ticker: price, trend, supply and how each moves against the rest of the tour. Use when the user asks which night of a tour to buy or sell."
---

# Two tour dates

**Plan:** Pro

**Usual cost:** 6 requests: the plan check, one search, two analytics reads, two charts.

Two dates of one act, side by side: what each costs, where each price is going, how much resale supply each has, and how each date's weekly move compares with the act's other dates. A broker picks the night to buy, or the night to list.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| act | none: ask for one | one act or team name | the `search_events` call |
| dates | the next two upcoming dates | any two upcoming dates of the act, by date or city | which two events are compared |
| history | 28 days | 7 to 90 days | the chart `range` (`7d`, `28d` or `90d`) |

## Steps

1. **Check the plan** with `list_views` `{"limit": 1}`. `views_cap` 0 means the Free plan. On Free, start the answer with this sentence, exactly as written:
   ```text
   Two tour dates is a Pro skill: https://findticker.com/plans. Here is pre-purchase check, the closest skill on your plan.
   ```
   Then load the `pre-purchase-check` skill and run it on the first of the two dates (if it is not installed, stop here). The plan sentence stays the first line of the whole answer, above the values line of the skill you hand over to.
   Done when you know the plan is Pro or higher, or you have handed over.

2. **Read the parameters** from the user's words ("Boston and Philly", "the two Chicago nights", "over 90 days"); keep the default for the rest. A value outside its range: do not run; say the range ("History takes 7 to 90 days.") and ask for a value inside it.
   Done when you hold the act, two dates or cities, and the history.

3. **Find both events** with ONE `search_events` call: `{"search": "<act name>", "status": "active", "limit": 100}`. One name only, never the act and a city together. Drop tribute acts and venues that share the name. Pick the two rows by `local_date` and city; if the user named none, take the next two dates. If two rows fit one date, ask.
   Done when you hold two `event_id`s.

4. **Read each event** with `get_event_analytics`:
   ```json
   {"event_id": "<id>", "columns": ["median_price_current", "lowest_price_current",
     "lowest_aip_price_current", "median_price_pct_7d", "tickets_current", "tickets_delta_7d",
     "days_to_event", "price_self_z_7d_xs_z_tour_tte", "data_quality_score",
     "last_price_snapshot_date"]}
   ```
   `price_self_z_7d_xs_z_tour_tte` compares this date's weekly move with the act's other dates at a similar distance; null means too few dates to compare.
   Done when both events have their headline numbers.

5. **Read each trend** with `get_event_price_chart` `{"event_id": "<id>", "range": "<7d, 28d or 90d>", "render": false}`. Take the first and the last `median_price` in `rows` for each. `days_missing` lists real gaps: never fill them.
   Done when you can say rising, falling or flat for each date, with the dates compared.

6. **Report.** First line, the values used: "Values: act <name>, dates <date, city> and <date, city>, history 28 days." Then one table, one column per date: date and venue, Median, Lowest, Lowest all-in, Median %Δ7d, trend over the history, Tickets, Tickets Δ7d, tour score, days to go, priced as of. Then two lines: which date is cheaper to get into now, and which is moving faster against the rest of the tour. End with both event links.
   Done when every number has its read date.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Prices are resale list prices before fees, except Lowest all-in. Label the all-in one.
- Tickets is resale tickets on sale. Name no marketplace. Never write "sold".
- The decision is the user's: say which way the numbers lean, not what to do.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Zach Bryan in Foxborough or in Philly, which night is the better buy?"

`list_views` shows a cap of 25; one search finds both nights; two analytics reads and two 28-day charts. Answer: "Values: act Zach Bryan, dates 2026-10-02 Foxborough and 2026-10-06 Philadelphia, history 28 days." Then the side-by-side table, then "Foxborough is $40 cheaper to get into; Philadelphia is rising faster than the rest of the tour (tour score 1.8)."
