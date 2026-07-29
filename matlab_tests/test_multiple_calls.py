import numpy as np

# Test multiple function calls in expression

def test_multiple_calls(a, b, c):
    result = (np.maximum(a, np.maximum(b, c)) + np.minimum(a, np.minimum(b, c)))
    
    return result
