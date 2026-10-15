---
name: watchlist-sellers
description: "Seller concentration across your watched events on Ticker: how listed inventory is distributed among sellers for the events you watch. Use when the user asks how seller concentration changed across watched events."
---

# Watchlist sellers

**Plan:** Ultra

**Usual cost:** up to 10 requests: the plan check, the watchlist, one concentration read per watched event.

For each event on the account's watchlist, soonest first, how concentrated its resale inventory is among sellers. Concentration describes the observed listings; it does not establish price control or seller intent.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| events | 8 | 1 to 8 | how many watched events are read, soonest first |
| dominated at | 50% | 30 to 90% | the largest seller's share used to flag concentration |

## Steps

1. **Check the plan first**, before any other tool, with `list_views` `{"limit": 1}`. `views_cap` null means no cap: the Ultra plan. A number means a lower plan. Treat a plan_required or locked response as a plan restriction. A null reading alone does not establish a plan restriction. Below Ultra, start the answer with this sentence, exactly as written, and stop:
   ```text
   Watchlist sellers reads seller concentration, which the Ultra plan opens: https://findticker.com/plans.
   ```
   That sentence is the whole answer: call no other tool.
   Done when you know the plan is Ultra, or you have written the sentence.

2. **Read the parameters** from the user's words ("my next 5 events"); keep the default for the rest. A value outside its range: do not run; say the range and ask for a value inside it.
   Done when you hold both values.

3. **Read the watchlist** with `list_watchlist` `{"sort": "utc_date", "order": "asc", "limit": 50}`. Keep the upcoming events, soonest first, up to "events". An empty watchlist: say so, and point to the `watch-event` skill to add one.
   Done when you hold the `event_id`s.

4. **Read each event** with `get_event_seller_concentration` `{"event_id": "<id>"}`, one call per event. A null `concentration` means that event has no reading.
   Done when every event has a reading or "no reading".

5. **Report.** First line, the values used: "Values: events 8, dominated at 50%." Then one table: event (linked), date, sellers, tickets, largest seller's share, largest three's share, band, coverage, as of. Mark "concentrated" each event at or over "dominated at". Close with how many watched events meet that threshold.
   Done when every event read is in the table.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Never name, rank or guess who a seller is. Use the labels the tool gives ("Seller D"); a label means nothing outside its event.
- Tickets a seller holds are resale tickets on sale. A seller whose count fell may have had sales or pulled listings: never write "sold".
- A low `coverage_pct` means the shares describe a small part of the house; say it beside them.
- Use the source labels returned by the tools; do not guess provider names. Link each event with its `event_url`.
- Use "primary market" and "resale" in answers. Explain a plan requirement when it blocks the task; avoid unsolicited plan recommendations.

## Example

User: "Which events I'm watching have the most concentrated resale listings?"

`list_views` shows no cap; the watchlist holds 5 upcoming events; five concentration reads. Answer: "Values: events 8, dominated at 50%." Then the table, and "2 of your 5 watched events meet the concentration threshold."
