"""
Simulation Class

V Sridharbabu 21/08/2022

"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pylab as pl
import numpy as np

class Simulation:
    
    def __init__(self, container_radius, ball_array, dt):
        "initialises the simulation"
        self._container_radius = container_radius
        self._ball_array = ball_array
        self.dt = dt
        self.time = 0
        self.next_collision_time = None
        self.check_next_collision = True
        self.collision_codex = None

    def run(self, num_frames, animate=False):#
        if animate:
            self.fig = pl.figure()
            self.ax = self.fig.add_subplot(111, projection = '3d')
            self.plot_container()
            for ball in self._ball_array:
                self.plot_ball(ball)
            
            
        for frame in range(num_frames):
            self.next_collision()
            
            
            
            
            for ball in self._ball_array:
                ball.move(self.dt)
            
            
            if animate:
                self.fig.clear()
                self.ax = self.fig.add_subplot(111, projection = '3d')
                self.plot_container()
                for ball in self._ball_array:
                    self.plot_ball(ball)
                pl.pause(0.001)
            self.time += self.dt
        if animate:
            pl.show()
        

    def next_collision(self):
        min_col_time = []
        
        print(f"Current time is {self.time}")
        if self.check_next_collision:
            for ball in self._ball_array:
                
                v_dot_r = np.dot(ball.vel(), ball.pos())
                v_sqr = np.dot(ball.vel(), ball.vel())
                r_sqr = np.dot(ball.pos(), ball.pos())
                # Check collision of ball with container wall
                
                ball_wall_collide_time = (-(v_dot_r) + np.sqrt(v_dot_r**2 - v_sqr*(r_sqr - self._container_radius**2)))/(v_sqr)
                
                if not np.isnan(ball_wall_collide_time) and ball_wall_collide_time > 0:
                    # checks for valid time
                    min_col_time.append([ball, None, ball_wall_collide_time])
                
                # Loops through all other balls and checks collision time
                for colliding_ball in self._ball_array:
                    if id(ball) != id(colliding_ball):
                        ball1_ball2_collide_time =  ball.time_to_collision(colliding_ball)
                        if not np.isnan(ball1_ball2_collide_time) and ball1_ball2_collide_time > 0:
                            min_col_time.append([ball, colliding_ball, ball1_ball2_collide_time])
    
            # orders collision times in ascending order
            min_col_time = np.array(min_col_time)
            min_col_time = min_col_time[min_col_time[:, 2].argsort()]
            min_col_time[:,2] = self.dt*(min_col_time[:,2]//self.dt)
            min_col_time_indices = np.where(min_col_time[:,2] == np.min(min_col_time[:,2]))[0]
            
            self.collision_codex = min_col_time[min_col_time_indices]

            self.next_collision_time = self.time + self.collision_codex[0][2]
            
            #print(f"Next collision at {self.next_collision_time}")
            self.check_next_collision = False
        
        if self.next_collision_time >= self.time:
            
            pl.pause(5)
            for col_codex in self.collision_codex:
                if col_codex[1] is not None: 
                    col_codex[0].collide(col_codex[1])
                elif col_codex[1] is None:
                    col_codex[0].collide_wall()
                else:
                    raise Exception("Undefined collision sequence!")
            self.check_next_collision = True
        
    def plot_container(self):
        "plots a 3d translucent sphere with a radius of the container"
        u = np.linspace(0, 2 * np.pi, 25)
        v = np.linspace(0, np.pi, 25)
        
        x = self._container_radius * np.outer(np.cos(u), np.sin(v)) 
        y = self._container_radius * np.outer(np.sin(u), np.sin(v))
        z = self._container_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot the surface
        self.ax.plot_surface(x, y, z, color='g', alpha = 0.2)
    
    def plot_ball(self, ball):
        "plots a 3d sphere with a radius of the ball"
        u = np.linspace(0, 2 * np.pi, 10)
        v = np.linspace(0, np.pi, 10)
        
        x = ball.radius() * np.outer(np.cos(u), np.sin(v)) + ball.pos()[0]
        y = ball.radius() * np.outer(np.sin(u), np.sin(v)) + ball.pos()[1]
        z = ball.radius() * np.outer(np.ones(np.size(u)), np.cos(v)) + ball.pos()[2]
        
        # Plot the surface
        self.ax.plot_surface(x, y, z, color='b')
        
    
    
    __doc__ = """
    This class defines and handles the simulation
    """
    
if __name__ == "__main__":
    from ball import Ball
    ball1 = Ball(10, 5, np.array([0,0,0]), np.array([0.1, 0.1,0.1]))
    ball2 = Ball(10, 5, np.array([5,5,5]), np.array([0, 0, 0]))

    s = Simulation(100, [ball1])
