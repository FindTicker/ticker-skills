---
name: pre-purchase-check
description: "Pre-purchase check on one event with Ticker: price trend, cheapest sections, primary against resale. Use when the user asks whether to buy now or wait, or for the cheapest way in."
---

# Pre-purchase check

**Plan:** Free

**Usual cost:** 4 requests: search, analytics, chart, sections. `list_screen_columns` is free.

One event, read before a person buys: where the price is going, the cheapest way in by section, and, on Max, the primary market (the box office) beside resale. A Free account reads one resale source, and this check reads at most 28 days of history; that is enough. Max adds the primary market.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| event | none: ask for one | one event: an act, team or venue name, with a date when the act plays more than once | the `search_events` call |
| trend window | 28 days | 7 to 28 days | the chart `range` (`7d` or `28d`) and the dates compared |
| sections shown | 3 | 1 to 10 | how many of the cheapest sections the verdict names |

Read the values from the user's words ("the last week", "top 5 sections"); keep the default for the rest. A value outside its range: do not run; say the range ("The trend window takes 7 to 28 days.") and ask for a value inside it. The first line of the answer says the values used.

## Steps

1. **Check the plan** with `list_screen_columns` `{}`. If `ea.tm_lowest_aip_price_current` has `locked: true`, this account does not read the primary market: skip every primary field below, and in the verdict write this sentence, exactly as written:
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

4. **Read the trend** with `get_event_price_chart` `{"event_id": "<id>", "range": "28d", "render": false}` (`"7d"` when the trend window is 7 days). 28 days fits every plan. Compare the latest `median_price` in `rows` with 7 days back and with the start of the window. `days_missing` lists real gaps: never fill them.
   Done when you can say rising, falling or flat, with the two dates you compared.

5. **Find the cheapest way in** with `get_event_sections` `{"event_id": "<id>", "include_history": false, "limit": 100}`. Each section carries one object per source: `vs` is resale; on Max, `tm_primary` is the box office and `tm_resale` its resale. Pick the cheapest sections by `min_price`, as many as "sections shown", and note which source holds each. When `truncated` is true, say the section list was partial (`sections_returned` of `sections_total`); do not page.
   Done when you can name the cheapest section, its price and its source.

6. **Give the verdict.** First line, the values used (a skill of a higher plan that handed over to this one puts its plan sentence above it): "Values: event <name, date>, trend window 28 days, sections shown 3." Then four lines: trend, cheapest way in, primary against resale, and one risk (few days to go, thin supply, a `data_quality_score` under 0.5, an old read). On Max, primary against resale compares `tm_lowest_aip_price_current` with `lowest_aip_price_current`, both all-in. Below Max, that line is the plan sentence of step 1. Say which way the numbers lean; the decision is the user's. End with the event link.
   Done when every number in the verdict has its read date.

## Reporting rules

- Quote each stamp as the tool gave it ("priced 2026-09-28", "as of 05:02 UTC"). Give the stamp, not an age: you do not know the current time.
- Every number carries its read date: `last_price_snapshot_date` for daily prices, `tm_asof_at` for primary, `as_of` inside each section source.
- Say the primary market and resale. Name sources only by their code (`vs`, `tm`, `tmr`), and name no marketplace.
- All-in (`*_aip_*`) is the buyer's final price with fees. Label which one you quote.
- Tickets that left the market are listings gone: never write "sold".
- Use no seat-by-seat or live-section tool in this check.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Should I buy Zach Bryan at Gillette now or wait?"

`search_events` finds the event; the analytics read shows median $202, down 18.6% in 7 days (priced 2026-09-28), 4 days to go; the 28-day chart falls from $248; the cheapest sections are 139 and 141 at $76 resale. On Free the third line reads "The primary market's prices are read on the Max plan: https://findticker.com/plans." Verdict: "Resale has fallen for a week. Four days out, the risk of waiting is supply drying up, not price rising."
