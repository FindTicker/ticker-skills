---
name: numbers
description: How Ticker's numbers are made: sources, read times, and what taken, absorbed and Gone mean. Use when the user asks how fresh a number is, where it comes from, or whether a count means sales.
---

# How Ticker's numbers are made

**Plan:** Free

**Usual cost:** 0 to 2 requests: a general question needs none; a question about one event's number needs a search and one analytics read.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| number | none: ask which | one figure or word: a price, a count, a rank, a seat state, a score, a stamp | the reference entry the answer draws on |
| event | none | one event, when the question is about its figure | the `search_events` and `get_event_analytics` calls |

Read both from the user's words. With no event, answer from the reference alone and call no tool. The first line of the answer says the values used (a skill of a higher plan that handed over to this one puts its plan sentence above it) ("Values: number median, event Zach Bryan, Gillette, 2026-10-02").

## Steps

1. **Name the number.** Find which figure the question is about (a price, a count, a rank, a seat state) and which event, performer or View it belongs to.
   Done when you can name the field or term.

2. **Fetch its stamp** when the question is about one event. Find the event with `search_events` and ONE name in `search` (the act, team or venue, never two together), then call `get_event_analytics` `{"event_id": "<id>", "columns": ["<field>", "last_price_snapshot_date", "computed_at", "demand_asof_date"]}`, adding `"tm_asof_at"` when the field is a primary one. Every figure has a stamp beside it. Quote the stamp itself ("computed 05:30 UTC today"). Give the stamp, not an age in hours: you do not know the current time. Call no seat-by-seat or live-section tool from this skill.
   Done when you hold the stamp, or the question is general.

3. **Answer from the reference below**: what the number is, where it comes from, its stamp, and what it cannot tell.
   Done when the answer states all four.

## Words

- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Reference

**Sources and plans.** Two sides of the market: primary (the box office) and resale. Tools name sources by code: `vs` and `tp` resale, `tm` primary, `tmr` primary's own resale, `gt` and `sg` resale quoted all-in. Free reads `vs`. Pro adds `tp`. Daily price history is full depth on every plan through these tools. Max adds `tm`, `tmr`, `gt` and `sg`. Ultra adds one more source when it lands, and seller concentration. A source above the plan is refused by name or left out of the answer. The tools sometimes call a side of the market a "book"; in the answer, say the primary market and resale. Name no marketplace; say primary or resale, or the code.

**Stamps.** How often a number is read differs by event (priority 1 events are read most often), so never assume a cadence: read the stamp.

| Number | Grain | Stamp |
|---|---|---|
| Event prices, tickets, listings, z-scores | daily rollup of the day's readings | `last_price_snapshot_date`, `computed_at` |
| Primary prices, tickets and Primary remaining (Max) | latest primary reading | `tm_asof_at` |
| Live seats per section (Max) | latest seat reading | `as_of` |
| Interest, Sales | daily | `demand_asof_date` |
| Performer rank | daily | `rank_asof_date` |
| Absorbed listings | daily, can lag about two days while it settles | `absorption_asof_date` |

A row whose `last_price_snapshot_date` is more than a day old is not a move today. `partial_row: true` means a hollow row: its nulls are unknown, not zero.

**Prices.** List prices exclude fees; all-in (`*_aip_*`) is the buyer's final price. On an analytics row, median, lowest, p25 and p75 are over the listings of the day's latest reading. On a daily chart row, median and p25/p75 are the mean of that day's readings and lowest is the day's low. Never blend a primary and a resale series.

**Remaining.** Primary remaining is the share of the room still on sale at the box office; Secondary remaining is the share listed on resale. Both can read above 100 when the capacity figure is wrong.

**Words that must not become "sold".**
- Taken: the share of a section's seats not open on the primary market now. A seat sold, held back, killed or not yet released counts the same.
- Absorbed, delisted, `sold_or_pulled`: listings that left the resale market, sold or withdrawn; the price beside them is an asking price.
- Primary remaining 0: the box office listed nothing at its last read. It does not say why.
- Interest and Sales: rolling-window levels of shoppers and sales pace. Read the change as momentum; never "X tickets sold today".

**Seat states (seat map, Max).** Four dots. Available: on sale now. Gone or Repriced in the last hour. Gone: a seat we saw go off sale, at any age, while the newest read of the whole venue does not list it; the hover gives the age ("Gone, 16h ago"). No history: a seat we never saw on sale. The age of the newest read of the whole venue is how fresh the map is. In a seat's history, gone is a seat that left and never came back: sold or pulled, the log does not say which.

**Scores.** A self z-score compares an event's move with its own normal swing; a peer score (`_xs_z_subcat_tte`) compares it with events of the same sub-category at a similar distance from the date; a tour score (`_xs_z_tour_tte`) with the same act's other dates. `data_quality_score` under 0.5 means thin history.

**Views and Matches.** A View is a saved screen; a Match is one event entering it. Baseline Matches, recorded when a View learns its contents, are never alerted. An alert went out only when `delivery_status` is `sent`.

**Empty answers.** A lookup by id that finds nothing is a failure (wrong id or missing thing). A search or screen that finds nothing is a correct answer.

## Example

User: "Is that $202 median live? And does 57% taken mean 57% of the seats are gone for good?"

`get_event_analytics` returns `last_price_snapshot_date` 2026-09-28 and `computed_at` 04:30 UTC. Answer: "The median is from the reading of 2026-09-28, computed at 04:30 UTC: a recent reading, not a live quote. Taken is not a sales count: it is the share of seats not open on the primary market right now, which includes seats held back or not yet released."
