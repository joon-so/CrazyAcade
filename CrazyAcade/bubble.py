from pico2d import *
import game_world

class IdleState():
    @staticmethod
    def enter(bubble, event):
        pass

    @staticmethod
    def exit(bubble, event):
        pass

    @staticmethod
    def do(bubble):
        bubble.frame = (bubble.frame + 1) % 4
        bubble.timer -= 1
        if bubble.timer == 0:
            game_world.remove_object(bubble)
            print('Delete Bubble')
            #bubble.add_event(BUBBLE_TIMER)

    @staticmethod
    def draw(bubble):
        bubble.image.clip_draw(bubble.frame * 40, 0, 40, 40, bubble.x, bubble.y - 7)
    pass


class Bubble:
    image = None

    def __init__(self, x = 9999, y = 9999):
        self.timer = 20
        self.frame = 0
        self.x, self.y = x, y
        self.cur_state = IdleState
        if Bubble.image == None:
            Bubble.image = load_image('resource/Bubble.png')

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        #bubble delete