import random
import pygame
from rocket import Rocket
from rocket_launcher import RocketLauncher
from building import Building
import numpy as np

MAX_BUILDINGS = 10
MAX_STEPS = 200


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
        self.current_step = 0
        self.reset()

    def reset(self):
        self.current_step = 0
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
                state.append(self.buildings[i].get_height() / self.screen_height)
                state.append(self.buildings[i].get_x_position() / self.screen_width)
            else:
                state.extend([0, 0])

        # Attacking rocket
        attack_x, attack_y = self.attacking_rocket.get_pos_header()
        attack_angle = self.attacking_rocket.get_orientation() / 360  # normalized
        state.append(attack_x / self.screen_width)
        state.append(attack_y / self.screen_height)
        state.append(attack_angle)

        # Defensive rocket
        defend_x, defend_y = self.defensive_rocket.get_pos_header()
        defend_angle = self.defensive_rocket.get_orientation() / 360  # normalized
        state.append(defend_x / self.screen_width)
        state.append(defend_y / self.screen_height)
        state.append(defend_angle)

        # Distance between rockets
        distance = self.calculate_rocket_distances() / np.hypot(self.screen_width, self.screen_height)
        state.append(distance)

        # --- Head-to-head angle difference ---
        # Vector from defensive rocket to attacking rocket
        vector_x = attack_x - defend_x
        vector_y = attack_y - defend_y
        target_angle = np.degrees(np.arctan2(vector_y, vector_x)) % 360  # angle from defensive rocket to attacker

        # Defensive rocket orientation
        defensive_angle = self.defensive_rocket.get_orientation() % 360

        # Angle difference
        angle_diff = (target_angle - defensive_angle + 180) % 360 - 180  # normalize to [-180, 180]
        state.append(angle_diff / 180)  # normalized to [-1, 1]

        return state


    def calculate_rocket_distances(self):
        attack_x, attack_y = self.attacking_rocket.get_pos_header()
        defend_x, defend_y = self.defensive_rocket.get_pos_header()

        x_difference = attack_x - defend_x
        y_difference = attack_y - defend_y

        return np.sqrt(x_difference**2 + y_difference**2)

    def calculate_reward(self):
        # Distance-based reward
        distance = self.calculate_rocket_distances()
        distance_reward = 1 - distance / np.hypot(self.screen_width, self.screen_height)

        # Head-to-head angle reward
        attack_x, attack_y = self.attacking_rocket.get_pos_header()
        defend_x, defend_y = self.defensive_rocket.get_pos_header()

        # Vector from defensive rocket to attacking rocket
        vector_x = attack_x - defend_x
        vector_y = attack_y - defend_y
        target_angle = np.degrees(np.arctan2(vector_y, vector_x)) % 360

        # Defensive rocket orientation
        defensive_angle = self.defensive_rocket.get_orientation() % 360

        # Angle difference normalized to [0,1], smaller is better
        angle_diff = (target_angle - defensive_angle + 180) % 360 - 180  # [-180, 180]
        angle_reward = 1 - abs(angle_diff) / 180  # 1 if perfect, 0 if pointing away

        # Combine distance and angle reward
        reward = distance_reward + angle_reward  # can weight them if needed

        # Sparse rewards
        if self.defended:
            reward += 10
        if self.building_collision:
            reward -= 20

        return reward



    def execute_action(self, action):
        if action == 0:
            pass
        elif action == 1:
            self.defensive_rocket.increase_speed()
        elif action == 2:
            self.defensive_rocket.decrease_speed()
        elif action == 3:
            self.defensive_rocket.rotate(-5)
        elif action == 4:
            self.defensive_rocket.rotate(5)


        self.step()

        reward = self.calculate_reward()

        # check whether all rockets are out of bounds or if there is a collision with a building
        done = True
        if (
            0 <= self.attacking_rocket.get_pos_header()[0] <= self.screen_width
            and 0 <= self.attacking_rocket.get_pos_header()[1] <= self.screen_height
        ):
            done = False

        if self.defended or self.building_collision or self.current_step > MAX_STEPS:
            done = True

        self.current_step += 1

        return self.get_state(), reward, done, {}
