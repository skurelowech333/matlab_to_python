import numpy as np

# Test basic cell array creation and indexing

def test_cell_arrays():
    # Create a simple cell array of numbers
    c = [1, 2, 3]
    # Modify a middle element
    c[1] = 10
    # Read out and combine values
    out = ((c[0] + c[1]) + c[2])
    # 1 + 10 + 3 = 14
    
    return out
