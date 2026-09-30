---
name: performer-concentration
description: Seller concentration across one act's upcoming dates on Ticker: which nights a few sellers control and which are spread out. Use when the user asks where sellers hold an act's tour, date by date.
---

# Concentration across an act

**Plan:** Ultra

**Usual cost:** up to 8 requests: the plan check, one search, one concentration read per date.

For one act, the seller concentration of each upcoming date side by side: how many sellers, the largest one's share, and the band. A date that one seller dominates prices differently from a date many sellers compete on.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| act | none: ask for one | one act or team name | the `search_events` call |
| dates | 6 | 2 to 8 | how many upcoming dates are read, soonest first |
| days to event | 0 to 365 | 0 to 365 | which upcoming dates count |

## Steps

1. **Check the plan first**, before any other tool, with `list_views` `{"limit": 1}`. `views_cap` null means no cap: the Ultra plan. A number means a lower plan. The seller tools answer null below Ultra, the same answer as an event with no reading, so this check comes first. Below Ultra, start the answer with this sentence, exactly as written, and stop:
   ```text
   Concentration across an act reads seller concentration, which the Ultra plan opens: https://findticker.com/plans.
   ```
   That sentence is the whole answer: call no other tool.
   Done when you know the plan is Ultra, or you have written the sentence.

2. **Read the parameters** from the user's words ("the next 4 shows", "this month"); keep the default for the rest. A value outside its range: do not run; say the range ("Dates takes 2 to 8.") and ask for a value inside it.
   Done when you hold the act, the number of dates and the window.

3. **Find the dates** with ONE `search_events` call: `{"search": "<act name>", "status": "active", "limit": 100}`. Drop tribute acts and venues that share the name. Keep the upcoming dates inside the window, soonest first, up to "dates".
   Done when you hold the `event_id`s.

4. **Read each date** with `get_event_seller_concentration` `{"event_id": "<id>"}`, one call per date. A null `concentration` means that date has no reading; keep it in the table as "no reading".
   Done when every date has a reading or "no reading".

5. **Report.** First line, the values used: "Values: act <name>, dates 6, days to event 0 to 365." Then one table: date, city, sellers, tickets, largest seller's share, largest three's share, band, coverage, as of. Close with two lines: the most concentrated date and the most spread one.
   Done when every date is in the table.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Never name, rank or guess who a seller is. Use the labels the tool gives ("Seller D"); a label means nothing outside its event.
- Tickets a seller holds are resale tickets on sale. A seller whose count fell may have had sales or pulled listings: never write "sold".
- A low `coverage_pct` means the shares describe a small part of the house; say it beside them.
- Name no marketplace. Link each event with its `event_url`.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Across Usher and Chris Brown's next shows, where do a few sellers hold most of the tickets?"

`list_views` shows no cap; one search finds the dates; four concentration reads. Answer: "Values: act Usher and Chris Brown, dates 4, days to event 0 to 365." Then the table, and "Most concentrated: Columbia, 2026-10-29 (largest seller 35%, three 70%). Most spread: Indianapolis, 2026-10-31."
