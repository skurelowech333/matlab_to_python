import numpy as np

# Test break and continue

def test_break_continue(limit):
    result = 0
    for i in range(1, limit+1):
        if (i == 5):
            continue
        if (i == 10):
            break
        result = (result + i)
    
    return result
