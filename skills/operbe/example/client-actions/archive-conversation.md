---
name: archive-conversation
class: do
status: firm
form: 1
behaviors: [B-0001]
operations: [archive-conversation]
available-when: the conversation is not already archived and I may change it
applies-to: all
replaced-by:
---

## Sentence
Archive {conversation}.

## Inputs
- conversation: a conversation, by its id. Needed.

## Result
- done: the conversation has left the active list, and Undo is offered.
- started: offline; it is marked as waiting and completes when the connection returns.
- refused: says why, and nothing changed. If the server refuses after the list has changed, the conversation returns to it.
