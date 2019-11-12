from pico2d import *
import game_world
import stage1_state
import stage2_state
import boss_stage
import bazzi

POP_TIMER = range(1)


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
            #game_world.remove_object(bubble)
            print('Pop Bubble')
            bubble.add_event(POP_TIMER)

    @staticmethod
    def draw(bubble):
        bubble.image.clip_draw(bubble.frame * 40, 0, 40, 40, bubble.x, bubble.y - 7)
    pass


class PopState():
    @staticmethod
    def enter(bubble, event):
        bubble.timer = 15
        print('Pop')
        pass

    @staticmethod
    def exit(bubble, event):
        pass

    @staticmethod
    def do(bubble):
        bubble.timer -= 1
        if bubble.timer < 4:
            bubble.frame = (bubble.frame + 1) % 4
        else:
            bubble.frame = 0
        if bubble.timer == 0:
            game_world.remove_object(bubble)
            print('Delete Bubble')
        # bubble.frame = (bubble.frame + 1) % 4
        # bubble.timer -= 1
        # if bubble.timer == 0:
        #     game_world.remove_object(bubble)
        #     print('Delete Bubble')

    @staticmethod
    def draw(bubble):
        bubble.pop_image.clip_draw(bubble.frame * 40, 320, 40, 40, bubble.x, bubble.y - 7)
        if bubble.stage == 1:
            for i in range(195):
                if stage1_state.block[i].block_x <= bubble.x < stage1_state.block[i].block_x + 40.2:
                    if stage1_state.block[i].block_y <= bubble.y < stage1_state.block[i].block_y + 40:
                        for j in range(bubble.range_left):
                            if (i - j - 1) == -1 or i % 15 == 0:
                                bubble.range_left = 0
                                break
                            elif ((i - j - 1) % 15) - 14 == 0:
                                bubble.range_left = j
                                break
                            else:
                                if stage1_state.block[i - j - 1].box_color != 0:
                                    if stage1_state.block[i - j - 1].box_color == 1 or stage1_state.block[i - j - 1].box_color == 2 \
                                            or stage1_state.block[i - j - 1].box_color == 3:
                                        stage1_state.block[i - j - 1].box_broken = 0
                                    bubble.range_left = j
                                    break

                        for j in range(bubble.range_right):
                            if (i + j + 1) >= 195 or i % 15 - 14 == 0:
                                bubble.range_right = 0
                                break
                            elif (i + j + 1) % 15 == 0:
                                bubble.range_right = j
                                break
                            else:
                                if stage1_state.block[i + j + 1].box_color != 0:
                                    if stage1_state.block[i + j + 1].box_color == 1 or stage1_state.block[i + j + 1].box_color == 2 \
                                            or stage1_state.block[i + j + 1].box_color == 3:
                                        stage1_state.block[i + j + 1].box_broken = 0
                                    bubble.range_right = j
                                    break

                        for j in range(bubble.range_down):
                            if i + 15 * (j + 1) <= 195:
                                if stage1_state.block[i + 15 * (j + 1)].box_color != 0:
                                    if stage1_state.block[i + 15 * (j + 1)].box_color == 1 or stage1_state.block[i + 15 * (j + 1)].box_color == 2 \
                                            or stage1_state.block[i + 15 * (j + 1)].box_color == 3:
                                        stage1_state.block[i + 15 * (j + 1)].box_broken = 0
                                    bubble.range_down = j
                                    break
                            else:
                                bubble.range_down = 0
                                break

                        for j in range(bubble.range_up):
                            if i - 15 * (j + 1) >= 0:
                                if stage1_state.block[i - 15 * (j + 1)].box_color != 0:
                                    if stage1_state.block[i - 15 * (j + 1)].box_color == 1 or stage1_state.block[i - 15 * (j + 1)].box_color == 2 \
                                            or stage1_state.block[i - 15 * (j + 1)].box_color == 3:
                                        stage1_state.block[i - 15 * (j + 1)].box_broken = 0
                                    bubble.range_up = j
                                    break
                            else:
                                bubble.range_up = 0
                                break

                        break

        elif bubble.stage == 2:
            for i in range(195):
                if stage2_state.block[i].block_x <= bubble.x < stage2_state.block[i].block_x + 40.2:
                    if stage2_state.block[i].block_y <= bubble.y < stage2_state.block[i].block_y + 40:
                        for j in range(bubble.range_left):
                            if (i - j - 1) == -1 or i % 15 == 0:
                                bubble.range_left = 0
                                break
                            elif ((i - j - 1) % 15) - 14 == 0:
                                bubble.range_left = j
                                break
                            else:
                                if stage2_state.block[i - j - 1].box_color != 0:
                                    if stage2_state.block[i - j - 1].box_color == 1 or stage2_state.block[i - j - 1].box_color == 2 \
                                            or stage2_state.block[i - j - 1].box_color == 3:
                                        stage2_state.block[i - j - 1].box_broken = 0
                                    bubble.range_left = j
                                    break

                        for j in range(bubble.range_right):
                            if (i + j + 1) >= 195 or i % 15 - 14 == 0:
                                bubble.range_right = 0
                                break
                            elif (i + j + 1) % 15 == 0:
                                bubble.range_right = j
                                break
                            else:
                                if stage2_state.block[i + j + 1].box_color != 0:
                                    if stage2_state.block[i + j + 1].box_color == 1 or stage2_state.block[i + j + 1].box_color == 2 \
                                            or stage2_state.block[i + j + 1].box_color == 3:
                                        stage2_state.block[i + j + 1].box_broken = 0
                                    bubble.range_right = j
                                    break

                        for j in range(bubble.range_down):
                            if i + 15 * (j + 1) <= 195:
                                if stage2_state.block[i + 15 * (j + 1)].box_color != 0:
                                    if stage2_state.block[i + 15 * (j + 1)].box_color == 1 or stage2_state.block[i + 15 * (j + 1)].box_color == 2 \
                                            or stage2_state.block[i + 15 * (j + 1)].box_color == 3:
                                        stage2_state.block[i + 15 * (j + 1)].box_broken = 0
                                    bubble.range_down = j
                                    break
                            else:
                                bubble.range_down = 0
                                break

                        for j in range(bubble.range_up):
                            if i - 15 * (j + 1) >= 0:
                                if stage2_state.block[i - 15 * (j + 1)].box_color != 0:
                                    if stage2_state.block[i - 15 * (j + 1)].box_color == 1 or stage2_state.block[i - 15 * (j + 1)].box_color == 2 \
                                            or stage2_state.block[i - 15 * (j + 1)].box_color == 3:
                                        stage2_state.block[i - 15 * (j + 1)].box_broken = 0
                                    bubble.range_up = j
                                    break
                            else:
                                bubble.range_up = 0
                                break

                        break

        for i in range(bubble.range_left):
            if i == bubble.range_left - 1:
                bubble.pop_image.clip_draw(bubble.frame * 40, 160, 40, 40, bubble.x - 40.2 * (i + 1), bubble.y - 7)
            else:
                bubble.pop_image.clip_draw(bubble.frame * 40, 0, 40, 40, bubble.x - 40.2 * (i + 1), bubble.y - 7)

        for i in range(bubble.range_right):
            if i == bubble.range_right - 1:
                bubble.pop_image.clip_draw(bubble.frame * 40, 200, 40, 40, bubble.x + 40.2 * (i + 1), bubble.y - 7)
            else:
                bubble.pop_image.clip_draw(bubble.frame * 40, 40, 40, 40, bubble.x + 40.2 * (i + 1), bubble.y - 7)

        for i in range(bubble.range_down):
            if i == bubble.range_down - 1:
                bubble.pop_image.clip_draw(bubble.frame * 40, 240, 40, 40, bubble.x, bubble.y - 7 - 40 * (i + 1))
            else:
                bubble.pop_image.clip_draw(bubble.frame * 40, 80, 40, 40, bubble.x, bubble.y - 7 - 40 * (i + 1))

        for i in range(bubble.range_up):
            if i == bubble.range_up - 1:
                bubble.pop_image.clip_draw(bubble.frame * 40, 280, 40, 40, bubble.x, bubble.y - 7 + 40 * (i + 1))
            else:
                bubble.pop_image.clip_draw(bubble.frame * 40, 120, 40, 40, bubble.x, bubble.y - 7 + 40 * (i + 1))
    pass


next_state_table = {
    IdleState: {POP_TIMER: PopState}
}


class Bubble:
    image = None
    pop_image = None
    def __init__(self, x = 9999, y = 9999, bubble_range = 0, stage = 0):
        self.timer = 30
        self.frame = 0
        self.range_right, self.range_left, self.range_up, self.range_down = bubble_range, bubble_range, bubble_range, bubble_range
        self.x, self.y = x, y
        self.stage = stage
        self.cur_state = IdleState
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        if Bubble.image == None:
            Bubble.image = load_image('resource/Bubble.png')
            Bubble.pop_image = load_image('resource/BubbleFlow.png')

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
        #bubble delete