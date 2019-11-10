from pico2d import *

import game_world

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
        enemy.timer += 1
        if enemy.timer == 2:
            if enemy.dir == 1:
                enemy.frame_y = 195
                enemy.y -= 1
            elif enemy.dir == 2:
                enemy.frame_y = 156
                enemy.x -= 1
            elif enemy.dir == 3:
                enemy.frame_y = 117
                enemy.x += 1
            elif enemy.dir == 4:
                enemy.frame_y = 78
                enemy.y += 1

            if enemy.frame_x == 1:
                enemy.frame_x = 0
            else:
                enemy.frame_x = 1
            enemy.timer = 0

        #check crush

    @staticmethod
    def draw(enemy):
        enemy.image.clip_draw(enemy.frame_x * 41, enemy.frame_y, 41, 39, enemy.x, enemy.y)
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
        self.timer = 0
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