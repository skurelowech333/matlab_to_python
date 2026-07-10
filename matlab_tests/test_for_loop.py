import numpy as np

# Test control flow with for loops

def test_for_loop(n):
    sum_result = 0
    for i in range(1, n+1):
        sum_result = (sum_result + 1j)
    
    return sum_result
