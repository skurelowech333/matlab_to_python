# -*- coding: utf-8 -*-
"""
Abstract Syntax Tree definitions for the MATLAB-to-Python translator.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional


# ==========================================================
# Base Node
# ==========================================================

@dataclass
class Node:
    """Base class for every AST node."""
    line: int = 0
    source: str = ""


# ==========================================================
# Program
# ==========================================================

@dataclass
class Program(Node):
    body: List["Node"] = field(default_factory=list)


# ==========================================================
# Functions
# ==========================================================

@dataclass
class Function(Node):
    name: str = ""
    inputs: List[str] = field(
        default_factory=list
    )
    outputs: List[str] = field(
        default_factory=list
    )
    body: List["Node"] = field(
        default_factory=list
    )


# ==========================================================
# Statements
# ==========================================================

@dataclass
class Assignment(Node):
    target: "Node" = None
    value: "Node" = None


@dataclass
class Return(Node):
    values: List["Node"] = field(
        default_factory=list
    )


@dataclass
class ExpressionStatement(Node):
    expression: "Node" = None


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


# ==========================================================
# Conversion Recovery
# ==========================================================

@dataclass
class FailedConversion(Node):
    """
    Represents MATLAB code that could not be translated.
    The translator will preserve it as comments.

    Example:
        # CONVERSION FAILED:
        # Unsupported syntax
        # ORIGINAL MATLAB:
        # foo(bar)
    """
    matlab_text: str = ""
    error: str = ""


@dataclass
class RawMATLAB(Node):
    """
    Preserves original MATLAB source.
    Used when exact source preservation is required.
    """
    text: str = ""


# ==========================================================
# Control Flow
# ==========================================================

@dataclass
class If(Node):
    condition: "Node" = None
    body: List["Node"] = field(
        default_factory=list
    )
    elseif_blocks: List["ElseIf"] = field(
        default_factory=list
    )
    else_body: List["Node"] = field(
        default_factory=list
    )


@dataclass
class ElseIf(Node):
    condition: "Node" = None
    body: List["Node"] = field(
        default_factory=list
    )


@dataclass
class For(Node):
    variable: str = ""
    start: "Node" = None
    stop: "Node" = None
    step: Optional["Node"] = None
    body: List["Node"] = field(
        default_factory=list
    )


@dataclass
class While(Node):
    condition: "Node" = None
    body: List["Node"] = field(
        default_factory=list
    )


@dataclass
class Switch(Node):
    expression: "Node" = None
    cases: List["Case"] = field(
        default_factory=list
    )
    default_body: List["Node"] = field(
        default_factory=list
    )


@dataclass
class Case(Node):
    value: "Node" = None
    body: List["Node"] = field(
        default_factory=list
    )


@dataclass
class Try(Node):
    body: List["Node"] = field(
        default_factory=list
    )
    catch_body: List["Node"] = field(
        default_factory=list
    )
    catch_var: str = ""


# ==========================================================
# Expressions
# ==========================================================

@dataclass
class Identifier(Node):
    name: str = ""


@dataclass
class Number(Node):
    value: Any = 0


@dataclass
class String(Node):
    value: str = ""


@dataclass
class Boolean(Node):
    value: bool = False


@dataclass
class BinaryOp(Node):
    operator: str = ""
    left: "Node" = None
    right: "Node" = None


@dataclass
class UnaryOp(Node):
    operator: str = ""
    operand: "Node" = None


# ==========================================================
# Function Calls
# ==========================================================

@dataclass
class Call(Node):
    function: "Node" = None
    arguments: List["Node"] = field(
        default_factory=list
    )


# ==========================================================
# Indexing
# ==========================================================

@dataclass
class Index(Node):
    value: "Node" = None
    indices: List["Node"] = field(
        default_factory=list
    )


@dataclass
class Slice(Node):
    start: Optional["Node"] = None
    stop: Optional["Node"] = None
    step: Optional["Node"] = None


@dataclass
class End(Node):
    """
    Represents MATLAB's end keyword.
    """
    pass


# ==========================================================
# Arrays / Matrices
# ==========================================================

@dataclass
class Matrix(Node):
    rows: List[List["Node"]] = field(
        default_factory=list
    )
    shape: Optional[tuple] = None


@dataclass
class CellArray(Node):
    rows: List[List["Node"]] = field(
        default_factory=list
    )


@dataclass
class Range(Node):
    """
    Represents MATLAB range expressions: start:step:stop
    """
    start: "Node" = None
    step: Optional["Node"] = None
    stop: "Node" = None


# ==========================================================
# Structs
# ==========================================================

@dataclass
class FieldAccess(Node):
    value: "Node" = None
    field: str = ""


# ==========================================================
# Anonymous Functions
# ==========================================================

@dataclass
class Lambda(Node):
    parameters: List[str] = field(
        default_factory=list
    )
    body: "Node" = None


# ==========================================================
# Comments
# ==========================================================

@dataclass
class Comment(Node):
    text: str = ""


# ==========================================================
# Utilities
# ==========================================================

def walk(node):
    """
    Recursively walk the AST.
    """
    yield node

    for value in vars(node).values():
        if isinstance(value, Node):
            yield from walk(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, Node):
                    yield from walk(item)


def pretty(node, indent=0):
    """
    Pretty-print the AST.
    """
    prefix = "    " * indent
    print(
        f"{prefix}{node.__class__.__name__}"
    )

    for name, value in vars(node).items():
        if isinstance(value, Node):
            print(
                f"{prefix}  {name}:"
            )
            pretty(
                value,
                indent + 2
            )
        elif isinstance(value, list):
            print(
                f"{prefix}  {name}:"
            )
            for item in value:
                if isinstance(item, Node):
                    pretty(
                        item,
                        indent + 2
                    )
                else:
                    print(
                        f"{prefix}    {item}"
                    )
        else:
            print(
                f"{prefix}  {name}: {value}"
            )
