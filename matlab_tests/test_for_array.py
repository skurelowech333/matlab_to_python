import numpy as np

# Test for loop over a vector (array iteration)

def test_for_array(n):
    values = np.array([1, 3, 5, 7, 9])
    total = 0
    for v in values:
        if (v <= n):
            total = (total + v)
    
    return total
