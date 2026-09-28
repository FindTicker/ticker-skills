---
name: ticker-performer-demand
description: Performer demand read on Ticker: rank and its trend, upcoming dates, and which cities are hot for one act or team. Use when the user asks how an artist or team is selling, whether demand is rising, or where their shows are hottest.
---

# Performer demand read

**Plan:** every plan.

Demand on Ticker is shopping pressure: people viewing listings (Interest) and recent sales pace (Sales), both rolling-window levels read from the resale market. Rank is by recent sales revenue, and a HIGHER rank number is better.

## Steps

1. **Find the performer id.** Call `search_events` `{"search": "<act or team>", "status": "active", "limit": 10}` and take `performer_id` from the rows whose act is the one asked about (a sports title reads "A at B", so check which side is the performer).
   Done when you hold one `performer_id` (`pf` plus ten characters).

2. **Read the performer** with `get_performer_analytics` `{"performer_id": "<id>", "columns": ["popularity_rank", "popularity_rank_d7", "popularity_rank_d28", "lifetime_rank", "rank_asof_date", "interest", "interest_d7", "sales", "demand_asof_date", "event_count", "avg_median_price_current", "avg_median_price_pct_7d"]}`. `x_buzz` and `prediction_markets` come back beside the row when they exist; quote a market as information about expectations, never as advice.
   Done when you hold rank, its 7- and 28-day change, and Interest, each with its as-of date.

3. **Read the rank trend** with `get_performer_rank_chart` `{"performer_id": "<id>", "range": "90d", "render": false}` (keep `render` true when the user wants a chart). Read the change across the window; null is a day unranked, not zero.
   Done when you can say climbing, falling or flat over 90 days, with the start and end values.

4. **Rank the upcoming dates** with `screen_events`:
   ```json
   {"predicate": {"all": [{"col": "p.name", "op": "contains", "val": "<act name>"}]},
    "sort": {"col": "ea.interest", "dir": "desc"},
    "columns": ["e.event_name", "e.local_date", "v.city", "v.venue_name",
                "ea.interest", "ea.interest_d7", "ea.median_price_current",
                "ea.median_price_pct_7d", "ea.days_to_event",
                "ea.demand_asof_date", "ea.last_price_snapshot_date"],
    "limit": 50}
   ```
   `p.name` is the act the row is keyed on; never filter the event title for an act. A city is hot when its dates lead on Interest AND Interest rose over 7 days (`interest_d7` above 0) or the median price rose.
   Done when you can name the three hottest cities and the next three dates.

5. **Report**: rank now and its trend, Interest now, the hot cities with the numbers that make them hot, the next dates, and any buzz or market line. Close with the links of the dates you named.
   Done when every number has its as-of date.

## Reporting rules

- Every number carries its read age: `rank_asof_date` for ranks, `demand_asof_date` for Interest and Sales, `last_price_snapshot_date` for prices.
- Interest and Sales are levels of a rolling window. Read day-over-day change as momentum; never write "X tickets sold today".
- Performer Interest is its own reading across the catalogue, not a sum of its events.
- Link dates with `event_url`. Name no marketplace.

## Example

User: "How is Zach Bryan selling right now, and where is he hottest?"

`search_events` gives `pfmwaep8e3vq`; the analytics read shows popularity rank 9053, down 299 in 7 days (as of 2026-09-27), Interest 4882 (2026-09-28); the rank chart is flat over 90 days; the screen ranks the dates by Interest. Answer leads with "Rank slipped this week but holds its 90-day level", then the cities table.
