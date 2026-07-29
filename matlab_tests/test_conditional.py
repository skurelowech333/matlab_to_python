import numpy as np

# Test if-elseif-else statements

def test_conditional(value):
    if (value < 0):
        category = 'negative'
    elif (value == 0):
        category = 'zero'
    elif (value < 10):
        category = 'small'
    else:
        category = 'large'
    
    return category
