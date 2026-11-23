---
name: unarchive-conversation
class: do
status: firm
form: 1
behaviors: [B-0001]
operations: [unarchive-conversation]
available-when: the conversation is archived and I may change it
applies-to: all
replaced-by:
---

## Sentence
Return {conversation} to the active list.

## Inputs
- conversation: a conversation, by its id. Needed.

## Result
- done: the conversation is back in the active list, where it was.
- refused: says why, and nothing changed.
