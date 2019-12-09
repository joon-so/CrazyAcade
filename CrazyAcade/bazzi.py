from pico2d import *
from bubble import Bubble

import game_framework
import game_world
import stage1_state
import stage2_state
import boss_stage

# Bazzi Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bazzi Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, G, H, BUBBLE_TIME, ESCAPE_TIME = range(12)

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_w): UP_DOWN,
    (SDL_KEYDOWN, SDLK_s): DOWN_DOWN,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYUP, SDLK_w): UP_UP,
    (SDL_KEYUP, SDLK_s): DOWN_UP,
    (SDL_KEYDOWN, SDLK_g): G,
    (SDL_KEYDOWN, SDLK_h): H
}


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


class IdleState():
    @staticmethod
    def enter(bazzi, event):
        if event == RIGHT_DOWN:
            bazzi.bazzi_dir_x += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            bazzi.bazzi_dir_x -= RUN_SPEED_PPS
        elif event == UP_DOWN:
            bazzi.bazzi_dir_y += RUN_SPEED_PPS
        elif event == DOWN_DOWN:
            bazzi.bazzi_dir_y -= RUN_SPEED_PPS

        elif event == RIGHT_UP:
            bazzi.bazzi_dir_x -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            bazzi.bazzi_dir_x += RUN_SPEED_PPS
        elif event == UP_UP:
            bazzi.bazzi_dir_y -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            bazzi.bazzi_dir_y += RUN_SPEED_PPS

    @staticmethod
    def exit(bazzi, event):
        if event == G:
            if Bazzi.bubble_limit - bazzi.bubble_count > 0:
                bazzi.bubble_count += 1
                bazzi.make_bubble()

    @staticmethod
    def do(bazzi):
        if bazzi.bazzi_dir == 1:
            bazzi.frame_y = 350
        elif bazzi.bazzi_dir == 2:
            bazzi.frame_y = 280
        elif bazzi.bazzi_dir == 3:
            bazzi.frame_y = 490
        elif bazzi.bazzi_dir == 4:
            bazzi.frame_y = 420
        # collide enemy check
        for enemy in game_world.objects[2]:
            if collide(bazzi, enemy):
                Bazzi.in_bubble = 1
                bazzi.frame_x = 0
                bazzi.real_death = 1
                bazzi.frame_y = 70
                bazzi.death_animation_time = 0.025

    @staticmethod
    def draw(bazzi):
        if bazzi.life == 1:
            bazzi.dart.clip_draw(80, 0, 40, 40, 85, 17)
        bazzi.image.clip_draw(0, bazzi.frame_y, 70, 70, bazzi.x, bazzi.y)
        if Bazzi.in_bubble == 1:
            bazzi.add_event(BUBBLE_TIME)


class RunState():
    @staticmethod
    def enter(bazzi, event):
        if event == RIGHT_DOWN:
            bazzi.bazzi_dir = 1
            bazzi.bazzi_dir_x += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            bazzi.bazzi_dir = 2
            bazzi.bazzi_dir_x -= RUN_SPEED_PPS
        elif event == UP_DOWN:
            bazzi.bazzi_dir = 3
            bazzi.bazzi_dir_y += RUN_SPEED_PPS
        elif event == DOWN_DOWN:
            bazzi.bazzi_dir = 4
            bazzi.bazzi_dir_y -= RUN_SPEED_PPS

        elif event == RIGHT_UP:
            bazzi.bazzi_dir_x -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            bazzi.bazzi_dir_x += RUN_SPEED_PPS
        elif event == UP_UP:
            bazzi.bazzi_dir_y -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            bazzi.bazzi_dir_y += RUN_SPEED_PPS
        bazzi_dir = 0

    @staticmethod
    def exit(bazzi, event):
        if event == G:
            if Bazzi.bubble_limit - bazzi.bubble_count > 0:
                bazzi.bubble_count += 1
                bazzi.make_bubble()

    @staticmethod
    def do(bazzi):
        if bazzi.bazzi_dir == 1:
            bazzi.frame_x = (bazzi.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif bazzi.bazzi_dir == 2:
            bazzi.frame_x = (bazzi.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif bazzi.bazzi_dir == 3:
            bazzi.frame_x = (bazzi.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif bazzi.bazzi_dir == 4:
            bazzi.frame_x = (bazzi.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        bazzi.x += bazzi.bazzi_dir_x * game_framework.frame_time * bazzi.speed
        bazzi.y += bazzi.bazzi_dir_y * game_framework.frame_time * bazzi.speed

        if bazzi.bazzi_dir_x > 0:
            bazzi.frame_y = 350
        elif bazzi.bazzi_dir_x < 0:
            bazzi.frame_y = 280
        if bazzi.bazzi_dir_y > 0:
            bazzi.frame_y = 490
        elif bazzi.bazzi_dir_y < 0:
            bazzi.frame_y = 420

        # collide block check
        for block in game_world.objects[0]:
            if collide(bazzi, block):
                if block.box_color == 1 or block.box_color == 2 or block.box_color == 3 or block.box_color == 4\
                        or block.box_color == 5 or block.box_color == 6 or block.box_color == 7:
                    if bazzi.bazzi_dir_x != 0:
                        bazzi.x -= bazzi.bazzi_dir_x * game_framework.frame_time * bazzi.speed
                    if bazzi.bazzi_dir_y != 0:
                        bazzi.y -= bazzi.bazzi_dir_y * game_framework.frame_time * bazzi.speed
                    break
                elif block.box_color == 9:
                    bazzi.bubble_count -= 1
                    block.box_color = 0
                    break
                elif block.box_color == 10:
                    bazzi.bubble_range += 1
                    block.box_color = 0
                    break
                elif block.box_color == 11:
                    bazzi.speed += 0.05
                    block.box_color = 0
                    break

        # collide enemy check
        for enemy in game_world.objects[2]:
            if collide(bazzi, enemy):
                if bazzi.bazzi_dir_x != 0:
                    bazzi.x -= bazzi.bazzi_dir_x * game_framework.frame_time * bazzi.speed
                if bazzi.bazzi_dir_y != 0:
                    bazzi.y -= bazzi.bazzi_dir_y * game_framework.frame_time * bazzi.speed
                Bazzi.in_bubble = 1
                bazzi.frame_x = 0
                bazzi.real_death = 1
                bazzi.frame_y = 70
                bazzi.death_animation_time = 0.025

        bazzi.x = clamp(35, bazzi.x, 600)
        bazzi.y = clamp(70, bazzi.y, 565)

    @staticmethod
    def draw(bazzi):
        if bazzi.life == 1:
            bazzi.dart.clip_draw(80, 0, 40, 40, 85, 17)
        bazzi.image.clip_draw(int(bazzi.frame_x) * 70, int(bazzi.frame_y), 70, 70, bazzi.x, bazzi.y)
        if Bazzi.in_bubble == 1:
            bazzi.add_event(BUBBLE_TIME)


class DeathState():
    @staticmethod
    def enter(bazzi, event):
        if bazzi.bazzi_dir_x != 0:
            bazzi.x -= bazzi.bazzi_dir_x * game_framework.frame_time * bazzi.speed
        if bazzi.bazzi_dir_y != 0:
            bazzi.y -= bazzi.bazzi_dir_y * game_framework.frame_time * bazzi.speed
        bazzi.bazzi_dir_y = 0
        bazzi.bazzi_dir_x = 0
        if bazzi.real_death == 0:
            bazzi.frame_x = 0

    @staticmethod
    def exit(bazzi, event):
        if event == H:
            if bazzi.life == 1:
                if bazzi.real_death == 0:
                    bazzi.real_death = 2
                    bazzi.frame_x = 0
                    bazzi.death_animation_time = 0.025
                    bazzi.life -= 1

    @staticmethod
    def do(bazzi):
        bazzi.death_animation_time -= game_framework.frame_time
        if Bazzi.in_bubble == 1:
            if bazzi.death_animation_time <= 0:
                if bazzi.real_death == 0:
                    bazzi.frame_y = 210
                    bazzi.frame_x = bazzi.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
                    bazzi.death_animation_time = 0.25
                    if int(bazzi.frame_x) == 4:
                        bazzi.frame_x = 0
                        bazzi.real_death = 1
                        bazzi.frame_y = 70

                elif bazzi.real_death == 1:
                    bazzi.frame_x = bazzi.frame_x + 5 * ACTION_PER_TIME * game_framework.frame_time
                    bazzi.death_animation_time = 0.025
                    if int(bazzi.frame_x) > 5:
                        bazzi.frame_x = 5
                        bazzi.go_main = 1

                elif bazzi.real_death == 2:
                    bazzi.frame_y = 140
                    if bazzi.death_animation_time <= 0:
                        bazzi.frame_x = bazzi.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
                        bazzi.death_animation_time = 0.025

    @staticmethod
    def draw(bazzi):
        if bazzi.life == 1:
            bazzi.dart.clip_draw(80, 0, 40, 40, 85, 17)
        if bazzi.real_death == 2:
            if int(bazzi.frame_x) == 4:
                Bazzi.in_bubble = 0
                bazzi.real_death = 0
                bazzi.death_animation_time = 0.25
                bazzi.bazzi_dir = 0
                bazzi.frame_y = 420
                bazzi.add_event(ESCAPE_TIME)
        bazzi.image.clip_draw(int(bazzi.frame_x) * 70, int(bazzi.frame_y), 70, 70, bazzi.x, bazzi.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, UP_UP: RunState, DOWN_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UP_DOWN: RunState, DOWN_DOWN: RunState,
                G: IdleState, H: IdleState, BUBBLE_TIME: DeathState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState, DOWN_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, UP_DOWN: IdleState, DOWN_DOWN: IdleState,
               G: RunState, H: RunState, BUBBLE_TIME: DeathState},
    DeathState: {RIGHT_UP: DeathState, LEFT_UP: DeathState, UP_UP: DeathState, DOWN_UP: DeathState,
               LEFT_DOWN: DeathState, RIGHT_DOWN: DeathState, UP_DOWN: DeathState, DOWN_DOWN: DeathState,
               G: DeathState, H: DeathState, ESCAPE_TIME: IdleState}
}


class Bazzi:
    bubble_limit = 1
    in_bubble = 0
    def __init__(self):
        self.go_main = 0
        self.bazzi_dir = 0
        self.x, self.y = 0, 0
        self.bazzi_dir_x = 0
        self.bazzi_dir_y = 0
        self.death_animation_time = 0.25
        self.life = 1
        self.real_death = 0
        self.stage = 0
        self.bubble_count = 0
        self.bubble_range = 1
        self.speed = 1
        self.frame_x, self.frame_y = 0, 420
        self.dart = load_image('resource/Dart.png')
        self.image = load_image('resource/Character1_edit.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.sound = load_wav('sound/bubble.wav')
        self.sound.set_volume(50)

    def make_bubble(self):
        if self.stage == 1:
            for i in range(195):
                if stage1_state.block[i].block_x <= self.x + 20.1 < stage1_state.block[i].block_x + 40.2:
                    if stage1_state.block[i].block_y <= self.y - 3 < stage1_state.block[i].block_y + 40:
                        if stage1_state.block[i].box_color == 0 or stage1_state.block[i].box_color == 9\
                                or stage1_state.block[i].box_color == 10 or stage1_state.block[i].box_color == 11:
                            #stage1_state.block[i].box_color = 8
                            bubble = Bubble(stage1_state.block[i].block_x, stage1_state.block[i].block_y + 10, self.bubble_range, self.stage)
                            game_world.add_object(bubble, 1)
                            self.sound.play()
                            break
        elif self.stage == 2:
            for i in range(195):
                if stage2_state.block[i].block_x <= self.x + 20.1 < stage2_state.block[i].block_x + 40.2:
                    if stage2_state.block[i].block_y <= self.y - 3 < stage2_state.block[i].block_y + 40:
                        if stage2_state.block[i].box_color == 0 or stage2_state.block[i].box_color == 9\
                                or stage2_state.block[i].box_color == 10 or stage2_state.block[i].box_color == 11:
                            #stage1_state.block[i].box_color = 8
                            bubble = Bubble(stage2_state.block[i].block_x, stage2_state.block[i].block_y + 10, self.bubble_range, self.stage)
                            game_world.add_object(bubble, 1)
                            self.sound.play()
                            break
        elif self.stage == 3:
            for i in range(195):
                if boss_stage.block[i].block_x <= self.x + 20.1 < boss_stage.block[i].block_x + 40.2:
                    if boss_stage.block[i].block_y <= self.y - 3 < boss_stage.block[i].block_y + 40:
                        if boss_stage.block[i].box_color == 0 or boss_stage.block[i].box_color == 9\
                                or boss_stage.block[i].box_color == 10 or boss_stage.block[i].box_color == 11:
                            #stage1_state.block[i].box_color = 8
                            bubble = Bubble(boss_stage.block[i].block_x, boss_stage.block[i].block_y + 10, self.bubble_range, self.stage)
                            game_world.add_object(bubble, 1)
                            self.sound.play()
                            break

    def get_bb(self):
        return self.x - 11, self.y - 28, self.x + 11, self.y - 15

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)