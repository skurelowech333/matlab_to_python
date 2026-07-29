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
            # MATLAB: function obj = ClassName(args)
            # Python: def __init__(self, args)
            if node.name == self.class_name:
                method_name = "__init__"
                args = ", ".join(["self"] + node.inputs)
    
            # Normal class method:
            # MATLAB: function obj = foo(obj, a, b)
            # Python: def foo(self, a, b)
            else:
                if node.inputs and node.inputs[0] == "obj":
                    method_inputs = node.inputs[1:]
                else:
                    method_inputs = node.inputs
                args = ", ".join(["self"] + method_inputs)
    
        # ==========================================
        # Normal MATLAB functions
        # ==========================================
        else:
            args = ", ".join(node.inputs)
    
        self.emit(f"def {method_name}({args}):")
        self.indent += 1
    
        if not node.body:
            self.emit("pass")
        else:
            for statement in node.body:
                self.visit(statement)
    
        # ==========================================
        # Return values
        # ==========================================
        # Constructors and methods returning 'obj' normally don't
        # return in Python; they mutate self.
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
                self.emit(f"return {node.outputs[0]}")
            else:
                self.emit("return " + ", ".join(node.outputs))
    
        self.indent -= 1
        
    def visit_FieldAccess(self, node):
        value = self.visit(node.value)
    
        # MATLAB object variable: obj.mass -> self.mass
        if value == "obj":
            value = "self"
    
        return f"{value}.{node.field}"

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
        """
        Convert assignment targets, handling multiple return values.
        
        MATLAB: [U, S, V] = svd(A)
        Python: U, S, V = np.linalg.svd(A)
        """
        # Matrix used as tuple assignment target
        if isinstance(node, Matrix):
            # Extract identifiers from matrix rows
            targets = []
            for row in node.rows:
                for cell in row:
                    if isinstance(cell, Identifier):
                        targets.append(cell.name)
                    else:
                        targets.append(self.visit(cell))
            return ", ".join(targets)
        
        # Regular assignment target
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
        if node.stop is None:
            # Array / vector iteration: for x = array
            iterable = self.visit(node.start)
            self.emit(f"for {node.variable} in {iterable}:")
        else:
            start = self.visit(node.start)
            stop = self.visit(node.stop)
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
            "Inf": "np.inf",
            "NaN": "np.nan",
            "nan": "np.nan",
            # MATLAB logicals
            "true": "True",
            "false": "False",
            "True": "True",
            "False": "False",
            "nargin": "len(locals())",
        }
        return constants.get(node.name, node.name)

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
    
    def visit_ClassDef(self, node):
        # Emit class header
        self.emit(f"class {node.name}:")
        self.indent += 1
    
        # Mark class context so visit_Function can treat constructors specially
        self.in_class = True
        self.class_name = node.name
    
        # ------------------------------------------
        # Class properties: turn each property name
        # into a class attribute with default None
        # ------------------------------------------
        if node.properties:
            for prop_block in node.properties:
                for stmt in prop_block.body:
                    if isinstance(stmt, ExpressionStatement):
                        if isinstance(stmt.expression, Identifier):
                            self.emit(f"{stmt.expression.name} = None")
    
        # ------------------------------------------
        # Methods
        # ------------------------------------------
        if node.methods:
            self.emit()  # blank line after properties
            for method in node.methods:
                self.visit(method)
                self.emit()
        else:
            # No methods: emit 'pass' to make class valid Python
            self.emit("pass")
    
        # Restore context
        self.indent -= 1
        self.in_class = False
        self.class_name = None

    # ======================================================
    # Matrix
    # ======================================================

    def visit_Matrix(self, node):
        # --------------------------------------------------
        # Case 1: vertical stacking of row vectors
        # MATLAB: D = [A; B];
        # Python: D = np.vstack((A, B))
        # --------------------------------------------------
        if all(len(row) == 1 for row in node.rows):
            first_elems = [row[0] for row in node.rows]
            # Each row is a single identifier, e.g. [A; B; C]
            if all(isinstance(x, Identifier) for x in first_elems):
                parts = [self.visit(x) for x in first_elems]
                return f"np.vstack(({', '.join(parts)}))"
    
        # --------------------------------------------------
        # Case 2: single row of identifiers -> horizontal concat
        # MATLAB: C = [A, B];
        # Python: C = np.hstack((A, B))
        # --------------------------------------------------
        if len(node.rows) == 1:
            row = node.rows[0]
    
            # Horizontal concatenation of arrays
            if all(isinstance(x, Identifier) for x in row):
                parts = [self.visit(x) for x in row]
                return f"np.hstack(({', '.join(parts)}))"
    
            # Single row of strings / identifiers -> string concatenation
            if all(isinstance(x, String) or isinstance(x, Identifier) for x in row):
                parts = [self.visit(x) for x in row]
                return " + ".join(parts)
    
            # Single row of numbers -> 1D numeric array
            if all(isinstance(x, Number) for x in row):
                values = ", ".join(self.visit(x) for x in row)
                return f"np.array([{values}])"
    
        # --------------------------------------------------
        # Case 3: general numeric/mixed matrix -> 2D NumPy array
        # --------------------------------------------------
        rows = []
        for row in node.rows:
            values = ", ".join(self.visit(x) for x in row)
            rows.append(f"[{values}]")
        return "np.array([" + ", ".join(rows) + "])"

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
            ~x (logical not)
        """

        operand = self.visit(
            node.operand
        )

        if node.operator == "~":
            return f"not {operand}"

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
            "*": "*",

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
        # Plain identifier: map MATLAB builtin → Python name
        if isinstance(node.function, Identifier):
            name = node.function.name
            func_name = self.map_function(name)
        else:
            name = None
            func_name = self.visit(node.function)

        # When any argument is a Slice, MATLAB is using array-indexing syntax:
        # A(:, 2) or A(1:3, :) — translate to Python bracket indexing.
        if any(isinstance(arg, Slice) for arg in node.arguments):
            indices = []
            for index in node.arguments:
                if isinstance(index, Slice):
                    indices.append(convert_slice(index))
                else:
                    indices.append(convert_index(index))
            return f"{func_name}[{','.join(indices)}]"
    
        # Special-case array creation: zeros, ones, etc.
        if name in {"zeros", "ones"}:
            # NumPy expects shape as a single tuple if there are multiple dims
            if len(node.arguments) == 1:
                # e.g. zeros(n) -> np.zeros(n)
                arg_str = self.visit(node.arguments[0])
                return f"{func_name}({arg_str})"
            else:
                # e.g. zeros(1,10) -> np.zeros((1,10))
                dims = ", ".join(self.visit(a) for a in node.arguments)
                return f"{func_name}(({dims}))"

        # Special-case max/min with 2 args: MATLAB max(a,b) is element-wise max
        # numpy equivalent is np.maximum / np.minimum
        if name in {"max", "min"} and len(node.arguments) == 2:
            a = self.visit(node.arguments[0])
            b = self.visit(node.arguments[1])
            numpy_func = "np.maximum" if name == "max" else "np.minimum"
            return f"{numpy_func}({a}, {b})"
    
        # Default case: normal function call
        args = ", ".join(self.visit(x) for x in node.arguments)
        return f"{func_name}({args})"

    # ======================================================
    # Lambda / anonymous function
    # ======================================================

    def visit_Lambda(self, node):
        params = ", ".join(node.parameters)
        body = self.visit(node.body)
        return f"lambda {params}: {body}"

    # ======================================================
    # Cell array literal
    # ======================================================

    def visit_CellArray(self, node):
        all_elements = [elem for row in node.rows for elem in row]
        elements = ", ".join(self.visit(e) for e in all_elements)
        return f"[{elements}]"
    
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
