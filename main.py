"""
main.py

Batch MATLAB-to-Python converter.

Usage:

    python main.py

The converter will:
    - Search recursively for .m files in matlab_tests/
    - Convert each MATLAB file
    - Generate matching .py files
    - Validate generated Python syntax
    - Generate conversion_report.json
"""

from pathlib import Path
import ast
import sys
import json
import traceback
import py_compile

from lexer import Lexer
from parser import Parser
from translate.semantic import SemanticAnalyzer
from translate.translator import Translator


def validate_python_file(filename):
    """
    Check generated Python syntax.
    """

    try:

        source = filename.read_text(
            encoding="utf-8"
        )

        ast.parse(source)

        return {
            "success": True,
            "error": None
        }

    except SyntaxError as error:

        return {
            "success": False,
            "error": (
                f"{error.msg} "
                f"(line {error.lineno}, "
                f"column {error.offset})"
            )
        }


def compile_python_file(filename):
    """
    Compile generated Python bytecode.
    """

    try:

        py_compile.compile(
            str(filename),
            doraise=True
        )

        return {
            "success": True,
            "error": None
        }

    except py_compile.PyCompileError as error:

        return {
            "success": False,
            "error": str(error)
        }


def convert_file(m_file):
    """
    Convert one MATLAB file.
    """

    report = {
        "matlab_file": str(m_file),
        "success": False,
        "stages": {}
    }

    print(f"\nConverting {m_file}")

    try:

        source = m_file.read_text(
            encoding="utf-8"
        )

        # --------------------------------------------------
        # Lexing
        # --------------------------------------------------

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        print(f"    Tokens: {len(tokens)}")

        report["stages"]["lexer"] = {
            "success": True,
            "tokens": len(tokens)
        }

        # --------------------------------------------------
        # Parsing
        # --------------------------------------------------

        parser = Parser(tokens)
        tree = parser.parse()

        print("    Parsed")

        report["stages"]["parser"] = {
            "success": True
        }

        # --------------------------------------------------
        # Semantic Analysis
        # --------------------------------------------------

        semantic = SemanticAnalyzer()

        tree = semantic.analyze(tree)

        report["stages"]["semantic"] = {
            "success": True,
            "warnings": semantic.warnings
        }

        if semantic.warnings:

            print(
                f"    Semantic warnings: {len(semantic.warnings)}"
            )

            for warning in semantic.warnings:

                print(f"      {warning}")

        else:

            print("    Semantic analysis passed")

        # --------------------------------------------------
        # Translation
        # --------------------------------------------------

        translator = Translator()

        python_code = translator.translate(tree)

        py_file = m_file.with_suffix(".py")

        py_file.write_text(
            python_code,
            encoding="utf-8"
        )

        print(f"    Generated {py_file.name}")

        report["stages"]["translation"] = {
            "success": True,
            "output": str(py_file)
        }

        # --------------------------------------------------
        # Syntax validation
        # --------------------------------------------------

        syntax_result = validate_python_file(py_file)

        report["stages"]["syntax_check"] = syntax_result

        if syntax_result["success"]:

            print("    Python syntax valid")

        else:

            print("    Python syntax error")
            print(f"      {syntax_result['error']}")

        # --------------------------------------------------
        # Compile validation
        # --------------------------------------------------

        compile_result = compile_python_file(py_file)

        report["stages"]["compile_check"] = compile_result

        if compile_result["success"]:

            print("    Python compile valid")

        else:

            print("    Python compile failed")
            print(f"      {compile_result['error']}")

        report["success"] = (
            syntax_result["success"]
            and compile_result["success"]
        )

    except Exception as error:

        report["error"] = str(error)
        report["traceback"] = traceback.format_exc()

        print("\n    Failed:")
        print(f"      {error}")

    return report


def convert_directory(directory):
    """
    Convert every MATLAB file in a directory tree.
    """

    directory = Path(directory)

    if not directory.exists():

        raise FileNotFoundError(directory)

    matlab_files = list(
        directory.rglob("*.m")
    )

    if not matlab_files:

        print("No MATLAB files found.")
        return

    print(f"Found {len(matlab_files)} MATLAB files")

    reports = []

    successful = 0
    failed = 0

    for m_file in matlab_files:

        result = convert_file(m_file)

        reports.append(result)

        if result["success"]:

            successful += 1

        else:

            failed += 1

    report_file = Path(
        "conversion_report.json"
    )

    report_file.write_text(
        json.dumps(
            reports,
            indent=4
        ),
        encoding="utf-8"
    )

    print("\n==========================")
    print("Conversion Summary")
    print("==========================")
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")
    print(f"Report:     {report_file}")


def main():

    matlab_directory = Path(
        "matlab_tests"
    )

    if not matlab_directory.exists():

        print(f"Missing directory: {matlab_directory}")
        print("Create matlab_tests and add .m files.")

        sys.exit(1)

    convert_directory(matlab_directory)


if __name__ == "__main__":

    main()