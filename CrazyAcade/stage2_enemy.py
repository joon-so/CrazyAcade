from pico2d import *

import game_world
import game_framework
# enemy1 Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 1500cm
RUN_SPEED_KMPH = 8 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# enemy1 Action Speed
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

DEATH = range(1)


class RunState():
    @staticmethod
    def enter(enemy, event):
        pass

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        if enemy.dir == 1:
            enemy.frame_y = 195
            enemy.y -= RUN_SPEED_PPS * game_framework.frame_time
        elif enemy.dir == 2:
            enemy.frame_y = 156
            enemy.x -= RUN_SPEED_PPS * game_framework.frame_time
        elif enemy.dir == 3:
            enemy.frame_y = 117
            enemy.x += RUN_SPEED_PPS * game_framework.frame_time
        elif enemy.dir == 4:
            enemy.frame_y = 78
            enemy.y += RUN_SPEED_PPS *game_framework.frame_time

        enemy.frame_x = (enemy.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        #check crush

    @staticmethod
    def draw(enemy):
        enemy.image.clip_draw(int(enemy.frame_x) * 41, enemy.frame_y, 41, 39, enemy.x, enemy.y)
    pass


class DeathState():
    pass


next_state_table = {
    RunState: {DEATH: DeathState}
}


class Enemy:
    def __init__(self, x, y, dir):
        self.x, self.y = x, y
        self.frame_x, self.frame_y = 1, 0
        self.dir = dir
        self.image = load_image('resource/Monster_Normal.png')
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(1, event)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)