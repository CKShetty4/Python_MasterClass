# run_tests.py (robust change-detection + diagnostics)
import unittest
import os
import time
import tracemalloc
from io import StringIO
import importlib
import ast
import io
import tokenize
import difflib
import sys

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

def find_student_file_for_test(test_filename):
    """Try several common locations for the student's file.

    test_filename is like "test_welcome_message.py" -> base "welcome_message"
    We'll try:
      - BASE/<base>/<base>.py
      - BASE/<base>.py
      - BASE/<Base>/<Base>.py (titlecased)
    """
    base = test_filename[len("test_"):-3]  # remove 'test_' and '.py'
    candidates = [
        os.path.join(BASE_DIR, base, base + ".py"),
        os.path.join(BASE_DIR, base + ".py"),
    ]
    # also try Title_Case / Camel-ish variant (handles Alien_Visit)
    alt = "".join(part.capitalize() if "_" in base else part for part in base.split("_"))
    candidates.append(os.path.join(BASE_DIR, alt, alt + ".py"))
    for c in candidates:
        if os.path.exists(c):
            return c
    # if none exist, return the first candidate (useful so caller can see attempted path)
    return candidates[0]

# ---- normalization utilities ----
def ast_equal(src1, src2):
    """Return True if ASTs are identical, False if different, None if either fails to parse."""
    try:
        a1 = ast.parse(src1)
        a2 = ast.parse(src2)
    except SyntaxError:
        return None
    return ast.dump(a1, include_attributes=False) == ast.dump(a2, include_attributes=False)

def normalized_code_lines(src):
    """Return list of logical code lines after removing comments/encodings/indent/dedent/newlines.
    This is a line-oriented, whitespace-agnostic representation suitable for 'added/removed line' checks.
    """
    if src is None:
        return []
    try:
        reader = io.StringIO(src).readline
        lines_map = {}
        for tok in tokenize.generate_tokens(reader):
            toknum, tokval, (srow, _), _, _ = tok
            # Ignore comments, encoding, pure newlines and indentation tokens
            if toknum in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING):
                continue
            lines_map.setdefault(srow, []).append(tokval)
        # produce ordered lines; strip surrounding whitespace and ignore empty lines
        result = []
        for lineno in sorted(lines_map):
            joined = "".join(lines_map[lineno]).strip()
            if joined:
                result.append(joined)
        return result
    except Exception:
        # Fallback: remove lines that are only whitespace or comments (simple heuristic)
        out = []
        for ln in src.splitlines():
            s = ln.strip()
            if not s:
                continue
            if s.startswith("#"):
                continue
            out.append(" ".join(s.split()))
        return out

def files_have_meaningful_diff(template_src, student_src):
    """Return True if there is a meaningful difference (ignore whitespace/comments)."""
    # 1) Try AST equality: if both parse and AST equal -> no meaningful change
    ast_res = ast_equal(template_src, student_src)
    if ast_res is True:
        return False
    if ast_res is False:
        return True
    # ast_res is None (parse failure for at least one) -> fall back to line-based compare
    templ_lines = normalized_code_lines(template_src)
    stud_lines = normalized_code_lines(student_src)
    return templ_lines != stud_lines

def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

# ---- Test runner ----
def run_test_module(module_name):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(module_name)
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)

    tracemalloc.start()
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    duration = end_time - start_time
    output = stream.getvalue()
    return result, output, duration, peak_mem

if __name__ == "__main__":
    debug = ("--debug" in sys.argv) or (os.environ.get("DEBUG_TESTS") == "1")
    print(YELLOW + f"Running all tests in '{TEST_DIR}'..." + RESET)
    total_passed = 0
    total_failed = 0

    for test_file in sorted(os.listdir(TEST_DIR)):
        if not (test_file.startswith("test_") and test_file.endswith(".py")):
            continue
        module_name = f"tests.{test_file[:-3]}"
        print(YELLOW + f"\nTesting {module_name}..." + RESET)

        student_file = find_student_file_for_test(test_file)

        # import the test module to read TEMPLATE_SOURCE or custom hook
        try:
            test_mod = importlib.import_module(module_name)
        except Exception as e:
            print(RED + f"❌ Could not import {module_name}: {e}" + RESET)
            continue

        # If test module supplies its own student_changed routine, prefer it
        changed = None
        if hasattr(test_mod, "student_changed"):
            try:
                changed = bool(test_mod.student_changed(student_file))
            except Exception as e:
                print(YELLOW + f"⚠ Warning: {module_name}.student_changed() raised {e}. Falling back to template compare." + RESET)
                changed = None

        # If module provides TEMPLATE_SOURCE, compare it to the student's file
        if changed is None and hasattr(test_mod, "TEMPLATE_SOURCE"):
            template_src = test_mod.TEMPLATE_SOURCE
            student_src = read_file_safe(student_file)
            if student_src is None:
                # student file not found -> no change (skip) but show where we looked
                if debug:
                    print(RED + f"Student file not found at: {student_file}" + RESET)
                changed = False
            else:
                changed = files_have_meaningful_diff(template_src, student_src)
                if not changed and debug:
                    print(YELLOW + "No meaningful diff detected between TEMPLATE_SOURCE and student file." + RESET)
                    templ_lines = normalized_code_lines(template_src)
                    stud_lines = normalized_code_lines(student_src)
                    print(YELLOW + "--- TEMPLATE (normalized) ---" + RESET)
                    for i, L in enumerate(templ_lines[:12], 1):
                        print(f"{i:3d}: {L}")
                    print(YELLOW + "--- STUDENT (normalized) ---" + RESET)
                    for i, L in enumerate(stud_lines[:12], 1):
                        print(f"{i:3d}: {L}")
                    # show small unified diff of the normalized lines
                    ud = "\n".join(difflib.unified_diff(templ_lines, stud_lines, lineterm=""))
                    if ud:
                        print(YELLOW + "--- unified diff (normalized) ---" + RESET)
                        print(ud)
        # fallback: legacy marker-based check (useful when no template is embedded)
        if changed is None:
            # try legacy marker in student file (same as before)
            def legacy_check(path):
                if not os.path.exists(path):
                    return False
                with open(path, "r", encoding="utf-8") as f:
                    lines = [ln.strip() for ln in f.readlines()]
                legacy_marker = "#Code here"
                if legacy_marker in lines:
                    idx = lines.index(legacy_marker)
                    for line in lines[idx+1:]:
                        if line and not line.startswith("#"):
                            return True
                    return False
                return True
            changed = legacy_check(student_file)

        if not changed:
            print(RED + "❌ Student has not changed the template (no code changes detected). Skipping this test." + RESET)
            if debug:
                print(YELLOW + f"(Looked for student file at: {student_file})" + RESET)
            continue

        # Run tests
        try:
            result, output, duration, peak_mem = run_test_module(module_name)
        except Exception as e:
            print(RED + f"❌ Failed to run {module_name}: {e}" + RESET)
            continue

        print(output)
        failed = len(result.failures) + len(result.errors)
        passed = max(0, result.testsRun - failed)   # prevent negative
        total_passed += passed
        total_failed += failed


        print(f"Duration: {duration:.4f} sec | Peak Memory: {peak_mem} bytes")
        if failed == 0:
            print(GREEN + f"✅ All {passed} test cases passed!" + RESET)
        else:
            print(RED + f"❌ {failed} test case(s) failed, {passed} passed." + RESET)

    print("\n" + YELLOW + "="*50 + RESET)
    print(GREEN + f"Total passed: {total_passed}" + RESET)
    print(RED + f"Total failed: {total_failed}" + RESET)
    print(YELLOW + "="*50 + RESET)
