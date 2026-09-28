---
name: ticker-compare-events
description: Compare two events on Ticker side by side, or two dates of one tour: price, trend, supply, cheapest way in. Use when the user asks which of two shows, games or nights is the better buy.
---

# Compare two events

**Plan:** every plan. Max adds the primary market (box office) columns to the table.

## Steps

1. **Find both events.** Use ids you already have. Otherwise call `search_events` with `search` set to ONE name (the act, the team or the venue, never two together) and `date_from`/`date_to` as full ISO date-times spanning both dates plus one day after the last (`2026-10-09T00:00:00Z` to `2026-10-11T23:59:59Z`): the filter reads UTC, and an evening show in the Americas falls on the next UTC day. For two dates of one tour, one search lists them all; pick the two named.
   Done when you hold two `event_id`s and each one's name, date and venue.

2. **Read both** with `get_event_analytics`, one call each, the same columns:
   ```json
   {"event_id": "<id>", "columns": ["median_price_current", "lowest_price_current",
     "lowest_aip_price_current", "median_price_pct_7d", "listings_current",
     "listings_delta_7d", "days_to_event", "data_quality_score",
     "price_self_z_7d_xs_z_tour_tte", "last_price_snapshot_date",
     "tm_lowest_price_current", "tm_tickets_current", "tm_asof_at"]}
   ```
   `price_self_z_7d_xs_z_tour_tte` compares an event's 7-day price move with the same act's other dates; null means fewer than 5 such dates. On Pro the `tm_*` columns come back absent.
   Done when both rows are back and you have checked `primary_status` on each (cancelled, postponed or rescheduled goes first in the answer).

3. **Read both trends** with `get_event_price_chart` `{"event_id": "<id>", "range": "28d", "render": false}`, one call each. Compare the first and last `median_price` in the same window.
   Done when you can say, for each, rising, falling or flat over 28 days.

4. **Find each get-in** with `get_event_sections` `{"event_id": "<id>", "include_history": false, "limit": 40}`: the section with the lowest `min_price` and its source (`vs` resale; on Max `tm_primary` primary, `tm_resale`).
   Done when you hold one cheapest section per event.

5. **Report** one table with a column per event: date, venue, days to go, median, lowest, all-in lowest, 7-day change, 28-day trend, listings and their 7-day change, cheapest section, and on Max the primary lowest and tickets. Under it, two or three lines on what differs and which way it leans for the user's goal (cheapest seat, best value, least risk).
   Done when every cell has its read age or sits under a column header that states it.

## Reporting rules

- Quote each stamp as the tool gave it ("priced 2026-09-28", "as of 05:02 UTC"). Give the stamp, not an age: you do not know the current time.
- Every number carries its read age: `last_price_snapshot_date`, `tm_asof_at`, and `as_of` inside each section source. If the two reads have different dates, say so; do not compare a stale row with a fresh one as if they were the same day.
- The tools call each side of the market a "book". In the answer, say the primary market and resale.
- Never blend price bases: list price before fees, all-in with fees, primary face value. Label each row.
- Link both events with `event_url`. Name no marketplace.

## Example

User: "Karol G Miami Oct 2 or Oct 3, which is the better deal?"

One `search_events` lists the Miami dates; two analytics reads, two 28-day charts, two section reads; the table puts Oct 2 at a $439 median (priced 2026-09-28) against Oct 3, then: "Oct 3 is cheaper at the median and its price fell harder this week than the rest of the tour (tour score -1.4)."
