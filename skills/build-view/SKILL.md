---
name: build-view
description: Build a saved View on Ticker that alerts when events enter a screen, tested on today's market, at the right cadence. Use when the user wants alerts whenever events match a condition or a screen.
---

# Build a View

**Plan:** Pro

**Usual cost:** 4 requests: the Views list, one test screen, the create, the preview. `list_screen_columns` is free.

A View is a saved screen that runs on a schedule. A Match is one event entering it. When a View is created it records what it already holds as baseline Matches, which are never alerted: alerts start with the next market change. Saved Views and watched events share one allowance: Free 0 Views, Pro 25, Max 100, Ultra no cap. A View with a primary-market leaf (`ea.tm_*`) needs Max.

## Parameters

| Parameter | Default | Range | Sets |
|---|---|---|---|
| screen | none: ask for one | an installed screen skill by name (its parameters too, inside its ranges), or a condition in words | the predicate |
| delivery | the daily email | instant, the hourly email, the daily email, or muted | `notification_mode` and `notification_cadence` |
| cap per run | 25 | 1 to 100 | `max_firings_per_eval` |
| name | the screen's name | up to 120 characters | `name` |

Read the values from the user's words ("hot events in Boston", "once a day", "don't email me yet", "call it Boston heat"); keep the default for the rest. A value outside its range: do not write; say the range and ask for a value inside it. The first line of the answer says the values used.

## Steps

1. **Check the plan and look for a twin** with `list_views`, alone, and wait for its answer before any other call: `{"limit": 100}`. `views_cap` 0 means the Free plan: write this sentence, exactly as written, and stop:
   ```text
   Saved Views start on the Pro plan: https://findticker.com/plans.
   ```
   That sentence is the whole answer: call no other tool.
   When `counts.all` already equals `views_cap`, tell the user the plan's Views are all in use before you create one. A View with the same aim or the same predicate already exists: offer `update_view` on it instead of a second one, and stop there unless the user wants both.
   Done when you know the plan holds Views and there is no twin, or the user chose.

2. **Build the predicate.**
   - **A screen skill** (any installed skill with a `## The screen` table, such as `price-drop`): load that skill and take the leaves of its `## The screen` table as they are. For the two resale-against-primary screens, take the three leaves and the match leg. Change no threshold unless the user asks. A screen that reads the primary market needs Max: call `list_screen_columns` `{}` and, if `ea.tm_percent_remaining` or `ea.tm_lowest_aip_price_current` has `locked: true`, write "This screen reads the primary market, which the Max plan opens: https://findticker.com/plans." and stop.
   - **Anything else:** read the columns with `list_screen_columns` `{}` and pick from it, never from memory. Price drop: `ea.median_price_pct_1d` `<=` -10 (a one-day % change), or `ea.price_self_z_1d` `<=` -2 (unusual for this event's own swings). Listing collapse: `ea.listings_delta_7d` together with `ea.median_price_pct_7d`; never `ea.inventory_velocity_1d`, a one-day ratio. Scope: `e.sub_category_id` for a league or genre, `p.name` `contains` for a named act or team, `v.city` for a place, `ea.days_to_event` `between` for a window.
   Always keep the freshness leaf `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}`: a stale row is never a move.
   Done when you hold one predicate in the DSL (`{"all": [...]}`).

3. **Test it on today's market** with `screen_events` `{"predicate": <p>, "count": true, "diagnostics": true, "limit": 3, "columns": ["e.event_name", "e.local_date", "ea.median_price_current", "ea.last_price_snapshot_date"]}`. `diagnostics.root.passed` is how many events it holds today (`total` stops at 1,000).
   - 0: read `diagnostics`. `ALL_NULL` on a leg means that column is not computed for these events: change the column. Otherwise loosen one threshold.
   - Over 100 on a screen you built: offer a scope (a city, a category, a window). A screen skill's View stays as it is unless the user narrows it: it alerts only on events that newly enter.
   Done when you have shown the user the count and three sample rows.

4. **Pick the cadence.** For one event or a narrow screen, `notification_mode: "instant"` (an email per Match). For a broad screen, `notification_mode: "digest"` with `notification_cadence` `"hourly"` or `"daily"` (Matches wait for the hourly email or the daily email). `muted` records Matches and sends nothing. Bound volume with `max_firings_per_eval` (default 25). Take what the user asked for, and say which you chose and why.
   Done when mode and cap are fixed.

5. **Create it** with `create_view`:
   ```json
   {"name": "<short name the user will recognise>", "predicate": <p>, "channels": ["email"],
    "notification_mode": "digest", "notification_cadence": "daily", "max_firings_per_eval": 25}
   ```
   A validation error names the bad leg: fix that leg and call again. A refusal for the plan's View allowance is final: tell the user the allowance, and leave any delete to them.
   Done when you hold the new View's `id` and `view_url`.

6. **Read back what it will send** with `get_view_alert_preview` `{"view_id": "<id>"}`. A new View shows 0: its first contents are baseline Matches. `paused: true` means the account has alert email switched off; say so.
   Done when you have told the user what the preview says.

7. **Only if the user wants a channel:** `list_destinations`, then `set_view_target` `{"view_id", "delivery_target_id", "cadence": "instant" | "hourly" | "daily"}`. With no destination yet, the user adds one in the app or gives you the channel's posting URL for `create_destination`, which sends a live test message first.
   Done when `list_view_targets` shows the destination on this View.

## Reporting rules

- Tell the user, in plain words: what the View catches (in the app's column words), how many events it would hold today with the `last_price_snapshot_date` of the test, how often it emails, and the `view_url`.
- A Match is an event entering the View. Never report an alert as sent unless `list_matches` shows `delivery_status: "sent"`.
- Call the emails "the hourly email" or "the daily email"; never "digest", which names another feature.
- Name no marketplace. Never write "sold".
- To remove a View, `delete_view` `{"view_id"}`.
- Say primary market and resale, never "book", even where a tool's text does. Name a higher plan only with this skill's plan sentence; never write "upgrade" or "unlock".

## Example

User: "Save the hot-events screen as an alert, once a day is enough."

`list_views` shows 8 of 100 Views and no twin; the `hot-events` table gives five leaves; `list_screen_columns` shows the primary columns open; the test holds 230 events today (priced 2026-09-29); `create_view` with `notification_mode: "digest"`; the preview shows 0 so far. Answer: "Saved 'Hot events'. It holds 230 events today. You will get the daily email with the events that newly enter it."
