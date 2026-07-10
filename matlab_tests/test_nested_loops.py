import numpy as np

# Test nested loops

def test_nested_loops(n, m):
    matrix_sum = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            matrix_sum = (matrix_sum + (1j @ 1j))
    
    return matrix_sum
