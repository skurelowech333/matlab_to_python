import numpy as np

# Test for loop with a step value

def test_for_step(n):
    result = 0
    for i in range(1, n+1, 2):
        result = (result + i)
    
    return result
