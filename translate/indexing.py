from __future__ import annotations

# -*- coding: utf-8 -*-

"""
indexing.py

MATLAB indexing translation utilities.
"""


from abstract_syntax_tree import (
    Node,
    Number,
    Identifier,
    End,
    Slice,
    BinaryOp,
)



# ==========================================================
# Single index conversion
# ==========================================================

def convert_index(index: Node) -> str:
    """
    Convert MATLAB index into Python index.
    """


    # Numeric index
    #
    # MATLAB:
    #   A(1)
    #
    # Python:
    #   A[0]
    #

    if isinstance(index, Number):

        return str(
            int(index.value) - 1
        )



    # end keyword
    #

    if isinstance(index, End):

        return "-1"



    # Variable index
    #
    # MATLAB:
    #   A(i)
    #
    # Python:
    #   A[i-1]
    #

    if isinstance(index, Identifier):

        return (
            f"{index.name}-1"
        )



    # Expressions
    #

    if isinstance(index, BinaryOp):

        return convert_expression(
            index
        )


    return str(index)



# ==========================================================
# Expressions inside indexes
# ==========================================================

def convert_expression(node):

    """
    Convert expressions like:

        end-1
        i+2
    """


    if isinstance(node.left, End):

        left = "-1"

    else:

        left = convert_index(
            node.left
        )



    if isinstance(node.right, Number):

        right = str(
            int(node.right.value)
        )

    else:

        right = convert_index(
            node.right
        )


    return (
        f"({left}{node.operator}{right})"
    )



# ==========================================================
# Slice conversion
# ==========================================================

def convert_slice(slice_node):

    """
    Convert MATLAB colon expressions.

    MATLAB:
        2:end

    Python:
        1:-1

    """


    start = ""

    stop = ""

    step = ""



    if slice_node.start:

        start = convert_slice_value(
            slice_node.start
        )



    if slice_node.stop:

        stop = convert_slice_value(
            slice_node.stop
        )



    if slice_node.step:

        step = convert_slice_value(
            slice_node.step
        )



    if step:

        return (
            f"{start}:{stop}:{step}"
        )


    return (
        f"{start}:{stop}"
    )



def convert_slice_value(node):

    if isinstance(node, End):

        return ""


    if isinstance(node, Number):

        return str(
            int(node.value)-1
        )


    if isinstance(node, Identifier):

        return (
            f"{node.name}-1"
        )


    if isinstance(node, BinaryOp):

        return convert_expression(
            node
        )


    return str(node)



# ==========================================================
# MATLAB indexing translator
# ==========================================================

def translate_index(variable, indices):

    """
    Convert:

        A(1,2)

    into:

        A[0,1]


    Convert:

        A(:,2)

    into:

        A[:,1]
    """

    converted = []


    for index in indices:


        # Slice

        if isinstance(index, Slice):

            converted.append(
                convert_slice(index)
            )


        # Regular index

        else:

            converted.append(
                convert_index(index)
            )



    return (
        f"{variable}["
        +
        ",".join(converted)
        +
        "]"
    )