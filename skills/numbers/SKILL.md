---
name: numbers
description: How Ticker's numbers are made: sources, read ages, and what taken, absorbed, Gone and Not seen mean. Use when the user asks how fresh a number is, where it comes from, or whether seats sold.
---

# How Ticker's numbers are made

**Plan:** every plan. Which sources a plan reads is in step 3.

## Steps

1. **Name the number.** Find which figure the question is about (a price, a count, a rank, a seat state) and which event, performer or View it belongs to.
   Done when you can name the field or term.

2. **Fetch its stamp** when the question is about one event. Find the event with `search_events` and ONE name in `search` (the act, team or venue, never two together), then call `get_event_analytics` `{"event_id": "<id>", "columns": ["<field>", "last_price_snapshot_date", "computed_at", "demand_asof_date", "tm_asof_at"]}`, or the tool that produced the number. Every figure has a stamp beside it. Quote the stamp itself ("computed 05:30 UTC today"). Give the stamp, not an age in hours: you do not know the current time.
   Done when you hold the stamp, or the question is general.

3. **Answer from the reference below**: what the number is, where it comes from, its stamp, and what it cannot tell.
   Done when the answer states all four.

## Reference

**Sources.** Two sides of the market: primary (the box office) and resale. The tools call each side a "book"; in the answer, say the primary market and resale. Tools name sources by code: `vs` and `tp` resale, `tm` primary, `tmr` primary's resale twin, `gt` and `sg` resale quoted all-in. Pro reads `vs` and `tp`; Max adds `tm`, `tmr`, `gt` and `sg`; Ultra adds one more. A source above the plan is refused by name or left out of the answer. Name no marketplace; say primary or resale, or the code.

**Stamps.** How often a number is read differs by event (coverage tier 1 is read most often), so never assume a cadence: read the stamp.

| Number | Grain | Stamp |
|---|---|---|
| Event prices, listings, z-scores | daily rollup of the day's readings | `last_price_snapshot_date`, `computed_at` |
| Primary prices and tickets | latest primary reading | `tm_asof_at`, chart `meta.lastMeasuredAt` |
| Live seats per section | latest seat-log reading | `as_of`, `observed_at` (a count carried forward from that reading) |
| Interest, Sales | daily | `demand_asof_date` |
| Performer rank | daily | `rank_asof_date` |
| Absorbed listings | daily, can lag about two days while it settles | `absorption_asof_date` |

A row whose `last_price_snapshot_date` is more than a day old is not a move today. `partial_row: true` means a hollow row: its nulls are unknown, not zero.

**Prices.** List prices exclude fees; all-in (`*_aip_*`) is the buyer's final price. On an analytics row, median, lowest, p25 and p75 are over the listings of the day's latest reading. On a daily chart row, median and p25/p75 are the mean of that day's readings and lowest is the day's low. Never blend a primary and a resale series.

**Words that must not become "sold".**
- Taken: the share of a section's seats not open on the primary market now. Sold, held back, killed and not yet released all count the same.
- Absorbed, delisted, `sold_or_pulled`: listings that left the resale market, sold or withdrawn; the price beside them is an asking price.
- Interest and Sales: rolling-window levels of shoppers and sales pace. Read the change as momentum; never "X tickets sold today".

**Seat states.** On the seat map, "Gone" is a seat seen leaving sale within the last six hours; "Not seen" is a seat whose last sighting off sale is older, so it says "since" that time instead of claiming the seat is gone now. In a seat's history (`get_event_seat_history`), `gone` is a seat that left and never came back: sold or pulled, the log does not say which.

**Scores.** A self z-score compares an event's move with its own normal swing; a peer score (`_xs_z_subcat_tte`) compares it with events of the same sub-category at a similar distance from the date; a tour score (`_xs_z_tour_tte`) with the same act's other dates. `data_quality_score` under 0.5 means thin history.

**Views and Matches.** A View is a saved screen; a Match is one event entering it. Baseline Matches, recorded when a View learns its contents, are never alerted. An alert went out only when `delivery_status` is `sent`.

**Empty answers.** A lookup by id that finds nothing is a failure (wrong id or missing thing). A search or screen that finds nothing is a correct answer. `available: false` on seat tools means no live seat data for that event.

## Example

User: "Is that $202 median live? And does 57% taken mean 57% sold?"

`get_event_analytics` returns `last_price_snapshot_date` 2026-09-28 and `computed_at` 04:30 UTC. Answer: "The median is from this morning's reading, about an hour old, not a live quote. Taken is not sold: it is the share of seats not open on the primary market right now, which includes seats held back or not yet released."
