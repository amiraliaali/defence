from rocket import Rocket

class RocketLauncher:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rocket_launched = False

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
        self.rocket_launched = True


    def get_launched_rocket(self):
        return self.rocket

    def is_rocket_launched(self):
        return self.rocket_launched