import numpy as np

# Test logical NOT operator (~)

def test_logical_not(x):
    if not (x > 5):
        result = 1
    else:
        result = 0
    
    return result
