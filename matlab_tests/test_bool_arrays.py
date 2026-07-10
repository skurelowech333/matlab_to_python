import numpy as np

# Test boolean arrays

def test_bool_arrays():
    A = np.array([[1, 2, 3], [4, 5, 6]])
    mask = (A > 3)
    selected = A[mask-1]
