import numpy as np

# Test multiple function calls in expression

def test_multiple_calls(a, b, c):
    result = (np.max(a, np.max(b, c)) + np.min(a, np.min(b, c)))
    
    return result
