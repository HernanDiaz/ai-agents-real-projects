"""Checks the task bank of the North Cycles repository.

For each task, on a clean copy of the repository:
1. The hidden tests must fail before anything is touched (otherwise the task measures
   nothing).
2. The reference solution is applied with the edit tool, as the agent would do it.
3. The hidden and the visible tests must pass.
4. The solution may only touch paths allowed by its scope contract.

Usage: python check_bank.py [T01 T02 …]
"""
import json
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent.parent / "shared"))

from repo_tools import (Tools, Workspace, apply_solution,  # noqa: E402
                        evaluate_attempt, read_task, run_hidden)

TYPES = {"bug", "feature", "rule", "refactoring"}


def check_card(task):
    """The formal problems of a task: missing files or invalid data."""
    problems = []
    meta, contract = task["meta"], task["contract"]
    if meta["type"] not in TYPES:
        problems.append(f"unknown type: {meta['type']}")
    if meta["difficulty"] not in (1, 2, 3):
        problems.append(f"invalid difficulty: {meta['difficulty']}")
    if not isinstance(meta["two_sessions"], bool):
        problems.append("two_sessions must be true or false")
    for key in ("goal", "allowed_paths", "forbidden_paths", "acceptance_criteria"):
        if not contract.get(key):
            problems.append(f'"{key}" is missing from contract.json')
    if not list((task["folder"] / "hidden_tests").glob("test_*.py")):
        problems.append("there are no hidden tests")
    if not (task["folder"] / "solution").is_dir():
        problems.append("there is no reference solution")
    return problems


def check_task(task_id):
    """Checks a task and returns (row for the table, list of problems)."""
    task = read_task(task_id)
    problems = check_card(task)
    with Workspace() as workspace:
        if run_hidden(workspace.folder, task)["pass"]:
            problems.append("the hidden tests already pass on the original repository")
        edits = apply_solution(Tools(workspace), task["folder"] / "solution")
        problems += [f"failed edit: {e['error']}" for e in edits if "error" in e]
        evaluation = evaluate_attempt(workspace, task)
    if not evaluation["hidden"]:
        problems.append("with the solution, the hidden tests fail:\n"
                        + evaluation["hidden_output"])
    if not evaluation["visible"]:
        problems.append("with the solution, the visible tests fail")
    for key in ("out_of_scope", "forbidden"):
        if evaluation[key]:
            problems.append(f"{key}: {', '.join(evaluation[key])}")
    meta = task["meta"]
    two_sessions = "yes" if meta["two_sessions"] else "no"
    row = (f"{task_id}  {meta['type']:<16}{meta['difficulty']}  "
           f"{two_sessions:<3} {len(edits):>3} edits  "
           f"{', '.join(evaluation['changed'])}")
    return row, problems


def main(task_ids):
    """Checks the requested tasks (all of them if none is given)."""
    if not task_ids:
        task_ids = sorted(p.name for p in FOLDER.glob("T[0-9][0-9]") if p.is_dir())
    print("Task type            dif 2s  changes")
    failed = {}
    for task_id in task_ids:
        row, problems = check_task(task_id)
        print(("   " if not problems else "BAD ") + row)
        if problems:
            failed[task_id] = problems
    summary = {"tasks": len(task_ids), "correct": len(task_ids) - len(failed)}
    print(json.dumps(summary, ensure_ascii=False))
    for task_id, problems in failed.items():
        print(f"\n{task_id}:")
        for problem in problems:
            print("  -", problem)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
