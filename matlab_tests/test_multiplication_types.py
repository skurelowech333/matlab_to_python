import numpy as np

# Test matrix multiplication vs element-wise

def test_multiplication_types():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    matrix_mult = (A @ B)
    element_mult = (A @ B)
