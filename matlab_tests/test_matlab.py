# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:34:49 2026

@author: Sarah
"""

import subprocess
from pathlib import Path
import sys


def run_matlab(matlab_file, output_file):

    matlab_file = Path(matlab_file)
    output_file = Path(output_file)


    script = f"""
    clear;
    clc;

    run('{matlab_file.as_posix()}');

    vars = whos;

    save(
        '{output_file.as_posix()}'
    );

    exit;
    """


    command = [
        "matlab",
        "-batch",
        script
    ]


    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )


    if result.returncode != 0:

        print(result.stdout)
        print(result.stderr)

        raise RuntimeError(
            "MATLAB execution failed"
        )


if __name__ == "__main__":

    run_matlab(
        sys.argv[1],
        sys.argv[2]
    )