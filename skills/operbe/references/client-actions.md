# Client actions

*Part of operbe. This guide covers the third list: what a client action is, its three classes, what each declares, who calls it, and how an assistant reaches one. The list is optional. A project takes it up when it wants a command palette, shortcuts, or an assistant that can work a UI for a person. Record formats are in `formats.md`.*

## Contents
- 1. What a client action is
- 2. Not a behavior, not an operation
- 3. Three classes: show, prepare, do
- 4. One list, several callers
- 5. What every client action declares
- 6. Results
- 7. Rules that hold everywhere
- 8. How big
- 9. Client actions or operations
- 10. Reaching a screen from outside
- 11. Keeping UIs in step
- 12. What to guard against
- 13. Checklist for adding a client action
- 14. What each project decides
- Where this comes from

Two words used throughout. A **UI** is a kind of front end the project builds (the phone app, the desktop app). A **screen** is one running copy of a UI in front of one person.

## 1. What a client action is

A client action is one named thing a UI can be asked to do on its own screen: open something, go somewhere, filter a list, start a draft, press Send. It has a name, stated inputs, and a result. It is code, and it lives in the UI.

The test: could something other than a finger on the control ask for this, and would the UI know what to do? If so, it is a client action.

An operation is asked of the server. A client action is asked of a screen, and the screen runs it. The server runs none.

## 2. Not a behavior, not an operation

A **behavior** says, in words for a designer, what must hold in a UI. It may be rough, and its wording may change freely. A **client action** is a contract with a name and inputs that callers depend on. They are separate records for four reasons:

- Some behaviors have nothing to call. "Archived conversations look dimmed" is a rule.
- The counts differ. One behavior may need several actions, and one action may serve several behaviors.
- They change at different speeds. Rewording a behavior breaks nobody. Changing an action's inputs breaks its callers.
- They answer different questions: "what must be true on screen?" and "what can I ask this screen to do, with what, and what comes back?"

Every client action **must** name at least one behavior it carries out. An action with no behavior behind it is the UI doing something the designer never decided. For plain moving around (open this, go back), the behavior is usually a general one, such as "Anything shown in a list can be opened". If no such behavior exists, write it first.

A client action is not an operation. It never crosses the membrane by itself. When it needs the server, the UI sends operations exactly as it would for a person.

## 3. Three classes: show, prepare, do

Every client action is exactly one of these.

| Class | What it does | Example |
|---|---|---|
| **show** | Changes only what this person sees on this screen | Show the archive; open a conversation |
| **prepare** | Sets something up and leaves it for the person to commit or drop | Open the title for editing with some text in it; bring up the review for a delete |
| **do** | Commits something: other people see it or are bound by it, or the person can't take it back by moving their view | Archive the conversation; send the reply; clear what this device has kept |

The class is the line a person cares about: it moved my view, it set something up for me, or it acted.

- A `show` **must not** send any operation except queries.
- A `prepare` **must not** leave anything other people can see or are bound by. Saving a draft that only the person can see is allowed.
- A `do` **must** list the operations it ends in, at least one of them a change or a signal. A `do` that commits something on the device alone lists none and says `local: yes`.

Three cases come up often.

- **A view that also sends something.** If opening a conversation marks it read and the other person sees that, the action sends a change, so it is a `do`. A project may decide that such a change is a consequence the person has already agreed to (a setting), record that decision, and class the action `show`. It still lists the operation, and the record says why.
- **An act with a review.** An action that only brings up the review is a `prepare` and lists no operations. Committing is a separate `do`. Run by anything other than the person, that `do` stops at the review (rule 2).
- **Taking it back.** If a `do` can be taken back, there **should** be an action that takes it back. Otherwise a caller that archives by mistake can't undo it through the UI.

**When a caller asks first.** A caller that acts for a person, such as an assistant, **should** not ask before a `show` or a `prepare`, and **must** have the person's ask before a `do`. A clear request from the person for this act on these inputs is the ask. The caller **should** ask again when an operation the action ends in destroys something, changes who may do what, or can't be taken back. Those facts are already on the operation.

## 4. One list, several callers

A project has one list of client actions. Everything that can ask a UI to do something goes through it:

- **The command palette.** It offers client actions, which read better to a person than operations do.
- **Shortcuts and menus.** A shortcut is a key bound to a client action.
- **An assistant acting for the person**, built into the app or reaching it from outside (section 10).

The UI's own palette and shortcuts **must** run on the same definitions that outside callers reach. A list kept beside the app for outside callers only will drift from it, which is what happened to scripting dictionaries kept by hand.

The record is the place the project agrees on an action. A project that defines its client actions in code **may** generate the records from the code, or check one against the other. Either way the two **must** agree, and the code is what runs.

Where an action is shown (which menu, which group, whether the palette lists it) is each UI's business and is not in the record.

## 5. What every client action declares

| Fact | Meaning |
|---|---|
| Name | A verb, then the thing: `open-conversation`. The name is the action's identity and never changes. |
| Class | `show`, `prepare` or `do`. |
| Status | `rough`, `firm` or `retired`, as for a behavior. |
| Behaviors | The behaviors it carries out. At least one. |
| Operations | The operations it sends. |
| Available when | The condition under which it can run. `always` if there is none. |
| Applies to | The UIs that have it. |
| Sentence | One sentence, inputs in `{braces}`. |
| Inputs | One line for each input: what it is, how a caller names it, and whether it is needed. |
| Result | What the caller is told afterwards (section 6). |

**Inputs are stated.** An action never takes an input from the selection without naming it. When a person runs an action from a control, the UI fills the named input from what is selected. When anything else runs it, the caller names the thing. Unnamed inputs are what made recorded macros impossible to replay.

**Availability is said twice.** The record declares the condition, so a caller can read it without a screen. The screen also reports, live, which actions can run now and, for one that can't, why. `available-when` restates the behavior's *Appears when* and *Usable when* for a caller. Where they differ, the behavior is right and the action is wrong. A condition written as words or data **should** be preferred to code that answers "can I run?", because another UI and an assistant can read it.

## 6. Results

A call never ends in silence. Every call ends in exactly one of these.

| Result | Meaning |
|---|---|
| **done** | It happened. Says where the screen is now. A `show` also hands back what it showed, as far as the caller may see it. |
| **refused** | Nothing changed. Says why. |
| **waiting for the person** | The screen is asking the person something: a review, a confirmation, a choice. Says what. |
| **started** | It was accepted and hasn't finished: it is queued while offline, or it takes a while. Says how the caller will learn the end. |
| **unknown** | The screen went away or the call timed out after it may have sent something. |

What happens later is reported the same way, on the caller's next turn or as an event the project defines: the person confirmed or cancelled, the queued change went through, the server refused and the screen put things back.

After **unknown**, a caller **must not** simply run the action again. It asks the server what is true (a query), and looks at whether the operations are safe to repeat. That fact is on each operation.

A UI that shows a change before the server has agreed reports **started**, not done, until the server agrees.

## 7. Rules that hold everywhere

1. **The same as by hand.** Running a client action leaves the screen, and the server, as if the person had done it with the control. The same checks run, the same reviews appear, the same operations are sent.
2. **A review is never skipped.** If doing it by hand shows a review or a confirmation, the action stops there and its result is "waiting for the person". Nothing a caller passes can answer for the person.
3. **Who asked is carried.** When an action sends operations, the server learns who asked: the person, or an assistant for them. Otherwise the record would say the person did something an assistant chose.
4. **Nothing outside the list.** A caller does nothing through a UI except by a client action. The method has no "press whatever is at this position".
5. **An action never widens rights.** It can do what the person at that screen can do, and no more.
6. **The person can see it.** When something other than the person runs an action, the screen shows that it happened and what asked.

## 8. How big

Size a client action for what a person would ask for.

- Too small: `click-archive-button`. That is a control, and it means nothing on a UI that archives by swiping.
- Too big: `clean-up-inbox`. That is a task, and belongs to whoever is calling.
- Right: `archive-conversation`, with the conversation as its input.

Two tests. **The same on every UI:** if the action only makes sense on one UI's layout, it is named after a control. **One result:** if it can half happen, it is two actions.

A filter or a choice among a few is usually an input, not an action of its own: `show-conversations {which: all, active or archived}`. Moving around is usually one action for each kind of place, with the place as the input. Where a UI's places have addresses (URLs, deep links), a `show` and the address for the same place **should** agree.

A gesture is a way of running an action. Swiping to archive runs `archive-conversation`; it gets no action of its own.

## 9. Client actions or operations

An assistant may be able to reach both. They are for different things.

- **Client actions** are for working with the person on their screen: they see it happen, reviews appear, Undo is offered.
- **Operations** are for acting with no screen, as any other front end does.

A protection that must hold against every caller belongs on the operation. Rule 2 guards the UI path only. If deleting for good must always have the person's fresh agreement, the operation has to require proof of it, or an assistant with the operation could go around the review.

## 10. Reaching a screen from outside

The rules are that a screen runs its own actions, that only the person or their assistant may ask, and that the caller always gets a result. How a call reaches a screen is the project's choice. Three ways that work:

**Built in.** The UI sends the assistant the actions that can run now with each request. The assistant answers with the ones to run. The UI runs them and reports each result on the next turn.

**Through the server.** The server offers the client action list to outside assistants beside its operations, for example as tools on an MCP server, and passes each call to one of the person's screens. Passing a call to a screen crosses the membrane, so it is an operation like any other: the project keeps a query that lists the person's screens and an operation that passes a call to one.

- The tools offered are the whole list the person may use. They don't change with what is on screen.
- The screen list gives, for each screen, a **screen handle**, which UI it is, where it is, which actions can run there now, and the form of each.
- Every client action takes a screen handle.
- With several screens, the caller **should** use the one the person is using now, and ask if that is unclear.
- With no screen, the caller may ask the person to open one, or use operations.
- A connection to a screen is temporary. Nothing is lost when it ends; the caller lists the screens again.
- The server knows who is asking because it passed the call along, so it, and not the screen, says who asked (rule 3).

**From the page.** Where a browser lets a page offer tools to the browser's own assistant, a web UI can offer its list that way.

A server that passes calls along **must** first check that the caller is the person whose screen it is, or acts with a grant from that person that the server can check.

## 11. Keeping UIs in step

A client action applies to every UI unless its record says otherwise. Each UI's coverage file has a line for each action it has built, with the same values as for a behavior: `honours`, `differs`, `limited`, `not-here`.

An action that exists on one UI only is an exception, and the record says so in `applies-to`, as a behavior's does.

A behavior a person can trigger is carried out by at least one client action, or it says `client-actions: none`. That covers two cases: there is nothing to call (a rule, a gesture), or the designer has chosen not to offer it to callers. A note on the line says which.

The check reports as gaps: a firm action a UI hasn't built, an action a UI has built whose behavior it hasn't, and a firm behavior that sends a change or a signal and has neither an action nor `client-actions: none`. It doesn't look for missing actions on behaviors that only show something.

An action is retired the way a behavior is: its status becomes `retired` and it says what replaced it. Renaming is retiring one and adding another.

## 12. What to guard against

- **Text on screen that addresses the assistant.** Content is not instruction. The classes limit the harm: the worst a tricked caller does through a `show` is move the view.
- **A class that lies.** The check compares each action's class with the operations it lists. A `show` that lists a change is an error.
- **The screen changing between asking and running.** The screen checks again when the call arrives, and refuses with the reason if the action can no longer run.
- **A crowded palette.** Not every action belongs in a palette. Leave out one that needs an input the palette can neither ask for nor take from the selection.
- **Drift.** An action that names a retired behavior is an error. An action built against an older form of its record is a gap.

## 13. Checklist for adding a client action

1. Which behavior does it carry out? If none, raise it with the designer first.
2. Is there already an action for this that could take it as an input?
3. Is it named for what a person would ask, not for a control or a gesture?
4. Which class is it? If `do`, which operations does it end in, or is it local?
5. What are its inputs, each named, with how a caller names the thing?
6. When can it run, in the behavior's own words?
7. What does it report for each result that can happen?
8. Does doing it by hand show a review or a confirmation? Then it stops there, and bringing up the review may be a `prepare` of its own.
9. If it can be taken back, which action takes it back?
10. Which UIs have it?

## 14. What each project decides

Whether to keep client actions at all. Who settles a new action or a change to one. Which callers exist, and which of the ways in section 10 it offers. How availability conditions are written. How an assistant is told to ask before a `do`. How a grant to an assistant is given and checked. How a screen shows that something else is working it. How later outcomes reach a caller. Whether its palette lists every action.

## Where this comes from

Editors and creative tools that keep one command registry for menus, shortcuts and scripts. Operating systems that let an app declare actions for the system's assistant. Protocols in which a front end sends its own tools to an assistant and runs them itself. The tool shape of the Model Context Protocol, which a client action's record can be turned into: a name, a description, inputs, a result. The three classes, the link to a design record, one list across several UIs, and the screen handle are operbe's own.
