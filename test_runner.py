"""
test_runner.py

MATLAB vs Python numerical equivalence testing.
"""

from pathlib import Path
import subprocess
import numpy as np

from scipy.io import loadmat



def run_matlab(matlab_file):

    """
    Run MATLAB script.
    MATLAB script must save matlab_result.mat
    """

    folder = matlab_file.parent
    name = matlab_file.stem


    command = [
        "matlab",
        "-batch",
        f"cd('{folder}'); {name}"
    ]


    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )


    if result.returncode != 0:
        raise RuntimeError(
            result.stderr
        )


def run_python(python_file):

    """
    Run generated Python script.
    Python script must save python_result.mat
    """

    result = subprocess.run(
        [
            "python",
            str(python_file)
        ],
        capture_output=True,
        text=True
    )


    if result.returncode != 0:
        raise RuntimeError(
            result.stderr
        )



def compare_mat_files(
        matlab_result,
        python_result
):

    matlab = loadmat(
        matlab_result
    )

    python = loadmat(
        python_result
    )


    matlab_keys = {
        k for k in matlab.keys()
        if not k.startswith("__")
    }


    python_keys = {
        k for k in python.keys()
        if not k.startswith("__")
    }


    if matlab_keys != python_keys:

        return {
            "success":False,
            "error":
                f"Variable mismatch: "
                f"{matlab_keys} vs {python_keys}"
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

        return {
            "success":False,
            "errors":errors
        }


    return {
        "success":True
    }



def run_equivalence_test(
        matlab_file,
        python_file
):

    folder = matlab_file.parent


    matlab_result = (
        folder /
        "matlab_result.mat"
    )


    python_result = (
        folder /
        "python_result.mat"
    )


    try:

        run_matlab(
            matlab_file
        )


        run_python(
            python_file
        )


        return compare_mat_files(
            matlab_result,
            python_result
        )


    except Exception as e:

        return {
            "success":False,
            "error":str(e)
        }