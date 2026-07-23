# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:35:14 2026

@author: Sarah
"""

import runpy
import scipy.io
import sys
from pathlib import Path


def run_python(
    python_file,
    output_file
):

    namespace = runpy.run_path(
        python_file
    )


    # remove python internals
    namespace = {
        k:v
        for k,v in namespace.items()
        if not k.startswith("__")
    }


    scipy.io.savemat(
        output_file,
        namespace
    )


if __name__ == "__main__":

    run_python(
        sys.argv[1],
        sys.argv[2]
    )