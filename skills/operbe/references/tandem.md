# In tandem

*Part of operbe. This guide covers how the operation list and the behavior list are worked out together. It is the place to start for a new feature, and it points to `operations.md`, `behaviors.md` and `formats.md` as you need them.*

## Why together

The two lists find each other's gaps, so they are never written one after the other.

- A behavior often reveals an operation that doesn't exist yet.
- The operation list stops two behaviors, or two front ends, from doing the same thing in two different ways.
- An operation that no behavior and no other front end uses is probably not needed.
- A behavior that needs the server to do something no operation does can't be built yet.

## The loop for one feature

1. The designer says what they want in the UI, as rough behaviors. These can be as specific or as loose as the designer likes.
2. For each behavior, ask whether anything crosses the membrane. If nothing does, the behavior ends in no operation; go to step 5. If something does, say each thing that crosses in a sentence.
3. Look for each of those in the operation list first. If it's there, use it. If something close is there, ask whether the difference is real, using the split and merge tests in `operations.md`.
4. For anything still missing, add an operation by the checklist in `operations.md`. Size it for what it means, which is rarely the same as what this one screen needs. Then ask what the other front ends would call it. If the answer is awkward, the operation is shaped too much like the UI.
5. Write the behavior's examples. Include what the UI shows when an operation refuses, fails or takes a while. A missing fact on an operation usually shows up here.
6. Build the operations, then the front ends. A command line or MCP server uses the operations directly.
7. Record coverage for each UI and run the check.
8. A behavior becomes firm once one real UI has built it and it read the same to everyone.

Working a feature through often turns up something the designer didn't mention, such as a way to take an action back. Ask the designer. Don't add it quietly, and don't leave it out quietly.

## Signs something is off

| Sign | Likely cause |
|---|---|
| A behavior's statement describes what the system permits | That part is an operation's precondition |
| An operation is named after a screen or a button | It was shaped for one front end |
| Two behaviors end in two nearly identical operations | They are one operation, or there is a real difference nobody has named |
| A UI needs three operations in a row to do one thing, and a half-done result is nonsense | They are one operation |
| The command line can do something the UI can't, or the reverse | Fine if deliberate; otherwise a behavior is missing |
| Nobody can check a behavior on a real UI | It is too vague and stays rough |
| Every change in the project is a named change | Some are plain data and should be generic |

## A worked example

The files are in `example/`. The project is a small conversations app with a phone UI, a desktop UI and a command line.

The designer wants three things:

- Archiving a conversation gets it out of the way, with a chance to change your mind.
- On the phone, swiping a row left archives it.
- An archived conversation looks dimmed wherever it appears.

Archiving first. Something crosses the membrane, because the conversation becomes archived for everyone who has it. This is more than setting a field: it is a restricted change of state that other people notice, so it is a named change, `archive-conversation`. Taking it back is a second operation, `unarchive-conversation`, because someone would do that alone. The behavior B-0001, "Archive a conversation", ends in both.

Swipe to archive sends nothing new across the membrane. It ends in the same operation. It is still a separate decision, though: a builder could get archiving right and the swipe wrong, and it applies only to the phone. So it is its own behavior, B-0002, with `applies-to: [phone]`.

Dimmed when archived sends nothing across at all. It is a rule about appearance, so B-0003 has no operations.

Writing the examples for B-0001 ("it appears in the archive") shows that a UI must be able to ask for archived conversations. That is a query, `list-conversations`, and the command line wants it too.

The app also lets people retitle a conversation. That is plain data with no side effect, so it is a generic change, `set-conversation-title`, with nothing in `named-because`.

The result is four operations and three behaviors. The command line gets `archive`, `unarchive`, `list` and `retitle` straight from the operations, with no behaviors involved.
