import numpy as np

# Test anonymous function (lambda) translation

def test_lambda(x):
    f = lambda t: ((t * t) + 1)
    result = f(x)
    
    return result
