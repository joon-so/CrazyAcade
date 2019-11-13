from pico2d import *
import game_world
import game_framework
# Bubble Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

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
        if block.box_color != 0:
            if block.box_broken == 0:
                print('broke')
                block.add_event(BLOCK_POP)
        pass

    @staticmethod
    def draw(block):
        if block.box_color == 1:
            block.stage1_box2.clip_draw(block.box_frame_x * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 2:
            block.stage1_box3.clip_draw(block.box_frame_x * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 3:
            block.stage1_box1.clip_draw(block.box_frame_x * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 4:
            block.stage1_house1.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 5:
            block.stage1_house2.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 6:
            block.stage1_house3.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 7:
            block.stage1_tree.clip_draw(0, 0, 40, 70, block.block_x, block.block_y + 12)
    pass


class BrokeState:
    @staticmethod
    def enter(block, event):
        pass

    @staticmethod
    def exit(block, event):
        pass

    @staticmethod
    def do(block):
        block.timer -= FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 1.5
        if block.timer <= 0:
            block.box_frame_x = (block.box_frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            block.timer = 1
            if int(block.box_frame_x) % 3 == 0:
                block.box_frame_y -= 1
                if block.box_frame_y == 0:
                    block.box_color = 0
                    game_world.remove_object(block)
                    print('Delete Block')
        pass

    @staticmethod
    def draw(block):
        if block.box_color == 1:
            block.stage1_box2.clip_draw(int(block.box_frame_x) * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 2:
            block.stage1_box3.clip_draw(int(block.box_frame_x) * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 3:
            block.stage1_box1.clip_draw(int(block.box_frame_x) * 40, block.box_frame_y * 45, 41, 45, block.block_x, block.block_y)
        elif block.box_color == 4:
            block.stage1_house1.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 5:
            block.stage1_house2.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 6:
            block.stage1_house3.clip_draw(0, 0, 41, 57, block.block_x, block.block_y + 7)
        elif block.box_color == 7:
            block.stage1_tree.clip_draw(0, 0, 40, 70, block.block_x, block.block_y + 12)
    pass

next_state_table = {
    IdleState: {BLOCK_POP: BrokeState}
}


class Block:
    def __init__(self, block_x, block_y, box_color, box_broken):
        self.block_x, self.block_y, self.box_color, self.box_broken = \
            block_x, block_y, box_color, box_broken
        self.box_frame_x, self.box_frame_y = 0, 2
        self.timer = 1
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        # 0: NULL
        # 1: red block
        # 2: yellow block
        # 3: box
        # 4: red house
        # 5: yellow house
        # 6: blue house
        # 7: tree
        # 8: bubble
        if self.box_color == 1:
            self.stage1_box2 = load_image('resource/vilige_Box_1_M1.png')
        elif self.box_color == 2:
            self.stage1_box3 = load_image('resource/vilige_Box_2_M1.png')
        elif self.box_color == 3:
            self.stage1_box1 = load_image('resource/vilige_Box_0_M1.png')
        elif self.box_color == 4:
            self.stage1_house1 = load_image('resource/vilige_House_0.png')
        elif self.box_color == 5:
            self.stage1_house2 = load_image('resource/vilige_House_1.png')
        elif self.box_color == 6:
            self.stage1_house3 = load_image('resource/vilige_House_2.png')
        elif self.box_color == 7:
            self.stage1_tree = load_image('resource/vilige_Tree.png')

    def add_event(self, event):
        self.event_que.insert(0, event)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)