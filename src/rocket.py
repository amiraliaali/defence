import math

class Rocket:
    def __init__(self, x, y, orientation, speed, width, height, defensive_mode=False):
        self.x = x
        self.y = y
        self.orientation = orientation  # in degrees
        self.speed = speed
        self.defensive_mode = defensive_mode
        self.width = width
        self.height = height

    def move_one_step(self):
        # Convert orientation to radians for trigonometric functions
        radians = math.radians(self.orientation)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)

    def get_position(self):
        return (self.x, self.y)
    
    def get_pos_header(self):
        x_head = self.x + (self.width / 2) * math.cos(math.radians(self.orientation))
        y_head = self.y + (self.height / 2) * math.sin(math.radians(self.orientation))

        return (x_head, y_head)
    
    def get_orientation(self):
        return self.orientation
    
    def is_defensive_mode(self):
        return self.defensive_mode
    
    def collides_rocket(self, other_rocket):
        # Check if the distance between the two rockets is less than a threshold
        distance = math.sqrt((self.x - other_rocket.x) ** 2 + (self.y - other_rocket.y) ** 2)
        return distance < 1.0
