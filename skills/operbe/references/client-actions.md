# Client actions

*Part of operbe. This guide covers the third list: what a client action is, its three classes, what each declares, who calls it, and how an assistant reaches one. It is optional: a project takes it up when it wants a command palette, shortcuts, or an assistant that can work the UI for a person. Record formats are in `formats.md`.*

## Contents
- 1. What a client action is
- 2. Not a behavior, not an operation
- 3. Three classes: show, prepare, do
- 4. One catalogue, several callers
- 5. What every client action declares
- 6. Rules that hold everywhere
- 7. How big
- 8. Reaching a screen from outside
- 9. Keeping UIs in step
- 10. What to guard against
- 11. Checklist for adding a client action
- 12. What each project decides
- Where this comes from

## 1. What a client action is

A client action is one named thing a UI can be asked to do on its own screen: open something, go somewhere, filter a list, start a draft, press Send. It has a name, explicit inputs, and a result. It is code, and it lives in the UI.

The test: could something other than a finger on the control ask for this, and would the UI know what to do? If so, it is a client action.

An operation is asked of the server. A client action is asked of a screen. The server never runs one and never drives a screen.

## 2. Not a behavior, not an operation

A **behavior** says, in words for a designer, what must hold in a UI. It may be rough, and its wording may change freely. A **client action** is a contract with a name and inputs that callers depend on. They stay separate records for four reasons:

- Some behaviors have nothing to call. "Archived conversations look dimmed" is a rule.
- The counts differ. One behavior may need several actions, and one action (open this thing) may serve many behaviors.
- They change at different speeds. Rewording a behavior breaks nobody. Renaming an action breaks its callers.
- They answer different questions: "what must be true on screen?" and "what can I ask this screen to do, with what, and what comes back?"

Every client action **must** name at least one behavior it carries out. An action with no behavior behind it is the UI doing something the designer never decided.

A client action is not an operation either. It never crosses the membrane by itself. A client action of class `do` ends in one or more operations, which the UI sends exactly as it would for a person.

## 3. Three classes: show, prepare, do

Every client action is exactly one of these.

| Class | What it changes | Example |
|---|---|---|
| **show** | Only what this person sees on this screen | Open a conversation; filter the list to archived |
| **prepare** | Something only this person can see so far, left for them to commit | Start a reply with this text; fill the rename field |
| **do** | Something other people see or are bound by | Send the reply; archive the conversation |

The class is the line a person cares about: did it only move my view, did it set something up for me, or did it act. A caller that must ask before acting (an assistant) asks before a `do`, and need not ask before a `show`.

- A `show` **must not** send any operation except queries.
- A `prepare` **must not** leave anything other people can see or are bound by. If the project keeps drafts on the server, the operation that saves a draft is allowed.
- A `do` **must** name the operations it ends in, and at least one of them changes something.

An action that sounds like a step and acts ("review order" that also buys) is the commonest way this kind of catalogue hurts people. The class is declared so that it can be checked against the operations the action lists.

## 4. One catalogue, several callers

A project has one catalogue of client actions. Everything that can ask a UI to do something goes through it:

- **The command palette.** It lists client actions, which read better to a person than operations do.
- **Shortcuts and menus.** A shortcut is a key bound to a client action.
- **An assistant acting for the person**, built into the app or reaching it from outside (section 8).

The catalogue **must** be what the UI itself uses for its palette and shortcuts. A catalogue kept beside the app for outside callers only will drift from it. That is what happened to hand-kept scripting dictionaries.

Where an action is shown (which menu, which group, whether the palette lists it) is kept apart from the action. The record says only whether the palette lists it.

## 5. What every client action declares

| Fact | Meaning |
|---|---|
| Name | A verb, then the thing: `open-conversation`. |
| Class | `show`, `prepare` or `do`. |
| Behaviors | The behaviors it carries out. At least one. |
| Operations | The operations it sends. Required for a `do`. |
| Available when | The condition under which it can run, in words another UI or an assistant can read. `always` if there is none. |
| Applies to | The UIs that have it. |
| In palette | Whether the command palette lists it. |
| Sentence | One sentence, inputs in `{braces}`. |
| Result | What the caller is told afterwards. |

**Inputs are explicit.** "Whatever is selected" is never a hidden input. When a person runs an action from a button, the UI fills the input from the selection. When anything else runs it, the caller names the thing. Hidden inputs are what made recorded macros unreplayable.

**Availability is said twice.** The record declares the condition, so a caller can read it without a screen. The UI also reports, live, which actions are available now and, for one that isn't, why. Prefer a declared condition to code that answers "can I run?": a condition can be read by another UI and by an assistant.

**The result is never silence.** Every call ends in one of: done, with where the screen now is; refused, with the reason; or waiting for the person, with what they are being asked. A call that does nothing and says nothing is the commonest complaint about command systems.

## 6. Rules that hold everywhere

1. **The same as by hand.** Running a client action leaves the screen, and the server, exactly as if the person had done it with the control. The same checks run, the same review steps appear, the same operations are sent.
2. **A review step is never skipped.** If doing it by hand shows a review or asks for a fresh approval, the action stops there and its result is "waiting for the person". Nothing a caller passes can answer for the person.
3. **Who asked is carried.** When a `do` sends its operations, the UI marks who asked: the person, or an assistant acting for them. Otherwise the server would record that the person did something an assistant chose.
4. **No client action, no control.** A caller can do nothing through a UI that isn't a client action. There is no "press whatever is at this position".
5. **An action never widens rights.** It can do what the person at that screen can do, and no more.
6. **The person can see it.** When something other than the person runs an action, the screen shows that it happened and what asked.

## 7. How big

Size a client action for what a person would ask for, not for a control.

- Too small: `click-archive-button`. That is the control, and it means nothing on a UI that archives by swiping.
- Too big: `clean-up-inbox`. That is a task, and belongs to whoever is calling.
- Right: `archive-conversation`, with the conversation as its input.

Two tests. **Same on every UI:** if the action only makes sense on one UI's layout, it is named after a control. **One result:** if it can half happen, it is two actions.

Navigation is usually one action per kind of destination, with the destination as the input: `open-conversation {conversation}`, not one action per screen. Where the project's UIs have addresses (URLs, deep links), a `show` action and an address for the same place **should** agree.

## 8. Reaching a screen from outside

An assistant reaches client actions by one of three routes. The records are the same on all three.

**Built in.** The UI sends the assistant the actions available now with each request. The assistant answers with the ones to run, and the UI runs them and reports each result on the next turn.

**Through the server.** The server offers the catalogue to outside assistants beside its operations, for example as tools on an MCP server. It runs none of them. It passes each call to one of the person's open screens and returns the screen's result.

- The list of tools is the whole catalogue the person may use. It does not change with what is on screen.
- One tool lists the person's open screens. For each it gives a **screen handle**, which UI it is, where it is, and what is available there now.
- Every client action takes a screen handle. The server passes the call down that screen's live connection.
- No screen, a handle that has gone, or an action unavailable there: the result is "refused", with the reason.
- The connection to a screen is a session. Nothing is lost when it ends; the caller lists the screens again.

**From the page.** Where a browser lets a page offer tools to the browser's own assistant, a web UI can offer its catalogue that way.

A server that passes calls along **must** check that the caller is the person whose screen it is, or their assistant, before passing anything.

## 9. Keeping UIs in step

A client action applies to every UI unless its record says otherwise. Each UI's coverage file has a line for each action it has built, in the same file and with the same values as for behaviors: `honours`, `differs`, `limited`, `not-here`.

An action that exists on one UI only is not a fault. It is an exception, and the record says so in `applies-to`, as a behavior does.

The check reports as gaps: an action a UI hasn't built, and a firm behavior that sends a change and has no client action. A behavior with nothing to call says so (`client-actions: none`).

## 10. What to guard against

- **Text on screen that addresses the assistant.** Content is not instruction. The class and rule 2 limit the harm: the worst a tricked assistant can do through a `show` is move the view.
- **A class that lies.** The check compares each action's class with the operations it lists. A `show` that lists a change is an error.
- **The screen changing between asking and running.** The UI checks availability again when the call arrives, and refuses with the reason if it no longer holds.
- **Palette clutter.** Not every action belongs in the palette. Rank by use, and leave out actions that only make sense with an input the palette can't ask for.
- **Drift.** An action whose behavior was retired is an error. An action built against an older form of its record is a gap.

## 11. Checklist for adding a client action

1. Which behavior does it carry out? If none, raise it with the designer first.
2. Is there already an action for this, with a different input?
3. Is it named for what a person would ask, not for a control?
4. Which class is it? If `do`, which operations does it end in?
5. What are its inputs, each named, none hidden?
6. When is it available, in words another UI could act on?
7. What does it report when done, refused, and waiting for the person?
8. Does doing it by hand show a review or need approval? Then it stops there.
9. Which UIs have it? Does the palette list it?

## 12. What each project decides

Whether to keep client actions at all. Which callers exist. How availability conditions are written. How an assistant is told to ask before a `do`. How a screen shows that something else is working it. Which of the three routes it offers.

## Where this comes from

Editors and creative tools that keep one command registry for menus, shortcuts and scripts; operating systems that let an app declare actions for the system's assistant; protocols in which a front end sends its own tools to an assistant and runs them itself; and the tool shape of the Model Context Protocol, which a client action's record maps onto (name, description, input schema, result, hints). The three classes, the link to a design record, one catalogue across several UIs, and the screen handle are operbe's own.
