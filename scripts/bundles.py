#!/usr/bin/env python3
"""The four plan bundles, built from one source: each skill's `**Plan:**` line.

A skill's plan lives in one place, the `**Plan:**` line of its SKILL.md. A bundle
is a list: the skills of its plan and of every plan below it. Nothing is copied.

usage:
  python3 scripts/bundles.py table            the README table of skills
  python3 scripts/bundles.py list <plan>      the skill folders of one bundle (free, pro, max, ultra)
  python3 scripts/bundles.py marketplace      rewrite .claude-plugin/marketplace.json from the plan lines
  python3 scripts/bundles.py check            exit 1 if marketplace.json does not match the plan lines
  python3 scripts/bundles.py build            write dist/<plugin>-plugin.zip and dist/<plugin>-skills.zip for each bundle
"""
import json
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLANS = ["Free", "Pro", "Max", "Ultra"]
# the plugin each bundle installs as; the free one is the public listing
PLUGIN = {"Free": "ticker", "Pro": "ticker-pro", "Max": "ticker-max", "Ultra": "ticker-ultra"}
TAGLINE = {
    "Free": "Ticker's free skills: price-drop and last-week screens, a pre-purchase check, and how the numbers are made.",
    "Pro": "Ticker skills for the Pro plan: the free skills, plus watching events and saving screens as Views that alert.",
    "Max": "Ticker skills for the Max plan: the Pro skills, plus the screens that read the primary market beside resale.",
    "Ultra": "Ticker skills for the Ultra plan: every skill, including who holds an event's inventory.",
}
MCP = {"ticker": {"type": "http", "url": "https://api.findticker.com/mcp"}}


def skills():
    out = []
    for f in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = f.read_text()
        name = re.search(r"^name: (.+)$", text, re.M).group(1).strip()
        # quoted in the file: an unquoted ": " is invalid YAML, and strict parsers
        # (npx skills) skip the whole skill
        desc = re.search(r"^description: (.+)$", text, re.M).group(1).strip().strip('"')
        plan = re.search(r"^\*\*Plan:\*\* (\w+)$", text, re.M).group(1)
        if plan not in PLANS or name != f.parent.name:
            sys.exit(f"{f}: plan {plan!r} or name {name!r} is wrong")
        out.append({"name": name, "plan": plan, "desc": desc})
    return sorted(out, key=lambda s: (PLANS.index(s["plan"]), s["name"]))


def bundle(plan):
    top = PLANS.index(plan)
    return [s["name"] for s in skills() if PLANS.index(s["plan"]) <= top]


def marketplace():
    return {
        "name": "ticker",
        "description": "Ticker's skills and MCP server for AI assistants, one bundle per plan.",
        "owner": {"name": "Ticker", "url": "https://findticker.com"},
        "plugins": [
            {
                "name": PLUGIN[p],
                "source": "./",
                "description": TAGLINE[p],
                "version": "0.2.0",
                "homepage": "https://findticker.com",
                "skills": [f"./skills/{n}" for n in bundle(p)],
                "mcpServers": MCP,
            }
            for p in PLANS
        ],
    }


def free_readme():
    """The README inside the two Free ZIPs, the public download.

    Not the repository README: that one names every paid skill and installs from
    this private repository, which fails for anyone outside the organization.
    """
    rows = "\n".join(
        f"| `{s['name']}` | {s['desc'].split(' Use ')[0].rstrip('.')} |"
        for s in skills() if s["plan"] == "Free"
    )
    return f"""# Ticker skills

Skills that teach an AI assistant a broker's daily work with the [Ticker](https://findticker.com) MCP tools. Each skill is one folder under `skills/` with a `SKILL.md` in the open [Agent Skills](https://agentskills.io) format, so the same files work in Claude, Codex, Cursor, GitHub Copilot, Gemini CLI and the other clients that read that format.

| Skill | What it does |
|---|---|
{rows}

More skills come with a plan: findticker.com/plans

## Install

Every skill needs the Ticker MCP server: `https://api.findticker.com/mcp`. You sign in with your Ticker account the first time; there is no key to paste.

**Claude Code**, from `ticker-plugin.zip` (the skills and the Ticker server as one plugin):

```
mkdir -p ~/.claude/skills/ticker
unzip -o ticker-plugin.zip -d ~/.claude/skills/ticker
```

Then start Claude Code, run `/mcp`, and sign in to Ticker.

**Codex, Cursor, GitHub Copilot, Gemini CLI and others**, from `ticker-skills.zip`:

```
unzip -o ticker-skills.zip -d ticker-skills
npx skills add ./ticker-skills
```

Then add the Ticker MCP server in that assistant's MCP settings.

Every step, and Claude on claude.ai: https://docs.findticker.com/docs/skills
"""


def build():
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    for p in PLANS:
        names = bundle(p)
        manifest = {"name": PLUGIN[p], "displayName": "Ticker" if p == "Free" else f"Ticker {p}",
                    "version": "0.2.0", "description": TAGLINE[p],
                    "author": {"name": "Ticker", "url": "https://findticker.com"},
                    "homepage": "https://findticker.com"}
        with zipfile.ZipFile(dist / f"{PLUGIN[p]}-plugin.zip", "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(".claude-plugin/plugin.json", json.dumps(manifest, indent=2) + "\n")
            z.writestr(".mcp.json", json.dumps({"mcpServers": MCP}, indent=2) + "\n")
            # the free bundle is public: its own README, never the repository's
            if p == "Free":
                z.writestr("README.md", free_readme())
            else:
                z.write(ROOT / "README.md", "README.md")
            for n in names:
                for f in sorted((ROOT / "skills" / n).rglob("*")):
                    if f.is_file():
                        z.write(f, str(f.relative_to(ROOT)))
        # skills only, no .mcp.json: the form a skills upload takes
        with zipfile.ZipFile(dist / f"{PLUGIN[p]}-skills.zip", "w", zipfile.ZIP_DEFLATED) as z:
            if p == "Free":
                z.writestr("README.md", free_readme())
            for n in names:
                for f in sorted((ROOT / "skills" / n).rglob("*")):
                    if f.is_file():
                        z.write(f, str(f.relative_to(ROOT)))
        print(f"{PLUGIN[p]}: {len(names)} skills")


cmd = sys.argv[1] if len(sys.argv) > 1 else "table"
path = ROOT / ".claude-plugin" / "marketplace.json"
if cmd == "table":
    print("| Plan | Skill | What it does |")
    print("|---|---|---|")
    for s in skills():
        print(f"| {s['plan']} | `{s['name']}` | {s['desc'].split(' Use ')[0].rstrip('.')} |")
elif cmd == "list":
    print("\n".join(bundle(sys.argv[2].capitalize())))
elif cmd == "marketplace":
    path.write_text(json.dumps(marketplace(), indent=2) + "\n")
elif cmd == "check":
    ok = json.loads(path.read_text()) == marketplace()
    print("marketplace.json matches the plan lines" if ok else "marketplace.json is stale: run `python3 scripts/bundles.py marketplace`")
    sys.exit(0 if ok else 1)
elif cmd == "build":
    build()
else:
    sys.exit(__doc__)
