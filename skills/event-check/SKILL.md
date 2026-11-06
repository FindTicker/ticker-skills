---
name: event-check
description: "Event check on Ticker: one event's price trend, its sections and the market around it, with resale vs face value on Max. Use when the user asks how an event is priced, where its price is heading or how its market looks."
---

# Event check

**Plan:** Free

**Usual cost:** 4 requests: search, analytics, chart, sections. `list_screen_columns` is free.

One event, read as a market: the price trend, the lowest-priced sections, supply and how close the date is, and, on Max, resale vs face value on the primary market. A Free account reads one resale source, and this check reads at most 28 days of history; that is enough. Max adds the primary market.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| event | none: ask for one | one event: an act, team or venue name, with a date when the act plays more than once | the `search_events` call |
| trend window | 28 days | 7 to 28 days | the chart `range` (`7d` or `28d`) and the dates compared |
| sections shown | 3 | 1 to 10 | how many of the lowest-priced sections the answer names |

Read the values from the user's words ("the last week", "top 5 sections"); keep the default for the rest. A value outside its range: do not run; say the range ("The trend window takes 7 to 28 days.") and ask for a value inside it. The first line of the answer says the values used.

## Steps

1. **Check the plan** with `list_screen_columns` `{}`. If `ea.tm_lowest_aip_price_current` has `locked: true`, this account does not read the primary market: skip every primary field below, and in the answer write this sentence, exactly as written:
   ```text
   The primary market's prices are read on the Max plan: https://findticker.com/plans.
   ```
   Never guess a primary price and never take one from the web.
   Done when you know whether the plan reads the primary market.

2. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC, and an evening show in the Americas falls on the next UTC day. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

3. **Read the event** with `get_event_analytics`:
   ```json
   {"event_id": "<id>", "columns": ["median_price_current", "lowest_price_current",
     "lowest_aip_price_current", "median_price_pct_7d", "lowest_price_pct_7d",
     "tickets_current", "tickets_delta_7d", "days_to_event", "data_quality_score",
     "last_price_snapshot_date"]}
   ```
   On Max, add `"tm_lowest_aip_price_current", "tm_tickets_current", "tm_percent_remaining", "tm_asof_at"`. `primary_status` comes back on every read: if it is `cancelled`, `postponed` or `rescheduled`, tell the user first and stop unless they still want the rest.
   Done when you hold the headline prices and their read date.

4. **Read the trend** with `get_event_chart` `{"event_id": "<id>", "range": "28d", "render": false}` (`"7d"` when the trend window is 7 days). 28 days fits every plan. Compare the latest `median` in `series` with 7 days back and with the start of the window. A date with no point has no reading: never fill it.
   Done when you can say rising, falling or flat, with the two dates you compared.

5. **Read the sections** with `get_event_sections` `{"event_id": "<id>", "include_history": false, "limit": 100}`. Each section carries one object per source, keyed by the source's code:
   ```text
   vs          resale
   tm_primary  primary market (Max)
   tm_resale   resale on the primary market's own site (Max)
   ```
   Pick the lowest-priced sections by `min_price`, as many as "sections shown", and note which market each price is from. When `truncated` is true, say the section list was partial (`sections_returned` of `sections_total`); do not page.
   Done when you can name the lowest-priced sections, their prices and their market.

6. **Report.** First line, the values used (a skill of a higher plan that handed over to this one puts its plan sentence above it): "Values: event <name, date>, trend window 28 days, sections shown 3." Then four lines: the price trend; the lowest-priced sections; resale vs face value; the market context (days to go, resale supply and its weekly change, a `data_quality_score` under 0.5, an old read). On Max, resale vs face compares `lowest_aip_price_current` with `tm_lowest_aip_price_current`, both all-in, as a percent difference ("+18%"), with Primary remaining beside it as how far the event has sold through. Below Max, that line is the plan sentence of step 1. Describe what the numbers show; give no advice on whether or when to buy. End with the event link.
   Done when every number in the answer has its read date.

## Reporting rules

- Quote each stamp as the tool gave it ("priced 2026-09-28", "as of 05:02 UTC"). Give the stamp, not an age: you do not know the current time.
- Every number carries its read date: `last_price_snapshot_date` for daily prices, `tm_asof_at` for primary, `as_of` inside each section source.
- Say the primary market and resale. Describe each price by market, not by source code, and do not guess provider names.
- All-in (`*_aip_*`) is the price with fees. Label which one you quote.
- Write resale vs face as a percent difference, never as a multiple of face value.
- Tickets that left the market are listings gone: never write "sold".
- Use no seat-level or live-section tool in this check.
- Explain a plan requirement when it blocks the task; avoid unsolicited plan recommendations.

## Example

User: "How is Zach Bryan at Gillette priced right now?"

`search_events` finds the event; the analytics read shows median $202, down 18.6% in 7 days (priced 2026-09-28), 4 days to go; the 28-day chart falls from $248; the lowest-priced sections are 139 and 141 at $76 resale. On Free the third line reads "The primary market's prices are read on the Max plan: https://findticker.com/plans." Answer: "The median resale price has fallen for a week, from $248 to $202. Sections 139 and 141 list from $76. Resale supply grew 9% over the week, with four days to the event."
