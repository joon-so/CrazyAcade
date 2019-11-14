from pico2d import *
import game_world

class IdleState():
    @staticmethod
    def enter(block, event):
        pass

    @staticmethod
    def exit(block, event):
        pass

    @staticmethod
    def do(block):
        #bubble.add_event(BLOCK_POP)
        pass

    @staticmethod
    def draw(block):
        if block.box_color == 4:
            block.stage2_box4.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 5:
            block.stage2_box5.clip_draw(0, 0, 40, 70, block.block_x, block.block_y + 15)
    pass


class Block:
    def __init__(self, block_x, block_y, box_color, box_broken):
        self.block_x, self.block_y, self.box_color, self.box_broken = \
            block_x, block_y, box_color, box_broken
        self.cur_state = IdleState
        # 0: NULL
        # 4: No broken
        # 5: No broken

        if self.box_color == 4:
            self.stage2_box4 = load_image('resource/pirate_Box_3.png')
        elif self.box_color == 5:
            self.stage2_box5 = load_image('resource/pirate_Box_4.png')

    def get_bb(self):
        return self.block_x - 20, self.block_y - 20, self.block_x + 20, self.block_y + 20

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())