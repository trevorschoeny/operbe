# Behaviors

*Part of operbe, the operations and behaviors method. This guide covers how to think about behaviors and how to write them down. It doesn't say what a designer should decide, or how a UI is built.*

## Contents
1. What a behavior is
2. Behaviors are for UIs only
3. Not an operation
4. What is fixed and what is free
5. One behavior, one decision
6. The record
7. Writing it so two builders read it the same
8. Coverage
9. Keeping the list true
10. Checklist for adding a behavior
11. What each project decides

## 1. What a behavior is

A **behavior** is anything the designer wants to hold true in the user interface.

It can be a flow ("archiving a conversation moves it out of the way and offers Undo"). It can be a placement ("you always reach your profile through a bubble at the bottom right"). It can be a gesture, a motion, a piece of wording, or a rule that holds across many screens ("destructive buttons are always red"). If the designer wants it to be so everywhere it applies, it is a behavior.

Behaviors are documentation. They are never code, and nothing reads them at runtime. The **behavior list** is the source of truth for the UI: every UI is built from it and checked against it. Nothing keeps a UI in line automatically, so builders, human or agent, go back to the list and check their work.

## 2. Behaviors are for UIs only

A command line, an MCP server or an API has no behaviors. Those front ends go straight to operations (see `operations.md`).

The list matters most when a product has several UIs built separately. It is still useful with one UI, because it is what the designer hands the builder and what the builder is checked against.

## 3. Not an operation

| | Behavior | Operation |
|---|---|---|
| Says | what the experience is | what the system can do |
| Owned by | design | engineering |
| Is | documentation | code |
| Lives | on the UI side | at the server membrane |

What separates them is who owns each and which side of the membrane it sits on. Level of detail has nothing to do with it: a behavior can be as specific as a corner of the screen.

Many behaviors touch no operation at all, such as how Back works or how one screen gives way to another. And where an operation is involved, the two still say different things. "You can't archive without the right" is the operation's business. What the UI shows when that happens is a behavior.

## 4. What is fixed and what is free

Whatever the designer states is fixed. Whatever the designer leaves unstated is free.

Nothing is off limits for a behavior to mention. If the designer cares where something sits, the behavior says so. If they don't care, the behavior is silent on it and each builder decides.

The more a behavior fixes, the fewer UIs can honour it. A corner bubble may not exist on a watch. That trade is the designer's to make, and the record says which UIs the behavior applies to.

## 5. One behavior, one decision

A behavior is one thing the designer decided, small enough to be right or wrong by itself. Three questions help:

- Could a builder get this right while getting the neighbouring thing wrong? Then they are two behaviors.
- Would the designer ever change this without changing that? Then they are two behaviors.
- Is it a yes-or-no question whether a given UI honours it? If not, it is too vague or too big.

There is no fixed size beyond that. A behavior can be a single sentence about a colour, or a flow of several steps.

Some things are not behaviors:

- what the system permits or does (those are operations);
- how the UI is built (frameworks, components, code);
- why the designer decided it (keep reasons elsewhere, because the list is reference);
- anything about a front end that isn't a UI.

## 6. The record

Each behavior is one file, named by its id. Here is a whole record:

```
---
id: B-0031
name: Profile bubble
status: firm
form: 1
applies-to: all
operations: []
replaced-by:
---

## Statement
The person's own profile is always reached through a round bubble showing their picture, fixed at the bottom right of the screen. It is present on every screen and never covered by other content.

## Examples
- **Usual.** On any screen, the bubble is at the bottom right; choosing it opens my profile.
- **Scrolling.** When I scroll a long list, the bubble stays where it is.
- **Keyboard up.** When the on-screen keyboard is showing, the bubble sits above it, still at the right.
- **Signed out.** When nobody is signed in, there is no bubble.

## Changes
- form 1: first version.
```

The header identifies the behavior and says where it stands:

- The id is permanent and separate from the name, so a rename costs nothing. Cite the id in code, tickets and tests.
- The status is `rough` while the behavior is still being worked out, `firm` once at least one real UI has built it and it reads the same to everyone, and `retired` when it is no longer wanted.
- The form is a number that goes up when the meaning changes. Fixing the wording doesn't raise it.
- `applies-to` is `all`, or the UIs the behavior applies to.
- `operations` lists the operations it ends in, if any.

Three sections are required. The Statement is the behavior itself: what must be so, as specific as the designer wants. The Examples are concrete cases a builder can check on a real UI, covering the usual case and the edges. Changes has one line per form.

Five more sections may be used when they fit, always under these names: Flow (numbered steps, for a behavior that is a sequence), Appears when, Usable when, Undo, and Differs on (a UI where the behavior deliberately takes another form). No other sections are allowed.

The exact rules, which a script checks, are in `formats.md`.

## 7. Writing it so two builders read it the same

Say what must be so. Use must, should and may with their strict meanings, and treat anything unmarked as a must.

Write for a stranger. Someone who has never seen the product should picture the same thing the designer does.

Use one word for one thing, and keep a short word list beside the behavior list.

Be exact where you care and silent where you don't. Vague wording such as "near the bottom" or "quickly" neither fixes anything nor frees anything.

Lean on the examples. People read a one-line statement differently, and the examples are what pin it down. A behavior with no checkable example stays rough.

## 8. Coverage

Each UI keeps one line for each behavior it has built:

| Value | Meaning |
|---|---|
| honours | Built, and matches the form named on the line. |
| differs | Built, but not as written. The line says how. This is temporary: either the UI or the record is wrong. |
| limited | Honours part of it. The line says which part. |
| not-here | Deliberately absent. The line says why and who decided. |

A behavior with no line on a UI hasn't been built there yet. A rough behavior may already have coverage lines; a UI building it is how it becomes firm.

Coverage is checked in both directions. Forward: has every UI built every firm behavior that applies to it? Backward: does any UI do something the designer cares about that isn't on the list? If so, it either becomes a behavior or comes out of the UI.

## 9. Keeping the list true

A written list drifts unless people check it on purpose. These practices help, and each project decides how strictly to apply them.

- Keep records small and uniform. People keep current what is short, regular and used every day.
- Let the list show only what is true now. How it got there is history, and belongs somewhere else.
- Treat the list as a gate. A UI change that alters a behavior isn't finished until the record and that UI's coverage line are updated.
- When a UI differs from a record, decide which one is wrong and fix it.
- Let a script check the form of the records (required fields, allowed values, unique ids, operations that exist) and generate the index and the coverage table. People write the statements; never generate a statement from a UI.
- Build from one record at a time, plus the index. Have someone other than the builder do the check.

## 10. Checklist for adding a behavior

1. Is it something the designer wants to hold true in the UI? If it's about what the system does, it's an operation.
2. Is it already on the list?
3. Is it one decision? Could it be right while its neighbour is wrong?
4. Write the statement, exact where it matters and silent where it doesn't.
5. Write the examples: the usual case, then the edges.
6. Say which UIs it applies to.
7. Name the operations it ends in, if any. If one is missing, that is a finding for the operation list.
8. Give it the next id, with status `rough` and form 1.

A behavior that a palette, a shortcut or an assistant could ask a UI to do is carried out by one or more client actions, where the project keeps them. See `client-actions.md`.

## 11. What each project decides

- Which UIs exist, and which is built first.
- How its behaviors are grouped.
- How strict its change process is, and who owns the list.
- Its word list.
