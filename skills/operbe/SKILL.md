---
name: operbe
description: The operations and behaviors method (operbe) for projects with a server and front ends (UI, MCP, command line, API). Use when a project has an operbe.md file or the user asks to use operbe. Covers adding, sizing or reviewing an operation (a server call or API endpoint, anything that crosses the server membrane), writing or changing a behavior (a UI spec item, anything the designer wants to hold true in a UI), adding a client action (a command a palette, a shortcut or an assistant can ask a UI to run) in an operbe project, building or checking a UI against the behavior list and its coverage, and adopting operbe in a project.
compatibility: The check script needs python3 (standard library only).
metadata:
  version: "0.2"
---

# operbe

operbe has each project keep two lists, and offers a third.

Operations are everything that crosses the server membrane. There is one set, every front end uses it, and it is code.

Behaviors are everything the designer wants to hold true in a UI. They are documentation that UIs are built from and checked against. Front ends that aren't UIs have no behaviors and go straight to operations.

The third list is optional. Client actions are everything a UI can be asked to do on its own screen, by a command palette, a shortcut or an assistant. They are code in the UI. Each is classed show, prepare or do, and each names the behavior it carries out.

The one rule: nothing crosses the membrane except an operation, and nothing the designer cares about in a UI is off the behavior list.

operbe covers how these are thought about, written down and checked. It doesn't prescribe architecture, language or tooling. Those belong to the project.

## Start here

Read the project's `operbe.md`. It says where the lists live, which UIs exist, what the project decided, and which rules it doesn't follow yet. If the project has no `operbe.md`, read `references/adopting.md`.

## Which reference to read

| You are about to | Read |
|---|---|
| work out a feature | `references/tandem.md` first; it sends you to the others as you need them |
| add, split, merge or question an operation | `references/operations.md` |
| add or change a behavior, or build or check a UI | `references/behaviors.md` |
| add a client action, build a command palette, or let an assistant work a UI | `references/client-actions.md` |
| write or edit a record file | `references/formats.md` |
| set operbe up in a project | `references/adopting.md` |

Read what the task needs and leave the rest. `example/` is a small project done this way, and `templates/` has blank copies of every file.

## While you work

- Work from one record at a time, plus the index. Don't load the whole list.
- When you change what a UI does, update the behavior record and that UI's coverage line in the same change.
- If a UI does something the designer would care about and it isn't on the list, stop and raise it. Don't add or remove it yourself.
- Behaviors belong to the designer. Propose a change to a statement; don't rewrite one to match what was built.
- A client action does what doing it by hand does and stops at any review or confirmation. It never takes an input from the selection without naming it; a person's selection may fill a named input.
- Don't add a client action of class `do` without asking. Propose it.
- If a feature needs something the designer didn't ask for (a way to take an action back, say), ask before adding it.

## Before you finish

Run the check script (run it, don't read it) and fix every error it reports:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/check.py <project root>
```

Outside Claude Code, `${CLAUDE_SKILL_DIR}` is the folder this file was loaded from.

Lines marked `gap` are information: a behavior or a client action some UI hasn't built yet, a UI that differs from a record, or a behavior that sends a change and has no client action. They don't fail the check. Add `--write` to rebuild the behavior index, the coverage table and the client action index.
