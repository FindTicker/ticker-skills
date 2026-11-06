---
name: pre-purchase-check
description: "Former name of the event-check skill, kept so existing installs and saved commands keep working. Runs event-check."
disable-model-invocation: true
---

# pre-purchase-check (renamed)

This skill is now `event-check`. Load the `event-check` skill and run it on the user's request. Follow that skill in full: its plan, parameters, steps and reporting rules apply unchanged.

If `event-check` is not installed, answer with this sentence and stop:

```text
This skill is now called event-check. Update the Ticker plugin to get it.
```
