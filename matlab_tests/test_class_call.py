import numpy as np

class TestSatellite:
    mass = None
    area = None
    name = None
    
    def __init__(self, m, a, n):
        self.mass = m
        self.area = a
        self.name = n
    
    def getMass(self):
        m = self.mass
        
        return m
    
    def ballisticCoefficient(self):
        beta = (self.mass / self.area)
        
        return beta
    

# =====================================================

# Test class usage

# =====================================================
