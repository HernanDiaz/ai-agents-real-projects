"""Checks the incidents of Northside Veterinary Clinic, as check_bank.py does with the
North Cycles tasks: on a clean copy of the repository, the hidden tests must fail
before anything is touched; with the reference solution, applied with the edit tool,
the hidden and the visible tests must pass; and the solution may only touch allowed
paths.

Usage: python check_incidents.py [I01 I02 …]
"""
import json
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
REPO = FOLDER.parent / "northside_vet"
sys.path.insert(0, str(FOLDER.parent.parent / "shared"))

from repo_tools import (Tools, Workspace, apply_solution,  # noqa: E402
                        evaluate_attempt, run_hidden)


def read(incident_id):
    """An incident, in the same format as the North Cycles tasks."""
    folder = FOLDER / incident_id
    return {"id": incident_id, "folder": folder,
            "request": (folder / "request.md").read_text(encoding="utf-8"),
            "contract": json.loads(
                (folder / "contract.json").read_text(encoding="utf-8")),
            "meta": json.loads((folder / "meta.json").read_text(encoding="utf-8"))}


def check(incident):
    """The problems of an incident, or an empty list."""
    problems = []
    with Workspace(REPO) as workspace:
        if run_hidden(workspace.folder, incident)["pass"]:
            problems.append("the hidden tests already pass without touching anything")
        results = apply_solution(Tools(workspace), incident["folder"] / "solution")
        errors = [r for r in results if "error" in r]
        if errors:
            problems.append(f"the solution cannot be applied: {errors[0]}")
        evaluation = evaluate_attempt(workspace, incident)
        if not evaluation["hidden"]:
            problems.append("with the solution, the hidden tests fail: "
                            + evaluation["hidden_output"][-300:])
        if not evaluation["visible"]:
            problems.append("with the solution, the visible tests fail")
        if evaluation["out_of_scope"] or evaluation["forbidden"]:
            problems.append(f"it touches paths that are not allowed: "
                            f"{evaluation['changed']}")
    return problems


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(p.name for p in FOLDER.glob("I[0-9][0-9]"))
    correct = 0
    for incident_id in ids:
        problems = check(read(incident_id))
        correct += not problems
        print(f"{incident_id}  {'ok' if not problems else '; '.join(problems)}")
    print(json.dumps({"incidents": len(ids), "correct": correct}))
