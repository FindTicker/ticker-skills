# How the skills reach people, plan by plan

**Replaced on 2026-09-30.** alim decided that the skills go out from this repository, public, installed by link, and that the plan is checked by the Ticker tools, not by the skill files. The marketplace now holds one plugin, `ticker`, with all 24 skills; the README says how each app installs it. The rest of this page is the per-plan design it replaced, kept for its vendor research and its limits.

alim, 2026-09-29: "per plan the skills, need to see which ones go where". Each plan gets its own bundle. This page says, client by client, how an account on each plan gets its bundle today, and where a client can not do it per plan. Vendor documentation read on 2026-09-28 and 2026-09-29; links at the end.

## The bundles

A skill's plan lives in one place: the `**Plan:**` line of its `SKILL.md`. A bundle is a list, built from those lines by `scripts/bundles.py`: the skills of its plan and of every plan below it. No skill file is copied.

| Bundle | Plugin name | Skills | Who gets it |
|---|---|---|---|
| Free | `ticker` | 6 | everyone; the public bundle, the only one in the Claude and ChatGPT listings |
| Pro | `ticker-pro` | 12 (Free + 6) | Pro accounts |
| Max | `ticker-max` | 18 (Pro + 6) | Max accounts |
| Ultra | `ticker-ultra` | 24 (Max + 6) | Ultra accounts |

`python3 scripts/bundles.py list max` prints the Max bundle. `python3 scripts/bundles.py marketplace` writes the four plugins into `.claude-plugin/marketplace.json`, and `check` fails when that file and the plan lines disagree. `python3 scripts/bundles.py build` writes, for each bundle, a plugin ZIP and a skills-only ZIP into `dist/` (not committed). The two Free ZIPs are the public download (docs.findticker.com/docs/skills); the Ticker app serves the paid ones (ENG-1829). Every ZIP carries a README of its own plan, written by `bundles.py`: that plan's skills, the install lines, and no skill of a higher plan or install from this private repository.

Every skill still checks the account's plan through the tools, because a person can copy a skill folder by hand: a skill run on a lower plan says which plan opens it and runs the closest skill of that plan. The tools enforce the plan either way.

## Client by client

| Client | Free | Pro, Max, Ultra | Per plan today? |
|---|---|---|---|
| Claude Code | `/plugin marketplace add FindTicker/ticker-skills`, then `/plugin install ticker@ticker` | the same marketplace, then `/plugin install ticker-max@ticker` (or `ticker-pro`, `ticker-ultra`) | Yes, four plugins in one marketplace. Tested: each installs its own list of skills and the Ticker MCP server. Nothing stops a Free person installing `ticker-max`: the skills then say which plan opens them, and the tools refuse what the plan does not hold |
| claude.ai, Claude desktop, Cowork | the Claude directory listing (connector plus the Free plugin), or upload of `dist/ticker-plugin.zip` | upload of the plan's ZIP (`dist/ticker-max-plugin.zip`) under Customize, Plugins, Upload plugin; or add this repository as a marketplace and pick the plan's plugin | Partly. A person can install any plugin by hand. An organization owner can install one for everyone, but for the whole organization, not by plan. There is no hook that gives a person a plugin because of their Ticker plan |
| ChatGPT (apps and plugins directory) | the listing, submitted "With MCP" with the Free skills only | no route | No. One submission carries one skill bundle, and skills imported from an MCP server are a snapshot taken at submission, not read per person. A paid bundle in ChatGPT has no route today |
| Codex, Cursor, GitHub Copilot, Gemini CLI | `npx skills add FindTicker/ticker-skills --skill <name>` once per Free skill name (several `--skill` flags in one command) | the same, with the names that `bundles.py list <plan>` prints | By hand only. The installer copies what it is told to; nothing checks the plan |
| The MCP server itself | not served | not served | Not built. The MCP "Skills over MCP" extension could serve each account its plan's skills, since the server knows the plan. Claude does not read that extension yet, and ChatGPT reads it only as a snapshot at submission |

## What does not exist, and the one piece that would close it

- **A per-plan download in the app.** A paid account has no place in Ticker to get its bundle: it has to find this repository. A page in the app (Settings or Connect AI) that serves the plan's ZIP and its install lines would give each plan its bundle in every client that takes a ZIP or a folder. Not built here; a ticket draft is in the pull request.
- **Per-person gating in Claude and ChatGPT.** Neither vendor documents a way for a third-party product to give different skills to different users by their plan. Only the product can: through its own download, or later through Skills over MCP.
- **A private paid bundle.** When this repository goes public, every skill file is readable by anyone, the Ultra ones too. The data stays behind the plan; the instructions do not. Keeping paid skills private means serving them from the app instead of from a public repository.

## Limits that shaped the files

- **Name:** lowercase letters, digits and hyphens, at most 64 characters, equal to the folder name. OpenAI also caps `plugin-name:skill-name` at 64: the longest here, `ticker-ultra:performer-concentration`, is 36.
- **Description:** at most 1,024 characters in the open format; an older Claude help article says 200, so every description here is 200 or fewer.
- **Body:** under 500 lines is the open format's advice. Ours run 50 to 95 lines.
- **Claude plugin:** no top-level `bin/`; a README of at least 40 words and a LICENSE to be listed; the repository public before a listing goes live.
- **Claude Code marketplace:** a plugin entry whose `source` is the marketplace root and which lists `skills` loads only those folders, and the entry is the plugin's manifest when the plugin has no `plugin.json`. That is why the repository has no `.claude-plugin/plugin.json`: each bundle's manifest is its entry in `marketplace.json`.
- **OpenAI:** each skill an immediate child of `skills/`; a skills-only ZIP must not contain `.mcp.json` (the `-skills.zip` files do not).

## What was tested here

- The four plugins installed from this repository's marketplace into a throwaway Claude Code configuration (Claude Code 2.1.284): `ticker` loaded the Free skills, `ticker-pro` the Pro bundle, `ticker-max` the Max bundle and `ticker-ultra` all of them, each with one MCP server, `ticker`. `claude plugin validate` passed on the marketplace.
- Each skill was run by Claude Code in print mode from one user prompt, with this repository's skills as the only skills and the Ticker MCP server as the only tools, as the test account of each plan.
- Not tested: a claude.ai upload, the OpenAI portal, Cursor, Codex, Copilot and Gemini.

## Decisions for alim

1. **The plugin names.** `ticker` for the public Free bundle, and `ticker-pro`, `ticker-max`, `ticker-ultra`. In Claude Code a skill shows as `ticker-max:hot-events`.
2. **The per-plan download in the app** (the ticket draft), or leave paid bundles to this repository.
3. **Public or private paid skills.** A public repository shows every skill's instructions; the data behind them stays gated.
4. **A licence** (the Claude directory needs one) and **the day the repository goes public**.

Sources: [agentskills.io specification](https://agentskills.io/specification), [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference), [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [Claude plugins overview](https://claude.com/docs/plugins/overview), [Claude skills how-to](https://claude.com/docs/skills/how-to), [Claude directory publishing](https://claude.com/docs/directory/publish), [OpenAI plugin submission](https://developers.openai.com/plugins/deploy/submission), [OpenAI skills](https://developers.openai.com/plugins/build/skills), [Codex skills](https://developers.openai.com/codex/skills), [Cursor skills](https://cursor.com/docs/context/skills), [Copilot agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [Gemini CLI skills](https://geminicli.com/docs/cli/skills/), [vercel-labs/skills](https://github.com/vercel-labs/skills), [SEP-2640 Skills extension](https://modelcontextprotocol.io/seps/2640-skills-extension).
