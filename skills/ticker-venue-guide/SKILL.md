---
name: ticker-venue-guide
description: Venue guide from Ticker for one room: capacity, how sections are named, where the get-in price sits, what is on next. Use when the user asks about a venue, its seating or its cheapest way in.
---

# Venue guide

**Plan:** every plan. The room's capacity is on every plan; the capacity of each section is a Max reading.

Get-in is the lowest price to enter an event: the lowest listed resale price before fees (`lowest_price_current`), the all-in lowest with fees (`lowest_aip_price_current`), and per section the section's lowest price. It belongs to one event on one day; a venue's "usual" get-in is a pattern across its events, never one number.

## Steps

1. **Find the venue** with `find_venue` `{"name": "<name>"}`. Expand nicknames first ("MSG" is Madison Square Garden). More than one match: pick by city, or ask.
   Done when you hold one `venue_id` (`vn` plus ten characters) with its city.

2. **Read what is on** with `get_venue_schedule` `{"venue_id": "<id>", "days": 60}`. Each event carries its date, on-sale dates and current get-in price.
   Done when you hold the upcoming events, or know there are none in 60 days.

3. **Read the room's capacity** with `screen_events` `{"predicate": {"all": [{"col": "v.venue_name", "op": "contains", "val": "<venue name>"}]}, "columns": ["e.event_name", "e.local_date", "v.capacity"], "limit": 5}`. Each row's `venue.capacity` is the seats in the room that event sells; null means Ticker does not know it. Quote only this number for capacity, never one from memory.
   Done when you hold the capacity, or know it is not known.

4. **Read the layout** from the next event that has seat data: `get_event_sections_live` `{"event_id": "<id>", "limit": 650}`. `sections_total` is the section count; section codes are as printed on a ticket; `is_general_admission` marks a floor or lawn with a declared allocation; `base_section` names the section an accessible row belongs to. If `available` is false, try the next event, at most three.
   Done when you can describe the section naming.

5. **Read where the get-in sits** with `get_event_sections` `{"event_id": "<id>", "include_history": false, "limit": 200}` for the same event: sort sections by lowest `min_price` in each source. Group them the way the room is built (floor, lower bowl 100s, upper 200s or 300s, clubs), as the section codes show.
   Done when you can name the level that holds the get-in and the price there.

6. **Report**: venue, city, capacity (with the event it is from), section count, how sections are named, where the get-in sits on the next event and its price, and the next five events with dates and get-in. Close with the event links.
   Done when every price carries its read age.

## Reporting rules

- Quote each stamp as the tool gave it ("priced 2026-09-28", "as of 05:02 UTC"). Give the stamp, not an age: you do not know the current time.
- Every number carries its read age: `as_of` on live sections and inside each section source, and the date on each schedule row.
- A capacity is seats in the room this event sells. Stage layouts differ, so two events at one venue can differ.
- The tools call each side of the market a "book". In the answer, say the primary market and resale, name sources only by their code (`vs`, `tm`), and name no marketplace. Link events with `event_url`.

## Example

User: "Tell me about Gillette Stadium's seating and the cheapest way in."

`find_venue` gives `vndsnxzj3gr3` (Foxborough, 20 upcoming); the schedule lists the next events; the live sections for the Zach Bryan show list 95 sections, 100s lower bowl, 200s and 300s upper, CL club sections; the get-in sits in the upper 200s at $133 on the primary market (as of 04:36 UTC), against a resale lowest of $76 before fees.
