from pico2d import *

import game_world

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
        boss.timer += 1
        if boss.timer == 2:
            if boss.dir == 1:
                boss.frame_y = 2484
                boss.y += 1
            elif boss.dir == 2:
                boss.frame_y = 2277
                boss.y -= 1
            elif boss.dir == 3:
                boss.frame_y = 2070
                boss.x += 1
            elif boss.dir == 4:
                boss.frame_y = 1863
                boss.x -= 1

            boss.frame_x = (boss.frame_x + 1) % 6
            boss.timer = 0

        #check crush

    @staticmethod
    def draw(boss):
        boss.image.clip_draw(boss.frame_x * 120, boss.frame_y, 120, 207, boss.x, boss.y)
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
        self.timer = 0
        self.image = load_image('resource/Monster_Boss.png')
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(1, event)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.image.clip_draw(self.frame_x * 120, self.frame_y, 120, 207, self.x, self.y)