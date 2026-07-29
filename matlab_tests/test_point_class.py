import numpy as np

class Point:
    X = None
    Y = None
    
    def __init__(self, x, y):
        # Constructor: initialize properties
        self.X = x
        self.Y = y
    
    def move(self, dx, dy):
        # Translate the point by (dx, dy)
        self.X = (self.X + dx)
        self.Y = (self.Y + dy)
    
    def distanceToOrigin(self):
        # Return Euclidean distance from origin
        d = np.sqrt(((self.X ** 2) + (self.Y ** 2)))
        
        return d
    
    def isAboveXAxis(self):
        # Return true if the point is above the x‑axis
        isAbove = (self.Y > 0)
        
        return isAbove
    
    def isRightOfYAxis(self):
        # Return true if the point is right of the y‑axis
        isRight = (self.X > 0)
        
        return isRight
    
