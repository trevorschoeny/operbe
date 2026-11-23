---
name: start-retitle
class: prepare
status: firm
form: 1
behaviors: [B-0004]
operations: []
available-when: I may change the conversation
applies-to: [phone]
replaced-by:
---

## Sentence
Open the title of {conversation} for editing, filled with {text}.

## Inputs
- conversation: a conversation, by its id. Needed.
- text: the title to suggest. If left out, the field holds the present title.

## Result
- done: the title field is open with the text in it. The person saves or cancels; which they did is reported afterwards.
- refused: says why.
