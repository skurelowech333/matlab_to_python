# -*- coding: utf-8 -*-
"""
builtins.py

MATLAB built-in function translation table.

Maps MATLAB functions to Python/NumPy/SciPy equivalents.
"""



# ==========================================================
# NumPy mappings
# ==========================================================

NUMPY_FUNCTIONS = {


    # ------------------------------------------------------
    # Math functions
    # ------------------------------------------------------

    "sin": "np.sin",
    "cos": "np.cos",
    "tan": "np.tan",

    "asin": "np.arcsin",
    "acos": "np.arccos",
    "atan": "np.arctan",
    "atan2": "np.arctan2",

    "sinh": "np.sinh",
    "cosh": "np.cosh",
    "tanh": "np.tanh",

    "sqrt": "np.sqrt",

    "exp": "np.exp",

    "log": "np.log",
    "log10": "np.log10",

    "abs": "np.abs",

    "floor": "np.floor",
    "ceil": "np.ceil",
    "round": "np.round",



    # ------------------------------------------------------
    # Matrix / array creation
    # ------------------------------------------------------

    "zeros": "np.zeros",

    "ones": "np.ones",

    "eye": "np.eye",

    "linspace": "np.linspace",

    "logspace": "np.logspace",



    # ------------------------------------------------------
    # Matrix information
    # ------------------------------------------------------

    "length": "np.size",

    "size": "np.shape",

    "ndims": "np.ndim",



    # ------------------------------------------------------
    # Matrix manipulation
    # ------------------------------------------------------

    "reshape": "np.reshape",

    "transpose": "np.transpose",

    "diag": "np.diag",

    "trace": "np.trace",



    # ------------------------------------------------------
    # Linear algebra
    # ------------------------------------------------------

    "dot": "np.dot",

    "cross": "np.cross",

    "norm": "np.linalg.norm",



    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    "sum": "np.sum",

    "prod": "np.prod",

    "mean": "np.mean",

    "median": "np.median",

    "std": "np.std",

    "var": "np.var",

    "min": "np.min",

    "max": "np.max",



    # ------------------------------------------------------
    # Matrix utilities
    # ------------------------------------------------------

    "rank": "np.linalg.matrix_rank",

    "cond": "np.linalg.cond",

    "pinv": "np.linalg.pinv",

}



# ==========================================================
# SciPy mappings
# ==========================================================

SCIPY_FUNCTIONS = {


    # ------------------------------------------------------
    # Linear algebra
    # ------------------------------------------------------

    "eig":
        "np.linalg.eig",


    "eigvals":
        "np.linalg.eigvals",


    "svd":
        "np.linalg.svd",


    "inv":
        "np.linalg.inv",


    "det":
        "np.linalg.det",



    # ------------------------------------------------------
    # Optimization
    # ------------------------------------------------------

    "fmincon":
        "scipy.optimize.minimize",



    # ------------------------------------------------------
    # Integration
    # ------------------------------------------------------

    "ode45":
        "scipy.integrate.solve_ivp",

}



# ==========================================================
# Special MATLAB constants
# ==========================================================

SPECIAL_FUNCTIONS = {


    "pi":
        "np.pi",


    "inf":
        "np.inf",


    "NaN":
        "np.nan",


    "eps":
        "np.finfo(float).eps",

}



# ==========================================================
# Lookup
# ==========================================================

def translate_builtin(name: str) -> str:
    """
    Return Python equivalent of MATLAB function.
    """

    if name in NUMPY_FUNCTIONS:

        return NUMPY_FUNCTIONS[name]


    if name in SCIPY_FUNCTIONS:

        return SCIPY_FUNCTIONS[name]


    if name in SPECIAL_FUNCTIONS:

        return SPECIAL_FUNCTIONS[name]


    # Unknown:
    # assume user-defined MATLAB function

    return name