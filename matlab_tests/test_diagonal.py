import numpy as np

# Test matrix diagonal extraction

def test_diagonal():
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    d = diag[A-1]
    D = diag[d-1]
