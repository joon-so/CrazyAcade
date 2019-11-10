from pico2d import *
import game_world

BLOCK_POP = range(1)

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
        if block.box_color == 1:
            block.stage2_box1.clip_draw(block.box_frame_x * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 2:
            block.stage2_box2.clip_draw(block.box_frame_x * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 3:
            block.stage2_box3.clip_draw(block.box_frame_x * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 4:
            block.stage2_box4.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 5:
            block.stage2_box5.clip_draw(0, 0, 40, 70, block.block_x, block.block_y + 15)
    pass


class BrokeState:
    pass

next_state_table = {
    IdleState: {BLOCK_POP: BrokeState}
}


class Block:
    def __init__(self, block_x, block_y, box_color, box_broken):
        self.block_x, self.block_y, self.box_color, self.box_broken = \
            block_x, block_y, box_color, box_broken
        self.cur_state = IdleState
        self.box_frame_x, self.box_frame_y = 0, 2
        # 0: NULL
        # 1: box1
        # 2: box2
        # 3: box3
        # 4: No broken
        # 5: No broken

        if self.box_color == 1:
            self.stage2_box1 = load_image('resource/pirate_Box_0.png')
        elif self.box_color == 2:
            self.stage2_box2 = load_image('resource/pirate_Box_1.png')
        elif self.box_color == 3:
            self.stage2_box3 = load_image('resource/pirate_Box_2.png')
        elif self.box_color == 4:
            self.stage2_box4 = load_image('resource/pirate_Box_3.png')
        elif self.box_color == 5:
            self.stage2_box5 = load_image('resource/pirate_Box_4.png')

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)