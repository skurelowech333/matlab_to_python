import numpy as np

# Test try-catch error handling

def test_try_catch(a, b):
    try:
        result = (a / b)
    except Exception as e:
        result = 0
    
    return result
