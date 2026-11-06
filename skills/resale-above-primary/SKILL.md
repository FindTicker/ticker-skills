---
name: resale-above-primary
description: "Former name of the resale-vs-face skill, kept so existing installs and saved commands keep working. Runs resale-vs-face."
disable-model-invocation: true
---

# resale-above-primary (renamed)

This skill is now `resale-vs-face`. Load the `resale-vs-face` skill and run it on the user's request with direction above face, unless the request says otherwise. Follow that skill in full: its plan, parameters, steps and reporting rules apply unchanged.

If `resale-vs-face` is not installed, answer with this sentence and stop:

```text
This skill is now called resale-vs-face. Update the Ticker plugin to get it.
```
