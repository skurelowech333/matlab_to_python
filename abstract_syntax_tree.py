# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any, Optional


NodeList = list["Node"]


@dataclass
class Node:
    line: int = 0
    source: str = ""


@dataclass
class Program(Node):
    body: NodeList = field(default_factory=list)


# Functions

@dataclass
class Function(Node):
    name: str = ""
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    body: NodeList = field(default_factory=list)


# Statements

@dataclass
class Assignment(Node):
    target: Node = None
    value: Node = None


@dataclass
class Return(Node):
    values: NodeList = field(default_factory=list)


@dataclass
class ExpressionStatement(Node):
    expression: Node = None


class Break(Node):
    pass


class Continue(Node):
    pass


@dataclass
class FailedConversion(Node):
    matlab_text: str = ""
    error: str = ""


@dataclass
class RawMATLAB(Node):
    text: str = ""


# Control flow

@dataclass
class If(Node):
    condition: Node = None
    body: NodeList = field(default_factory=list)
    elseif_blocks: list["ElseIf"] = field(default_factory=list)
    else_body: NodeList = field(default_factory=list)


@dataclass
class ElseIf(Node):
    condition: Node = None
    body: NodeList = field(default_factory=list)


@dataclass
class For(Node):
    variable: str = ""
    start: Node = None
    stop: Node = None
    step: Optional[Node] = None
    body: NodeList = field(default_factory=list)


@dataclass
class While(Node):
    condition: Node = None
    body: NodeList = field(default_factory=list)


@dataclass
class Switch(Node):
    expression: Node = None
    cases: list["Case"] = field(default_factory=list)
    default_body: NodeList = field(default_factory=list)


@dataclass
class Case(Node):
    value: Node = None
    body: NodeList = field(default_factory=list)


@dataclass
class Try(Node):
    body: NodeList = field(default_factory=list)
    catch_body: NodeList = field(default_factory=list)
    catch_var: str = ""


# Expressions

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
    left: Node = None
    right: Node = None


@dataclass
class UnaryOp(Node):
    operator: str = ""
    operand: Node = None


# Calls

@dataclass
class Call(Node):
    function: Node = None
    arguments: NodeList = field(default_factory=list)


# Indexing

@dataclass
class Index(Node):
    value: Node = None
    indices: NodeList = field(default_factory=list)


@dataclass
class Slice(Node):
    start: Node = None
    stop: Node = None
    step: Node = None


class End(Node):
    pass


# Arrays

@dataclass
class Matrix(Node):
    rows: list[list[Node]] = field(default_factory=list)
    shape: Optional[tuple] = None


@dataclass
class CellArray(Node):
    rows: list[list[Node]] = field(default_factory=list)


@dataclass
class Range(Node):
    start: Node = None
    step: Node = None
    stop: Node = None


# Structs

@dataclass
class FieldAccess(Node):
    value: Node = None
    field: str = ""


# Anonymous functions

@dataclass
class Lambda(Node):
    parameters: list[str] = field(default_factory=list)
    body: Node = None


@dataclass
class Comment(Node):
    text: str = ""


# Utilities

def walk(node):
    yield node

    for value in vars(node).values():
        if isinstance(value, Node):
            yield from walk(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, Node):
                    yield from walk(item)


def pretty(node, indent=0):
    print("  " * indent + node.__class__.__name__)

    for name, value in vars(node).items():
        if isinstance(value, Node):
            pretty(value, indent + 1)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, Node):
                    pretty(item, indent + 1)