---
name: archive-conversation
class: do
behaviors: [B-0001]
operations: [archive-conversation]
available-when: the conversation is not archived and I may change it
applies-to: all
in-palette: yes
form: 1
---

## Sentence
Archive {conversation}.

## Result
Done: the conversation has left the list and Undo is offered. Refused: says why, and nothing changed.
