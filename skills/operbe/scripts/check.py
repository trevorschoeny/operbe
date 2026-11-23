#!/usr/bin/env python3
"""operbe check: validates a project's operation records, behavior records and
coverage files against references/formats.md, and (with --write) rebuilds the
generated index and coverage table.

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
    names = set()
    for p in sorted(folder.glob("*.md")):
        h, s, _ = read(p); w = f"operations/{p.name}"
        need(w, h, ["name", "class"])
        name = h.get("name", "")
        if name != p.stem: err(w, f"name '{name}' doesn't match the file name")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", name or ""): err(w, "name must be lowercase words joined by hyphens: a verb, then the thing")
        names.add(name)
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
        if not str(h.get("form", "")).isdigit() or int(h["form"]) < 1: err(w, "form must be a whole number, 1 or more")
        applies = h.get("applies-to")
        if applies != "all":
            if not isinstance(applies, list) or not applies: err(w, "applies-to must be 'all' or a list of UIs")
            else:
                for u in applies:
                    if u not in uis: err(w, f"applies-to names '{u}', which is not a UI in operbe.md")
        for o in h.get("operations") or []:
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
        out[bid] = dict(name=name, status=status, form=int(h["form"]) if str(h.get("form", "")).isdigit() else 0,
                        uis=uis if applies == "all" else (applies if isinstance(applies, list) else []))
    for p in sorted(folder.glob("B-*.md")):
        h, _, _ = read(p); r = h.get("replaced-by")
        if r and r not in out: err(f"behaviors/{p.name}", f"replaced-by '{r}' is not a behavior")
    return out


def check_coverage(folder, behaviors, uis):
    table = {}                                         # (behavior id, ui) -> value
    for ui in uis:
        p = folder / f"{ui}.md"; w = f"behaviors/coverage/{ui}.md"
        if not p.exists(): gaps.append(f"{w}: no coverage file for this UI yet"); continue
        for line in p.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not cells[0].startswith("B-"): continue
            bid, value, form, note = cells[:4]
            if bid not in behaviors: err(w, f"{bid} is not a behavior"); continue
            b = behaviors[bid]
            if (bid, ui) in table: err(w, f"{bid} has more than one line")
            if ui not in b["uis"]: err(w, f"{bid} doesn't apply to {ui}")
            if value not in COVER: err(w, f"{bid}: value must be one of {sorted(COVER)}")
            if value in ("differs", "limited", "not-here") and not note: err(w, f"{bid}: '{value}' needs a note")
            if value != "not-here":
                if not form.isdigit(): err(w, f"{bid}: '{value}' needs the form it was built against")
                elif int(form) > b["form"]: err(w, f"{bid}: form {form} is newer than the record (form {b['form']})")
                elif int(form) < b["form"]: gaps.append(f"{w}: {bid} was built against form {form}; the record is now form {b['form']}")
            if value == "differs": gaps.append(f"{w}: {bid} differs ({note})")
            table[(bid, ui)] = value
    for bid, b in behaviors.items():                   # the forward check
        if b["status"] == "firm":
            for ui in b["uis"]:
                if (bid, ui) not in table: gaps.append(f"{ui}: {bid} '{b['name']}' is firm and not yet built")
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
    ops = check_operations(ops_dir) if ops_dir.is_dir() else set()
    behaviors = check_behaviors(beh_dir, ops, uis) if beh_dir.is_dir() else {}
    table = check_coverage(beh_dir / "coverage", behaviors, uis)

    if "--write" in sys.argv and beh_dir.is_dir():
        note = "<!-- Generated by operbe check.py. Do not edit. -->\n\n"
        rows = "".join(f"| {i} | {b['name']} | {b['status']} | {b['form']} |\n" for i, b in sorted(behaviors.items()))
        (beh_dir / "INDEX.md").write_text(encoding="utf-8", data=note + "# Behaviors\n\n| id | name | status | form |\n|---|---|---|---|\n" + rows)
        head = "| id | name | " + " | ".join(uis) + " |\n|---|---|" + "---|" * len(uis) + "\n"
        rows = "".join(f"| {i} | {b['name']} | " + " | ".join(
            table.get((i, u), "" if u in b["uis"] else "n/a") for u in uis) + " |\n" for i, b in sorted(behaviors.items()))
        (beh_dir / "COVERAGE.md").write_text(encoding="utf-8", data=note + "# Coverage\n\nBlank = not yet built. n/a = doesn't apply to that UI.\n\n" + head + rows)

    print(f"operbe {profile.get('operbe', '?')}: {len(ops)} operations, {len(behaviors)} behaviors, {len(uis)} UIs")
    if gaps: print(f"  {len(gaps)} gap(s). Gaps are information and do not fail the check:")
    for g in gaps: print("  gap:   " + g)
    for e in errors: print("  ERROR: " + e)
    print("ok" if not errors else f"{len(errors)} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
