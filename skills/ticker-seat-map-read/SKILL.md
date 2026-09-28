---
name: ticker-seat-map-read
description: Seat map read for one event on Ticker: which sections drained or filled in the last 24 hours and where seats just opened. Use when the user asks what moved on the seat map, which sections are selling down, or where new seats appeared.
---

# Seat map read

**Plan:** Pro reads open seats per section, past counts and recent seat moves. Max adds each section's capacity and share taken, and the hour-by-hour series of one section. On Pro, `get_event_section_series` answers `available: false` with no points, the same answer as an event with no series: say it is a Max reading, not that the section has no history.

The seat map reads the primary market's seat log. Many events have none; then every tool here answers `available: false`, which is an answer, not an error.

## Steps

1. **Find the event.** Use the `event_id` the user or an earlier tool gave you; otherwise `search_events` with `search` and `status: "active"`.
   Done when you hold one `event_id`.

2. **Read the house now** with `get_event_sections_at` `{"event_id": "<id>"}`. If `available` is false, stop and say this event has no live seat data. Keep each section's `open_count` and `observed_at`.
   Done when you hold the current open count per section, or you stopped.

3. **Read the house 24 hours ago** with `get_event_sections_at` `{"event_id": "<id>", "at": "<now minus 24 hours, ISO 8601>"}`. Subtract per section: a fall in `open_count` is a section that drained, a rise is a section that filled. A section absent at one time has no reading then; leave it out of the subtraction. `total` is null when some sections were not read; add the read sections yourself if you need a house total, and say it is partial.
   Done when you hold the five largest drains and the five largest fills.

4. **Read what just moved** with `get_event_seats_recent` `{"event_id": "<id>", "minutes": 120, "limit": 100}`. `kind: "open"` is a seat that came on sale, `close` one that left sale (sold or held back; the row does not say which). `republish: true` is a re-listing at a new price, so a burst of them is a price move, not demand.
   Done when you can name the sections where seats opened in the last two hours, or say none did.

5. **On Max only, draw the biggest mover** with `get_event_section_series` `{"event_id": "<id>", "section": "<code>", "bucket": "1h"}`. `open_count` is exact at every point; the prices are exact only on the newest point, so quote only that one.
   Done when you can say whether the drain was steady or one step.

6. **Report**: drained sections (before, now, change), filled sections, where seats opened recently, and on Max the share taken per drained section from `get_event_sections_live`. Close with the event link.
   Done when every count carries its read age.

## Reporting rules

- Every count carries its read age: `observed_at` on each section from `get_event_sections_at` (a count is carried forward from that reading), `at` on each recent seat move, `as_of` on live section counts.
- Taken is the share of a section's seats not open on the primary market right now. A seat held back, withdrawn or sold all count the same. Never write "sold".
- On the app's seat map, "Gone" is a seat seen leaving sale in the last six hours; "Not seen" is one whose last sighting off sale is older than that. Use the same words.
- Link the event with its `event_url` (`https://findticker.com/events/<event_id>`). Name no marketplace.

## Example

User: "What moved on the Zach Bryan Gillette seat map since yesterday?"

Two `get_event_sections_at` reads, 24 hours apart, then the subtraction: "Section 113 went from 655 to 620 open (observed 04:55 UTC today). Sections 139 and 141 gained 12 seats in the last two hours. On Max: 113 is now 41% taken."
