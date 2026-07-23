# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:35:29 2026

@author: Sarah
"""

import scipy.io
import numpy as np


def compare(
    matlab_file,
    python_file,
    tolerance=1e-10
):

    matlab = scipy.io.loadmat(
        matlab_file
    )

    python = scipy.io.loadmat(
        python_file
    )


    ignored = {
        "__header__",
        "__version__",
        "__globals__"
    }


    keys = (
        set(matlab.keys())
        |
        set(python.keys())
    )


    passed = True


    for key in keys:

        if key in ignored:
            continue


        if key not in matlab:

            print(
                f"Missing MATLAB variable {key}"
            )

            passed = False
            continue


        if key not in python:

            print(
                f"Missing Python variable {key}"
            )

            passed = False
            continue


        a = matlab[key]
        b = python[key]


        if np.shape(a) != np.shape(b):

            print(
                f"{key}: shape mismatch "
                f"{a.shape} vs {b.shape}"
            )

            passed = False
            continue


        error = np.max(
            np.abs(a-b)
        )


        if error > tolerance:

            print(
                f"{key}: FAILED "
                f"error={error}"
            )

            passed = False

        else:

            print(
                f"{key}: PASS "
                f"error={error}"
            )


    return passed