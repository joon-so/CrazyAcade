from pico2d import *
import game_world

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, G, H = range(10)

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

bazzi_running = False


class IdleState():
    @staticmethod
    def enter(bazzi, event):
        if event == RIGHT_DOWN:
            bazzi.bazzi_dir_x += 1
        elif event == LEFT_DOWN:
            bazzi.bazzi_dir_x -= 1
        elif event == UP_DOWN:
            bazzi.bazzi_dir_y += 1
        elif event == DOWN_DOWN:
            bazzi.bazzi_dir_y -= 1

        elif event == RIGHT_UP:
            bazzi.bazzi_dir_x -= 1
        elif event == LEFT_UP:
            bazzi.bazzi_dir_x += 1
        elif event == UP_UP:
            bazzi.bazzi_dir_y -= 1
        elif event == DOWN_UP:
            bazzi.bazzi_dir_y += 1

    @staticmethod
    def exit(bazzi, event):
        pass

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

    @staticmethod
    def draw(bazzi):
        bazzi.image.clip_draw(0, bazzi.frame_y, 70, 70, bazzi.x, bazzi.y)
    pass


class RunState():
    @staticmethod
    def enter(bazzi, event):
        if event == RIGHT_DOWN:
            bazzi.bazzi_dir = 1
            bazzi.bazzi_dir_x += 1
        elif event == LEFT_DOWN:
            bazzi.bazzi_dir = 2
            bazzi.bazzi_dir_x -= 1
        elif event == UP_DOWN:
            bazzi.bazzi_dir = 3
            bazzi.bazzi_dir_y += 1
        elif event == DOWN_DOWN:
            bazzi.bazzi_dir = 4
            bazzi.bazzi_dir_y -= 1
        elif event == RIGHT_UP:
            bazzi.bazzi_dir_x -= 1
        elif event == LEFT_UP:
            bazzi.bazzi_dir_x += 1
        elif event == UP_UP:
            bazzi.bazzi_dir_y -= 1
        elif event == DOWN_UP:
            bazzi.bazzi_dir_y += 1
        bazzi_dir = 0

    @staticmethod
    def exit(bazzi, event):
        pass

    @staticmethod
    def do(bazzi):
        if bazzi.bazzi_dir == 1:
            bazzi.frame_x = (bazzi.frame_x + 1) % 4
            bazzi.frame_y = 350
        elif bazzi.bazzi_dir == 2:
            bazzi.frame_x = (bazzi.frame_x + 1) % 4
            bazzi.frame_y = 280
        elif bazzi.bazzi_dir == 3:
            bazzi.frame_x = (bazzi.frame_x + 1) % 4 + 1
            bazzi.frame_y = 490
        elif bazzi.bazzi_dir == 4:
            bazzi.frame_x = (bazzi.frame_x + 1) % 4 + 1
            bazzi.frame_y = 420

        bazzi.x += bazzi.bazzi_dir_x * 8
        bazzi.y += bazzi.bazzi_dir_y * 8
        #Crush Check

    @staticmethod
    def draw(bazzi):
        bazzi.image.clip_draw(bazzi.frame_x * 70, bazzi.frame_y, 70, 70, bazzi.x, bazzi.y)
    pass


class DeathState():
    pass


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                G: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               G: RunState },
    #DeathState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                 #LEFT_UP: RunState, RIGHT_UP: RunState,
                 #G: IdleState}
}


class Bazzi:
    global bazzi_running

    def __init__(self):
        self.bazzi_dir = 0
        self.x, self.y = 40, 560
        self.bazzi_dir_x = 0
        self.bazzi_dir_y = 0
        self.frame_x, self.frame_y = 0, 420
        self.image = load_image('resource/Character1_edit.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]

    def draw(self):
        self.cur_state.draw(self)

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)