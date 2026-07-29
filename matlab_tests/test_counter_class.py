import numpy as np

class Counter:
    Value = None
    
    def __init__(self, initial):
        if (len(locals()) < 1):
            initial = 0
        self.Value = initial
    
    def increment(self, amount):
        if (len(locals()) < 2):
            amount = 1
        self.Value = (self.Value + amount)
    
    def getValue(self):
        v = self.Value
        
        return v
    
