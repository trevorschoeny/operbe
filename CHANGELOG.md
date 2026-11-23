# Changelog

## 0.2 (draft, 2026-11-23)
Still experimental.
- Client actions: an optional third list. Definition, three classes (show, prepare, do), what each declares, one catalogue for the palette, shortcuts and an assistant, the same-as-by-hand rules, reaching a screen from outside with a screen handle, coverage per UI.
- Formats: the client action record; `client-actions` in the profile; `client-actions: none` on a behavior; client action lines in a UI's coverage file; a generated client action index.
- The check validates client actions, refuses a class that disagrees with the operations listed, and reports unbuilt actions and uncarried behaviors as gaps.
- A project on 0.1 that keeps no client actions needs no change.

## 0.1 (2026-11-22)
First version. Everything is experimental: no rule has yet been proven on two projects.
- Operations: definition, three classes, the five reasons for a named change, split and merge tests, declared facts.
- Behaviors: definition (anything the designer wants to hold true in a UI; UIs only), one behavior one decision, record format, coverage.
- Formats, the check script, an example project.
