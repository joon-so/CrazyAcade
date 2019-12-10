from pico2d import *
import random

import game_world
import game_framework

# Boss Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 10 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# Boss Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

DEATH = range(1)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def boss_direct_y(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    a_y = (bottom_a + top_a) / 2
    b_y = (bottom_b + top_b) / 2
    if a_y > b_y: return 1
    if a_y < b_y: return 2


def boss_direct_x(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    a_x = (left_a + right_a) / 2
    b_x = (left_b + right_b) / 2
    if a_x < b_x: return 4
    if a_x > b_x: return 3


class RunState():
    @staticmethod
    def enter(boss, event):
        pass

    @staticmethod
    def exit(boss, event):
        pass

    @staticmethod
    def do(boss):
        for bazzi in game_world.objects[3]:
            boss.dir_x = boss_direct_x(bazzi, boss)
            boss.dir_y = boss_direct_y(bazzi, boss)
        if boss.dir_y == 1:
            boss.frame_y = 2484
            boss.y += RUN_SPEED_PPS * game_framework.frame_time
        elif boss.dir_y == 2:
            boss.frame_y = 2277
            boss.y -= RUN_SPEED_PPS * game_framework.frame_time
        if boss.dir_x == 3:
            boss.frame_y = 2070
            boss.x += RUN_SPEED_PPS * game_framework.frame_time
        elif boss.dir_x == 4:
            boss.frame_y = 1863
            boss.x -= RUN_SPEED_PPS * game_framework.frame_time

        for block in game_world.objects[0]:
            if collide(boss, block):
                # 벽돌 충돌시 랜덤으로 방향 변경
                if block.box_color == 1 or block.box_color == 2 or block.box_color == 3 or block.box_color == 4\
                        or block.box_color == 5 or block.box_color == 6 or block.box_color == 7:
                    if boss.dir_y == 2:
                        boss.y += RUN_SPEED_PPS * game_framework.frame_time
                    elif boss.dir_y == 1:
                        boss.y -= RUN_SPEED_PPS * game_framework.frame_time
                    if boss.dir_x == 4:
                        boss.x += RUN_SPEED_PPS * game_framework.frame_time
                    elif boss.dir_x == 3:
                        boss.x -= RUN_SPEED_PPS * game_framework.frame_time
                    break

        boss.frame_x = (boss.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        boss.x = clamp(50, boss.x, 590)
        boss.y = clamp(130, boss.y, 560)

        #check crush

    @staticmethod
    def draw(boss):
        boss.image.clip_draw(int(boss.frame_x) * 120, boss.frame_y, 120, 207, boss.x, boss.y)


class DeathState():
    pass


next_state_table = {
    RunState: {DEATH: DeathState}
}


class Boss:
    hp = 4
    def __init__(self):
        self.x, self.y = 180, 500
        self.frame_x, self.frame_y = 0, 0
        self.dir_x = 0
        self.dir_y = 0
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
        #draw_rectangle(*self.get_bb())