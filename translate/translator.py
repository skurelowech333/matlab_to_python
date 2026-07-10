from __future__ import annotations

# -*- coding: utf-8 -*-

"""
translator.py

Python code generator for the MATLAB-to-Python translator.
"""

from abstract_syntax_tree import *
from translate.builtins import translate_builtin
from translate.indexing import translate_index


class Translator:

    def __init__(self):

        self.lines = []
        self.indent = 0


    # ======================================================
    # Helpers
    # ======================================================

    def emit(self, text=""):

        self.lines.append(
            "    " * self.indent + text
        )


    def result(self):

        return "\n".join(self.lines)



    def translate(self, node):

        self.visit(node)

        return self.result()



    # ======================================================
    # Visitor
    # ======================================================

    def visit(self, node):

        if node is None:

            return None


        method = getattr(
            self,
            f"visit_{type(node).__name__}",
            None
        )


        if method is None:

            self.emit_failed(node)

            return ""


        return method(node)



    def emit_failed(self, node):

        source = getattr(
            node,
            "source",
            ""
        )

        self.emit(
            "# CONVERSION FAILED:"
        )

        if source:

            self.emit(
                f"# Original MATLAB: {source}"
            )



    # ======================================================
    # Program
    # ======================================================

    def visit_Program(self, node):

        self.emit(
            "import numpy as np"
        )

        self.emit()


        for statement in node.body:

            self.visit(statement)

            self.emit()



    # ======================================================
    # Comments
    # ======================================================

    def visit_Comment(self, node):

        text = node.text

        if text.startswith("%"):

            text = text[1:]


        self.emit(
            f"# {text.strip()}"
        )



    # ======================================================
    # Functions
    # ======================================================

    def visit_Function(self, node):

        args = ", ".join(
            node.inputs
        )


        self.emit(
            f"def {node.name}({args}):"
        )


        self.indent += 1


        if not node.body:

            self.emit(
                "pass"
            )

        else:

            for statement in node.body:

                self.visit(statement)



        if node.outputs:

            self.emit()


            if len(node.outputs) == 1:

                self.emit(
                    f"return {node.outputs[0]}"
                )

            else:

                self.emit(
                    "return "
                    +
                    ", ".join(node.outputs)
                )


        self.indent -= 1



    # ======================================================
    # Statements
    # ======================================================

    def visit_Assignment(self, node):

        lhs = self.visit(
            node.target
        )

        rhs = self.visit(
            node.value
        )


        self.emit(
            f"{lhs} = {rhs}"
        )



    def visit_ExpressionStatement(self, node):

        value = self.visit(
            node.expression
        )

        if value:

            self.emit(value)



    # ======================================================
    # Loops
    # ======================================================

    def visit_For(self, node):

        start = self.visit(
            node.start
        )

        stop = self.visit(
            node.stop
        )


        self.emit(
            f"for {node.variable} in range({start}, {stop}+1):"
        )


        self.indent += 1


        for statement in node.body:

            self.visit(statement)


        self.indent -= 1



    # ======================================================
    # If
    # ======================================================

    def visit_If(self, node):

        condition = self.visit(
            node.condition
        )


        self.emit(
            f"if {condition}:"
        )


        self.indent += 1


        for statement in node.body:

            self.visit(statement)


        self.indent -= 1



    # ======================================================
    # Expressions
    # ======================================================

    def visit_Identifier(self, node):

        constants = {

            "pi": "np.pi",

            "inf": "np.inf",

            "NaN": "np.nan",

        }


        return constants.get(
            node.name,
            node.name
        )



    def visit_Number(self, node):

        if float(node.value).is_integer():

            return str(
                int(node.value)
            )


        return str(node.value)



    def visit_String(self, node):

        return repr(
            node.value
        )



    # ======================================================
    # Matrix
    # ======================================================

    def visit_Matrix(self, node):

        rows = []


        for row in node.rows:

            values = ", ".join(
                self.visit(x)
                for x in row
            )

            rows.append(
                f"[{values}]"
            )


        return (
            "np.array(["
            +
            ", ".join(rows)
            +
            "])"
        )



    # ======================================================
    # Binary Operations
    # ======================================================

    def visit_BinaryOp(self, node):

        left = self.visit(
            node.left
        )

        right = self.visit(
            node.right
        )


        operator = self.convert_operator(
            node
        )


        return (
            f"({left} {operator} {right})"
        )



    def convert_operator(self, node):

        op = node.operator


        mapping = {

            # element-wise
            ".*": "*",
            "./": "/",
            ".^": "**",


            # logical
            "&&": "and",
            "||": "or",
            "~=": "!=",


            # MATLAB matrix multiplication
            "*": "@",


            # power
            "^": "**",

        }


        return mapping.get(
            op,
            op
        )



    # ======================================================
    # Calls
    # ======================================================

    def visit_Call(self, node):

        name = self.visit(
            node.function
        )


        args = ", ".join(
            self.visit(x)
            for x in node.arguments
        )


        return (
            f"{self.map_function(name)}({args})"
        )



    # ======================================================
    # Indexing
    # ======================================================

    def visit_Index(self, node):

        variable = self.visit(
            node.value
        )

        indices = []


        for index in node.indices:

            value = self.visit(index)

            if value.isdigit():

                value = str(
                    int(value)-1
                )

            indices.append(value)


        return (
            f"{variable}["
            +
            ", ".join(indices)
            +
            "]"
        )



    # ======================================================
    # Builtins
    # ======================================================

    def map_function(self, name):

        return translate_builtin(name)