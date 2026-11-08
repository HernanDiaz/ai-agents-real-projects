"""Tools of the coding agent, working on a copy of the repository.

They are the tools of chapter 12 of the previous book, grown for a real repository:
the agent lists the files, reads line ranges, searches with regular expressions,
edits by exact replacement, runs the visible tests and a few allowed commands.
Everything happens in a temporary copy of the repository, created for each attempt
and deleted at the end: nothing the agent does leaves it.

The module can also evaluate a finished attempt: it runs the task's hidden tests,
computes the diff against the original and lists the files touched out of scope.
To check that everything works, without any model:

    python repo_tools.py --test
"""
import difflib
import fnmatch
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
REPO = BOOK / "data" / "north_cycles"
TASKS = BOOK / "data" / "tasks"

TEST_SECONDS = 60              # maximum time to run the tests
COMMAND_SECONDS = 30           # maximum time for an allowed command
MAX_READ_LINES = 150           # lines per read: the model's context is short
MAX_RESULTS = 40               # results per search
MAX_OUTPUT = 2500              # characters of output returned to the model
IGNORED_FOLDERS = {"__pycache__", ".git", "_hidden", ".agent"}  # .agent: agent notes
TEST_COMMAND = ["-m", "unittest", "discover", "-s", "tests"]
ALLOWED_COMMANDS = (           # the command must start with one of these prefixes
    ("python", "manage.py"),
    ("python", "-m", "unittest"),
    ("python", "-m", "py_compile"),
)


# --- The copy of the repository -------------------------------------------------

class Workspace:
    """A copy of the repository in a temporary folder.

    "protected" are paths (or folders ending in /) that the agent can read but
    not edit, for example ("tests/",).
    """

    def __init__(self, source=REPO, protected=()):
        """Copies the repository "source" into a new temporary folder."""
        self.source = Path(source).resolve()
        self.folder = Path(tempfile.mkdtemp(prefix="north_cycles_")).resolve()
        shutil.copytree(self.source, self.folder, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(*IGNORED_FOLDERS))
        self.protected = tuple(protected)

    def path(self, name):
        """The absolute path of a file in the copy; ValueError if it tries to
        leave it."""
        path = (self.folder / str(name).strip()).resolve()
        if path != self.folder and not path.is_relative_to(self.folder):
            raise ValueError(f'"{name}" is outside the repository.')
        return path

    def relative(self, path):
        """The path of a file relative to the copy, with forward slashes."""
        return Path(path).relative_to(self.folder).as_posix()

    def is_protected(self, relative):
        """True if the (relative) path cannot be edited."""
        return path_matches(relative, self.protected)

    def delete(self):
        """Deletes the copy from disk."""
        shutil.rmtree(self.folder, ignore_errors=True)

    def __enter__(self):
        """Lets the workspace be used with "with": it is deleted on exit."""
        return self

    def __exit__(self, *exception):
        """Deletes the copy on leaving the "with" block."""
        self.delete()


def path_matches(relative, paths):
    """True if the relative path is one of "paths" or is inside one of its folders
    (folders end in /)."""
    return any(relative == p or (p.endswith("/") and relative.startswith(p))
               for p in paths)


def files_in(folder):
    """The relative paths of all the files in a folder, sorted."""
    folder = Path(folder)
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*")
                  if p.is_file() and not IGNORED_FOLDERS & set(p.parts))


def truncate(text, maximum=MAX_OUTPUT):
    """Keeps the end of a long text, which is where the errors usually are."""
    text = text.strip()
    if len(text) <= maximum:
        return text
    return f"[… {len(text) - maximum} characters omitted …]\n" + text[-maximum:]


def run_python(arguments, folder, seconds):
    """Runs the current Python with some arguments inside a folder.
    Returns (exit code, output) or (None, notice) if it takes too long."""
    environment = dict(os.environ, PYTHONIOENCODING="utf-8",
                       PYTHONDONTWRITEBYTECODE="1")
    try:
        r = subprocess.run([sys.executable, *arguments], cwd=folder, env=environment,
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=seconds)
    except subprocess.TimeoutExpired:
        return None, f"The command took more than {seconds} seconds and was stopped."
    return r.returncode, r.stdout + r.stderr


def unittest_summary(output):
    """The last line of unittest ("OK" or "FAILED (failures=1)") and the number of
    tests run."""
    ran = re.search(r"Ran (\d+) tests?", output)
    final = re.search(r"^(OK.*|FAILED.*)$", output, re.M)
    return {"ran": int(ran.group(1)) if ran else 0,
            "result": final.group(1) if final else "no summary"}


# --- The tools ------------------------------------------------------------------

class Tools:
    """The tools the agent can call, on a Workspace.

    Each tool returns a dictionary that can be turned into JSON. If something
    fails, the dictionary has an "error" and, when it helps, a "hint". Every call
    is kept in self.log, with its result and its duration.
    """

    def __init__(self, workspace):
        """Sets up the tools on a workspace, with an empty log."""
        self.workspace = workspace
        self.log = []

    def call(self, name, arguments=None):
        """Runs a tool by its name, as the model would ask for it."""
        start = time.time()
        function = getattr(self, name, None) if name in TOOL_NAMES else None
        if function is None:
            result = {"error": f'There is no tool "{name}".',
                      "hint": "Tools: " + ", ".join(sorted(TOOL_NAMES)) + "."}
        else:
            try:
                result = function(**(arguments or {}))
            except TypeError as e:
                result = {"error": f"Invalid arguments: {e}"}
            except ValueError as e:
                result = {"error": str(e)}
        self.log.append({"tool": name, "arguments": arguments or {},
                         "ok": "error" not in result,
                         "seconds": round(time.time() - start, 2),
                         "result": result})
        return result

    def list_files(self, folder="."):
        """The files of a folder of the repository, with their number of lines."""
        path = self.workspace.path(folder)
        if not path.is_dir():
            return {"error": f'There is no folder "{folder}".',
                    "hint": 'Use "." for the repository root.'}
        rows = []
        for relative in files_in(path):
            text = (path / relative).read_text(encoding="utf-8", errors="replace")
            rows.append(f"{relative} ({len(text.splitlines())} lines)")
        return {"folder": folder, "files": rows}

    def read_file(self, path, start=1, end=None):
        """Lines "start"-"end" of a file, numbered (150 at most)."""
        file = self.workspace.path(path)
        if not file.is_file():
            return {"error": f'There is no file "{path}".',
                    "hint": "Use list_files to see the paths."}
        lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        start = max(1, int(start))
        end = len(lines) if end is None else min(int(end), len(lines))
        if start > len(lines):
            return {"error": f'"{path}" only has {len(lines)} lines.'}
        end = min(end, start + MAX_READ_LINES - 1)
        numbered = (f"{i:4d}| {lines[i - 1]}" for i in range(start, end + 1))
        content = "\n".join(numbered)
        result = {"path": path, "lines": f"{start}-{end} of {len(lines)}",
                  "content": content}
        if end < len(lines):
            result["more"] = f"More lines: read with start={end + 1}."
        return result

    def search(self, pattern, folder=".", files="*.py"):
        """The lines that match a regular expression, as "path:line: text"."""
        try:
            expression = re.compile(pattern)
        except re.error as e:
            return {"error": f"Invalid regular expression: {e}.",
                    "hint": "To search for literal text, escape ( ) [ ] . * with \\."}
        base = self.workspace.path(folder)
        if base.is_file():                     # a single file can be searched too
            base, files = base.parent, base.name
        if not base.is_dir():
            return {"error": f'There is no folder "{folder}".'}
        found = []
        for relative in files_in(base):
            if not fnmatch.fnmatch(Path(relative).name, files):
                continue
            text = (base / relative).read_text(encoding="utf-8", errors="replace")
            path = self.workspace.relative(base / relative)
            for number, line in enumerate(text.splitlines(), 1):
                if expression.search(line):
                    found.append(f"{path}:{number}: {line.strip()}")
        result = {"pattern": pattern, "total": len(found),
                  "results": found[:MAX_RESULTS]}
        if len(found) > MAX_RESULTS:
            result["hint"] = "There are more results: narrow the pattern or the folder."
        return result

    def create_file(self, path, content):
        """Creates a new file with the given content; it never overwrites one."""
        file = self.workspace.path(path)
        relative = self.workspace.relative(file)
        if self.workspace.is_protected(relative):
            return {"error": f'"{relative}" is protected: it cannot be created.'}
        if file.exists():
            return {"error": f'"{relative}" already exists.',
                    "hint": "To change it, use edit."}
        failure = syntax_error(relative, content)
        if failure:
            return failure
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8", newline="\n")
        return {"created": relative, "lines": len(content.splitlines())}

    def edit(self, path, old, new):
        """Replaces an exact piece of a file, which must appear only once."""
        file = self.workspace.path(path)
        relative = self.workspace.relative(file)
        if self.workspace.is_protected(relative):
            return {"error": f'"{relative}" is protected: it cannot be changed.'}
        if not file.is_file():
            return {"error": f'There is no file "{path}".',
                    "hint": "Use list_files to see the paths, or create_file for a "
                            "new one."}
        if old == "":
            return {"error": '"old" is empty.',
                    "hint": "Copy the exact piece you want to replace."}
        if re.search(r"^\s*\d+\| ", old, re.M):
            return {"error": "The text to replace includes line numbers.",
                    "hint": 'Copy the code without the "  12| " prefix.'}
        text = file.read_text(encoding="utf-8")
        times = text.count(old)
        if times == 0:
            return {"error": "The text to replace does not appear in the file.",
                    **similar_hint(text, old)}
        if times > 1:
            lines = [text[:m.start()].count("\n") + 1
                     for m in re.finditer(re.escape(old), text)]
            return {"error": f"The text to replace appears {times} times "
                             f"(lines {', '.join(map(str, lines))}).",
                    "hint": "Add surrounding lines to make it unique."}
        start = text[:text.index(old)].count("\n") + 1
        changed = text.replace(old, new)
        failure = syntax_error(relative, changed)
        if failure:
            return failure
        file.write_text(changed, encoding="utf-8", newline="\n")
        return {"edited": relative,
                "lines": f"{start}-{start + new.count(chr(10))}"}

    def run_tests(self):
        """Runs the visible tests (tests/ folder) and summarizes the result."""
        code, output = run_python(TEST_COMMAND, self.workspace.folder, TEST_SECONDS)
        return {"all_pass": code == 0, **unittest_summary(output),
                "output": truncate(output)}

    def run_command(self, command):
        """Runs a command from the allowed list, without a shell and inside the
        copy."""
        try:
            parts = shlex.split(command)
        except ValueError as e:
            return {"error": f"The command cannot be understood: {e}."}
        if not any(tuple(parts[:len(p)]) == p for p in ALLOWED_COMMANDS):
            allowed = "; ".join(" ".join(p) + " …" for p in ALLOWED_COMMANDS)
            return {"error": "Command not allowed.",
                    "hint": f"Allowed: {allowed}"}
        for argument in parts[1:]:
            if ".." in argument or Path(argument).is_absolute():
                return {"error": f'Argument not allowed: "{argument}".',
                        "hint": "Use relative paths inside the repository."}
        code, output = run_python(parts[1:], self.workspace.folder, COMMAND_SECONDS)
        return {"exit_code": code, "output": truncate(output)}


TOOL_NAMES = {"list_files", "read_file", "search", "create_file", "edit",
              "run_tests", "run_command"}


def syntax_error(relative, text):
    """If a Python file would be left with a syntax error, the error with the
    surrounding lines as they would be; None if it is fine or not Python. This way
    a badly indented edit does not break the file: it is rejected and the file
    does not change."""
    if not relative.endswith(".py"):
        return None
    try:
        compile(text, relative, "exec")
    except SyntaxError as e:
        lines = text.splitlines()
        number = e.lineno or 1
        near = range(max(1, number - 3), min(len(lines), number + 2) + 1)
        return {"error": f'The edit would leave "{relative}" with a syntax error '
                         f"on line {number}: {e.msg}. Nothing was changed.",
                "hint": 'Check the indentation of "new": it must fit the '
                        "indentation of the surrounding lines.",
                "would_be": "\n".join(f"{i:4d}| {lines[i - 1]}" for i in near)}
    return None


def similar_hint(text, old):
    """A hint when the text to replace does not appear. It looks for the line of
    the file most similar to the first line searched for and, from it, the first
    line that does not match, which usually gives away a different space or quote.
    It also returns the actual piece of the file, to copy it as it is."""
    if "\\n" in old and old.replace("\\n", "\n") in text:
        return {"hint": 'You wrote "\\n" as two characters: use real line '
                        "breaks."}
    searched = old.splitlines()
    first = next((l for l in searched if l.strip()), "")
    lines = text.splitlines()
    similar = difflib.get_close_matches(first, lines, n=1, cutoff=0.6)
    if not similar:
        return {"hint": "Read the file and copy the exact piece."}
    start = lines.index(similar[0])
    start -= searched.index(first)             # in case it starts with empty lines
    actual = lines[max(start, 0):start + len(searched)]
    for k, (wanted, real) in enumerate(zip(searched, actual)):
        if wanted != real:
            return {"hint": f"Line {start + k + 1} of the file does not match "
                            f"line {k + 1} of your text: in the file it is "
                            f'"{real}" and you wrote "{wanted}". Copy the actual '
                            "piece, with its spaces.",
                    "actual_text": "\n".join(actual)}
    return {"hint": f"The piece starts on line {start + 1}, but the file ends "
                    "earlier or continues differently. Read it and copy the exact "
                    "piece."}


# --- Schemas for the model ------------------------------------------------------

def schema(name, description, parameters=None, required=()):
    """The JSON schema of a tool, in the format of chat templates.
    "parameters" is {name: (JSON type, description)}."""
    properties = {p: {"type": kind, "description": text}
                  for p, (kind, text) in (parameters or {}).items()}
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": properties,
                       "required": list(required)}}}


SCHEMAS = [
    schema("list_files",
           "Lists the files of a folder of the repository (and its subfolders), "
           "with the number of lines of each one.",
           {"folder": ("string", 'Folder relative to the root; "." by default.')}),
    schema("read_file",
           "Reads a range of lines of a file, 150 at most each time. Each line "
           "starts with its number and a bar, which are not part of the code.",
           {"path": ("string", "Path of the file, for example shipping.py."),
            "start": ("integer", "First line (1 by default)."),
            "end": ("integer", "Last line (by default, up to the end).")},
           ["path"]),
    schema("search",
           "Searches the files for a Python regular expression and returns "
           '"path:line: text" for each match.',
           {"pattern": ("string", "Regular expression, for example def zone."),
            "folder": ("string", 'Folder or file to search in; "." by default.'),
            "files": ("string", "File name pattern; *.py by default.")},
           ["pattern"]),
    schema("create_file",
           "Creates a new file with the given content. It does not overwrite files "
           "that already exist.",
           {"path": ("string", "Path of the new file, for example tests/test_x.py."),
            "content": ("string", "Full text of the file.")},
           ["path", "content"]),
    schema("edit",
           "Edits a file by replacing an exact piece, which must appear only once, "
           "with another. Copy the piece without the line numbers.",
           {"path": ("string", "Path of the file."),
            "old": ("string", "Exact text that is replaced."),
            "new": ("string", "New text.")},
           ["path", "old", "new"]),
    schema("run_tests",
           "Runs the tests of the repository (tests/ folder) and returns whether "
           "they all pass, the summary and the end of the output."),
    schema("run_command",
           "Runs an allowed command at the root of the repository: python manage.py "
           "…, python -m unittest … or python -m py_compile ….",
           {"command": ("string", "The full command, for example "
                                  "python manage.py sold_out 2026-10-13.")},
           ["command"]),
]


# --- Evaluating an attempt ------------------------------------------------------

def read_task(task_id):
    """The request, the scope contract and the data of a task of the bank
    (T01…T20)."""
    folder = TASKS / task_id

    def read(name):
        """The text of a file in the task folder."""
        return (folder / name).read_text(encoding="utf-8")

    return {"id": task_id, "folder": folder, "request": read("request.md"),
            "contract": json.loads(read("contract.json")),
            "meta": json.loads(read("meta.json"))}


def differences(original, copy):
    """What has changed in the copy: modified, new and deleted files, and the
    unified diff of all of them."""
    before, after = set(files_in(original)), set(files_in(copy))
    modified = sorted(r for r in before & after
                      if (Path(original) / r).read_bytes()
                      != (Path(copy) / r).read_bytes())
    new, deleted = sorted(after - before), sorted(before - after)
    parts = []
    for relative in modified + new + deleted:
        parts += difflib.unified_diff(lines_of(Path(original) / relative),
                                      lines_of(Path(copy) / relative),
                                      f"a/{relative}", f"b/{relative}")
    return {"modified": modified, "new": new, "deleted": deleted,
            "changed": modified + new + deleted, "diff": "".join(parts)}


def lines_of(path):
    """The lines of a file, with their line breaks; none if it does not exist."""
    return path.read_text(encoding="utf-8").splitlines(True) if path.exists() else []


def check_scope(changed, contract):
    """The changed files that are not among the allowed paths and those that are
    among the forbidden ones."""
    return {"out_of_scope": [r for r in changed
                             if not path_matches(r, contract["allowed_paths"])],
            "forbidden": [r for r in changed
                          if path_matches(r, contract["forbidden_paths"])]}


def run_hidden(folder, task):
    """Runs the hidden tests of a task inside a copy. It copies them into a
    separate folder, runs them and deletes them, whatever happens."""
    destination = Path(folder) / "_hidden"
    shutil.copytree(task["folder"] / "hidden_tests", destination, dirs_exist_ok=True)
    try:
        code, output = run_python(
            ["-m", "unittest", "discover", "-s", "_hidden"], folder, TEST_SECONDS)
    finally:
        shutil.rmtree(destination, ignore_errors=True)
    return {"pass": code == 0, **unittest_summary(output),
            "output": truncate(output)}


def evaluate_attempt(workspace, task):
    """Evaluates a finished attempt on its copy of the repository.

    A task is solved if the hidden and the visible tests pass and no forbidden
    path has been touched. Changes outside the allowed paths are counted
    separately: they do not invalidate the task, but they are work someone will
    have to review.
    """
    if isinstance(task, str):
        task = read_task(task)
    changes = differences(workspace.source, workspace.folder)
    scope = check_scope(changes["changed"], task["contract"])
    visible = Tools(workspace).run_tests()
    hidden = run_hidden(workspace.folder, task)
    return {"task": task["id"],
            "solved": hidden["pass"] and visible["all_pass"]
                      and not scope["forbidden"],
            "hidden": hidden["pass"], "visible": visible["all_pass"],
            "tests_touched": [r for r in changes["changed"]
                              if r.startswith("tests/")],
            **scope, "changed": changes["changed"], "diff": changes["diff"],
            "hidden_output": hidden["output"]}


# --- Applying a solution with the tools themselves -------------------------------

def replacements(before, after):
    """Turns the change of a file into replacements (old, new) that can be applied
    with the edit tool: one piece per group of changes, with just enough lines of
    context for the piece searched for to be unique."""
    old_lines, new_lines = before.splitlines(True), after.splitlines(True)
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    for context in (1, 2, 3, 5, 8, 13):
        pieces = []
        for group in matcher.get_grouped_opcodes(context):
            i1, i2 = group[0][1], group[-1][2]
            j1, j2 = group[0][3], group[-1][4]
            pieces.append(("".join(old_lines[i1:i2]), "".join(new_lines[j1:j2])))
        if all(old and before.count(old) == 1 for old, _ in pieces):
            return pieces
    return [(before, after)]  # last resort: the whole file


def apply_solution(tools, solution_folder):
    """Applies a reference solution (the changed files) with the edit tool, piece
    by piece, as the agent would. Returns the results."""
    results = []
    for relative in files_in(solution_folder):
        after = (Path(solution_folder) / relative).read_text(encoding="utf-8")
        current = tools.workspace.path(relative)
        if not current.exists():
            results.append(tools.call(
                "create_file", {"path": relative, "content": after}))
            continue
        before = current.read_text(encoding="utf-8")
        for old, new in replacements(before, after):
            results.append(tools.call(
                "edit", {"path": relative, "old": old, "new": new}))
    return results


# --- Self-test ------------------------------------------------------------------

def check(condition, description):
    """Shows one check of the self-test and returns whether it holds."""
    print(("  ok    " if condition else "  FAIL  ") + description)
    return condition


def self_test():
    """Tests the tools without a model: typical errors, a task's solution applied
    with edit, and an attempt that touches a forbidden path."""
    ok = True
    print("Tools")
    with Workspace() as workspace:
        t = Tools(workspace)
        files = " ".join(t.call("list_files")["files"])
        ok &= check("shipping.py (" in files, "list_files sees shipping.py")
        reading = t.call("read_file", {"path": "orders.py", "start": 5, "end": 8})
        ok &= check(reading["lines"].startswith("5-8"), "read_file by range")
        ok &= check("error" in t.call("read_file", {"path": "../INDEX.md"}),
                    "read_file does not leave the repository")
        found = t.call("search", {"pattern": r"def zone\("})
        ok &= check(found["results"][0].startswith("shipping.py:"),
                    "search finds def zone")
        repeated = t.call("edit", {"path": "notices.py", "old": "Best regards",
                                   "new": "Regards"})
        ok &= check("times" in repeated.get("error", ""),
                    "edit rejects a repeated piece")
        similar = t.call("edit", {"path": "shipping.py",
                                  "old": "def zone(code):", "new": "x"})
        ok &= check("def zone" in similar.get("hint", ""),
                    "edit points to the most similar line")
        ok &= check("error" in t.call("run_command", {"command": "rm -rf ."}),
                    "run_command rejects commands that are not allowed")
        command = t.call("run_command",
                         {"command": "python manage.py sold_out 2026-10-13"})
        ok &= check(command["exit_code"] == 0 and "E-City 600" in command["output"],
                    "run_command with manage.py")
        ok &= check(t.call("run_tests")["all_pass"],
                    "the visible tests pass on the original")
        ok &= check(len(t.log) == 9, "the log keeps every call")

    print("Reference solution of T16 applied with edit")
    with Workspace() as workspace:
        t = Tools(workspace)
        task = read_task("T16")
        ok &= check(not evaluate_attempt(workspace, task)["hidden"],
                    "before, the hidden tests fail")
        edits = apply_solution(t, task["folder"] / "solution")
        ok &= check(all("edited" in e for e in edits),
                    f"{len(edits)} edits without errors")
        evaluation = evaluate_attempt(workspace, task)
        ok &= check(evaluation["solved"], "after, the task is solved")
        ok &= check(not evaluation["out_of_scope"], "no changes out of scope")

    print("An attempt that fixes the data instead of the code (T02)")
    with Workspace() as workspace:
        t = Tools(workspace)
        t.call("edit", {"path": "data/orders.json",
                        "old": '"zip_code": 907',
                        "new": '"zip_code": "00907"'})
        evaluation = evaluate_attempt(workspace, "T02")
        ok &= check(not evaluation["solved"], "it does not count as solved")
        ok &= check(evaluation["forbidden"] == ["data/orders.json"],
                    "it detects the forbidden path")
    print("All good." if ok else "Some checks fail.")
    return ok


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
