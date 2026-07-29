import numpy as np

def simple_test(x):
    # Basic arithmetic
    a = (x ** 2)
    b = np.sqrt(a)
    # MATLAB built-in conversion test
    c = np.sin(x)
    # Loop test
    total = 0
    for i in range(1, 5+1):
        total = (total + i)
    # Final output
    y = ((b + c) + total)
    
    return y
