# How these skills reach people

Question: when someone installs the Ticker MCP server, how do they get these skills with it? Answered from each vendor's own documentation, read on 2026-09-28. Links are at the end of each section.

## The answer in five lines

1. One unchanged `skills/<name>/SKILL.md` folder works in every client below. They all read the open Agent Skills format.
2. A skill cannot carry an MCP connection. What bundles skills with an MCP server is a **plugin**, and each vendor has its own plugin manifest.
3. "Installed with the MCP" is one step only in Claude Code: installing the plugin starts its MCP server. In claude.ai it is one plugin install, then one Connect click. In ChatGPT it is one plugin that holds both the server and the skills. Everywhere else, skills and the MCP server are two installs.
4. The MCP server itself can now carry skills (the MCP "Skills over MCP" extension, final since 2026-09-13). Today only ChatGPT reads it (partly, as a snapshot taken at submission), plus two developer tools. Claude does not read it yet. Our server serves tools only: `prompts/list` and `resources/list` answer "Method not found" (measured on the development deployment, 2026-09-28).
5. This repo is laid out so the same `skills/` folder feeds all of these routes. Which routes to use is alim's decision; the options are at the end.

## Client by client

| Client | How it takes a skill | One SKILL.md unchanged? | What "installed with the MCP" can honestly mean |
|---|---|---|---|
| Claude Code | `.claude/skills/`, `~/.claude/skills/`, or a plugin's `skills/` | Yes | One install: `/plugin install` adds the skills and starts the plugin's MCP server; `/mcp` signs in |
| claude.ai, Claude desktop, Cowork | A skill ZIP under Customize, Skills; or a plugin (ZIP upload or a GitHub marketplace) | Yes | One plugin install; the skills load at once; the user clicks Connect on the plugin's Connectors tab to sign in |
| Claude directory | Connectors and plugins are separate listings; "Skills aren't a submission type on their own" | Yes, inside a plugin | Two submissions (the connector, then a plugin whose `.mcp.json` points at the same URL), paired as one listing |
| Claude API | Upload with `POST /v1/skills`, then name the skill in `container.skills` | Yes | No bundle. The MCP connector (`mcp_servers`) sits beside skills in a request; the docs do not show the two together |
| ChatGPT (apps and plugins directory) | Portal submission: "Skills only", or "With MCP" with an uploaded skill bundle, or skills imported from the MCP server at submission | Yes (same open format) | One plugin holding the server and the skills. A server already live in ChatGPT is submitted again from scratch as a new MCP-backed plugin |
| Codex, ChatGPT desktop | `.agents/skills/`, `$HOME/.agents/skills/`, or a Codex plugin | Yes | A plugin (`codex plugin marketplace add owner/repo`) carries both; a bare skill can only name the server it needs |
| Cursor | `.agents/skills/`, `.cursor/skills/`, `.claude/skills/` | Yes | A Cursor plugin, or the vendor-neutral Agent Plugins format, carries both |
| GitHub Copilot, VS Code | `.github/skills/`, `.claude/skills/`, `.agents/skills/` | Yes | An Agent Plugins plugin; bare skill folders carry no MCP |
| Gemini CLI | `.gemini/skills/`, `.agents/skills/`, `gemini skills install <git url>` | Yes | A Gemini extension (`gemini-extension.json`) carries both |
| `npx skills` (open installer, 50+ agents) | Reads a GitHub repo's `skills/` folder; `--skill <name>` for one | Yes | Skills only; it never configures an MCP server |
| The MCP server itself | Skills served as resources under the Skills over MCP extension (`skills/list`, `skills/get`, `skill://` resources) | Yes | The real "attached everywhere" answer, once clients read it. Today: ChatGPT partly (a snapshot at submission), fast-agent, MCP Inspector |

Sources: [agentskills.io specification](https://agentskills.io/specification), [Claude skills how-to](https://claude.com/docs/skills/how-to), [Claude plugins overview](https://claude.com/docs/plugins/overview), [build a Claude plugin](https://claude.com/docs/plugins/build), [Claude directory publishing](https://claude.com/docs/directory/publish), [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference), [Claude Code marketplaces](https://code.claude.com/docs/en/plugins/marketplace-reference), [Claude API skills guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide), [OpenAI plugin submission](https://developers.openai.com/plugins/deploy/submission), [OpenAI submission errors](https://developers.openai.com/plugins/deploy/submission-errors), [OpenAI MCP server skills import](https://developers.openai.com/plugins/build/mcp-server), [Codex skills](https://developers.openai.com/codex/skills), [Cursor skills](https://cursor.com/docs/context/skills), [Copilot agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [Gemini CLI skills](https://geminicli.com/docs/cli/skills/), [vercel-labs/skills](https://github.com/vercel-labs/skills), [SEP-2640 Skills extension](https://modelcontextprotocol.io/seps/2640-skills-extension), [MCP extension support matrix](https://modelcontextprotocol.io/extensions/client-matrix), [Agent Plugins](https://agent-plugins.org/).

One string on the ticket, "Drop a skill ZIP or folder here", is from the OpenAI portal, which needs a login. The public docs describe the same step as "Upload the final skill bundle"; the exact wording was not checked.

## Limits that shaped the files

- **Name:** lowercase letters, digits and hyphens, at most 64 characters, equal to the folder name (the open format). OpenAI also caps `plugin-name:skill-name` at 64: `ticker:ticker-underpriced-events` is 32.
- **Description:** at most 1,024 characters in the open format, claude.com and OpenAI. An older Claude help article still says 200, so every description here is 200 or fewer.
- **Body:** under 500 lines is the open format's advice. Ours run 42 to 60 lines.
- **Claude plugin:** no top-level `bin/` (chat and Cowork refuse the whole plugin); a README of at least 40 words and a LICENSE to be listed; the repository must be public before the listing goes live.
- **OpenAI:** each skill an immediate child of `skills/`; a skills-only ZIP must not contain `.mcp.json`; up to 5 skills can be imported from an MCP server.

## What was tested here

- Each skill was run by Claude Code in print mode, from one user prompt, with the 12 skills in `.claude/skills/` and the Ticker MCP server as the only tools. Reads ran as test accounts on the development deployment; writes ran on a private local copy of the backend. Transcripts are in `evidence/`.
- `claude --plugin-dir .` on this repository loaded all 12 skills as `ticker:ticker-...`. The plugin's MCP half (`.mcp.json`) was not started in that test, because starting it would also start the tester's own MCP servers; Claude Code's documentation says a plugin's MCP servers start when the plugin is enabled.
- Not tested: a claude.ai upload, the OpenAI portal, Cursor, Codex, Copilot and Gemini.

## The layout chosen, and why

```
skills/<name>/SKILL.md            one folder per skill: the unit every client reads
.claude-plugin/plugin.json        makes the repository a Claude plugin named "ticker"
.claude-plugin/marketplace.json   makes the same repository its own marketplace (source "./")
.mcp.json                         the Ticker MCP server, bundled with the plugin
evidence/<skill>/                 the transcripts that prove each skill
docs/distribution.md              this page
```

- One `skills/` folder is the single source. `npx skills`, Codex, Cursor, Copilot and Gemini read it as it is, and the OpenAI Skills step takes a ZIP of it.
- The Claude plugin manifests are the only bundle format tested here, and Claude is where a plugin brings the MCP server with it in one install.
- No Agent Plugins `plugin.json` or `mcp.json` at the root yet: it is untested, and no vendor documents the two manifests side by side. OpenAI converts `.claude-plugin/plugin.json` when a Claude plugin is submitted.
- The skill names carry a `ticker-` prefix, so a user who installs them next to other skills with `npx skills` sees no name clash.

## Decisions for alim

1. **Which bundling routes.** The options, cheapest first:
   - a. Publish this repository and list it as a Claude plugin, paired with the Ticker connector in the Claude directory.
   - b. Submit a new "With MCP" plugin in the OpenAI portal with the `skills/` bundle (the existing ChatGPT listing cannot be referenced; the server is submitted again).
   - c. Serve the skills from the MCP server itself (Skills over MCP). One copy, every client that reads it, no second install; today only ChatGPT reads it, as a snapshot.
   Recommendation: a and b now from this repository, c when Claude reads the extension.
2. **A licence.** The Claude directory needs one; none is in the repository yet.
3. **The day the repository goes public.** Needed before any directory listing goes live and before `npx skills add` or the Claude Code marketplace works for people outside the organisation.
4. **Where skills show in the app.** Not decided and not in this work.
