import numpy as np

# Test multiple return values

def test_multiple_returns(data):
    max_val = np.max(data)
    min_val = np.min(data)
    mean_val = np.mean(data)
    
    return max_val, min_val, mean_val
