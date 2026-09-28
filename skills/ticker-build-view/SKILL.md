---
name: ticker-build-view
description: Build a saved View on Ticker that alerts on a price drop or listing collapse, tested on today's market, at the right cadence. Use when the user wants alerts whenever events match a condition.
---

# Build a View

**Plan:** every plan. Saved Views and watched events share one allowance: Free 1, Pro 25, Max 100, Ultra unlimited. Alert destinations (a Slack or Discord channel): Pro 1, Max 5, Ultra 50. A predicate on a primary-market column (`ea.tm_*`, `ea.tmr_*`) needs Max; on Pro the screen refuses it by name.

A View is a saved screen that runs on a schedule. A Match is one event entering it. When a View is created it records what it already holds as baseline Matches, which are never alerted: alerts start with the next market change.

## Steps

1. **Read the columns** with `list_screen_columns` `{}` (free). Pick from it, never from memory. Common legs:
   - price drop: `ea.median_price_pct_1d` `<=` -10 (a one-day % change), or `ea.price_self_z_1d` `<=` -2 (unusual for this event's own swings);
   - listing collapse: `ea.listings_delta_7d` (negative = fewer listings than a week ago) together with `ea.median_price_pct_7d`; never `ea.inventory_velocity_1d`, which is a one-day ratio;
   - scope: `e.sub_category_id` for a league or genre (1 is NFL, 3 is NBA; the column description lists all), `p.name` `contains` for a named act or team, `v.city` for a place, `ea.days_to_event` `between` for a window.
   Always add the freshness leg `{"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}`: a stale row is never a move.
   Done when you hold one predicate in the DSL (`{"all": [...]}` of `{col, op, val}` leaves).

2. **Test it on today's market** with `screen_events` `{"predicate": <p>, "count": true, "limit": 10, "columns": ["e.event_name", "e.local_date", "ea.median_price_current", "ea.median_price_pct_1d", "ea.listings_delta_7d", "ea.last_price_snapshot_date"]}`.
   - `total` 0: read `diagnostics`. `ALL_NULL` on a leg means that column is not computed for these events: change the column. Otherwise loosen one threshold.
   - `total` above 100: tighten a threshold or narrow the scope; a View that matches everything is noise.
   Done when `total` is between 1 and 100, or the user accepts a quiet View, and you have shown them three sample rows.

3. **Pick the cadence.** For one event or a narrow screen, `notification_mode: "instant"` (an email per Match). For a broad screen, `notification_mode: "digest"` (one daily email). Bound volume with `max_firings_per_eval` (default 25). Say which you chose and why.
   Done when mode and cap are fixed.

4. **Check for a twin** with `list_views` `{"limit": 100}`. A View with the same aim or the same predicate already exists: offer `update_view` on it instead of a second one, and stop there unless the user wants both.
   Done when you know there is no twin, or the user chose.

5. **Create it** with `create_view`:
   ```json
   {"name": "<short name the user will recognise>", "predicate": <p>, "channels": ["email"],
    "notification_mode": "digest", "max_firings_per_eval": 25}
   ```
   A validation error names the bad leg: fix that leg and call again. A refusal for the plan's View allowance is final: tell the user the allowance, and leave any delete to them.
   Done when you hold the new View's `id` and `view_url`.

6. **Read back what it will send** with `get_view_alert_preview` `{"view_id": "<id>"}`. A new View shows 0: its first contents are baseline Matches. `paused: true` means the account has alert email switched off; say so.
   Done when you have told the user what the preview says.

7. **Only if the user wants a channel:** `list_destinations`, then `set_view_target` `{"view_id", "delivery_target_id", "cadence": "instant" | "hourly" | "daily"}`. With no destination yet, the user adds one in the app or gives you the channel's posting URL for `create_destination`, which sends a live test message first.
   Done when `list_view_targets` shows the destination on this View.

## Reporting rules

- Tell the user, in plain words: what the View catches, how many events it would hold today (with the `last_price_snapshot_date` of the test), how often it emails, and the `view_url`.
- A Match is an event entering the View. Never report an alert as sent unless `list_matches` shows `delivery_status: "sent"`.
- Name no marketplace.

## Example

User: "Alert me when NFL games in the next month see listings collapse. Once a day is enough."

Predicate `{"all": [{"col": "e.sub_category_id", "op": "=", "val": 1}, {"col": "ea.days_to_event", "op": "between", "val": [0, 30]}, {"col": "ea.listings_delta_7d", "op": "<=", "val": -300}, {"col": "ea.last_price_snapshot_date", "op": ">=", "val": {"days_ago": 1}}]}`; the test holds 12 games today; `create_view` with `notification_mode: "digest"`; the preview shows 0 so far. Answer: "Saved 'NFL listing collapse'. It holds 12 games today (priced 2026-09-28). You will get one email a day listing the games that newly enter it."
