import numpy as np

# Test basic arithmetic operations

def test_arithmetic(a, b):
    result = (a + b)
    result = (result - a)
    result = (result @ 2)
    result = (result / b)
    
    return result
