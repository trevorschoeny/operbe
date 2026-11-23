# Operations

*Part of operbe, the operations and behaviors method. This guide covers how to think about operations, how big to make them and how to write them down. It says nothing about how to build them: language, architecture, storage and transport are each project's choice.*

## Contents
1. What an operation is
2. Why size matters
3. Three classes
4. Generic or named
5. Split and merge
6. What is never an operation
7. What every operation declares
8. Rules that hold everywhere
9. Operations and behaviors
10. Checklist for adding an operation
11. What each project decides

## 1. What an operation is

An **operation** is anything that passes through the server membrane. If a front end needs the server to do something or tell it something, that is an operation. If nothing crosses, there is no operation.

A project has one set of operations, defined once. The UI, the MCP server, the command line, tests and scripts all use that same set, and no front end gets a private way in.

An operation is one intent, done completely or not at all, and the server may refuse it.

## 2. Why size matters

The operation is the unit for everything the system does around a call:

- who may do it
- whether it's recorded, and as what
- whether it can be sent again safely
- whether it can be taken back
- whether a person must confirm it

If two things differ in any of these, they are two operations. If they never differ in any of them and never happen apart, they are one.

## 3. Three classes

| Class | What it does | Kept? |
|---|---|---|
| Query | Returns information and changes nothing. | No |
| Change | Changes something that matters to others or must be kept. Returns only its outcome and what it made. | Yes |
| Signal | Passes something momentary, such as "is typing". | No |

A call belongs to exactly one class. A change doesn't also fetch, and a query never changes anything. The same rules about who may call apply to all three.

## 4. Generic or named

Every operation has a name. The question here is whether a change needs a meaning of its own.

A **generic change** edits plain data on a thing: "set a conversation's title", "set my notification preference". It has no side effects and moves nothing through a lifecycle. Most changes in most systems are generic, and that is normal.

A **named change** means something beyond the edit. A change earns that only if at least one of these is true:

1. It has a side effect on others: it sends, notifies, publishes or starts something.
2. It needs a different right, or it can't be taken back.
3. Several things must change together, because a half-done result would be a state nobody should see.
4. It is a restricted change of state: only some people may make it, or only from some states.
5. It carries intent that a plain edit can't. A move is more than a delete plus a create, and correcting a name is a different act from renaming.

If none of the five is true, keep it generic. And don't hide any of the five behind a generic change: if setting a field would send an email, that is a named change.

## 5. Split and merge

Split one operation into two when:

- the two parts could be accepted or refused independently;
- the parts need different rights;
- the parts differ in whether they can be taken back; or
- one part is useful alone.

Merge two into one when they never usefully happen apart, or when a half-done result would be a state nobody should ever see.

There is also a one-sentence test. Every operation can be said in one plain sentence with its inputs filled in: "Move Leo from Front Desk to Billing on Monday." If the sentence needs "and" between two unrelated things, split it. If it can't be said without naming a field, it is probably a generic change.

## 6. What is never an operation

- Setting something derived. If a value can be computed from other things, it is computed and never written.
- A consequence. What follows from an operation by rule is not part of that operation.
- Policy. Who may, when, in what order and with what defaults are settings and rules around operations.
- A step. A flow having a step doesn't make the step an operation.
- A mode. A flag that changes what an operation means is really a second operation.
- Something shaped for one front end. If only one front end would ever want it, it belongs in that front end.

## 7. What every operation declares

| Fact | Meaning |
|---|---|
| Name | A verb, then the thing, in the project's own plain words. |
| Sentence | Its one-sentence form, with the inputs marked. |
| Class | Query, change or signal. |
| Named because | For a named change, which of the five reasons. Empty for a generic change. |
| Needs | The one right it requires, in the project's own words. |
| Holds only if | Its precondition, stated as a meaning ("the seat is empty") and not as an old value. |
| Safe to repeat | Whether sending it twice has the effect of once. |
| Taken back by | How it is undone, or that it can't be. |
| Risk | Whether it only reads, changes something, destroys something, or changes who may do what. |
| Many at once | If this is a batch form: whether it is all-or-nothing or gives a result per item. |

A project may add facts of its own, but it keeps these. The exact record form is in `formats.md`.

These facts are stated once, on the operation, and every front end reads them from there. How a front end presents an operation (a button, a command, a tool) is that front end's business.

## 8. Rules that hold everywhere

1. The operation protects itself. It checks who may call it every time. When a front end hides or labels something, that is presentation and protects nothing.
2. Changing who may do what is always its own operation. It is never a side effect of another one.
3. Doing many at once is a separate operation from doing one.
4. Front ends stay thin. A front end may group, rename or reshape operations for its users, but it adds no rules of its own.
5. Add late. When in doubt, leave an operation out: adding one later is safe, and changing or removing one is not.

## 9. Operations and behaviors

A project with a UI also has behaviors (see `behaviors.md`), which say what the designer wants the experience to be. The two are different things with different owners.

| | Operation | Behavior |
|---|---|---|
| Says | what the system can do | what the experience is |
| Is | code | documentation |
| Lives | at the membrane | on the UI side |
| Used by | every front end | UIs only |

A behavior may end in no operation, in one, or in several. An operation may serve many behaviors, or none if it is only used from the command line. The two lists are worked out together (see `tandem.md`).

## 10. Checklist for adding an operation

1. Does it cross the membrane? If not, stop.
2. Is it a query, a change or a signal?
3. If it's a change: is it plain data with no side effect? Then it's generic.
4. Otherwise, which of the five reasons makes it a named change?
5. Run the split tests, then the merge tests.
6. Say it in one sentence.
7. Is something very like it already on the list?
8. Fill in the facts in section 7.
9. If you're still unsure, leave it out.

## 11. What each project decides

- How operations are defined, and in what language.
- The architecture, storage, transport and sync underneath.
- Which front ends exist.
- What its rights are called.
- Any extra facts an operation declares.
- How refusals, retries and undo work in practice.
