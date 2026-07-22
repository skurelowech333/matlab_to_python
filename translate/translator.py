from __future__ import annotations

# -*- coding: utf-8 -*-
"""
translator.py

Python code generator for the MATLAB-to-Python translator.
Supports: functions, loops, conditionals, try-catch, and more.
"""

from abstract_syntax_tree import *
from translate.builtins import translate_builtin
from translate.indexing import (
    convert_index,
    convert_slice,
)


class Translator:

    def __init__(self):
        self.lines = []
        self.indent = 0
    
        self.in_class = False
        self.class_name = None
        self.current_method = None

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

        method_name = node.name
    
    
        # ==========================================
        # MATLAB class methods
        # ==========================================
    
        if self.in_class:
    
            # Constructor:
            # MATLAB:
            # function obj = ClassName(args)
            #
            # Python:
            # def __init__(self,args)
    
            if node.name == self.class_name:
    
                method_name = "__init__"
    
                args = ", ".join(
                    ["self"] + node.inputs
                )
    
    
            # Normal class method:
            #
            # MATLAB:
            # function x = foo(obj,a)
            #
            # Python:
            # def foo(self,a)
    
            else:
    
                args = ", ".join(
                    ["self"] + node.inputs[1:]
                )
    
    
        # ==========================================
        # Normal MATLAB functions
        # ==========================================
    
        else:
    
            args = ", ".join(
                node.inputs
            )
    
    
        self.emit(
            f"def {method_name}({args}):"
        )
    
    
        self.indent += 1
    
    
        if not node.body:
    
            self.emit("pass")
    
        else:
    
            for statement in node.body:
                self.visit(statement)
    
    
    
        # ==========================================
        # Return values
        # ==========================================
    
        # Constructors never return MATLAB obj
        if (
                node.outputs
                and not (
                    self.in_class
                    and (
                        method_name == "__init__"
                        or node.outputs == ["obj"]
                    )
                )
            ):
                
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
        lhs = self.visit_assignment_target(
            node.target
        )
        rhs = self.visit(
            node.value
        )
        self.emit(
            f"{lhs} = {rhs}"
        )

    def visit_assignment_target(self, node):

        # obj.mass = x
        # becomes
        # self.mass = x
    
        if isinstance(
            node,
            FieldAccess
        ):
    
            return self.visit(node)
    
    
        # Multiple outputs:
        # [a,b,c] = func()
    
        if isinstance(
            node,
            Matrix
        ):
    
            targets = []
    
            for row in node.rows:
    
                for cell in row:
    
                    targets.append(
                        self.visit(cell)
                    )
    
            return ", ".join(targets)
    
    
        return self.visit(node)

    def visit_ExpressionStatement(self, node):
        value = self.visit(
            node.expression
        )
        if value:
            self.emit(value)

    def visit_Return(self, node):
        if not node.values:
            self.emit("return")
        elif len(node.values) == 1:
            value = self.visit(node.values[0])
            self.emit(f"return {value}")
        else:
            values = ", ".join(
                self.visit(v) for v in node.values
            )
            self.emit(f"return {values}")

    def visit_Break(self, node):
        self.emit("break")

    def visit_Continue(self, node):
        self.emit("continue")

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
        step = ""
        if node.step:
            step_val = self.visit(node.step)
            step = f", {step_val}"
        self.emit(
            f"for {node.variable} in range({start}, {stop}+1{step}):"
        )
        self.indent += 1
        for statement in node.body:
            self.visit(statement)
        self.indent -= 1

    def visit_While(self, node):
        condition = self.visit(
            node.condition
        )
        self.emit(
            f"while {condition}:"
        )
        self.indent += 1
        if not node.body:
            self.emit("pass")
        else:
            for statement in node.body:
                self.visit(statement)
        self.indent -= 1

    # ======================================================
    # Conditionals
    # ======================================================

    def visit_If(self, node):
        condition = self.visit(
            node.condition
        )
        self.emit(
            f"if {condition}:"
        )
        self.indent += 1
        if not node.body:
            self.emit("pass")
        else:
            for statement in node.body:
                self.visit(statement)
        self.indent -= 1
        for elseif_block in node.elseif_blocks:
            self.visit_ElseIf(elseif_block)
        if node.else_body:
            self.emit("else:")
            self.indent += 1
            for statement in node.else_body:
                self.visit(statement)
            self.indent -= 1

    def visit_ElseIf(self, node):
        condition = self.visit(
            node.condition
        )
        self.emit(
            f"elif {condition}:"
        )
        self.indent += 1
        if not node.body:
            self.emit("pass")
        else:
            for statement in node.body:
                self.visit(statement)
        self.indent -= 1

    def visit_Switch(self, node):
        expr = self.visit(
            node.expression
        )
        first = True
        for case in node.cases:
            if first:
                case_val = self.visit(case.value)
                self.emit(
                    f"if {expr} == {case_val}:"
                )
                first = False
            else:
                case_val = self.visit(case.value)
                self.emit(
                    f"elif {expr} == {case_val}:"
                )
            self.indent += 1
            for statement in case.body:
                self.visit(statement)
            self.indent -= 1
        if node.default_body:
            self.emit("else:")
            self.indent += 1
            for statement in node.default_body:
                self.visit(statement)
            self.indent -= 1

    def visit_Try(self, node):
        self.emit("try:")
        self.indent += 1
        if not node.body:
            self.emit("pass")
        else:
            for statement in node.body:
                self.visit(statement)
        self.indent -= 1
        self.emit("except Exception as e:")
        self.indent += 1
        if not node.catch_body:
            self.emit("pass")
        else:
            for statement in node.catch_body:
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
            "i": "1j",
            "j": "1j",
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

    def visit_Range(self, node):
        start = self.visit(node.start)
        stop = self.visit(node.stop)
        if node.step:
            step = self.visit(node.step)
            return f"np.arange({start}, {stop}+1, {step})"
        else:
            return f"np.arange({start}, {stop}+1)"

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


    # ======================================================
    # Unary Operations
    # ======================================================

    def visit_UnaryOp(self, node):
        """
        Handle unary MATLAB operators.

        Examples:
            -5
            -x
            -(a+b)

        MATLAB AST:
            UnaryOp(
                operator="-",
                operand=Number(5)
            )

        Python:
            -5
        """

        operand = self.visit(
            node.operand
        )

        return (
            f"{node.operator}{operand}"
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

        function = self.visit(
            node.function
        )
    
        args = ", ".join(
            self.visit(x)
            for x in node.arguments
        )
    
        return f"{function}({args})"

    def map_function(self, name):
        return translate_builtin(name)

    # ======================================================
    # Indexing
    # ======================================================

    def visit_Index(self, node):
        """
        Handle MATLAB array indexing: A(i,j) -> A[i-1,j-1]
        Converts Index AST nodes to Python bracket notation.
        """
        variable = self.visit(node.value)
        indices = []

        for index in node.indices:
            # Handle slice objects (colons)
            if isinstance(index, Slice):
                indices.append(
                    convert_slice(index)
                )
            # Handle regular indices
            else:
                indices.append(
                    convert_index(index)
                )

        return (
            f"{variable}["
            + ",".join(indices)
            + "]"
        )
    
    def visit_ClassDef(self, node):

        self.emit(
            f"class {node.name}:"
        )
    
        self.indent += 1
    
        self.in_class = True
        self.class_name = node.name
    
    
        # ==========================================
        # Class properties
        # ==========================================
    
        if node.properties:
    
            for prop in node.properties:
    
                for stmt in prop.body:
    
                    if isinstance(
                        stmt,
                        ExpressionStatement
                    ):
    
                        if isinstance(
                            stmt.expression,
                            Identifier
                        ):
    
                            self.emit(
                                f"{stmt.expression.name} = None"
                            )
    
    
        # ==========================================
        # Methods
        # ==========================================
    
        if node.methods:
    
            self.emit()
    
            for method in node.methods:
    
                self.visit(method)
    
                self.emit()
    
        else:
    
            self.emit(
                "pass"
            )
    
    
        self.indent -= 1
    
    
        self.in_class = False
        self.class_name = None
    
    def visit_FieldAccess(self, node):

        value = self.visit(
            node.value
        )
    
    
        # MATLAB object variable
        # obj.mass -> self.mass
    
        if value == "obj":
    
            value = "self"
    
    
        return (
            f"{value}.{node.field}"
        )