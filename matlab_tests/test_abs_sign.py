import numpy as np

# Test absolute value and sign

def test_abs_sign():
    values = np.array([[-5, -2, 0, 2, 5]])
    abs_values = np.abs(values)
    sign_values = np.sign(values)
