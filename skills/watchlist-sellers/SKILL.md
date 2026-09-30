---
name: watchlist-sellers
description: Seller concentration across your watched events on Ticker: which of the events you watch a few sellers control. Use when a broker asks who holds the inventory of the events they are tracking.
---

# Watchlist sellers

**Plan:** Ultra

**Usual cost:** up to 10 requests: the plan check, the watchlist, one concentration read per watched event.

For each event on the account's watchlist, soonest first, how concentrated its resale inventory is among sellers. The events a few sellers hold are the ones where a single seller's move shifts the price.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| events | 8 | 1 to 8 | how many watched events are read, soonest first |
| dominated at | 50% | 30 to 90% | the largest seller's share that marks an event as held |

## Steps

1. **Check the plan first**, before any other tool, with `list_views` `{"limit": 1}`. `views_cap` null means no cap: the Ultra plan. A number means a lower plan. The seller tools answer null below Ultra, the same answer as an event with no reading, so this check comes first. Below Ultra, start the answer with this sentence, exactly as written, and stop:
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

5. **Report.** First line, the values used: "Values: events 8, dominated at 50%." Then one table: event (linked), date, sellers, tickets, largest seller's share, largest three's share, band, coverage, as of. Mark "held" each event at or over "dominated at". Close with how many of the watched events are held.
   Done when every event read is in the table.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Never name, rank or guess who a seller is. Use the labels the tool gives ("Seller D"); a label means nothing outside its event.
- Tickets a seller holds are resale tickets on sale. A seller whose count fell may have had sales or pulled listings: never write "sold".
- A low `coverage_pct` means the shares describe a small part of the house; say it beside them.
- Name no marketplace. Link each event with its `event_url`.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Which of the events I'm watching does one seller control?"

`list_views` shows no cap; the watchlist holds 5 upcoming events; five concentration reads. Answer: "Values: events 8, dominated at 50%." Then the table, and "2 of your 5 watched events are held."
