import numpy as np

# Test switch-case statements

def test_switch(choice):
    if choice == 1:
        operation = 'addition'
    elif choice == 2:
        operation = 'subtraction'
    elif choice == 3:
        operation = 'multiplication'
    elif choice == 4:
        operation = 'division'
    else:
        operation = 'unknown'
    
    return operation
