import numpy as np

def matrix_test(x):
    # Matrix creation
    A = np.array([[1, 2], [3, 4]])
    # Matrix multiply
    B = (A * A)
    # Inverse
    C = np.linalg.inv(A)
    y = (C @ x)
    
    return y
