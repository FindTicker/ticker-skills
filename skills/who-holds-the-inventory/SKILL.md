---
name: who-holds-the-inventory
description: "Who holds one event's resale inventory on Ticker: how many sellers, the largest one's share, and how that moved. Use when the user asks how resale listings are distributed among sellers."
---

# Who holds the inventory

**Plan:** Ultra

**Usual cost:** 4 requests: the plan check, one search, the concentration, the hourly series.

How concentrated one event's resale inventory is among the sellers behind it. Concentration describes the observed listings. It does not establish price control, total ticket ownership or seller intent. Use the anonymous seller labels returned by the tools; a label applies only within its event.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| event | none: ask for one | one event: an act, team or venue name, with a date when the act plays more than once | the `search_events` call |
| window | 48 hours | 6 to 168 hours | the `hours` of `get_event_sellers` view series |

## Steps

1. **Check the plan first**, before any other tool, with `list_views` `{"limit": 1}`. `views_cap` null means no cap: the Ultra plan. A number means a lower plan. Treat a plan_required or locked response as a plan restriction. A null reading alone does not establish a plan restriction. Below Ultra, start the answer with this sentence, exactly as written, and stop:
   ```text
   Who holds the inventory reads seller concentration, which the Ultra plan opens: https://findticker.com/plans.
   ```
   That sentence is the whole answer: call no other tool.
   Done when you know the plan is Ultra, or you have written the sentence.

2. **Read the parameters** from the user's words ("over the last week", "since yesterday"); keep the default for the rest. A value outside its range: do not run; say the range ("The window takes 6 to 168 hours.") and ask for a value inside it.
   Done when you hold the event and the window.

3. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

4. **Read the concentration** with `get_event_sellers` `{"event_id": "<id>"}`. `concentration` null on Ultra means the event has no reading: say so and stop.
   Done when you hold the reading.

5. **Read how it moved** with `get_event_sellers` `{"event_id": "<id>", "view": "series", "hours": <window>}`. Take the first hour with a reading and the last: `distinct_sellers` and `attributed_tickets` at each, and the largest line in `sellers` by `peak_tickets`.
   Done when you hold the start and the end of the window, or `series` is null (then report the concentration alone).

6. **Report.** First line, the values used: "Values: event <name, date>, window 48 hours." Then: how many sellers hold inventory (`sellers_active`) and how many tickets they hold (`attributed_tickets`); the largest seller's share (`top1_share`) and the largest three's (`top3_share`), as percents; the band (`shape`: spread, concentrated or dominated); `coverage_pct`; the move over the window (sellers and tickets at the first and the last hour, and the label that held the most); the stamp `as_of`. Close with the event link.
   Done when every number has its stamp.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Never name, rank or guess who a seller is. Use the labels the tool gives ("Seller D"); a label means nothing outside its event.
- Tickets a seller holds are resale tickets on sale. A seller whose count fell may have had sales or pulled listings: never write "sold".
- A low `coverage_pct` means the shares describe a small part of the house; say it beside them.
- Use the source labels returned by the tools; do not guess provider names. Link each event with its `event_url`.
- Use "primary market" and "resale" in answers. Explain a plan requirement when it blocks the task; avoid unsolicited plan recommendations.

## Example

User: "How concentrated are the resale listings for Arsenal v Hull?"

`list_views` shows no cap; `search_events` finds the match; the concentration reads 17 sellers on 9,512 tickets, the largest at 69% and the largest three at 93%, shape dominated, coverage 99.9%. Answer: "Values: event Arsenal vs Hull City, Emirates Stadium, 2026-11-07, window 48 hours. One seller accounts for 69% of the attributed resale listings and three account for 93%. Seller D is the large one, with 6,551 tickets at 22:00 UTC."
