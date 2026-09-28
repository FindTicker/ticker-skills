---
name: ticker-underpriced-events
description: Underpriced events on Ticker, found by screening a city, a date window or a category for prices falling against their peers. Use when the user asks for cheap, undervalued or below-peer events, or for deals this weekend.
---

# Underpriced events

**Plan:** every plan. The screener counts against the plan's monthly allowance, so run one screen and read it well.

"Below its peers" on Ticker is a MOVE, not a price level. The peer columns compare this event's 7-day price change with events of the same sub-category at a similar number of days to the event. A strongly negative peer score means the price fell harder than its peers did this week. Say that, and never "cheaper than similar events".

## Steps

1. **Pin the place and the window.** Place is a `v.city` leg (`op: "in"` over every city of a metro: New York is also Brooklyn, Flushing, Elmont, Newark), or `v.venue_name` with `contains`, or `e.sub_category_id` for a category. Window is `ea.days_to_event` with `between`, counted from today: this weekend on a Monday is `[4, 6]`.
   Done when you hold one place leg and one window leg.

2. **Run one screen** with `screen_events`:
   ```json
   {
     "predicate": {"all": [
       <place leg>, <window leg>,
       {"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}},
       {"col": "ea.data_quality_score", "op": ">=", "val": 0.5}
     ]},
     "sort": {"col": "ea.price_self_z_7d_xs_z_subcat_tte", "dir": "asc"},
     "columns": ["e.event_name", "e.local_date", "v.venue_name", "v.city",
                 "ea.median_price_current", "ea.lowest_price_current",
                 "ea.median_price_pct_7d", "ea.price_self_z_7d_xs_z_subcat_tte",
                 "ea.price_self_z_7d_pct_rank_subcat_tte", "ea.listings_current",
                 "ea.last_price_snapshot_date"],
     "limit": 20
   }
   ```
   The server already applies its economic floor (at least 25 listings and a $40 median); add no floor of your own.
   Done when the page is back. When it is empty, read `diagnostics` before you answer: `ALL_NULL` on a leg means the signal is not computed for these events (say so and offer a wider window), and a real no-match means the legs are too tight.

3. **Keep the real ones.** Keep rows whose `price_self_z_7d_xs_z_subcat_tte` is -1 or lower. A null peer score means fewer than 30 peers, so the row cannot be ranked; leave it out and say how many you left out.
   Done when you hold at most 5 rows, or you know there are none.

4. **Report** a short table: event, date, venue, median and lowest price, 7-day change, peer score, link. Under it, one line on what the peer score means (the paragraph at the top). Close with the count screened and the count kept.
   Done when every kept row is in the table with its read age and link.

## Reporting rules

- Every number carries its read age: the `last_price_snapshot_date` on the row. Write "median $142, priced 2026-09-28".
- Link each event with the `event_url` on its row. Every row already carries `event_id` and `event_url`; never search again to find them.
- Prices here are resale list prices before fees. Name no marketplace.

## Example

User: "Anything underpriced in Chicago this weekend?" (asked on a Monday)

Place leg `{"col": "v.city", "op": "=", "val": "Chicago"}`, window leg `{"col": "ea.days_to_event", "op": "between", "val": [4, 6]}`, the screen above, then a table of the rows at -1 or lower:

| Event | Date | Median | 7d | Peer score |
|---|---|---|---|---|
| [Event A](https://findticker.com/events/ev...) | Sat Oct 3 | $88 (priced 2026-09-28) | -22% | -2.1 |

"Peer score: how this week's price move compares with similar events at the same distance from the show. -2.1 means it fell much harder than its peers."
