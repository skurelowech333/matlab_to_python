import numpy as np

# Test array concatenation

def test_concatenation():
    A = np.array([[1, 2, 3]])
    B = np.array([[4, 5, 6]])
    C = np.array([[A, B]])
    D = np.array([[A], [B]])
