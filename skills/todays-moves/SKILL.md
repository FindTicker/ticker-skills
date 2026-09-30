---
name: todays-moves
description: "Today's moves on Ticker: which events entered your saved Views and which watched events fired, since a time you pick. Use when a broker asks what moved today or what their alerts caught."
---

# Today's moves

**Plan:** Pro

**Usual cost:** 3 requests: your Views, the Matches, the watchlist.

What the account's own alerts caught: every event that entered one of its saved Views, and every watched event that fired, since the start of today or a time the user picks. A broker reads it at the end of the day to decide what to act on.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| since | today, from 00:00 UTC | 1 to 14 days back, at 00:00 UTC | the `since` of `list_matches`, as `"<YYYY-MM-DD>T00:00:00Z"` |
| view | every View | one View, by its name | the `view_id` of `list_matches` |
| rows | 25 | 5 to 50 | how many Matches the answer lists |

## Steps

1. **Check the plan and read the Views** with `list_views`, alone, and wait for its answer before any other call: `{"limit": 100}`. `views_cap` 0 means the Free plan: start the answer with this sentence, exactly as written, and stop:
   ```text
   Today's moves reads your saved Views and watched events, which start on the Pro plan: https://findticker.com/plans.
   ```
   That sentence is the whole answer: call no other tool.
   Otherwise note each View's `id` and `name`.
   Done when you know the plan holds Views, and you hold their names.

2. **Read the parameters** from the user's words ("since Monday", "the last 3 days", "only my NBA View", "top 10"); keep the default for the rest. You need today's date: take it from the conversation; if you do not have it, ask. A value outside its range: do not run; say the range ("Since takes 1 to 14 days back.") and ask for a value inside it.
   Done when you hold the `since` time, and a `view_id` if the user named one View.

3. **Read the Matches** with `list_matches` `{"since": "<YYYY-MM-DD>T00:00:00Z", "limit": <rows>}`, adding `"view_id"` for one View. Write `since` with a `Z`, never with an offset: the tool refuses an offset. `origin: "baseline"` Matches were recorded when a View first learned its contents and are never alerted; count them apart.
   Done when you hold the Matches since that time.

4. **Read the watchlist** with `list_watchlist` `{"sort": "last_matched_at", "order": "desc", "limit": 50}`. A watch whose `last_matched_at` is after `since` fired in the window. `alerts_live: false` marks a watch that is starred but not alerting.
   Done when you know which watched events fired in the window.

5. **Report.** First line, the values used: "Values: since 2026-09-29 00:00 UTC, view every View, rows 25." Then, per View with Matches: the View's name (linked with its `view_url`), how many events entered, and a short table (event linked, date, matched at, delivery). Then the watched events that fired, with their `last_matched_at`. Then one line each for: Views with no Match in the window, and watches that are not alerting. End with what to act on first: the events that entered more than one View, or entered a View and fired a watch.
   Done when every live Match in the window is counted and the first rows are listed.

## Reporting rules

- Quote each time as the tool gave it, in UTC.
- An alert went out only when `delivery_status` is `sent`. Any other value (`not_sent`, `pending`, `held`) is a Match that did not reach the inbox yet or will not; say which.
- A Match is an event entering a View, not a sale and not a price.
- Link each event with its `event_url` and each View with its `view_url`. Name no marketplace. Never write "sold".
- Call the emails "the hourly email" or "the daily email"; never "digest".
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "What did my alerts catch today?"

`list_views` shows 25 Views; `list_matches` since 00:00 UTC returns 7 live Matches in 3 Views; the watchlist has 2 events that fired. Answer: "Values: since 2026-09-29 00:00 UTC, view every View, rows 25." Then the three Views with their events, the two watched events, and "Act first on Oh, Mary! in San Diego: it entered two Views today."
