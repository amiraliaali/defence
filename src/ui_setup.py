import pygame
from rocket import Rocket
from building import Building
import math

WIDTH, HEIGHT = 1200, 800

pygame.init()
CLOCK = pygame.time.Clock()
FPS = 30

def setup_window():
    """Set up the game window."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rocket Simulation")
    return screen

def setup_fonts():
    """Set up fonts for rendering text."""
    pygame.font.init()
    font = pygame.font.Font(None, 36)  # Default font with size 36
    return font

def setup_colors():
    """Define colors used in the game."""
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    return {
        "white": white,
        "black": black,
        "red": red,
        "green": green,
        "blue": blue
    }

def setup_game():
    """Initialize the game setup."""
    screen = setup_window()
    font = setup_fonts()
    colors = setup_colors()
    
    return screen, font, colors

def overlay_rocket(rocket: Rocket, screen):
    """Overlay a rocket on the screen."""
    x, y = rocket.get_position()
    width, height = rocket.width, rocket.height
    orientation = rocket.get_orientation()

    rocket_image = pygame.image.load("images/rocket.png").convert_alpha()
    rocket_image = pygame.transform.scale(rocket_image, (width, height))
    rocket_image = pygame.transform.rotate(rocket_image, -orientation-90)
    rocket_rect = rocket_image.get_rect(center=(x, y))
    screen.blit(rocket_image, rocket_rect)

def overlay_building(building: Building, screen):
    """Overlay a building on the screen."""
    height = building.get_height()
    x_position = building.get_x_position()
    building_num = building.get_building_num()

    building_image = pygame.image.load(f"images/building_{building_num}.png").convert_alpha()
    building_image = pygame.transform.scale(building_image, (height, height))
    building_rect = building_image.get_rect(center=(x_position, HEIGHT - height // 2))
    screen.blit(building_image, building_rect)

def overlay_explosion(x, width, screen):
    """Overlay an explosion effect at the given coordinates."""
    explosion_image = pygame.image.load("images/explosion.png").convert_alpha()
    explosion_image = pygame.transform.scale(explosion_image, (width, width))
    explosion_rect = explosion_image.get_rect(center=(x, HEIGHT - width // 2))
    screen.blit(explosion_image, explosion_rect)
    pygame.time.delay(500)  # Display the explosion for a short time

def check_collision_rocket_building(rocket: Rocket, building: Building, screen_height):
    rocket_x, rocket_y = rocket.get_position()[0] - rocket.width // 2, rocket.get_position()[1] - rocket.height // 2
    building_x = building.get_x_position() - building.get_height() // 2
    building_y = screen_height - building.get_height()

    rocket_rect = pygame.Rect(rocket_x, rocket_y, rocket.width, rocket.height)
    building_rect = pygame.Rect(building_x, building_y, building.get_height(), building.get_height())

    return rocket_rect.colliderect(building_rect)

def main():
    """Main function to run the game setup."""
    screen, font, colors = setup_game()

    rocket_1 = Rocket(100, 100, 45, 2, 50, 200, False)
    rocket_2 = Rocket(200, 200, 135, 2, 50, 200, False)

    building_1 = Building(200, 150, 1)
    building_2 = Building(200, 350, 2)
    building_3 = Building(200, 750, 3)
    buildings = [building_1, building_2, building_3]
    rockets = [rocket_1]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(colors["white"])  # Clear the screen with white color

        for building in buildings:
            if any(check_collision_rocket_building(rocket, building, HEIGHT) for rocket in rockets):
                overlay_explosion(building.get_x_position(), 300, screen)
                running = False
            else:
                overlay_building(building, screen)

        if running:
            for rocket in rockets:
                overlay_rocket(rocket, screen)
            
        rockets[0].move_one_step()
        
        # Example of rendering text
        text_surface = font.render("Rocket Simulation", True, colors["black"])
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))
        
        pygame.display.flip()  # Update the display
        CLOCK.tick(FPS)  # Maintain the frame rate
    
    pygame.quit()

if __name__ == "__main__":
    main()