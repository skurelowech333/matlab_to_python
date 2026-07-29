import numpy as np

# Test any and all

def test_any_all():
    A = np.hstack((True, False, True))
    B = np.hstack((True, True, True))
    result1 = np.any(A)
    result2 = np.all(A)
    result3 = np.any(B)
    result4 = np.all(B)
