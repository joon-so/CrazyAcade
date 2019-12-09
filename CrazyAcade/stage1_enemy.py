from pico2d import *
import random

import game_world
import game_framework
# enemy1 Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 1500cm
RUN_SPEED_KMPH = 7 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# enemy1 Action Speed
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

DEATH = range(1)

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

class RunState():
    @staticmethod
    def enter(enemy, event):
        pass

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        # 일정 시간 경과 시 랜덤으로 방향 변경
        enemy.block_count += game_framework.frame_time
        if int(enemy.block_count) == 3:
            enemy.dir = random.randint(1, 4)
            enemy.block_count = 0

        if enemy.dir == 1:
            enemy.frame_y = 170
            enemy.y -= RUN_SPEED_PPS * game_framework.frame_time
        elif enemy.dir == 2:
            enemy.frame_y = 136
            enemy.x -= RUN_SPEED_PPS * game_framework.frame_time
        elif enemy.dir == 3:
            enemy.frame_y = 102
            enemy.x += RUN_SPEED_PPS * game_framework.frame_time
        elif enemy.dir == 4:
            enemy.frame_y = 68
            enemy.y += RUN_SPEED_PPS * game_framework.frame_time

        # 벽돌 충돌체크
        for block in game_world.objects[0]:
            if collide(enemy, block):
                # 벽돌 충돌시 랜덤으로 방향 변경
                if block.box_color == 1 or block.box_color == 2 or block.box_color == 3 or block.box_color == 4\
                        or block.box_color == 5 or block.box_color == 6 or block.box_color == 7:
                    if enemy.dir == 1:
                        enemy.y += RUN_SPEED_PPS * game_framework.frame_time
                    elif enemy.dir == 2:
                        enemy.x += RUN_SPEED_PPS * game_framework.frame_time
                    elif enemy.dir == 3:
                        enemy.x -= RUN_SPEED_PPS * game_framework.frame_time
                    elif enemy.dir == 4:
                        enemy.y -= RUN_SPEED_PPS * game_framework.frame_time

                    enemy.dir = random.randint(1, 4)
                    break
        # 맵 충돌체크
        if int(enemy.x) <= 35:
            while enemy.dir == 2:
                enemy.dir = random.randint(1, 4)
        if int(enemy.x) >= 607:
            while enemy.dir == 3:
                enemy.dir = random.randint(1, 4)
        if int(enemy.y) <= 58:
            while enemy.dir == 1:
                enemy.dir = random.randint(1, 4)
        if int(enemy.y) >= 551:
            while enemy.dir == 4:
                enemy.dir = random.randint(1, 4)

        enemy.frame_x = (enemy.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        #check crush

    @staticmethod
    def draw(enemy):
        enemy.image.clip_draw(int(enemy.frame_x) * 34, enemy.frame_y, 34, 34, enemy.x, enemy.y)
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
        self.image = load_image('resource/Monster_Basic.png')
        self.event_que = []
        self.block_count = 0
        self.cur_state = RunState
        self.cur_state.enter(self, None)

    def get_bb(self):
        return self.x - 12, self.y - 18, self.x + 12, self.y + 7

    def add_event(self, event):
        self.event_que.insert(1, event)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        #draw_rectangle(*self.get_bb())