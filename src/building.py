import pygame
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
    
    def check_collision_rocket(self, rocket: Rocket, screen_height):
        rocket_center = rocket.get_position()
        rocket_orientation = rocket.get_orientation()

        rocket_surface = pygame.Surface((rocket.width, rocket.height), pygame.SRCALPHA)
        rocket_surface.fill((255, 255, 255, 255))

        rotated_surface = pygame.transform.rotate(rocket_surface, -rocket_orientation - 90)
        rotated_rect = rotated_surface.get_rect(center=rocket_center)

        rocket_mask = pygame.mask.from_surface(rotated_surface)

        building_width = self.get_height()
        building_height = self.get_height()
        building_surface = pygame.Surface((building_width, building_height), pygame.SRCALPHA)
        building_surface.fill((255, 255, 255, 255))

        building_x = self.get_x_position() - building_width // 2
        building_y = screen_height - building_height
        building_mask = pygame.mask.from_surface(building_surface)
        building_rect = pygame.Rect(building_x, building_y, building_width, building_height)

        offset = (building_rect.left - rotated_rect.left, building_rect.top - rotated_rect.top)

        overlap = rocket_mask.overlap(building_mask, offset)

        return overlap is not None

    

