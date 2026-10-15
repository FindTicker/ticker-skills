---
name: seller-moves
description: "Seller moves on Ticker: changes in resale listings attributed to each seller over a window you pick. Use when the user asks which sellers' listed ticket counts changed."
---

# Seller moves

**Plan:** Ultra

**Usual cost:** 3 requests: the plan check, one search, the hourly series.

For one event, compare the resale ticket counts attributed to each seller at the start and end of the window. A change in listed inventory does not establish purchases, sales or seller intent. Sellers stay anonymous: "Seller J" is a label for this event only.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| event | none: ask for one | one event: an act, team or venue name, with a date when the act plays more than once | the `search_events` call |
| window | 72 hours | 6 to 168 hours | the `hours` of `get_event_sellers` view series |
| sellers shown | 5 | 3 to 8 | how many labels the answer names across decreases and increases |

## Steps

1. **Check the plan first**, before any other tool, with `list_views` `{"limit": 1}`. `views_cap` null means no cap: the Ultra plan. A number means a lower plan. Treat a plan_required or locked response as a plan restriction. A null reading alone does not establish a plan restriction. Below Ultra, start the answer with this sentence, exactly as written, and stop:
   ```text
   Seller moves reads seller concentration, which the Ultra plan opens: https://findticker.com/plans.
   ```
   That sentence is the whole answer: call no other tool.
   Done when you know the plan is Ultra, or you have written the sentence.

2. **Read the parameters** from the user's words ("over the last week", "since yesterday", "top 3"); keep the default for the rest. A value outside its range: do not run; say the range and ask for a value inside it.
   Done when you hold the event, the window and the count.

3. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

4. **Read the series** with `get_event_sellers` `{"event_id": "<id>", "view": "series", "hours": <window>}`. `series` null on Ultra means the event has no reading: say so and stop. Take the first hour whose `distinct_sellers` is not null, and the last hour. For each label in `tickets`, the change is its tickets at the last hour minus at the first (a null at the first hour means the line had not begun: count it from 0). Tickets held by sellers without a line of their own are `attributed_tickets` minus the sum of the lines.
   Done when you hold each label's change and the whole event's change.

5. **Report.** First line, the values used: "Values: event <name, date>, window 72 hours, sellers shown 5." Then the event: sellers and attributed tickets at the first and the last hour. Then one table: label, tickets at the start, tickets at the end, change, peak in the window, with the largest decreases first, then the largest increases. One closing line reports the change in the largest seller's listed count. Stamps: the first and last `hour`, and `as_of`.
   Done when every label shown has its change and the window's two hours.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Never name, rank or guess who a seller is. Use the labels the tool gives ("Seller D"); a label means nothing outside its event.
- Tickets a seller holds are resale tickets on sale. A seller whose count fell may have had sales or pulled listings: never write "sold".
- A low `coverage_pct` means the shares describe a small part of the house; say it beside them.
- Use the source labels returned by the tools; do not guess provider names. Link each event with its `event_url`.
- Use "primary market" and "resale" in answers. Explain a plan requirement when it blocks the task; avoid unsolicited plan recommendations.

## Example

User: "How have resale listings changed by seller for Zach Bryan at Gillette this week?"

`list_views` shows no cap; one search; the 168-hour series. Answer: "Values: event Zach Bryan, Gillette Stadium, 2026-10-02, window 168 hours, sellers shown 5. Sellers went from 82 to 66 and attributed tickets from 17,440 to 18,523. Largest decreases: Seller J -671 (peak 10,667), Seller B -410, Seller A -234. Largest increase: Seller L +652."
