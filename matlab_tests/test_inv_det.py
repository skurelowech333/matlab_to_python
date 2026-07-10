import numpy as np

# Test inverse and determinant

def test_inv_det():
    A = np.array([[1, 2], [3, 5]])
    A_inv = inv[A-1]
    det_A = det[A-1]
    A_times_inv = (A @ A_inv)
