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
    # Math functions
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
    "log2": "np.log2",
    "abs": "np.abs",
    "sign": "np.sign",
    "floor": "np.floor",
    "ceil": "np.ceil",
    "round": "np.round",
    "fix": "np.trunc",
    "mod": "np.mod",
    "rem": "np.remainder",
    "gcd": "np.gcd",
    "lcm": "np.lcm",
    # Matrix / array creation
    "zeros": "np.zeros",
    "ones": "np.ones",
    "eye": "np.eye",
    "rand": "np.random.rand",
    "randn": "np.random.randn",
    "randi": "np.random.randint",
    "linspace": "np.linspace",
    "logspace": "np.logspace",
    "arange": "np.arange",
    "meshgrid": "np.meshgrid",
    "repmat": "np.tile",
    # Matrix information
    "length": "len",
    "size": "np.shape",
    "ndims": "np.ndim",
    "numel": "np.size",
    # Matrix manipulation
    "reshape": "np.reshape",
    "transpose": "np.transpose",
    "flip": "np.flip",
    "flipud": "np.flipud",
    "fliplr": "np.fliplr",
    "rot90": "np.rot90",
    "diag": "np.diag",
    "trace": "np.trace",
    "sort": "np.sort",
    "sortrows": "np.sort",
    "unique": "np.unique",
    "find": "np.where",
    # Linear algebra
    "dot": "np.dot",
    "cross": "np.cross",
    "norm": "np.linalg.norm",
    "det": "np.linalg.det",
    "inv": "np.linalg.inv",
    "rank": "np.linalg.matrix_rank",
    "eig": "np.linalg.eig",
    "eigvals": "np.linalg.eigvals",
    "svd": "np.linalg.svd",
    "qr": "np.linalg.qr",
    "chol": "np.linalg.cholesky",
    # Statistics
    "sum": "np.sum",
    "prod": "np.prod",
    "mean": "np.mean",
    "median": "np.median",
    "mode": "scipy.stats.mode",
    "std": "np.std",
    "var": "np.var",
    "cov": "np.cov",
    "corrcoef": "np.corrcoef",
    "min": "np.min",
    "max": "np.max",
    "cumsum": "np.cumsum",
    "cumprod": "np.cumprod",
    "diff": "np.diff",
    # Sorting
    "sort": "np.sort",
    "sortrows": "np.lexsort",
    # Other utilities
    "any": "np.any",
    "all": "np.all",
}


# ==========================================================
# SciPy mappings
# ==========================================================

SCIPY_FUNCTIONS = {
    # Optimization
    "fmincon": "scipy.optimize.minimize",
    "fminsearch": "scipy.optimize.minimize",
    "fminbnd": "scipy.optimize.minimize_scalar",
    # Integration
    "ode45": "scipy.integrate.solve_ivp",
    "ode23": "scipy.integrate.solve_ivp",
    "quad": "scipy.integrate.quad",
    "dblquad": "scipy.integrate.dblquad",
    # Signal processing
    "fft": "scipy.fft.fft",
    "ifft": "scipy.fft.ifft",
    "fft2": "scipy.fft.fft2",
    "ifft2": "scipy.fft.ifft2",
    "conv": "scipy.signal.convolve",
    "deconv": "scipy.signal.deconvolve",
    "filter": "scipy.signal.lfilter",
}


# ==========================================================
# Visualization mappings (no-op or import warning)
# ==========================================================

VISUALIZATION_FUNCTIONS = {
    "plot": "plt.plot",
    "figure": "plt.figure",
    "hold": None,
    "subplot": "plt.subplot",
    "imshow": "plt.imshow",
    "image": "plt.imshow",
    "mesh": "plt.plot_surface",
    "surf": "plt.plot_surface",
    "scatter": "plt.scatter",
    "hist": "plt.hist",
    "bar": "plt.bar",
    "stem": "plt.stem",
    "xlabel": "plt.xlabel",
    "ylabel": "plt.ylabel",
    "title": "plt.title",
    "legend": "plt.legend",
    "grid": "plt.grid",
    "axis": "plt.axis",
    "xlim": "plt.xlim",
    "ylim": "plt.ylim",
    "show": "plt.show",
}


# ==========================================================
# I/O functions
# ==========================================================

IO_FUNCTIONS = {
    "disp": "print",
    "fprintf": "print",
    "sprintf": "str.format",
    "input": "input",
    "load": "scipy.io.loadmat",
    "save": "scipy.io.savemat",
}


# ==========================================================
# Special MATLAB constants
# ==========================================================

SPECIAL_FUNCTIONS = {
    "pi": "np.pi",
    "inf": "np.inf",
    "NaN": "np.nan",
    "nan": "np.nan",
    "eps": "np.finfo(float).eps",
    "i": "1j",
    "j": "1j",
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
    if name in VISUALIZATION_FUNCTIONS:
        return VISUALIZATION_FUNCTIONS[name] or name
    if name in IO_FUNCTIONS:
        return IO_FUNCTIONS[name]
    if name in SPECIAL_FUNCTIONS:
        return SPECIAL_FUNCTIONS[name]
    # Unknown: assume user-defined MATLAB function
    return name
