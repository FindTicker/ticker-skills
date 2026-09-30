---
name: sale-calendar
description: "On-sale and presale calendar on Ticker for one city or one act: which events go on sale or open a presale in the coming days. Use when the user asks when tickets go on sale or when a presale starts."
---

# Sale calendar

**Plan:** Free

**Usual cost:** 1 request (one search or one screener run).

The public on-sale dates and the first presale dates coming up for one act, or for every event in one city. A broker plans the week around these.

## Parameters

Every threshold of this skill is in this table.

| Parameter | Default | Range | Sets |
|---|---|---|---|
| city or act | none: ask for one | one city (a metro takes all its cities: New York is also Brooklyn, Flushing, Elmont, Newark), or one act or team name | the city screen, or the act search |
| days ahead | 30 | 1 to 90 | the window, from today |
| dates | both | on-sale, presale, or both | which date columns count |
| rows | 30 | 5 to 50 | how many events the answer lists |

## Steps

1. **Read the parameters** from the user's words ("in Boston", "Zach Bryan", "next two weeks", "presales only"). With neither a city nor an act, ask for one and stop. A value outside its range: do not run; say the range ("Days ahead takes 1 to 90.") and ask for a value inside it.
   Done when you hold a city or an act, and the window.

2. **One act:** call `search_events` `{"search": "<act name>", "status": "active", "limit": 100}` with ONE name, never the act and a venue together. Keep the rows whose act is the one asked for (drop tribute acts and venues that share the name), and whose `onsale_date` or `presale1_date` falls between now and the end of the window.
   **One city:** call `screen_events`:
   ```json
   {"predicate": {"all": [
      {"col": "v.city", "op": "in", "val": [<cities>]},
      {"any": [
        {"all": [{"col": "e.onsale_date", "op": ">=", "val": {"days_ago": 0}},
                 {"col": "e.onsale_date", "op": "<=", "val": {"days_ago": -<days ahead>}}]},
        {"all": [{"col": "e.presale1_date", "op": ">=", "val": {"days_ago": 0}},
                 {"col": "e.presale1_date", "op": "<=", "val": {"days_ago": -<days ahead>}}]}]}]},
    "sort": {"col": "e.onsale_date", "dir": "asc"},
    "columns": ["e.event_name", "e.local_date", "v.venue_name", "e.onsale_date", "e.presale1_date"],
    "count": true, "limit": <rows>, "apply_floor": false, "exclude_stale": false}
   ```
   Keep only the on-sale group or only the presale group when the user asked for one kind. Negative `days_ago` counts into the future.
   Done when you hold the events with a date inside the window.

3. **Report.** First line, the values used (a skill of a higher plan that handed over to this one puts its plan sentence above it): "Values: city New York, days ahead 30, dates both, rows 30." Then one line per event, in date order: the date and time of the on-sale or presale (as the tool gave it, in UTC), the kind (on-sale or presale), the event (linked), its date and venue. Close with the count ("25 events open a sale in the next 30 days").
   Done when every event in the window is listed, up to `rows`.

## Reporting rules

- Quote each date as the tool gave it and say it is UTC. You do not know the user's time zone unless they said it.
- An empty `onsale_date` means unknown, not "on sale now". Only about a third of events carry one.
- The city screen sees only events Ticker already prices; an event not yet listed on resale can be missing. Say so once.
- Link each event with its `event_url`. Name no marketplace, and quote no presale code or presale name.
- The named presale windows of an event (their names and every window) are read on the Max plan: https://findticker.com/plans. Say so only when the user asks for them.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "What goes on sale in New York in the next month?"

One city screen. Answer: "Values: city New York, Brooklyn, Flushing, Elmont, Newark, days ahead 30, dates both, rows 30." Then lines such as "2026-09-30 14:00 UTC, on-sale: John Summit, Brooklyn, 2026-11-29", and "25 events open a sale in the next 30 days."
