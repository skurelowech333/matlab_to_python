# -*- coding: utf-8 -*-
"""
Batch conversion + numerical equivalence test runner with explicit inputs.

For each MATLAB file in matlab_tests/:
    1. Convert .m -> .py using main.convert_file()
    2. If test inputs are configured for that function:
        - Call the MATLAB function with those inputs
        - Call the Python function with the same inputs
        - Save matlab_result.mat and python_result.mat
        - Compare outputs
    3. Record both conversion and equivalence results
    4. Write full_report.json with all details

Assumptions:
    - Each .m file defines a top-level function whose name == file stem.
    - Functions return a SINGLE output (stored as variable 'result').
    - MATLAB is installed and matlab_exe path is correct.
"""

from pathlib import Path
import json
import subprocess
import importlib.util

import numpy as np
from scipy.io import loadmat, savemat

from main import convert_file  # your existing conversion pipeline


# ==========================================================
# TEST CASES: configure inputs per function here
# ==========================================================
# Keys: MATLAB file stem (function name)
# Values: list/tuple of positional arguments to pass
TEST_CASES = {
    # Example:
    # "myfunc_single": [2.0],
    # "myfunc_multi": [3.0, 4.0],
}


# Default MATLAB executable path (override via CLI if needed)
DEFAULT_MATLAB_EXE = r"C:\Program Files\MATLAB\R2023b\bin\matlab.exe"


# ==========================================================
# Equivalence test helpers
# ==========================================================

def run_matlab_with_inputs(matlab_file: Path, matlab_exe: str, inputs) -> None:
    """
    Run MATLAB function with given inputs.

    Assumes:
        - File matlab_file defines function F where F == matlab_file.stem
        - Function has a single output:
              result = F(arg1, arg2, ...)
        - Saves 'matlab_result.mat' with variable 'result'.
    """
    folder = matlab_file.parent
    func_name = matlab_file.stem

    print(f"Trying to run MATLAB function {func_name} with inputs {inputs} ...")

    # Build argument string: e.g. "1, 2, 3" or "2.0, 3.5"
    arg_str = ", ".join(repr(x) for x in inputs) if inputs else ""

    # MATLAB batch command:
    #   cd('folder'); result = func_name(args); save('matlab_result.mat','result');
    cmd = (
        f"cd('{folder}'); "
        f"result = {func_name}({arg_str}); "
        f"save('matlab_result.mat','result');"
    )

    command = [matlab_exe, "-batch", cmd]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("MATLAB stderr:\n", result.stderr)
        raise RuntimeError(result.stderr)


def run_python_with_inputs(python_file: Path, inputs) -> None:
    """
    Import generated Python module, call corresponding function with inputs,
    and save python_result.mat with variable 'result'.

    Assumes:
        - python_file defines a function F where F == python_file.stem
        - Function returns a single output.
    """
    folder = python_file.parent
    module_name = python_file.stem
    func_name = module_name  # same as stem

    print(f"Trying to run Python function {func_name} with inputs {inputs} ...")

    # Dynamically import module from file
    spec = importlib.util.spec_from_file_location(module_name, python_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {python_file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get function
    if not hasattr(module, func_name):
        raise AttributeError(f"Python module {module_name} has no function {func_name}")

    func = getattr(module, func_name)

    # Call function with inputs
    result = func(*inputs)

    # Save result to python_result.mat
    python_result_path = folder / "python_result.mat"
    # Normalize to numpy array where possible
    savemat(python_result_path, {"result": np.array(result)})


def compare_mat_files(matlab_result: Path, python_result: Path) -> dict:
    """
    Compare variables in two .mat files using np.testing.assert_allclose.
    """
    matlab = loadmat(matlab_result)
    python = loadmat(python_result)

    matlab_keys = {k for k in matlab.keys() if not k.startswith("__")}
    python_keys = {k for k in python.keys() if not k.startswith("__")}

    if matlab_keys != python_keys:
        return {
            "success": False,
            "error": f"Variable mismatch: {matlab_keys} vs {python_keys}"
        }

    errors = {}

    for key in matlab_keys:
        try:
            np.testing.assert_allclose(
                matlab[key],
                python[key],
                rtol=1e-10,
                atol=1e-12
            )
        except AssertionError as e:
            errors[key] = str(e)

    if errors:
        return {"success": False, "errors": errors}

    return {"success": True}


def run_equivalence_test_with_inputs(
    matlab_file: Path,
    python_file: Path,
    matlab_exe: str,
    inputs
) -> dict:
    """
    Run MATLAB and Python functions with given inputs, and compare .mat outputs.
    """
    folder = matlab_file.parent

    matlab_result = folder / "matlab_result.mat"
    python_result = folder / "python_result.mat"

    try:
        run_matlab_with_inputs(matlab_file, matlab_exe, inputs)
        run_python_with_inputs(python_file, inputs)
        return compare_mat_files(matlab_result, python_result)
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==========================================================
# Batch runner
# ==========================================================

def run_all_tests(
    matlab_root: str = "matlab_tests",
    report_filename: str = "full_report.json",
    matlab_exe: str = DEFAULT_MATLAB_EXE,
) -> None:
    """
    Convert and test every .m file under matlab_root for which we have inputs.

    Parameters
    ----------
    matlab_root : str
        Root directory containing MATLAB test files (default: 'matlab_tests').
    report_filename : str
        Output JSON report filename (default: 'full_report.json').
    matlab_exe : str
        Full path to MATLAB executable.
    """
    root = Path(matlab_root)

    if not root.exists():
        raise FileNotFoundError(f"MATLAB root directory not found: {root}")

    matlab_files = sorted(root.rglob("*.m"))

    if not matlab_files:
        print(f"No MATLAB files found under {root}")
        return

    print(f"Found {len(matlab_files)} MATLAB files under {root}")
    all_results = []

    for m_file in matlab_files:
        print(f"\n=== Processing {m_file} ===")

        func_name = m_file.stem
        inputs = TEST_CASES.get(func_name)

        # 1) Run the existing conversion pipeline
        conversion_report = convert_file(m_file)

        # Extract the generated Python file path, if any
        translation_stage = conversion_report["stages"].get("translation", {})
        py_path_str = translation_stage.get("output")
        python_file = Path(py_path_str) if py_path_str else None

        # 2) Run numerical equivalence test (if conversion succeeded AND we have inputs)
        if conversion_report.get("success") and python_file and python_file.exists():
            if inputs is not None:
                print(f"  Inputs configured for {func_name}: {inputs}")
                equivalence_report = run_equivalence_test_with_inputs(
                    m_file, python_file, matlab_exe, inputs
                )
            else:
                print(f"  No test inputs configured for {func_name}; skipping equivalence test.")
                equivalence_report = {
                    "success": False,
                    "error": f"No inputs configured for function {func_name}; equivalence test not run.",
                }
        else:
            print("  Conversion failed or Python file missing; skipping equivalence test.")
            equivalence_report = {
                "success": False,
                "error": "Conversion failed or Python file missing; equivalence test not run.",
            }

        # 3) Combine results for this file
        combined = {
            "matlab_file": str(m_file),
            "python_file": str(python_file) if python_file else None,
            "conversion": conversion_report,
            "equivalence": equivalence_report,
        }
        all_results.append(combined)

    # 4) Write consolidated JSON report
    out_path = Path(report_filename)
    out_path.write_text(json.dumps(all_results, indent=4), encoding="utf-8")

    print("\n==========================")
    print("Full Test Summary")
    print("==========================")
    successes = sum(
        1 for r in all_results
        if r["conversion"].get("success") and r["equivalence"].get("success")
    )
    failures = len(all_results) - successes
    print(f"Total files:         {len(all_results)}")
    print(f"Conversion+match OK: {successes}")
    print(f"Failed or mismatch:  {failures}")
    print(f"Report written to:   {out_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Batch MATLAB→Python conversion and equivalence tests with explicit inputs."
    )
    parser.add_argument(
        "--matlab-root",
        default="matlab_tests",
        help="Root directory containing MATLAB test files (default: matlab_tests)",
    )
    parser.add_argument(
        "--report",
        default="full_report.json",
        help="Output JSON report filename (default: full_report.json)",
    )
    parser.add_argument(
        "--matlab-exe",
        default=DEFAULT_MATLAB_EXE,
        help="Full path to MATLAB executable.",
    )

    args = parser.parse_args()

    run_all_tests(
        matlab_root=args.matlab_root,
        report_filename=args.report,
        matlab_exe=args.matlab_exe,
    )