import numpy as np

# Test assignment with expressions

def test_expr_assign():
    x = 10
    y = 20
    z = (((x + y) @ (x - y)) / (x @ y))
