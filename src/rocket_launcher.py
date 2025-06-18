from rocket import Rocket

class RocketLauncher:
    def __init__(self, x, y, width, height):
        self.launched_rockets = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def launch(self, orientation, speed, width, height):
        self.rocket = Rocket(
            x=self.x,
            y=self.y,
            orientation=orientation,
            speed=speed,
            width=width,
            height=height,
            defensive_mode=True
        )
        self.launched_rockets.append(self.rocket)

    def get_launched_rockets(self):
        return self.launched_rockets