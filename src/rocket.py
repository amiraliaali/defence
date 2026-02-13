import math
import pygame

MAX_SPEED = 20

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

    def rotate(self, angle):
        self.orientation = (self.orientation + angle) % 360

    def increase_speed(self):
        if self.speed + 1 <= MAX_SPEED:
            self.speed += 1
        else:
            self.speed = MAX_SPEED

    def decrease_speed(self):
        if self.speed - 1 > 0:
            self.speed -= 1
        else:
            self.speed = 1

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

    def check_collision_rocket(self, other_rocket, screen_height):
        rocket_center = other_rocket.get_position()
        rocket_orientation = other_rocket.get_orientation()

        rocket_surface = pygame.Surface((other_rocket.width, other_rocket.height), pygame.SRCALPHA)
        rocket_surface.fill((255, 255, 255, 255))

        rotated_surface = pygame.transform.rotate(rocket_surface, -rocket_orientation - 90)
        rotated_rect = rotated_surface.get_rect(center=rocket_center)

        rocket_mask = pygame.mask.from_surface(rotated_surface)

        self_rocket_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self_rocket_surface.fill((255, 255, 255, 255))

        self_rotated_surface = pygame.transform.rotate(self_rocket_surface, -self.orientation - 90)
        self_rotated_rect = self_rotated_surface.get_rect(center=self.get_position())

        self_rocket_mask = pygame.mask.from_surface(self_rotated_surface)

        offset = (self_rotated_rect.left - rotated_rect.left, self_rotated_rect.top - rotated_rect.top)
        overlap = rocket_mask.overlap(self_rocket_mask, offset)

        return overlap is not None

