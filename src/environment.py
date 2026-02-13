import random
import pygame
from rocket import Rocket
from rocket_launcher import RocketLauncher
from building import Building
import numpy as np

MAX_BUILDINGS = 10


class Env:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.attacking_rocket = None
        self.defensive_rocket = None
        self.defended = False
        self.buildings = []
        self.rocket_launcher = None
        self.building_collision = False
        self.last_iter_distance = np.inf
        self.reset()

    def reset(self):
        self.buildings = []
        self.rocket_launcher = None
        self.building_collision = False
        self.defended = False

        for i in range(int(self.screen_width / 200)):
            is_last_iteration = i == int(self.screen_width / 200) - 1
            x_position = i * 200 + 100

            if random.random() < 0.5:
                if is_last_iteration and self.rocket_launcher is None:
                    self.rocket_launcher = RocketLauncher(
                        x=x_position, y=self.screen_height - 60, width=120, height=120
                    )
                else:
                    height = random.randint(100, 200)
                    building_num = random.randint(1, 3)
                    self.buildings.append(Building(height, x_position, building_num))
            else:
                if self.rocket_launcher is None:
                    self.rocket_launcher = RocketLauncher(
                        x=x_position, y=self.screen_height - 60, width=120, height=120
                    )

        self.attacking_rocket = Rocket(
                x=random.randint(0, self.screen_width),
                y=20,
                orientation=random.randint(20, 160),
                speed=random.randint(5, 10),
                width=50,
                height=200,
                defensive_mode=False,
            )


        self.rocket_launcher.launch(
            orientation=random.randint(220, 300),
            speed=random.randint(10, 20),
            width=100,
            height=200
        )
        self.defensive_rocket = self.rocket_launcher.get_launched_rocket()

        self.buildings = self.buildings[:MAX_BUILDINGS]
        return self.get_state()

    def step(self):
        self.building_collision = False

        self.attacking_rocket.move_one_step()
        self.defensive_rocket.move_one_step()

        for building in self.buildings:
            if building.check_collision_rocket(self.attacking_rocket, self.screen_height):
                self.building_collision = True
                break

        self.defended = False
        if (
            self.attacking_rocket.check_collision_rocket(self.defensive_rocket, self.screen_height)
        ):
            self.defended = True


        # if 0 <= self.attacking_rocket.get_pos_header()[0] <= self.screen_width and 0 <= self.attacking_rocket.get_pos_header()[1] <= self.screen_height:
        #     self.attacking_rocket = None

        # if 0 <= self.defensive_rocket.get_pos_header()[0] <= self.screen_width and 0 <= self.defensive_rocket.get_pos_header()[1] <= self.screen_height:
        #     self.defensive_rocket = None

        return self.get_state()

    def get_state(self):
        state = [
            int(self.building_collision),
            int(self.defended),
        ]

        # Building info
        for i in range(MAX_BUILDINGS):
            if i < len(self.buildings):
                state.append(self.buildings[i].get_height())
                state.append(self.buildings[i].get_x_position())
            else:
                state.extend([0, 0])

        # Attacking rocket
        state.append(self.attacking_rocket.get_pos_header()[0])
        state.append(self.attacking_rocket.get_pos_header()[1])
        state.append(self.attacking_rocket.get_orientation())
        # state.append(int(self.rockets[i].is_defensive_mode()))


        # Defensive rockets
        state.append(self.defensive_rocket.get_pos_header()[0])
        state.append(self.defensive_rocket.get_pos_header()[1])
        state.append(self.defensive_rocket.get_orientation())
        # state.append(int(launched[i].is_defensive_mode()))

        state.append(self.calculate_rocket_distances())


        return state

    def calculate_rocket_distances(self):
        attack_x, attack_y = self.attacking_rocket.get_pos_header()
        defend_x, defend_y = self.defensive_rocket.get_pos_header()

        x_difference = attack_x - defend_x
        y_difference = attack_y - defend_y

        return np.sqrt(x_difference**2 + y_difference**2)

    def calculate_reward(self):
        current_iter_distance = self.calculate_rocket_distances()

        if current_iter_distance < self.last_iter_distance:
            reward = 1
        else:
            reward = -1

        self.last_iter_distance = current_iter_distance

        if self.building_collision:
            return -200

        if self.defended:
            return 100

        return reward

    def execute_action(self, action):
        if action == 1:
            self.defensive_rocket.increase_speed()
        elif action == 2:
            self.defensive_rocket.rotate(-10)
        elif action == 3:
            self.defensive_rocket.rotate(10)

        self.step()

        reward = self.calculate_reward()

        # check whether all rockets are out of bounds or if there is a collision with a building
        done = True
        if (
            0 <= self.attacking_rocket.get_pos_header()[0] <= self.screen_width
            and 0 <= self.attacking_rocket.get_pos_header()[1] <= self.screen_height
        ):
            done = False

        if self.defended or self.building_collision:
            done = True

        return self.get_state(), reward, done, {}
