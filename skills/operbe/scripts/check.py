#!/usr/bin/env python3
"""operbe check: validates a project's operation records, behavior records,
client action records (if the project keeps them) and coverage files against
references/formats.md, and (with --write) rebuilds the generated indexes and
the coverage table.

Usage:  python3 check.py <project root> [--write]
Exit code 0 = no errors (gaps are reported but are not errors).
Standard library only.
"""
import re, sys, pathlib

CLASSES = {"query", "change", "signal"}
REASONS = {"", "side-effect", "different-right", "together", "restricted-state", "intent"}
RISKS = {"reads", "changes", "destroys", "changes-rights"}
BATCH = {"none", "all-or-nothing", "per-item"}
STATUSES = {"rough", "firm", "retired"}
COVER = {"honours", "differs", "limited", "not-here"}
B_REQUIRED = ["Statement", "Examples", "Changes"]
B_OPTIONAL = ["Flow", "Appears when", "Usable when", "Undo", "Differs on"]
A_CLASSES = {"show", "prepare", "do"}
A_RESULTS = {"done", "refused", "waiting", "started", "unknown"}
NAME = r"[a-z0-9]+(-[a-z0-9]+)+"

def whole(v): return bool(re.fullmatch(r"[0-9]+", str(v)))     # isdigit() also accepts characters like a superscript 2
def as_list(where, head, key):
    """A header field that must be written [a, b]. Anything else is an error, never an empty list."""
    v = head.get(key)
    if isinstance(v, list): return v
    if key in head: err(where, f"{key} must be a list: [a, b]")
    return []

errors, gaps = [], []
def err(where, msg): errors.append(f"{where}: {msg}")


def read(path):
    """Split a record into (header dict, {section title: text}, [titles in order])."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        err(path.name, "no header between --- lines"); return {}, {}, []
    head = {}
    for line in m.group(1).splitlines():
        line = line.split(" #")[0].rstrip()          # text after " #" is a comment
        if ":" in line:
            k, v = line.split(":", 1); v = v.strip().strip('"')
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            head[k.strip()] = v
    parts = re.split(r"^## +(.+)$", m.group(2), flags=re.M)
    titles = [t.strip() for t in parts[1::2]]
    return head, dict(zip(titles, (b.strip() for b in parts[2::2]))), titles


def need(where, head, keys):
    for k in keys:
        if k not in head: err(where, f"missing header field '{k}'")


def check_operations(folder):
    names = {}                                       # name -> class
    for p in sorted(folder.glob("*.md")):
        h, s, _ = read(p); w = f"operations/{p.name}"
        need(w, h, ["name", "class"])
        name = h.get("name", "")
        if name != p.stem: err(w, f"name '{name}' doesn't match the file name")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", name or ""): err(w, "name must be lowercase words joined by hyphens: a verb, then the thing")
        names[name] = h.get("class")
        if h.get("class") not in CLASSES: err(w, f"class must be one of {sorted(CLASSES)}")
        if len(h) <= 2 and not s: continue           # header-only stub: facts live in the project's interface language
        need(w, h, ["needs", "safe-to-repeat", "taken-back-by", "risk", "many-at-once"])
        if h.get("named-because", "") not in REASONS: err(w, f"named-because must be empty or one of {sorted(REASONS - {''})}")
        if h.get("named-because") and h.get("class") != "change": err(w, "only a change can be named-because")
        if h.get("safe-to-repeat") not in ("yes", "no"): err(w, "safe-to-repeat must be yes or no")
        if h.get("risk") not in RISKS: err(w, f"risk must be one of {sorted(RISKS)}")
        if h.get("class") == "query" and h.get("risk") != "reads": err(w, "a query's risk is always 'reads'")
        if h.get("many-at-once") not in BATCH: err(w, f"many-at-once must be one of {sorted(BATCH)}")
        for sec in ("Sentence", "Holds only if"):
            if not s.get(sec): err(w, f"missing or empty section '{sec}'")
    for p in sorted(folder.glob("*.md")):            # taken-back-by must point at something real
        h, _, _ = read(p); t = h.get("taken-back-by")
        if t and t not in ("nothing", "itself") and t not in names: err(f"operations/{p.name}", f"taken-back-by '{t}' is not an operation")
    return names


def check_behaviors(folder, ops, uis):
    out, seen_names = {}, {}
    for p in sorted(folder.glob("B-*.md")):
        h, s, titles = read(p); w = f"behaviors/{p.name}"
        need(w, h, ["id", "name", "status", "form", "applies-to", "operations"])
        bid = h.get("id", "")
        if bid != p.stem: err(w, f"id '{bid}' doesn't match the file name")
        if not re.fullmatch(r"B-\d+", bid or ""): err(w, "id must be B- and a number")
        name = h.get("name", "")
        if not name: err(w, "name is empty")
        if name in seen_names: err(w, f"name '{name}' is already used by {seen_names[name]}")
        seen_names[name] = bid
        status = h.get("status")
        if status not in STATUSES: err(w, f"status must be one of {sorted(STATUSES)}")
        if not whole(h.get("form", "")) or int(h["form"]) < 1: err(w, "form must be a whole number, 1 or more")
        applies = h.get("applies-to")
        if applies != "all":
            if not isinstance(applies, list) or not applies: err(w, "applies-to must be 'all' or a list of UIs")
            else:
                for u in applies:
                    if u not in uis: err(w, f"applies-to names '{u}', which is not a UI in operbe.md")
        b_ops = as_list(w, h, "operations")
        for o in b_ops:
            if o not in ops: err(w, f"operation '{o}' is not in the operation list")
        if status == "retired" and not h.get("replaced-by"): err(w, "a retired behavior must say what replaced it")
        if status != "retired" and h.get("replaced-by"): err(w, "replaced-by is only for a retired behavior")
        for sec in B_REQUIRED:
            if not s.get(sec): err(w, f"missing or empty section '{sec}'")
        for t in titles:
            if t not in B_REQUIRED + B_OPTIONAL: err(w, f"section '{t}' is not allowed")
        order = ["Statement"] + B_OPTIONAL + ["Examples", "Changes"]
        if titles != sorted(titles, key=lambda t: order.index(t) if t in order else 99): err(w, "sections are out of order")
        n_examples = len(re.findall(r"^- ", s.get("Examples", ""), flags=re.M))
        if status == "firm" and n_examples < 2: err(w, "a firm behavior needs at least two examples")
        out[bid] = dict(callable=h.get("client-actions") != "none", changes=any(ops.get(o) in ("change", "signal") for o in b_ops), name=name, status=status, form=int(h["form"]) if whole(h.get("form", "")) else 0,
                        uis=uis if applies == "all" else (applies if isinstance(applies, list) else []))
    for p in sorted(folder.glob("B-*.md")):
        h, _, _ = read(p); r = h.get("replaced-by")
        if r and r not in out: err(f"behaviors/{p.name}", f"replaced-by '{r}' is not a behavior")
    return out


def check_client_actions(folder, ops, behaviors, uis):
    out = {}
    for p in sorted(folder.glob("*.md")):
        if p.name in ("INDEX.md", "README.md"): continue
        h, s, titles = read(p); w = f"client-actions/{p.name}"
        need(w, h, ["name", "class", "status", "form", "behaviors", "operations", "available-when", "applies-to"])
        name = h.get("name", "")
        if name != p.stem: err(w, f"name '{name}' doesn't match the file name")
        if not re.fullmatch(NAME, name or ""): err(w, "name must be lowercase words joined by hyphens: a verb, then the thing")
        cls, status = h.get("class"), h.get("status")
        if cls not in A_CLASSES: err(w, f"class must be one of {sorted(A_CLASSES)}")
        if status not in STATUSES: err(w, f"status must be one of {sorted(STATUSES)}")
        behs = as_list(w, h, "behaviors")
        if not behs: err(w, "a client action must name at least one behavior it carries out")
        for b in behs:
            if b not in behaviors: err(w, f"behavior '{b}' is not in the behavior list")
            elif behaviors[b]["status"] == "retired" and status != "retired": err(w, f"behavior '{b}' is retired")
            elif not behaviors[b]["callable"]: err(w, f"behavior '{b}' says 'client-actions: none', but this action carries it out")
        used = as_list(w, h, "operations")
        for o in used:
            if o not in ops: err(w, f"operation '{o}' is not in the operation list")
        acts = [o for o in used if ops.get(o) in ("change", "signal")]
        local = h.get("local") == "yes"
        if cls == "show" and acts: err(w, f"a show may send only queries, but lists {acts}")     # the class must not lie
        if cls == "do" and not acts and not local: err(w, "a do must list at least one operation that is a change or a signal, or say 'local: yes'")
        if local and cls != "do": err(w, "'local: yes' is only for a do")
        if cls == "prepare" and acts: gaps.append(f"{w}: a prepare that lists {acts}; make sure nobody else can see or is bound by what it sends")
        if not h.get("available-when"): err(w, "available-when is empty; write 'always' if there is no condition")
        if not whole(h.get("form", "")) or int(h["form"]) < 1: err(w, "form must be a whole number, 1 or more")
        applies = h.get("applies-to")
        if applies != "all":
            if not isinstance(applies, list) or not applies: err(w, "applies-to must be 'all' or a list of UIs")
            else:
                for u in applies:
                    if u not in uis: err(w, f"applies-to names '{u}', which is not a UI in operbe.md")
        if status == "retired" and not h.get("replaced-by"): err(w, "a retired client action must say what replaced it")
        if status != "retired" and h.get("replaced-by"): err(w, "replaced-by is only for a retired client action")
        for sec in ("Sentence", "Result"):
            if not s.get(sec): err(w, f"missing or empty section '{sec}'")
        order = ["Sentence", "Inputs", "Unavailable", "Result"]
        for t in titles:
            if t not in order: err(w, f"section '{t}' is not allowed")
        if titles != sorted(titles, key=lambda t: order.index(t) if t in order else 99): err(w, "sections are out of order")
        braces = set(re.findall(r"\{([^{}]+)\}", s.get("Sentence", "")))                   # every input is stated, none hidden
        stated = set(m.strip() for m in re.findall(r"^- ([^:\n]+):", s.get("Inputs", ""), flags=re.M))
        for x in sorted(braces - stated): err(w, f"input '{{{x}}}' in the sentence has no line under Inputs")
        for x in sorted(stated - braces): err(w, f"Inputs lists '{x}', which is not in the sentence")
        kinds = [m.strip() for m in re.findall(r"^- ([^:\n]+):", s.get("Result", ""), flags=re.M)]
        for k in kinds:
            if k not in A_RESULTS: err(w, f"result '{k}' must be one of {sorted(A_RESULTS)}")
        if s.get("Result") and "done" not in kinds: err(w, "Result must say what 'done' reports")
        out[name] = dict(name=name, status=status, cls=cls, behaviors=behs, form=int(h["form"]) if whole(h.get("form", "")) else 0,
                         uis=uis if applies == "all" else (applies if isinstance(applies, list) else []))
    for p in sorted(folder.glob("*.md")):
        if p.name in ("INDEX.md", "README.md"): continue
        h, _, _ = read(p); r = h.get("replaced-by")
        if r and r not in out: err(f"client-actions/{p.name}", f"replaced-by '{r}' is not a client action")
    carried = {b for a in out.values() if a["status"] != "retired" for b in a["behaviors"]}
    for bid, b in behaviors.items():                   # a firm behavior that sends something should be callable, or say why not
        if b["status"] == "firm" and b["changes"] and b["callable"] and bid not in carried:
            gaps.append(f"client actions: {bid} '{b['name']}' is firm, sends a change or a signal, and no client action carries it out (or mark it 'client-actions: none')")
    return out


def check_coverage(folder, behaviors, uis, actions=None):
    actions = actions or {}
    table = {}                                         # (behavior id, ui) -> value
    for ui in uis:
        p = folder / f"{ui}.md"; w = f"behaviors/coverage/{ui}.md"
        if not p.exists(): gaps.append(f"{w}: no coverage file for this UI yet"); continue
        for line in p.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            first = cells[0]
            known = first in behaviors or first in actions
            if not known and not re.fullmatch(r"B-\d+", first) and not (actions and re.fullmatch(NAME, first)): continue   # headers, totals, notes
            if len(cells) < 4: err(w, f"{first}: a coverage line has four cells: id, value, form, note"); continue
            bid, value, form, note = cells[:4]
            if not known: err(w, f"{bid} is not a behavior" + (" or a client action" if actions else "")); continue
            b = behaviors.get(bid) or actions[bid]
            if (bid, ui) in table: err(w, f"{bid} has more than one line")
            if ui not in b["uis"]: err(w, f"{bid} doesn't apply to {ui}")
            if value not in COVER: err(w, f"{bid}: value must be one of {sorted(COVER)}")
            if value in ("differs", "limited", "not-here") and not note: err(w, f"{bid}: '{value}' needs a note")
            if value != "not-here":
                if not whole(form): err(w, f"{bid}: '{value}' needs the form it was built against")
                elif int(form) > b["form"]: err(w, f"{bid}: form {form} is newer than the record (form {b['form']})")
                elif int(form) < b["form"]: gaps.append(f"{w}: {bid} was built against form {form}; the record is now form {b['form']}")
            if value == "differs": gaps.append(f"{w}: {bid} differs ({note})")
            table[(bid, ui)] = value
    for bid, b in behaviors.items():                   # the forward check
        if b["status"] == "firm":
            for ui in b["uis"]:
                if (bid, ui) not in table: gaps.append(f"{ui}: {bid} '{b['name']}' is firm and not yet built")
    for name, a in actions.items():                    # every UI offers each firm client action, or says why not
        for ui in a["uis"]:
            if not (folder / f"{ui}.md").exists(): continue
            if (name, ui) not in table:
                if a["status"] == "firm": gaps.append(f"{ui}: client action '{name}' is firm and not yet built")
            elif table[(name, ui)] != "not-here":
                for bid in a["behaviors"]:              # an action built ahead of the behavior it carries out
                    if bid in behaviors and ui in behaviors[bid]["uis"] and (bid, ui) not in table:
                        gaps.append(f"{ui}: client action '{name}' is built, but {bid} which it carries out has no coverage line")
    return table


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    unknown = [a for a in sys.argv[1:] if a.startswith("--") and a != "--write"]
    if unknown: sys.exit(f"unknown option {unknown[0]}. The only option is --write.")
    if not args: sys.exit(__doc__)
    root = pathlib.Path(args[0])
    if not (root / "operbe.md").exists(): sys.exit(f"{root}/operbe.md not found. See references/adopting.md.")
    profile, sections, _ = read(root / "operbe.md")
    need("operbe.md", profile, ["operbe", "operations", "behaviors", "uis"])
    for sec in ("Decisions", "Known deviations"):
        if sec not in sections: err("operbe.md", f"missing section '{sec}'")
    uis = profile.get("uis") if isinstance(profile.get("uis"), list) else []
    ops_dir, beh_dir = root / str(profile.get("operations", "operations")), root / str(profile.get("behaviors", "behaviors"))
    for d in (ops_dir, beh_dir):                     # a mistyped folder must not pass as an empty list
        if not d.is_dir(): err("operbe.md", f"the folder '{d.name}' it names does not exist")
    ops = check_operations(ops_dir) if ops_dir.is_dir() else {}
    behaviors = check_behaviors(beh_dir, ops, uis) if beh_dir.is_dir() else {}
    actions, act_dir = {}, None
    if "client-actions" in profile:                   # the third list is optional: no line, no list
        act_dir = root / str(profile["client-actions"])
        if not profile["client-actions"]: err("operbe.md", "client-actions is empty; name the folder, or remove the line"); act_dir = None
        elif act_dir.resolve() in (ops_dir.resolve(), beh_dir.resolve()): err("operbe.md", "client-actions must be a folder of its own"); act_dir = None
        elif not act_dir.is_dir(): err("operbe.md", f"the folder '{act_dir.name}' it names does not exist")
        else: actions = check_client_actions(act_dir, ops, behaviors, uis)
    table = check_coverage(beh_dir / "coverage", behaviors, uis, actions)

    if "--write" in sys.argv and beh_dir.is_dir():
        note = "<!-- Generated by operbe check.py. Do not edit. -->\n\n"
        rows = "".join(f"| {i} | {b['name']} | {b['status']} | {b['form']} |\n" for i, b in sorted(behaviors.items()))
        (beh_dir / "INDEX.md").write_text(encoding="utf-8", data=note + "# Behaviors\n\n| id | name | status | form |\n|---|---|---|---|\n" + rows)
        head = "| id | name | " + " | ".join(uis) + " |\n|---|---|" + "---|" * len(uis) + "\n"
        rows = "".join(f"| {i} | {b['name']} | " + " | ".join(
            table.get((i, u), "" if u in b["uis"] else "n/a") for u in uis) + " |\n" for i, b in sorted(behaviors.items()))
        (beh_dir / "COVERAGE.md").write_text(encoding="utf-8", data=note + "# Coverage\n\nBlank = not yet built. n/a = doesn't apply to that UI.\n\n" + head + rows)

    if "--write" in sys.argv and act_dir and act_dir.is_dir():
        head = "| name | class | status | behaviors | " + " | ".join(uis) + " |\n|---|---|---|---|" + "---|" * len(uis) + "\n"
        rows = "".join(f"| {n} | {a['cls']} | {a['status']} | {', '.join(a['behaviors'])} | " + " | ".join(
            table.get((n, u), "" if u in a["uis"] else "n/a") for u in uis) + " |\n" for n, a in sorted(actions.items()))
        (act_dir / "INDEX.md").write_text(encoding="utf-8", data="<!-- Generated by operbe check.py. Do not edit. -->\n\n# Client actions\n\nBlank = not yet built. n/a = doesn't apply to that UI.\n\n" + head + rows)

    print(f"operbe {profile.get('operbe', '?')}: {len(ops)} operations, {len(behaviors)} behaviors, " + (f"{len(actions)} client actions, " if act_dir else "") + f"{len(uis)} UIs")
    if gaps: print(f"  {len(gaps)} gap(s). Gaps are information and do not fail the check:")
    for g in gaps: print("  gap:   " + g)
    for e in errors: print("  ERROR: " + e)
    print("ok" if not errors else f"{len(errors)} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
