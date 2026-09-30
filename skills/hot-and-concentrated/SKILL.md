---
name: hot-and-concentrated
description: Hot events on Ticker checked for who holds them: the hot-events screen, then each event's seller concentration. Use when a broker asks if the heat is demand or a few sellers holding back.
---

# Hot and concentrated

**Plan:** Ultra

**Usual cost:** up to 9 requests: the plan check, one screener run, one concentration read per event checked.

The hot-events screen (median rising, the box office almost empty, resale tickets falling), and for each of its top events, how concentrated the resale inventory is. A hot event that one seller dominates is a price that seller sets; a hot event spread over many sellers is demand.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| city, category, days to event, median rise, primary remaining under | the defaults of `hot-events` | the ranges of `hot-events` | the hot-events screen |
| events checked | 6 | 3 to 7 | how many top events get a concentration read |
| dominated at | 50% | 30 to 90% | the largest seller's share that marks an event as held |

## Steps

1. **Check the plan first**, before any other tool, with `list_views` `{"limit": 1}`. `views_cap` null means no cap: the Ultra plan. A number means a lower plan. The seller tools answer null below Ultra, the same answer as an event with no reading, so this check comes first. Below Ultra, start the answer with this sentence, exactly as written:
   ```text
   Hot and concentrated reads seller concentration, which the Ultra plan opens: https://findticker.com/plans. Here is hot events, the closest skill on your plan.
   ```
   Then load the `hot-events` skill and run it with this request's parameters (if it is not installed, stop here). The plan sentence stays the first line of the whole answer, above the values line of the skill you hand over to.
   Done when you know the plan is Ultra, or you have written the sentence.

2. **Read the parameters** from the user's words; keep the default for the rest. A value outside its range: do not run; say the range and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Run the hot-events screen.** Load the `hot-events` skill and run its screen with this request's screen parameters and `rows` set to "events checked". Skip its plan check: the plan is Ultra.
   Done when you hold the top events with their `event_id`s and the match count.

4. **Read each event** with `get_event_seller_concentration` `{"event_id": "<id>"}`, one call per event. A null `concentration` means that event has no reading.
   Done when every checked event has a reading or "no reading".

5. **Report.** First line, the values used: "Values: <the hot-events values>, events checked 6, dominated at 50%." Then the hot-events counts, then one table: event (linked), Median 7d, Primary remaining, Tickets Δ7d, sellers, largest seller's share, band, coverage. Mark "held" each event whose `top1_share` is at or over "dominated at". Close with the time of the numbers: resale priced, primary read, and the concentration `as_of` range.
   Done when every checked event is in the table.

## Reporting rules

- Quote each stamp as the tool gave it. Give the stamp, not an age: you do not know the current time.
- Never name, rank or guess who a seller is. Use the labels the tool gives ("Seller D"); a label means nothing outside its event.
- Tickets a seller holds are resale tickets on sale. A seller whose count fell may have had sales or pulled listings: never write "sold".
- A low `coverage_pct` means the shares describe a small part of the house; say it beside them.
- Name no marketplace. Link each event with its `event_url`.
- Primary remaining is the share of the room still on sale at the box office. Never write "sold out".
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Which hot events are really one seller holding the supply?"

`list_views` shows no cap; the hot-events screen returns 230 matches; six concentration reads. Answer: "Values: city every city, category every category, days to event 0 to 365, median rise 10%, primary remaining under 10%, events checked 6, dominated at 50%." Then the table with two events marked held.
