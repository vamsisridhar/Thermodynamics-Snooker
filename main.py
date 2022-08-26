from simulation import Simulation
from ball import Ball 
import numpy as np
ball1 = Ball(10, 5, np.array([0,0,0]), np.array([1, 1,1]))
ball2 = Ball(10, 5, np.array([10,10,10]), np.array([0, 0, 0]))
ball3 = Ball(10, 5, np.array([12,3,30]), np.array([1, -2, 0.2]))

ball4 = Ball(10, 5, -np.array([0,10,0]), np.array([1, 1,1]))
ball5 = Ball(10, 5, -np.array([10,10,10]), np.array([0, 0, 0]))
ball6 = Ball(10, 5, -np.array([12,3,30]), np.array([1, -2, 0.2]))

s = Simulation(100, [ball1, ball2, ball3, ball4, ball5, ball6], 1)

s.run(200, True)