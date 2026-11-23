---
name: show-conversations
class: show
status: firm
form: 1
behaviors: [B-0005]
operations: [list-conversations]
available-when: always
applies-to: all
replaced-by:
---

## Sentence
Show {which} conversations.

## Inputs
- which: one of active or archived. Needed.

## Result
- done: the screen is that list. Hands back each conversation shown: its id, its title, and whether it is archived.
- refused: says why (for example, offline with nothing kept).
