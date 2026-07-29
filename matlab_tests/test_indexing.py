import numpy as np

# Test array indexing and slicing

def test_indexing():
    A = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])
    a = A(1, 1)
    b = A(2, 3)
    # CONVERSION FAILED:
    row = A(1, )
    # CONVERSION FAILED:
    col = A(, 2)
    # CONVERSION FAILED:
    # CONVERSION FAILED:
    submatrix = A(, )
