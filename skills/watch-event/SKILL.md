---
name: watch-event
description: Watch an event on Ticker with the alert the user wants: star it, arm triggers at the right thresholds, say where alerts go. Use when the user asks to watch or track an event, or to hear when it moves.
---

# Watch an event

**Plan:** Pro

**Usual cost:** 5 requests: search, watchlist, plan check, the watch, the defaults. `list_watch_triggers` is free.

Watched events and saved Views share one allowance: Free 1, Pro 25, Max 100, Ultra no cap. A plan over its allowance still stars the event, but only its newest watches alert; the result says which ones stopped. On Free the one slot goes to the newest star.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| event | none: ask for one | one event: an act, team or venue name, with a date when the act plays more than once | the `search_events` call |
| move | 10% | the `pct_move` range `list_watch_triggers` gives (5 to 100 today) | `pct_move` `threshold` |
| price | lowest | lowest or median | `pct_move` `metric` |
| window | 1 day | 1 day or 7 days | `pct_move` `window` (`1d` or `7d`) |
| alerts off | none | on-sale, presale, event week and low inventory (one switch, `lifecycle`); unusual move (`price_z`) | `{"enabled": false}` on each |
| delivery | instant | instant, the hourly or daily email (`digest`), or muted | `notification_mode` |

Read the values from the user's words ("15 percent", "the median", "over a week", "no presale emails", "don't email me yet"); keep the default for the rest. A value outside its range: do not write; say the range and ask for a value inside it. The first line of the answer says the values used.

## Steps

1. **Find the event.** Use an `event_id` you already have. Otherwise call `search_events` with `search` set to ONE name: the act, the team or the venue, never two together and never the whole title. Add `status: "active"`, and when the user named a date, `date_from` and `date_to` as full ISO date-times (`2026-10-02T00:00:00Z`), with `date_to` one day after the named date: the filter reads UTC, and an evening show in the Americas falls on the next UTC day. Pick the row by its `local_date` and venue; if two rows fit, ask.
   Done when you hold one `event_id`.

2. **Read the trigger catalogue** with `list_watch_triggers` `{}` (free). Each trigger has a `key`, its `params` with `min`, `max` and `default`, and sometimes a `caveat`. A value outside the range is clamped, not refused, so check the range before you write.
   Done when you know which keys and params express the user's wish.

3. **Map the wish to triggers.** Common asks:
   - "price drops 10%": `pct_move` enabled, `params: {"metric": "lowest", "window": "1d", "threshold": 10}` (use `median` when the user means the typical price, `7d` for a weekly move). It fires on a move either way; there is no drop-only setting, so tell the user a 10% rise alerts too. For drops only, offer a saved View on this event instead (the `build-view` skill).
   - "anything unusual": `price_z` enabled (on by default, `threshold` is the sensitivity).
   - "tickets disappearing": `absorption`; say its caveat: listings leaving are not confirmed sales.
   - "on-sale, presale, event week, low inventory": `lifecycle` (on by default).
   Turn off with `{"enabled": false}` every default trigger the user said they do not want. Name every trigger you arm and every one you turn off.
   Done when you hold one `triggers` object.

4. **Check the watchlist and the plan.** Call `list_watchlist` `{"search": "<event name>"}`: if the event is already watched, `watch_event` would return the old watch unchanged, so use `update_watch` `{"event_id", "triggers"}` instead. Then call `list_views` `{"limit": 1}`: `views_cap` 0 means the Free plan. On Free, write this sentence, exactly as written, before you write the watch:
   ```text
   On the Free plan one watched event alerts at a time, and a new watch takes that slot; the Pro plan keeps 25: https://findticker.com/plans.
   ```
   Done when you know whether to create or update, and the plan's rule is said.

5. **Write it** with `watch_event` `{"event_id": "<id>", "triggers": {...}, "notification_mode": "instant"}`, or `update_watch` from step 4. `notification_mode` takes `instant` (an email as each alert fires), `digest` (alerts wait for the hourly email or the daily email) or `muted` (recorded, never emailed). Take what the user asked for; `instant` when they did not say.
   Done when the result is back. Read `alerts_live`: false means this watch is starred but not alerting. Read `dormanted`: every event listed there stopped alerting to make room; tell the user by name.

6. **Say where alerts go.** Alerts are emailed to the account. `get_watch_defaults` shows the destinations a new watch also delivers to; `list_destinations` names them. Do not change the defaults unless asked: `set_watch_defaults` is account-wide.
   Done when you have told the user: the event, each armed trigger with its threshold, the delivery mode, and where it goes.

## Reporting rules

- Quote thresholds in the user's terms ("the lowest price moves 10% in a day"), then the trigger key in brackets.
- Never promise an alert fires at a price: triggers compare moves, and prices are read a few times a day.
- Call the emails "the hourly email" or "the daily email"; never "digest", which names another feature.
- Link the event with its `event_url`. Name no marketplace. Never write "sold".
- To stop watching, `unwatch_event` `{"event_id"}` removes the star.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Watch the Cowboys Thursday game and ping me if the lowest price drops more than 10% in a day. No presale or event-week emails."

`search_events` finds the game; `list_watch_triggers` shows `pct_move` threshold 5 to 100; `list_watchlist` shows it is not watched; `list_views` shows a cap of 25; `watch_event` with `{"pct_move": {"enabled": true, "params": {"metric": "lowest", "window": "1d", "threshold": 10}}, "lifecycle": {"enabled": false}}`. Answer: "Watching Buccaneers at Cowboys, Oct 8. Armed: lowest price moves 10% in a day, either way (pct_move); unusual price move stays on at the default (price_z). Off: on-sale, presale, event week and low inventory (lifecycle). Alerts are emailed as they fire."
