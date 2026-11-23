# Changelog

## 0.2 (2026-11-23)
Still experimental.
- Client actions: an optional third list. A client action is something a UI can be asked to do on its own screen, by a command palette, a shortcut or an assistant. Three classes (show, prepare, do), stated inputs, five results, the same-as-by-hand rules, when to use client actions and when operations, and ways to reach a screen from outside.
- Formats: the client action record; `client-actions` in the profile; `client-actions: none` on a behavior; client action lines in a UI's coverage file; a generated client action index.
- The check validates client actions. It refuses a class that disagrees with the operations listed, an input that isn't stated, and a list written without brackets. It reports unbuilt actions and uncarried behaviors as gaps.
- Operations: where a project keeps client actions, every change records who asked.
- Fixed in the check: a list field written without brackets was read as empty; `form` accepted characters that aren't plain digits.
- A project on 0.1 that keeps no client actions needs no change.

## 0.1 (2026-11-22)
First version. Everything is experimental: no rule has yet been proven on two projects.
- Operations: definition, three classes, the five reasons for a named change, split and merge tests, declared facts.
- Behaviors: definition (anything the designer wants to hold true in a UI; UIs only), one behavior one decision, record format, coverage.
- Formats, the check script, an example project.
