import numpy as np

# Test while loops

def test_while_loop(start, limit):
    result = start
    while (result < limit):
        result = (result + 1)
    
    return result
