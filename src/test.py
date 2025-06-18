import torch
import pygame
import time
from dqn import DQN
from environment import Env
from rocket import Rocket
from building import Building
from rocket_launcher import RocketLauncher

print("Starting test script...")
from ui_setup import (
    setup_game,
    overlay_rocket,
    overlay_building,
    overlay_rocket_launcher,
    overlay_explosion,
    overlay_explosion_rockets,
)

WIDTH, HEIGHT = 1200, 800
FPS = 30
RENDER_DELAY = 1 / FPS
MODEL_PATH = "dqn_defense_model.pth"

# Initialize game window
screen, font, colors = setup_game()

# Initialize environment
env = Env(WIDTH, HEIGHT)
state_size = len(env.get_state())
action_size = 1 + 3 * 10

# Load trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DQN(state_size, action_size).to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# Run one test episode
state = env.reset()
done = False
total_reward = 0

pygame.font.init()
reward_font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Choose greedy action
    with torch.no_grad():
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
        q_values = model(state_tensor)
        action = torch.argmax(q_values).item()

    # Step the environment
    next_state, reward, done, _ = env.execute_action(action)
    state = next_state
    total_reward += reward

    screen.fill(colors["white"])

    # Render game objects
    overlay_rocket_launcher(env.rocket_launcher, screen)

    for building in env.buildings:
        # Optional: explosion if hit
        if any(building.check_collision_rocket(r, HEIGHT) for r in env.rockets):
            overlay_explosion(building.get_x_position(), 300, screen)
            done = True
        else:
            overlay_building(building, screen)

    for r1 in env.rockets:
        for r2 in env.rockets:
            if r1 != r2 and r1.check_collision_rocket(r2, HEIGHT) and r1.is_defensive_mode() != r2.is_defensive_mode():
                overlay_explosion_rockets(r1.get_pos_header(), 200, screen)
                if r1 in env.rockets: env.rockets.remove(r1)
                if r2 in env.rockets: env.rockets.remove(r2)

    for rocket in env.rockets:
        overlay_rocket(rocket, screen)
    for rocket in env.rockets:
        rocket.move_one_step()
    for rocket in env.rocket_launcher.get_launched_rockets():
        rocket.move_one_step()

    # Display reward
    reward_text = reward_font.render(f"Reward: {total_reward:.2f}", True, colors["black"])
    screen.blit(reward_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

# Final reward message
time.sleep(1)
screen.fill(colors["white"])
final_msg = font.render(f"Test complete! Total Reward: {total_reward:.2f}", True, colors["black"])
screen.blit(final_msg, (WIDTH // 2 - final_msg.get_width() // 2, HEIGHT // 2))
pygame.display.flip()
time.sleep(3)
pygame.quit()
