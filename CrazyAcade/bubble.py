from pico2d import *
import game_world


class Bubble:
    image = None
    def __init__(self):
        self.time, self.state = 0, 0
        self.frame = 0
        self.x, self.y = 9999, 9999
        if Bubble.image == None:
            Bubble.image = load_image('resource/Bubble.png')

    def update(self):
        if self.state == 1:
            # if self.time == 100:
            self.frame = (self.frame + 1) % 4
            self.time += 1
        if self.time == 10000:
            self.state = 2

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 40, self.x, self.y + 5)