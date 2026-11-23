# Formats

*Part of operbe. This is the exact form of every file operbe asks a project to keep. These are the only parts of operbe that a script checks (`scripts/check.py`). Blank copies are in `templates/`.*

## Contents
- Where things live
- 1. The profile: `operbe.md`
- 2. An operation
- 3. A behavior
- 4. A client action
- 5. Coverage
- 6. Generated files

All files are plain text: a short header between `---` lines, then sections that each start with `## `. Header lines are `key: value`. A list is written `[a, b, c]`. Text after ` #` on a header line is a comment.

## Where things live

By default, at the project's root:

```
operbe.md                    the project's profile
operations/<name>.md         one file per operation
behaviors/<id>.md            one file per behavior
behaviors/coverage/<ui>.md   one file per UI
behaviors/INDEX.md           generated
behaviors/COVERAGE.md        generated
client-actions/<name>.md     one file per client action (optional list)
client-actions/INDEX.md      generated
```

A project may move the folders; it says where in `operbe.md`.

## 1. The profile: `operbe.md`

```
---
operbe: 0.2
operations: operations            # folder of operation records
behaviors: behaviors              # folder of behavior records
client-actions: client-actions    # folder of client action records; leave the line out if the project keeps none
uis: [phone, desktop]             # the project's UIs; [] if it has none
---

## Decisions
What this project chose where operbe leaves the choice open.

## Known deviations
Rules of operbe this project doesn't yet follow, one per line. This list may only shrink.
```

| Field | Rule |
|---|---|
| `operbe` | The version of the method the project follows. |
| `operations`, `behaviors` | Folders, relative to this file. |
| `client-actions` | Optional. A folder, relative to this file. A project without the line keeps no client actions, and nothing about them is checked. |
| `uis` | Names of the project's UIs. Other front ends are not listed: they have no behaviors. |
| Decisions | Required section; may be empty. |
| Known deviations | Required section; may be empty. |

## 2. An operation: `operations/<name>.md`

The file name is the operation's name.

```
---
name: archive-conversation
class: change                 # query | change | signal
named-because: restricted-state
needs: may change the conversation
safe-to-repeat: yes           # yes | no
taken-back-by: unarchive-conversation
risk: changes                 # reads | changes | destroys | changes-rights
many-at-once: none            # none | all-or-nothing | per-item
---

## Sentence
Archive {conversation}.

## Holds only if
The conversation is not already archived.
```

| Field | Rule |
|---|---|
| `name` | Lowercase words joined by hyphens: a verb, then the thing. Unique. Same as the file name. |
| `class` | Exactly one of `query`, `change`, `signal`. |
| `named-because` | Changes only. Leave empty for a generic change. Otherwise one of: `side-effect`, `different-right`, `together`, `restricted-state`, `intent`. |
| `needs` | The one right it requires, in the project's own words. `nothing` if open to all callers. |
| `safe-to-repeat` | `yes` if sending it twice has the effect of once. |
| `taken-back-by` | The operation that undoes it, `itself` if calling it again with the old value undoes it, or `nothing`. |
| `risk` | Exactly one. A query is always `reads`. |
| `many-at-once` | `none` unless this operation is the batch form. |
| Sentence | Required. One sentence, inputs in `{braces}`. |
| Holds only if | Required. The precondition as a meaning. `Always.` if there is none. |

A project that defines its operations in an interface language may keep these facts there instead, as long as each operation still has one file here naming it (the header alone is enough) so that behaviors can refer to it.

## 3. A behavior: `behaviors/<id>.md`

The file name is the behavior's id.

```
---
id: B-0031
name: Profile bubble
status: firm                  # rough | firm | retired
form: 1
applies-to: all               # all, or [phone, desktop]
operations: []                # names from the operation list
replaced-by:                  # an id; only when retired
---

## Statement
...

## Examples
- **Usual.** ...
- **Edge.** ...

## Changes
- form 1: first version.
```

| Field | Rule |
|---|---|
| `id` | `B-` and a number. Permanent, never reused. Same as the file name. |
| `name` | Short and unique. |
| `status` | `rough` (still being worked out), `firm` (at least one real UI has built it and it reads the same to everyone) or `retired` (no longer wanted). |
| `form` | A whole number, 1 or more. It goes up when the meaning changes, and stays put for wording fixes. |
| `applies-to` | `all`, or a list of names from the profile's `uis`. |
| `operations` | Names that exist in the operation list. May be empty. |
| `replaced-by` | Required when `retired`; otherwise empty. |
| `client-actions` | Optional. `none` says no client action carries this behavior out, because there is nothing to call or because the designer chose not to offer it; a comment on the line says which. The check then doesn't report it. |
| Statement | Required. |
| Examples | Required. At least two, each a list item. A `rough` behavior may have fewer. |
| Changes | Required. One list item per form, newest first. |

Optional sections, only under these names: **Flow**, **Appears when**, **Usable when**, **Undo**, **Differs on**. No other sections.

Order: Statement, then any optional sections, then Examples, then Changes.

## 4. A client action: `client-actions/<name>.md`

Only in a project whose profile has a `client-actions` line. The file name is the action's name.

```
---
name: archive-conversation
class: do                     # show | prepare | do
status: firm                  # rough | firm | retired
form: 1
behaviors: [B-0001]           # the behaviors it carries out; at least one
operations: [archive-conversation]
available-when: the conversation is not already archived and I may change it
applies-to: all               # all, or [phone, desktop]
replaced-by:                  # a client action's name; only when retired
---

## Sentence
Archive {conversation}.

## Inputs
- conversation: a conversation, by its id. Needed.

## Result
- done: the conversation has left the active list, and Undo is offered.
- started: offline; it is marked as waiting and completes when the connection returns.
- refused: says why, and nothing changed.
```

| Field | Rule |
|---|---|
| `name` | Lowercase words joined by hyphens: a verb, then the thing. Unique among client actions, and never changed. It may be the same as an operation's name. |
| `class` | Exactly one of `show`, `prepare`, `do`. |
| `status` | `rough`, `firm` or `retired`, with the same meanings as for a behavior. |
| `form` | A whole number, 1 or more. It goes up when the class, the inputs, the operations, the condition or the results change in meaning. |
| `behaviors` | A list of ids that exist and are not retired. At least one. |
| `operations` | A list of names from the operation list. A `show` lists only queries. A `do` lists at least one change or signal, unless it is local. |
| `show-because` | Only on a `show` that lists a change: why the project decided this change is a consequence the person has already agreed to, naming the decision in `operbe.md`. Without it, a `show` lists only queries. |
| `local` | Optional. `yes` on a `do` that commits something on the device alone and so lists no change. |
| `available-when` | The condition in words, or `always`. "I" is the person at the screen. |
| `applies-to` | `all`, or a list of names from the profile's `uis`. |
| `replaced-by` | Required when `retired`; otherwise empty. |
| Sentence | Required. One sentence, every input in `{braces}`. |
| Inputs | Required when the sentence has inputs. One list item for each, starting with the name in the braces and a colon: what it is, how a caller names it, the values allowed if they are few, and whether it is needed. |
| Result | Required. One list item for each result that can happen, starting with `done`, `refused`, `waiting`, `started` or `unknown` and a colon. `done` is always there. |

Optional section: **Unavailable**, the reasons it can't run, in the behavior's own words, one per list item.

Order: Sentence, Inputs, Unavailable, Result.

## 5. Coverage: `behaviors/coverage/<ui>.md`

One file per UI, named as in the profile.

```
# Coverage: phone

| id | value | form | note |
|---|---|---|---|
| B-0031 | honours | 1 | |
| B-0032 | differs | 1 | Undo appears only after a delay; being fixed. |
| B-0040 | not-here | | No room on this screen size. Decided by the designer. |
| archive-conversation | honours | 1 | |
```

| Column | Rule |
|---|---|
| `id` | A behavior that applies to this UI, or the name of a client action that does. At most one line each. Any other line is ignored. |
| `value` | `honours`, `differs`, `limited` or `not-here`. A behavior with no line in the file hasn't been built on this UI yet. A `rough` behavior may have lines. |
| `form` | For `honours`, `differs` and `limited`: the form the UI was built against. |
| `note` | Required for `differs`, `limited` and `not-here`. |

## 6. Generated files

`check.py --write` produces `behaviors/INDEX.md` (every behavior: id, name, status, form), `behaviors/COVERAGE.md` (behavior by UI) and, where the project keeps client actions, `client-actions/INDEX.md` (every action: name, class, status, behaviors, and each UI). Never edit them by hand.
