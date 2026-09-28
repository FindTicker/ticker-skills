---
name: ticker-sale-calendar
description: Presale and on-sale calendar from Ticker for one performer or one city: what goes on sale when, and the named presale windows before it. Use when the user asks when tickets go on sale, about presales, or what drops this week.
---

# Sale calendar

**Plan:** every plan.

Only events that state a sale date can be on the calendar. Most events state none, and only about 7% of upcoming events state any presale. An empty answer means "no stated dates", never "no sale".

## Steps

1. **Fix the window.** Default: today through 14 days out for a performer, 7 days for a city. Write both ends as ISO 8601 with the user's timezone offset when you know it.
   Done when you hold `from` and `to`.

2. **Find the events.**
   - A performer: `search_events` `{"search": "<act>", "onsale_from": from, "onsale_to": to, "sort_by": "onsale_date", "limit": 50}`, then again with `presale_from`/`presale_to` and `"sort_by": "presale1_date"`. Merge the two lists by `event_id`.
   - A city: `search_events` has no city filter and the screener only sees events that already have prices, so page the catalogue by sale window and keep the city yourself. Call `search_events` `{"onsale_from": from, "onsale_to": to, "sort_by": "onsale_date", "limit": 40, "page": n}` for n = 1, 2, 3... and keep rows whose `venue.city` is the city (a metro spans several cities: Chicago is also Rosemont and Evanston). A page cut short says `meta.truncated`; lower `limit` rather than repeat it. Stop at the last page or after 10 pages; past 10, say the calendar is partial and offer a shorter window. Do the same with `presale_from`/`presale_to` when the user asked about presales.
   Done when you hold the list of events with a presale or on-sale inside the window, or know it is empty.

3. **Read the named windows** with `get_event_sale_windows` `{"event_id": "<id>"}` for each event, at most 15 (the soonest first). `presales` are the event's own named windows, oldest first; `end: null` means the window runs to the event. `onsale` is the public window.
   Done when each listed event has its windows, or you have said which ones you did not read.

4. **Report a calendar** ordered by start time: date and time with timezone, window name quoted exactly as the event states it (for example "Artist Presale"), event, venue, link. Put presales and the public on-sale on separate lines.
   Done when every line has a start time and a link.

## Reporting rules

- Quote window names verbatim; they are the event's words, not a Ticker category.
- Times from the tools are UTC (`Z`). Convert to the venue's local time, which `local_date` shows with its offset, and say which zone you used.
- Say how many events you found and that events stating no date cannot appear.
- Name no marketplace; link with `event_url`.

## Example

User: "What's going on sale in Chicago this week?"

`search_events` pages over the 7-day on-sale window, rows kept where `venue.city` is Chicago, `get_event_sale_windows` for each, then:

- Tue Sep 29, 10:00 CT: "Artist Presale", Event A at Venue B ([link](https://findticker.com/events/ev...))
- Fri Oct 2, 10:00 CT: public on-sale, Event A
