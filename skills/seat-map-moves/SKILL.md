---
name: seat-map-moves
description: "Seat map moves on Ticker: primary seats taken by section for one event, and how that changed over the last day. Use when the user asks how an event is selling by section on the primary market."
---

# Seat map moves

**Plan:** Max

**Usual cost:** 4 requests: one search, two reads of the open seats, one read of the sections that changed. `list_screen_columns` is free.

Primary seats taken by section for one event, and how that changed over time: the open seats in each section now and a set number of hours ago. The difference shows which sections took up seats and where seats came back. Available for events with section-level primary data.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Sets |
|---|---|---|---|
| event | none: ask for one | one event: an act, team or venue name, with a date when the act plays more than once | the `search_events` call |
| window | 24 hours | 1 to 168 hours | how far back the second read looks |
| sections shown | 5 | 3 to 10 | how many sections with fewer and with more open seats the answer names |

## Steps

1. **Check the plan** with `list_screen_columns` `{}`. The answer is long (over 200 columns); you need only the row for `ea.tm_percent_remaining`. If it has `locked: true`, the account's plan does not read the primary market's seat map. Start the answer with this sentence, exactly as written:
   ```text
   Seat map moves reads the primary market's seat map, which the Max plan opens: https://findticker.com/plans. Here is event check, the closest skill on your plan.
   ```
   Then load the `event-check` skill and run it on the same event (if it is not installed, stop here). The plan sentence stays the first line of the whole answer, above the values line of the skill you hand over to. Call no seat or live-section tool below Max.
   Done when you know the plan reads the primary market, or you have handed over.

2. **Read the parameters** from the user's words ("last 6 hours", "the past week", "top 8 sections"); keep the default for the rest. A value outside its range: do not run; say the range ("The window takes 1 to 168 hours.") and ask for a value inside it.
   Done when every parameter has a value inside its range.

3. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

4. **Read the open seats now** with `get_event_sections_live` `{"event_id": "<id>", "view": "at"}`. `at` in the answer is now, to the second. `available: false` means the event has no per-section readings: say so and stop.
   Done when you hold `at`, `total` and each section's `open_count`.

5. **Read the open seats before** with `get_event_sections_live` `{"event_id": "<id>", "view": "at", "at": "<at minus the window, ISO 8601>"}`. Subtract, section by section: open now minus open then. A negative number means fewer open seats, a positive one more (seats released or returned). A section absent at one of the two times had no reading then; leave it out of the ranking and say how many you left out.
   Done when you hold the change per section and for the whole venue.

6. **Read the sections that changed** with `get_event_sections_live` `{"event_id": "<id>", "sections": [<the sections to show>]}`: `capacity`, `percent_taken`, `min_price` and `as_of` for each.
   Done when each section you will name has its taken share and lowest price, or you know the event states no capacity.

7. **Report.** First line, the values used: "Values: event <name, date>, window 24 hours, sections shown 5." Then the whole venue: open seats then and now, and the change. Then two short tables: the sections with the largest drop in open seats (section, open then, open now, change, taken, lowest price) and the ones with the largest rise. Close with the stamps: the two `at` times and the `as_of` of the live read, and the event link.
   Done when every number carries its stamp.

## Reporting rules

- Quote each stamp as the tool gave it, in UTC. Give the stamp, not an age.
- A count is carried forward from a section's last reading: `observed_at` says how old it is. Flag a section whose reading is older than the window.
- Taken is the share of a section's seats not open on the primary market now. A seat sold, held back, killed or not yet released counts the same: never write "sold" or "sold out".
- A section with fewer open seats lost them on the primary market; the reading does not say why.
- Say the primary market and resale. Describe numbers by market (primary market or resale), not by source code, and do not guess provider names. Link the event with its `event_url`.
- Use "primary market" and "resale" in answers. Explain a plan requirement when it blocks the task; avoid unsolicited plan recommendations.

## Example

User: "How is the Usher show in Indianapolis selling by section today?"

`search_events` finds the show; the venue reads 13,420 open seats 24 hours ago and 13,303 now. Answer: "Values: event Usher and Chris Brown, Lucas Oil Stadium, 2026-10-31, window 24 hours, sections shown 5. The primary market went from 13,420 to 13,303 open seats (-117). Largest drops: 143 (-9, 74% taken, from $209.50), 323 (-6) ..." then the stamps.
