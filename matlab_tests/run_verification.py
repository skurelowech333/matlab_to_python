# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:35:53 2026

@author: Sarah
"""

from pathlib import Path
import subprocess

from compare_mat import compare


MATLAB_DIR = Path(
    "../matlab_tests"
)


PYTHON_DIR = Path(
    "../matlab_tests"
)


RESULTS = Path(
    "results"
)

RESULTS.mkdir(
    exist_ok=True
)


for matlab_file in MATLAB_DIR.glob("*.m"):

    name = matlab_file.stem

    print("\n====================")
    print(name)
    print("====================")


    matlab_mat = (
        RESULTS /
        f"{name}_matlab.mat"
    )

    python_mat = (
        RESULTS /
        f"{name}_python.mat"
    )


    python_file = (
        PYTHON_DIR /
        f"{name}.py"
    )


    # MATLAB

    subprocess.run(
        [
            "python",
            "run_matlab_test.py",
            str(matlab_file),
            str(matlab_mat)
        ]
    )


    # Python

    subprocess.run(
        [
            "python",
            "run_python_test.py",
            str(python_file),
            str(python_mat)
        ]
    )


    # Compare

    result = compare(
        matlab_mat,
        python_mat
    )


    print(
        "RESULT:",
        "PASS" if result else "FAIL"
    )