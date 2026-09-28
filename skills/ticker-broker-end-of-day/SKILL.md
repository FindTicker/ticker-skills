---
name: ticker-broker-end-of-day
description: End-of-day review on Ticker of the user's own watchlist and saved Views: what moved, what matched, and what to act on. Use when the user asks for a daily recap, what happened today, or what needs attention on their events.
---

# End-of-day review

**Plan:** every plan. It reads only what the user owns: watched events, saved Views and their Matches.

## Steps

1. **Read the watchlist** with `list_watchlist` `{"limit": 100, "sort": "last_matched_at", "order": "desc"}`. Each row carries the event's current numbers, its armed triggers and how many alerts it produced. An empty watchlist is an answer; say so.
   Done when you hold every watched event, or know there are none.

2. **Read today's Matches** with `list_matches` `{"since": "<start of the user's day, ISO 8601 with offset>", "limit": 100}`. `origin: "live"` is an event that entered a View through a market change; `origin: "baseline"` was recorded when a View learned its contents and is never an alert. Count live Matches per View.
   Done when you hold the live Matches of the day by View, or know there are none.

3. **Read the Views** with `list_views` `{"limit": 100}` for their names, whether each is `enabled`, and `recent_match_count` (live Matches in 7 days). A View with a large `member_count` and zero recent Matches is holding steady, not broken.
   Done when you can name every View that matched today and every paused one.

4. **Find the movers.** From the watchlist rows, keep events whose price or listings changed by a lot in a day (the row's 1-day change, or a trigger that fired today). For at most five of them call `get_event_analytics` `{"event_id": "<id>", "columns": ["median_price_current", "median_price_pct_1d", "lowest_price_pct_1d", "listings_delta_1d", "days_to_event", "last_price_snapshot_date", "primary_status"]}`.
   Done when each mover has its 1-day change and read age.

5. **Report in three parts**:
   - **Watchlist:** the movers, biggest first, with the change and the read age. Then one line: "N others steady."
   - **Views:** live Matches today per View, with the two or three most notable events.
   - **To act on:** at most five lines, each an event and the reason (a big move close to the event, a listing collapse, a status change). When nothing moved, say so in one line and stop.
   Done when the three parts are written and every number has its read age.

## Reporting rules

- Every number carries its read age: `last_price_snapshot_date` on analytics rows, `matched_at` on Matches.
- Delivery truth: an alert went out only when a Match has `delivery_status: "sent"`. Never infer it from a timestamp.
- Absorbed or delisted listings are listings that left the market, not sales.
- Link events with `event_url` and Views with `view_url`. Name no marketplace.

## Example

User: "End of day. What moved on my stuff?"

Watchlist of 12: two movers ("Knicks at Celtics: median down 14% today, priced 2026-09-28; 9 days out"). Views: "NFL listing collapse" caught 3 games live today. To act on: the Knicks game (sharp drop, 9 days out) and one NFL game whose listings fell by 400 in a week.
