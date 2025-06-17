from rocket import Rocket

class Building:
    def __init__(self, height, x_position, building_num):
        self.height = height
        self.x_position = x_position
        self.building_num = building_num

    def get_height(self) -> float:
        return self.height
    
    def get_x_position(self) -> float:
        return self.x_position

    def get_building_num(self) -> int:
        return self.building_num
    
    def collides_rocket(self, rocket: Rocket, scree_height, threshold=50) -> bool:
        """Check if the rocket will collide with this building."""
        rocket_x, rocket_y = rocket.get_pos_header()
        building_x = self.get_x_position()
        building_height = self.get_height()

        # Check if the rocket's x position is within the building's x range
        if (building_x - threshold <= rocket_x <= building_x + threshold) and (rocket_y >= scree_height - building_height - threshold):
            return True
        return False
