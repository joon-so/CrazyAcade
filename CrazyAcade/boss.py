from pico2d import *
import random

import game_world
import game_framework
from bazzi import Bazzi

# Boss Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 9 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# Boss Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

DEATH = range(1)

class RunState():
    @staticmethod
    def enter(boss, event):
        pass

    @staticmethod
    def exit(boss, event):
        pass

    @staticmethod
    def do(boss):
        if boss.dir == 1:
            boss.frame_y = 2484
            boss.y += RUN_SPEED_PPS * game_framework.frame_time
        elif boss.dir == 2:
            boss.frame_y = 2277
            boss.y -= RUN_SPEED_PPS * game_framework.frame_time
        if boss.dir == 3:
            boss.frame_y = 2070
            boss.x += RUN_SPEED_PPS * game_framework.frame_time
        elif boss.dir == 4:
            boss.frame_y = 1863
            boss.x -= RUN_SPEED_PPS * game_framework.frame_time

        boss.frame_x = (boss.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        boss.x = clamp(50, boss.x, 590)
        boss.y = clamp(130, boss.y, 560)

        #check crush

    @staticmethod
    def draw(boss):
        boss.image.clip_draw(int(boss.frame_x) * 120, boss.frame_y, 120, 207, boss.x, boss.y)
    pass


class DeathState():
    pass


next_state_table = {
    RunState: {DEATH: DeathState}
}


class Boss:
    def __init__(self):
        self.x, self.y = 180, 500
        self.frame_x, self.frame_y = 0, 0
        self.dir = 2
        self.image = load_image('resource/Monster_Boss.png')
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)

    def get_bb(self):
        return self.x - 55, self.y - 88, self.x + 55, self.y

    def add_event(self, event):
        self.event_que.insert(1, event)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())