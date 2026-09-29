---
name: sale-calendar
description: Presale and on-sale calendar from Ticker for one act, venue or city, with the named presale windows. Use when the user asks when tickets go on sale, about presales, or what drops this week.
---

# Sale calendar

**Plan:** every plan.

Only events that state a sale date can be on the calendar. Most events state none, and only about 7% of upcoming events state any presale. An empty answer means "no stated dates", never "no sale".

## Steps

1. **Fix the window.** Default: today through 14 days out; 7 days for a city. Write both ends as ISO 8601 with the user's timezone offset when you know it.
   Done when you hold `from` and `to`.

2. **Find the events.** All dates below are full ISO date-times; a bare date is refused.
   - A performer: `search_events` `{"search": "<act>", "onsale_from": from, "onsale_to": to, "sort_by": "onsale_date", "limit": 50}`, then again with `presale_from`/`presale_to` and `"sort_by": "presale1_date"`. Merge the two lists by `event_id`.
   - A venue: the same two calls with `venue_id` from `find_venue` in place of `search`.
   - A city: no tool filters the catalogue by city, and the screener only sees events that already have prices, so this branch pages the whole catalogue and costs many calls. Say so, and offer a venue or an act first. If the user still wants the city: `search_events` `{"onsale_from": from, "onsale_to": to, "sort_by": "onsale_date", "limit": 40, "page": n}` for n = 1 to 5, keeping rows whose `venue.city` is the city or its metro (Chicago is also Rosemont and Evanston); the same for presales. After 5 pages each, stop and say the calendar is partial.
   Done when you hold the list of events with a presale or on-sale inside the window, or know it is empty.

3. **Read the named windows** with `get_event_sale_windows` `{"event_id": "<id>"}` for each event, at most 15 (the soonest first); past 15, list the rest with their dates from step 2 and say their named windows were not read. `presales` are the event's own named windows, oldest first; `end: null` means the window runs to the event. `onsale` is the public window.
   Done when each listed event has its windows, or you have said which ones you did not read.

4. **Report a calendar** ordered by start time: date and time with timezone, window name quoted exactly as the event states it (for example "Artist Presale"), event, venue, link. Put presales and the public on-sale on separate lines.
   Done when every line has a start time and a link.

## Reporting rules

- Quote window names verbatim, as the tool served them, even when a name carries a brand; they are the event's words, not a Ticker category. Add no marketplace name of your own.
- Times from the tools are UTC (`Z`). Convert to the venue's local time, which `local_date` shows with its offset, and say which zone you used.
- Check each weekday against today's date before you write it.
- Say how many events you found and that events stating no date cannot appear.
- Link each event with `event_url`.

## Example

User: "When do Lizzy McAlpine tickets go on sale? Any presales?"

`search_events` with the act and the 14-day on-sale window, then with the presale window; `get_event_sale_windows` for each hit, then:

- Wed Sep 30, 10:00 CT: "Artist Presale Wave 1", Lizzy McAlpine at United Center, Chicago ([link](https://findticker.com/events/ev...))
- Fri Oct 2, 10:00 CT: public on-sale, same event
