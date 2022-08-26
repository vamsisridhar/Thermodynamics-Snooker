"""
Ball Class
V Sridharbabu 21/08/2022
"""
import numpy as np

class Ball:
    def __init__(self, mass, radius, position, velocity):
        "Initialising Ball obj with mass, radius, position and velocity"
        self._mass = mass
        self._radius = radius
        
        if position.shape[0] != 3:
            raise ValueError("The position needs to be a 3 dimensional vector!")
        if velocity.shape[0] != 3:
            raise ValueError("The velocity needs to be a 3 dimensional vector!")
        
        self._position = position
        self._velocity = velocity
    
    def pos(self):
        "returns the current position of the Ball"
        return self._position
    def set_pos(self, new_pos):
        self._position = new_pos
    def set_vel(self, new_vel):
        self._velocity = new_vel
    def radius(self):
        return self._radius
    def mass(self):
        return self._mass
    def vel(self):
        "returns the current velocity of the Ball"
        return self._velocity
    
    def move(self, dt):
        "updates the new position of the Ball to time step dt"
        new_position = self.pos() + (dt * self.vel())
        self._position = new_position
    
    def time_to_collision(self, other):
        "calculate time to collision between self and other"
        r = self.pos() - other.pos()
        v = self.vel() - other.vel()
        R = self._radius + other.radius()
        R_n = self._radius - other.radius()
        
        flag_overlapping = (r.dot(r) - R**2) < 0
        
        if not flag_overlapping:
            
            col_t_1 = (-(np.dot(r,v))-np.sqrt((np.dot(r,v))**2 - np.dot(v,v)*(np.dot(r,r) - R**2)))/np.dot(v,v)
            return col_t_1
            
        else:
            raise RuntimeError(f"Ball found to be overlapping, unable to compute collision time between {self} and {other}")
            
    def collide(self, other):
        "update velcoities of both balls after collision"
        r = other.pos() - self.pos()
        r_dir = r/np.linalg.norm(r)
        u1_parallel = np.dot(self.vel(), r_dir)*r_dir        
        u2_parallel = np.dot(other.vel(), r_dir)*r_dir
        
        u1_perpendicular = self.vel() - u1_parallel
        u2_perpendicular = self.vel() - u2_parallel
        
        v1_parallel = (u1_parallel*(self._mass - other.mass()) + 2*other.mass()*u2_parallel)/(self._mass + other.mass())
        
        v2_parallel = u1_parallel + v1_parallel - u2_parallel
        
        v1 = v1_parallel + u1_perpendicular
        v2 = v2_parallel + u2_perpendicular
        
        self.set_vel(v1)
        other.set_vel(v2)
    
    def collide_wall(self):
        r = self.pos()
        r_dir = r/np.linalg.norm(r)
        u1_parallel = np.dot(self.vel(), r_dir)*r_dir
        u1_perpendicular = self.vel() - u1_parallel
        
        v1 = u1_perpendicular - u1_parallel
        
        self.set_vel(v1)
    
    def __repr__(self):
        return "%s(mass=%g, radius=%g, pos=[%g, %g, %g], vel=[%g, %g, %g])" % ("Ball", self._mass, self._radius, self.pos()[0], self.pos()[1], self.pos()[2], self.vel()[0], self.vel()[1], self.vel()[2])
    
    __doc__ = """
    This class defines a Ball object with mass, radius, position and velocity
    Position and Velocity are 3D Vectors
    
    """
    
if __name__ == "__main__":
    dt = 0.5
    ball1 = Ball(10, 5, np.array([0,0,0]), np.array([0.1, 0.1,0.1]))
    ball2 = Ball(10, 5, np.array([10,10,10]), np.array([0, 0, 0]))
    print(ball1)
    print(ball2)
    
    ball1.move(dt)
    ball2.move(dt)
    
    if not (np.array_equal(ball1.pos(), np.array([0.05, 0.05, 0.05])) and np.array_equal(ball2.pos(), np.array([10,10,10]))):
        raise Exception("Ball.move() incorrect!")
    else:
        print("Ball.move() successful!")
        print(ball1)
        print(ball2)
    
    ball2._position = np.array([10,10,10])
    
    t_col_1_2 = ball1.time_to_collision(ball2)
    print(t_col_1_2)
        