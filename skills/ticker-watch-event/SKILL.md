---
name: ticker-watch-event
description: Watch an event on Ticker with the alert the user actually wants: star it, arm the right triggers at the right thresholds, and say where alerts will go. Use when the user asks to watch, track or star an event, or to be told when its price or inventory moves.
---

# Watch an event

**Plan:** every plan. Watched events and saved Views share one allowance: Free 1, Pro 25, Max 100, Ultra unlimited. A plan over its allowance still stars the event but only its newest watches alert; the result says which ones stopped.

## Steps

1. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC, and an evening show in the Americas falls on the next UTC day. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

2. **Read the trigger catalogue** with `list_watch_triggers` `{}` (free). Each trigger has a `key`, its `params` with `min`, `max` and `default`, and sometimes a `caveat`. A value outside the range is clamped, not refused, so check the range before you write.
   Done when you know which keys and params express the user's wish.

3. **Map the wish to triggers.** Common asks:
   - "price drops 10%": `pct_move` enabled, `params: {"metric": "lowest", "window": "1d", "threshold": 10}` (use `median` when the user means the typical price, `7d` for a weekly move). It fires on a move either way; there is no drop-only setting, so tell the user a 10% rise alerts too. For drops only, offer a saved View on this event instead (the `ticker-build-view` skill).
   - "anything unusual": `price_z` enabled (on by default, `threshold` is the sensitivity).
   - "tickets disappearing": `absorption`; say its caveat: listings leaving are not confirmed sales.
   - "on-sale, presale, event week, low inventory": `lifecycle` (on by default).
   Turn off with `{"enabled": false}` every default trigger the user said they do not want. Name every trigger you arm and every one you turn off.
   Done when you hold one `triggers` object.

4. **Check for an existing watch** with `list_watchlist` `{"search": "<event name>"}`. If the event is already watched, `watch_event` returns the old watch unchanged, so use `update_watch` `{"event_id", "triggers"}` instead, which changes only the triggers you name.
   Done when you know whether to create or update.

5. **Write it** with `watch_event` `{"event_id": "<id>", "triggers": {...}, "notification_mode": "instant"}` (`digest` for one daily email, `muted` to record without sending), or `update_watch` from step 4.
   Done when the result is back. Read `alerts_live`: false means this watch is starred but not alerting. Read `dormanted`: every event listed there stopped alerting to make room; tell the user by name.

6. **Say where alerts go.** Alerts are emailed to the account. `get_watch_defaults` shows the destinations a new watch also delivers to; `list_destinations` names them. Do not change the defaults unless asked: `set_watch_defaults` is account-wide.
   Done when you have told the user: the event, each armed trigger with its threshold, the delivery mode, and where it goes.

## Reporting rules

- Quote thresholds in the user's terms ("the lowest price moves 10% in a day"), then the trigger key in brackets.
- Never promise an alert fires at a price: triggers compare moves, and the price data is read a few times a day.
- Link the event with its `event_url`. Name no marketplace.

## Example

User: "Watch the Cowboys Thursday game and ping me if the lowest price drops more than 10% in a day. No presale or event-week emails."

`search_events` finds the game; `list_watch_triggers` shows `pct_move` threshold 5 to 100; `list_watchlist` shows it is not watched; `watch_event` with `{"pct_move": {"enabled": true, "params": {"metric": "lowest", "window": "1d", "threshold": 10}}, "lifecycle": {"enabled": false}}`. Answer: "Watching Buccaneers at Cowboys, Oct 8. Armed: lowest price moves 10% in a day (pct_move); unusual price move stays on at the default (price_z). Off: on-sale, presale, event week and low inventory (lifecycle). Alerts are emailed as they happen."
