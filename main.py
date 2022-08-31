from simulation import Simulation
from ball import Ball 
import numpy as np
ball1 = Ball(10, 5, np.array([4,4,4]), np.array([1e-16, 1e-16,1e-16]))
ball2 = Ball(10, 5, np.array([15,15,15]), np.array([-2, -2, -2]))
ball3 = Ball(10, 5, np.array([10,-2,15]), np.array([-1, -2, -2]))

s = Simulation(100, [ball1, ball2, ball3], 0.1)

s.run(1000, True)