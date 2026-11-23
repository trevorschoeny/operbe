# operbe

operbe is the operations and behaviors method: a software development method for any project with a server and one or more front ends.

Version 0.2. Everything in it is experimental until it has been proven on two projects.

## What it is

operbe has every project keep two lists, in the same shape, and offers a third.

- **Operations** are everything that passes through the server membrane. There is one set, defined once and used by every front end. Operations are code.
- **Behaviors** are everything the designer wants to hold true in the user interface. They are documentation that every UI is built from and checked against.
- **Client actions** (optional) are everything a UI can be asked to do on its own screen: by a command palette, a shortcut, or an assistant working the app for a person. They are code in the UI. Each is classed show, prepare or do, and each names the behavior it carries out.

```
   people            agents            scripts
     │                 │                  │
  ┌──┴───┐        ┌────┴─────┐      ┌─────┴──────┐
  │  UI  │        │ MCP, API │      │ command    │      front ends
  └──┬───┘        └────┬─────┘      │ line       │
     │  ▲              │            └─────┬──────┘
     │  └ built from   │                  │
     │    the BEHAVIOR │                  │
     │    LIST         │                  │
 ════╪═════════════════╪══════════════════╪═════════   the membrane
     └────────── the OPERATION LIST ──────┘
                        │
                     the server
```

## The one rule

1. Nothing crosses the membrane except an operation.
2. Nothing the designer cares about in a UI is off the behavior list.

The rest of operbe follows from those two halves.

## What it is not

operbe is not an architecture. It says nothing about languages, frameworks, storage, transport or how the server is built.

It is not a spec either. A project's two lists are its specs, and operbe is how they get made.

It is not a design system. It doesn't say what a designer should decide, only how a decision is written down and checked.

And it generates nothing. No UI is produced from the behavior list, and nothing reads that list at runtime. Client actions are the exception. They are the UI's own code, and their records say what that code is agreed to do.

## When to use it

Use operbe when a project has a server and at least one front end, and you want every front end, and every agent working on one, to agree on what the system does and what the experience is.

It isn't meant for a script, a library with no server, or a throwaway prototype.

## Install

operbe is packaged as an agent skill.

In Claude Code, install it as a plugin:

```
/plugin marketplace add trevorschoeny/claude-plugins
/plugin install operbe@trevorschoeny-claude-plugins
```

In any other agent that reads skills, copy the `skills/operbe` folder into that agent's skills folder.

You can also use operbe with no agent at all. Read the references below, copy the templates into your project, and run the check with Python 3:

```
python3 skills/operbe/scripts/check.py <your project> --write
```

## What's here

| Part | What it covers | File |
|---|---|---|
| Operations | What an operation is, how big, what it declares | `skills/operbe/references/operations.md` |
| Behaviors | What a behavior is, how it's written, coverage | `skills/operbe/references/behaviors.md` |
| Client actions | What a UI can be asked to do, the three classes, reaching a screen from outside | `skills/operbe/references/client-actions.md` |
| In tandem | How the two lists are worked out together, with an example | `skills/operbe/references/tandem.md` |
| Formats | The exact form of each file | `skills/operbe/references/formats.md` |
| Adopting | Starting a project, or bringing operbe into one | `skills/operbe/references/adopting.md` |
| Check | A script that checks the records and builds the tables | `skills/operbe/scripts/check.py` |
| Example | A small project done this way | `skills/operbe/example/` |

`skills/operbe/SKILL.md` is the short file an AI agent loads. It points the agent to the reference a task needs.

## Rule strength

Each rule in the references is a must, a should or a may. A must is part of operbe, and a project that breaks one records a deviation. A should is a strong default that a project can depart from with a stated reason. A may is a suggestion. Anything unmarked is a must.

## Changes

See `CHANGELOG.md`.

## What each project decides

A project decides everything operbe doesn't state: the language its operations are defined in, the architecture underneath, which front ends exist, how behaviors are grouped, and how strict the change process is. It records those choices in its `operbe.md` file.

## License

MIT. See `LICENSE`.
