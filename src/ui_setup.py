import pygame
from rocket import Rocket
from building import Building
import math
import random
from rocket_launcher import RocketLauncher

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
    light_gray = (211, 211, 211)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    return {
        "white": white,
        "light_gray": light_gray,
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

    if rocket.is_defensive_mode():
        # Defensive mode rockets are drawn in red
        rocket_image = pygame.image.load("images/defensive_rocket.png").convert_alpha()
    else:
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
    # pygame.time.delay(1000)

def overlay_explosion_rockets(position, width, screen):
    """Overlay an explosion effect for rockets at the given coordinates."""
    x, y = position
    explosion_image = pygame.image.load("images/explosion_rockets.png").convert_alpha()
    explosion_image = pygame.transform.scale(explosion_image, (width, width))
    explosion_rect = explosion_image.get_rect(center=(x, y))
    screen.blit(explosion_image, explosion_rect)
    # pygame.time.delay(1000)

def overlay_rocket_launcher(rocket_launcher, screen):
    """Overlay the rocket launcher on the screen."""
    x, y = rocket_launcher.x, rocket_launcher.y
    width, height = rocket_launcher.width, rocket_launcher.height

    launcher_image = pygame.image.load("images/rocket_launcher.png").convert_alpha()
    launcher_image = pygame.transform.scale(launcher_image, (width, height))
    launcher_rect = launcher_image.get_rect(center=(x, y))
    screen.blit(launcher_image, launcher_rect)

def main():
    """Main function to run the game setup."""
    screen, font, colors = setup_game()

    building_1 = Building(200, 150, 1)
    building_2 = Building(200, 350, 2)
    building_3 = Building(200, 900, 3)
    buildings = [building_1, building_2, building_3]
    rockets = []
    for i in range(10):
        rockets.append(Rocket(random.randint(0, WIDTH), 20, random.randint(20, 160), random.randint(5, 10), 50, 200, False))
    
    rocket_launcher = RocketLauncher(600, HEIGHT - 60, 120, 120)
    for i in range(2):
        rocket_launcher.launch(
            orientation=random.randint(220, 300),
            speed=random.randint(10, 20),
            width=100,
            height=200
        )
    rockets.extend(rocket_launcher.launched_rockets)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(colors["white"])
        overlay_rocket_launcher(rocket_launcher, screen)
        
        for building in buildings:
            if any(building.check_collision_rocket(rocket, HEIGHT) for rocket in rockets):
                overlay_explosion(building.get_x_position(), 300, screen)
                running = False
                print("Rocket hit a building! Game Over.")
            else:
                overlay_building(building, screen)
        
        for rocket_1 in rockets:
            for rocket_2 in rockets:
                if rocket_1 != rocket_2 and rocket_1.check_collision_rocket(rocket_2, HEIGHT) and rocket_1.is_defensive_mode()!= rocket_2.is_defensive_mode():
                    overlay_explosion_rockets(rocket_1.get_pos_header(), 200, screen)
                    rockets.remove(rocket_1)
                    rockets.remove(rocket_2)


        if running:
            for rocket in rockets:
                overlay_rocket(rocket, screen)
            
        for rocket in rockets:
            rocket.move_one_step()

        
        text_surface = font.render("Rocket Simulator", True, colors["black"])
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))
        
        pygame.display.flip()
        CLOCK.tick(FPS)
    pygame.time.delay(2000)
    pygame.quit()

if __name__ == "__main__":
    main()