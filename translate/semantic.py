# -*- coding: utf-8 -*-
"""
semantic.py

Semantic analysis pass for MATLAB AST.

Responsibilities
----------------
- Variable scope analysis
- Detect undefined variables
- Register functions
- Register loop variables
- Ignore MATLAB built-ins
- Normalize MATLAB operators
- Collect warnings
"""

from abstract_syntax_tree import *


MATLAB_BUILTINS = {
    "abs", "acos", "asin", "atan", "atan2", "ceil", "cos", "diag",
    "disp", "eig", "exp", "eye", "find", "floor", "fprintf", "inv",
    "length", "linspace", "log", "log10", "log2", "max", "mean",
    "meshgrid", "min", "mod", "ones", "plot", "prod", "rem", "reshape",
    "round", "sin", "size", "sqrt", "std", "sum", "tan", "transpose",
    "zeros", "rand", "randn", "randi", "sort", "unique", "any", "all",
    "unique", "cumsum", "cumprod", "diff", "fft", "ifft", "conv",
}


MATLAB_CONSTANTS = {
    "i", "j", "pi", "eps", "inf", "nan", "true", "false",
}


class SemanticAnalyzer:

    def __init__(self):
        self.variables = set()
        self.functions = set()
        self.warnings = []

    # ==================================================
    # Entry
    # ==================================================

    def analyze(self, node):
        self.visit(node)
        return node

    # ==================================================
    # Dispatcher
    # ==================================================

    def visit(self, node):
        if node is None:
            return
        method = getattr(
            self,
            f"visit_{type(node).__name__}",
            self.generic_visit
        )
        return method(node)

    def generic_visit(self, node):
        for value in vars(node).values():
            if isinstance(value, Node):
                self.visit(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Node):
                        self.visit(item)

    # ==================================================
    # Program
    # ==================================================

    def visit_Program(self, node):
        for statement in node.body:
            self.visit(statement)

    # ==================================================
    # Functions
    # ==================================================

    def visit_Function(self, node):
        self.functions.add(node.name)
        old_scope = self.variables.copy()
        self.variables.update(node.inputs)
        self.variables.update(node.outputs)
        for statement in node.body:
            self.visit(statement)
        self.variables = old_scope

    # ==================================================
    # Assignments
    # ==================================================

    def visit_Assignment(self, node):
        self.visit(node.value)
        if isinstance(node.target, Identifier):
            self.variables.add(node.target.name)
        else:
            self.visit(node.target)

    # ==================================================
    # Loops
    # ==================================================

    def visit_For(self, node):
        self.visit(node.start)
        self.visit(node.stop)
        self.variables.add(node.variable)
        if node.step is not None:
            self.visit(node.step)
        for statement in node.body:
            self.visit(statement)

    def visit_While(self, node):
        self.visit(node.condition)
        for statement in node.body:
            self.visit(statement)

    def visit_Switch(self, node):
        self.visit(node.expression)
        for case in node.cases:
            self.visit(case)
        for statement in node.default_body:
            self.visit(statement)

    def visit_Case(self, node):
        self.visit(node.value)
        for statement in node.body:
            self.visit(statement)

    # ==================================================
    # Try-Catch
    # ==================================================

    def visit_Try(self, node):
        for statement in node.body:
            self.visit(statement)
        for statement in node.catch_body:
            self.visit(statement)

    # ==================================================
    # Identifier checking
    # ==================================================

    def visit_Identifier(self, node):
        if node.name in MATLAB_BUILTINS:
            return
        if node.name in MATLAB_CONSTANTS:
            return
        if node.name in self.functions:
            return
        if node.name not in self.variables:
            self.warnings.append(
                f"Unknown variable: {node.name}"
            )

    # ==================================================
    # Binary operations
    # ==================================================

    def visit_BinaryOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        mapping = {
            ".*": "*",
            "./": "/",
            ".^": "**",
        }
        node.operator = mapping.get(
            node.operator,
            node.operator
        )

    # ==================================================
    # Function calls
    # ==================================================

    def visit_Call(self, node):
        for arg in node.arguments:
            self.visit(arg)
        if isinstance(node.function, Identifier):
            name = node.function.name
            visualization = {
                "plot", "figure", "hold", "subplot",
                "imshow", "image", "mesh", "surf",
                "scatter", "hist", "bar", "stem",
                "clc", "clf", "clear", "close",
                "xlabel", "ylabel", "title", "legend",
                "grid", "axis", "xlim", "ylim", "show",
            }
            if name in visualization:
                self.warnings.append(
                    f"MATLAB visualization command skipped: {name}"
                )
