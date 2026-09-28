---
name: ticker-sell-through
description: Sell-through read for one event on Ticker: share of seats taken on the primary market, primary against resale, pace against days to go. Use when a promoter or venue asks how a show is selling.
---

# Sell-through read

**Plan: Max or Ultra.** Section capacity, the share taken, the primary price series and the primary columns are Max readings. On Pro, `get_event_sections_live` omits `capacity` and `percent_taken`, and the primary price series is refused; say at the start that a full sell-through read needs Max, then give the open seat counts and the resale side that Pro reads.

Taken is the share of a section's counted seats that are not open for sale on the primary market right now. A seat sold, held back, killed or not yet released all count the same, so taken is never "sold".

## Steps

1. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC, and an evening show in the Americas falls on the next UTC day. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

2. **Read the house** with `get_event_sections_live` `{"event_id": "<id>", "limit": 650}`. If `available` is false, the event has no live seat data: say so and go to step 3. Otherwise add up, over sections with a `capacity`: capacity, `open_count`, and taken = capacity minus open. General admission sections (`is_general_admission: true`) hold a declared allocation; list them apart. `sections_total` is the true section count.
   Done when you hold house capacity, open seats and the taken share, with how many sections had no capacity.

3. **Read primary against resale** with `get_event_analytics` `{"event_id": "<id>", "columns": ["days_to_event", "tm_tickets_current", "tm_percent_remaining", "tm_lowest_price_current", "tm_asof_at", "tickets_current", "listings_current", "percent_remaining", "median_price_current", "last_price_snapshot_date"]}`. `tm_*` is the primary market; `tickets_current` and `listings_current` are resale. `percent_remaining` can exceed 100 when the capacity figure is wrong; quote it only with that warning.
   Done when you hold primary tickets available and resale tickets listed, each with its read age.

4. **Read the pace** with `get_event_price_chart` `{"event_id": "<id>", "source": "tm", "render": false}`. From `series`, take `tickets` on the latest date and 7 days before it: the fall per day is the primary pace. Rows with null `tickets` are days with no count; skip them, never fill them.
   Done when you have the primary tickets change over the last 7 readable days, or know the series has no counts.

5. **Report**: taken share (house and the three most and least taken sections), primary tickets available against resale tickets listed, pace per day against days to go, and the risk in one line (for example "at this pace the primary market still holds 4,000 seats on the day"). Close with the event link.
   Done when every number has its read age.

## Reporting rules

- Quote each stamp as the tool gave it ("priced 2026-09-28", "as of 05:02 UTC"). Give the stamp, not an age: you do not know the current time.
- Every number carries its read age: `as_of` on live section counts, `tm_asof_at` and `meta.lastMeasuredAt` for primary, `last_price_snapshot_date` for resale.
- The tools call each side of the market a "book". In the answer, say the primary market and resale.
- Write taken, open and available. Never write sold, unsold, sold out or percent sold.
- `sold_or_pulled` counts resale listings that left the market, sold or withdrawn; its average is an asking price. Never a sales count.
- Link the event with `event_url`. Name no marketplace.

## Example

User: "How is the Zach Bryan Gillette show selling through?"

Live sections: 78 sections, capacity known on most; the counted sections are 57% taken (as of 05:02 UTC). Primary 11,612 tickets available against 19,282 resale tickets listed (priced 2026-09-28). The primary count fell by a few dozen a day over the last week, with 4 days to go.
