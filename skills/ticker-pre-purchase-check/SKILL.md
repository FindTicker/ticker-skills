---
name: ticker-pre-purchase-check
description: Pre-purchase check on one event with Ticker: price trend, get-in by section, primary against resale, open seats. Use when the user asks whether to buy now or wait, or for the cheapest way in.
---

# Pre-purchase check

**Plan:** Pro reads the resale prices. Max adds the primary market (the box office): its price series, its section prices and each section's share taken. When the primary side comes back absent, say it in these words: "The primary market (box office) side of this check needs the Max plan." Then give the resale answer.

## Steps

1. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC, and an evening show in the Americas falls on the next UTC day. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

2. **Read the event** with `get_event_analytics`:
   ```json
   {"event_id": "<id>", "columns": ["median_price_current", "lowest_price_current",
     "lowest_aip_price_current", "median_price_pct_7d", "lowest_price_pct_7d",
     "listings_current", "listings_delta_7d", "days_to_event", "data_quality_score",
     "last_price_snapshot_date", "tm_lowest_price_current", "tm_tickets_current", "tm_asof_at"]}
   ```
   `primary_status` comes back on every read. If it is `cancelled`, `postponed` or `rescheduled`, tell the user first and stop unless they still want the rest.
   Done when you hold the headline prices and their read age.

3. **Read the trend** with `get_event_price_chart` `{"event_id": "<id>", "range": "28d", "render": false}`. Compare the latest `median_price` with 7 and 28 days back. `days_missing` lists real gaps: never fill them.
   Done when you can say rising, falling or flat, with the two dates you compared.

4. **Find the get-in by section** with `get_event_sections` `{"event_id": "<id>", "include_history": false, "limit": 200}`. Each section carries one object per source: `vs` (resale), and on Max `tm_primary` (primary) and `tm_resale`. A missing source on a section means that source does not sell it. Pick the three cheapest sections by `min_price` and note which source holds each.
   Done when you can name the cheapest section, its price and its source.

5. **Check open seats** with `get_event_sections_live` `{"event_id": "<id>", "limit": 60}`. `available: false` means the event has no live seat data: say so and skip. Otherwise report how many seats are open on the primary market (`open_count`) in the sections from step 4, and in the whole house. On Max, `percent_taken` is the share of the section's seats not open on the primary market; it is not a sold count.
   Done when you have the open count for the step 4 sections, or you know there is no live seat data.

6. **Give the verdict** in four lines: trend, cheapest way in, primary against resale (Max, or on Pro the line "The primary market (box office) side of this check needs the Max plan."), and one risk (few days to go, thin listings, a low `data_quality_score`, an old read). End with the event link. Say what the numbers show and which way they lean; the decision is the user's. On Pro the `tm_*` columns come back absent: that is the plan, not missing data.
   Done when every number in the verdict has its read age.

## Reporting rules

- Quote each stamp as the tool gave it ("priced 2026-09-28", "as of 05:02 UTC"). Give the stamp, not an age: you do not know the current time.
- Every number carries its read age: `last_price_snapshot_date` for daily prices, `tm_asof_at` for primary, `as_of` for live seats, `as_of` inside each section source.
- The tools call each side of the market a "book". In the answer, say the primary market and resale.
- Say primary and resale. Name sources only by their code (`vs`, `tm`, `tmr`); name no marketplace.
- All-in (`lowest_aip_price_current`) is the buyer's final price with fees. Label which one you quote.
- `percent_taken` and anything that "left" the market are seats no longer on sale. Never call them sold.

## Example

User: "Should I buy Zach Bryan at Gillette now or wait?"

`search_events` finds the event; the analytics read shows median $202, down 18.6% in 7 days (priced 2026-09-28), 4 days to go; the 28-day chart falls from $248; the cheapest sections are 139 and 141 at $133 on the primary market (Max) against a resale lowest of $76 before fees. Verdict: "Resale has fallen for a week and sits under face value in the cheap seats. Four days out, the risk of waiting is supply drying up, not price rising."
