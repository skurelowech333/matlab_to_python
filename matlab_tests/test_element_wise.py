import numpy as np

# Test element-wise operations

def test_element_wise():
    A = np.array([[1, 2, 3], [4, 5, 6]])
    B = np.array([[2, 3, 4], [5, 6, 7]])
    C = (A @ B)
    D = (A / B)
    E = (A ** 2)
    F = (A + B)
    G = (A - B)
