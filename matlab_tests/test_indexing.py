import numpy as np

# Test array indexing and slicing

def test_indexing():
    A = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])
    a = A[0,0]
    b = A[1,2]
    row = A[0,:]
    col = A[:,1]
    submatrix = A[0:1,1:3]
