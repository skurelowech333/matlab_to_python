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


def _success_result(**extra):
    return {"success": True, "error": None, **extra}


def _error_result(error, **extra):
    return {"success": False, "error": str(error), **extra}


def _record_stage(report, stage_name, success, error=None, **extra):
    report["stages"][stage_name] = {
        "success": success,
        "error": error,
        **extra,
    }


def validate_python_file(filename):
    """
    Check generated Python syntax.
    """
    try:
        source = filename.read_text(encoding="utf-8")
        ast.parse(source)
        return _success_result()
    except SyntaxError as error:
        formatted = f"{error.msg} (line {error.lineno}, column {error.offset})"
        return _error_result(formatted)


def compile_python_file(filename):
    """
    Compile generated Python bytecode.
    """
    try:
        py_compile.compile(str(filename), doraise=True)
        return _success_result()
    except py_compile.PyCompileError as error:
        return _error_result(error)


def _run_lexing(source, report):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    print(f"    Tokens: {len(tokens)}")
    _record_stage(report, "lexer", True, tokens=len(tokens))
    return tokens


def _run_parsing(tokens, report):
    parser = Parser(tokens)
    tree = parser.parse()
    print("    Parsed")
    _record_stage(report, "parser", True)
    return tree


def _run_semantic_analysis(tree, report):
    semantic = SemanticAnalyzer()
    analyzed = semantic.analyze(tree)
    _record_stage(report, "semantic", True, warnings=semantic.warnings)

    if semantic.warnings:
        print(f"    Semantic warnings: {len(semantic.warnings)}")
        for warning in semantic.warnings:
            print(f"      {warning}")
    else:
        print("    Semantic analysis passed")

    return analyzed


def _run_translation(tree, m_file, report):
    translator = Translator()
    python_code = translator.translate(tree)
    py_file = m_file.with_suffix(".py")
    py_file.write_text(python_code, encoding="utf-8")
    print(f"    Generated {py_file.name}")
    _record_stage(report, "translation", True, output=str(py_file))
    return py_file


def _run_checks(py_file, report):
    checks = [
        ("syntax_check", validate_python_file, "Python syntax valid", "Python syntax error"),
        ("compile_check", compile_python_file, "Python compile valid", "Python compile failed"),
    ]

    check_results = []
    for stage_name, check_fn, success_message, failure_message in checks:
        result = check_fn(py_file)
        report["stages"][stage_name] = result
        check_results.append(result["success"])

        if result["success"]:
            print(f"    {success_message}")
        else:
            print(f"    {failure_message}")
            print(f"      {result['error']}")

    report["success"] = bool(check_results) and all(check_results)


def convert_file(m_file):
    """
    Convert one MATLAB file.
    """
    report = {"matlab_file": str(m_file), "success": False, "stages": {}}
    print(f"\nConverting {m_file}")

    try:
        source = m_file.read_text(encoding="utf-8")
        tokens = _run_lexing(source, report)
        tree = _run_parsing(tokens, report)
        tree = _run_semantic_analysis(tree, report)
        py_file = _run_translation(tree, m_file, report)
        _run_checks(py_file, report)
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

    matlab_files = list(directory.rglob("*.m"))

    if not matlab_files:
        print("No MATLAB files found.")
        return

    print(f"Found {len(matlab_files)} MATLAB files")
    reports = [convert_file(m_file) for m_file in matlab_files]
    successful = sum(result["success"] for result in reports)
    failed = len(reports) - successful

    report_file = Path("conversion_report.json")
    report_file.write_text(json.dumps(reports, indent=4), encoding="utf-8")

    print("\n==========================")
    print("Conversion Summary")
    print("==========================")
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")
    print(f"Report:     {report_file}")


def main():
    matlab_directory = Path("matlab_tests")

    if not matlab_directory.exists():
        print(f"Missing directory: {matlab_directory}")
        print("Create matlab_tests and add .m files.")
        sys.exit(1)

    convert_directory(matlab_directory)


if __name__ == "__main__":
    main()
