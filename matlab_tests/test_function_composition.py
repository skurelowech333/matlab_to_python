import numpy as np

# Test function composition

def test_function_composition(x):
    result = np.sin(np.cos(np.sqrt(np.abs(x))))
    
    return result
