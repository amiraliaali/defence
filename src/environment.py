import random
import pygame
from rocket import Rocket
from rocket_launcher import RocketLauncher
from building import Building

MAX_ROCKETS = 10
MAX_BUILDINGS = 10


class Env:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rockets = []
        self.last_num_rockets = 0
        self.buildings = []
        self.rocket_launcher = None
        self.collision_with_building = False
        self.reset()

    def reset(self):
        self.rockets = []
        self.buildings = []
        self.rocket_launcher = None
        self.collision_with_building = False

        for i in range(int(self.screen_width / 200)):
            is_last_iteration = (i == int(self.screen_width / 200) - 1)
            x_position = i * 200 + 100

            if random.random() < 0.5:
                if is_last_iteration and self.rocket_launcher is None:
                    self.rocket_launcher = RocketLauncher(
                        x=x_position,
                        y=self.screen_height - 60,
                        width=120,
                        height=120
                    )
                else:
                    height = random.randint(100, 200)
                    building_num = random.randint(1, 3)
                    self.buildings.append(Building(height, x_position, building_num))
            else:
                if self.rocket_launcher is None:
                    self.rocket_launcher = RocketLauncher(
                        x=x_position,
                        y=self.screen_height - 60,
                        width=120,
                        height=120
                    )

        for _ in range(MAX_ROCKETS):
            if random.random() < 0.5:
                self.rockets.append(Rocket(
                    x=random.randint(0, self.screen_width),
                    y=20,
                    orientation=random.randint(20, 160),
                    speed=random.randint(5, 10),
                    width=50,
                    height=200,
                    defensive_mode=False
                ))

        self.buildings = self.buildings[:MAX_BUILDINGS]
        self.rockets = self.rockets[:MAX_ROCKETS]
        return self.get_state()

    def step(self):
        self.collision_with_building = False
        for rocket in self.rockets:
            rocket.move_one_step()

        for building in self.buildings:
            for rocket in self.rockets[:]:
                if building.check_collision_rocket(rocket, self.screen_height):
                    self.rockets.remove(rocket)
                    self.collision_with_building = True
                    break

        for rocket in self.rockets[:]:
            for other_rocket in self.rocket_launcher.get_launched_rockets():
                if rocket.check_collision_rocket(other_rocket, self.screen_height) and \
                   rocket.is_defensive_mode() != other_rocket.is_defensive_mode():
                    self.rockets.remove(rocket)
                    self.rocket_launcher.launched_rockets.remove(other_rocket)
                    break

        return self.get_state()

    def get_state(self):
        state = [1 if self.collision_with_building else 0]

        # Building info
        for i in range(MAX_BUILDINGS):
            if i < len(self.buildings):
                state.append(self.buildings[i].get_height())
                state.append(self.buildings[i].get_x_position())
            else:
                state.extend([0, 0])

        # Attacking rockets
        for i in range(MAX_ROCKETS):
            if i < len(self.rockets):
                state.append(self.rockets[i].get_pos_header()[0])
                state.append(self.rockets[i].get_pos_header()[1])
                state.append(self.rockets[i].get_orientation())
                state.append(int(self.rockets[i].is_defensive_mode()))
            else:
                state.extend([0, 0, 0, 0])

        # Defensive rockets
        launched = self.rocket_launcher.get_launched_rockets()
        for i in range(MAX_ROCKETS):
            if i < len(launched):
                state.append(launched[i].get_pos_header()[0])
                state.append(launched[i].get_pos_header()[1])
                state.append(launched[i].get_orientation())
                state.append(int(launched[i].is_defensive_mode()))
            else:
                state.extend([0, 0, 0, 0])

        return state
    
    def calculate_reward(self):
        reward = 0

        if self.collision_with_building:
            return -100
        
        if self.last_num_rockets > len(self.rockets):
            reward += 50

        for i in range(len(self.rocket_launcher.get_launched_rockets())):
            reward -= 5
        
        return reward

    def execute_action(self, action):
        launched = self.rocket_launcher.get_launched_rockets()

        if action == 0:
            if len(launched) < MAX_ROCKETS:
                orientation = random.randint(220, 300)
                speed = random.randint(10, 20)
                width = 100
                height = 200
                self.rocket_launcher.launch(orientation, speed, width, height)

        for i in range(len(launched)):
            if action == 1 + i * 3:
                launched[i].increase_speed()
            elif action == 2 + i * 3:
                launched[i].rotate(-10)
            elif action == 3 + i * 3:
                launched[i].rotate(10)
        
        self.step()
        
        reward = self.calculate_reward()

        self.last_num_rockets = len(self.rockets)

        done = len(self.rockets) == 0 or self.collision_with_building

        return self.get_state(), reward, done, {}