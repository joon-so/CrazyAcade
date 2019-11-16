from pico2d import *
import game_world
import game_framework
import stage1_state
import stage2_state
import boss_stage
import bazzi

# Bubble Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

POP_TIMER = range(1)

def collide(left_a, bottom_a, right_a, top_a, b):
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


class IdleState():
    @staticmethod
    def enter(bubble, event):
        pass

    @staticmethod
    def exit(bubble, event):
        pass

    @staticmethod
    def do(bubble):
        # 겹칠시 터짐
        # for bub in game_world.objects[2]:
        #     if collide(bubble, bub):
        #         if bub != bubble:
        #             bub.add_event(POP_TIMER)

        bubble.frame = (bubble.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        bubble.timer -= game_framework.frame_time * 12
        if bubble.timer <= 0:
            bazzi.Bazzi.bubble_limit += 1
            bubble.add_event(POP_TIMER)

    @staticmethod
    def draw(bubble):
        bubble.image.clip_draw(int(bubble.frame) * 40, 0, 40, 40, bubble.x, bubble.y - 7)
    pass


class PopState():
    @staticmethod
    def enter(bubble, event):
        bubble.timer = 8
        pass

    @staticmethod
    def exit(bubble, event):
        pass

    @staticmethod
    def do(bubble):
        bubble.timer -= game_framework.frame_time * 15
        if bubble.timer < 4:
            bubble.frame = (bubble.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            bubble.frame = 0
        if bubble.timer <= 1:
            game_world.remove_object(bubble)

    @staticmethod
    def draw(bubble):
        bubble.pop_image.clip_draw(int(bubble.frame) * 40, 320, 40, 40, bubble.x, bubble.y - 7)
        # Delete Enemy
        for enemy in game_world.objects[2]:
            if collide(bubble.x - 20.1, bubble.y - 28, bubble.x + 20.1, bubble.y + 12, enemy):
                game_world.remove_object(enemy)
                break
        for bazzi_check in game_world.objects[3]:
            if collide(bubble.x - 20.1, bubble.y - 28, bubble.x + 20.1, bubble.y + 12, bazzi_check):
                bazzi.Bazzi.in_bubble = 1
                break

        # bubble bomb range check
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
                                if stage1_state.block[i - j - 1].box_color == 1 or stage1_state.block[i - j - 1].box_color == 2 \
                                        or stage1_state.block[i - j - 1].box_color == 3 or stage1_state.block[i - j - 1].box_color == 4\
                                        or stage1_state.block[i - j - 1].box_color == 5 or stage1_state.block[i - j - 1].box_color == 6\
                                        or stage1_state.block[i - j - 1].box_color == 7:
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
                                if stage1_state.block[i + j + 1].box_color == 1 or stage1_state.block[i + j + 1].box_color == 2 \
                                        or stage1_state.block[i + j + 1].box_color == 3 or stage1_state.block[i + j + 1].box_color == 4\
                                        or stage1_state.block[i + j + 1].box_color == 5 or stage1_state.block[i + j + 1].box_color == 6\
                                        or stage1_state.block[i + j + 1].box_color == 7:
                                    if stage1_state.block[i + j + 1].box_color == 1 or stage1_state.block[i + j + 1].box_color == 2 \
                                            or stage1_state.block[i + j + 1].box_color == 3:
                                        stage1_state.block[i + j + 1].box_broken = 0
                                    bubble.range_right = j
                                    break

                        for j in range(bubble.range_down):
                            if i + 15 * (j + 1) < 195:
                                if stage1_state.block[i + 15 * (j + 1)].box_color == 1 or stage1_state.block[i + 15 * (j + 1)].box_color == 2 \
                                        or stage1_state.block[i + 15 * (j + 1)].box_color == 3 or stage1_state.block[i + 15 * (j + 1)].box_color == 4 \
                                        or stage1_state.block[i + 15 * (j + 1)].box_color == 5 or stage1_state.block[i + 15 * (j + 1)].box_color == 6 \
                                        or stage1_state.block[i + 15 * (j + 1)].box_color == 7:
                                    if stage1_state.block[i + 15 * (j + 1)].box_color == 1 or stage1_state.block[i + 15 * (j + 1)].box_color == 2 \
                                            or stage1_state.block[i + 15 * (j + 1)].box_color == 3:
                                        stage1_state.block[i + 15 * (j + 1)].box_broken = 0
                                    bubble.range_down = j
                                    break
                            else:
                                bubble.range_down = j
                                break

                        for j in range(bubble.range_up):
                            if i - 15 * (j + 1) >= 0:
                                if stage1_state.block[i - 15 * (j + 1)].box_color == 1 or stage1_state.block[i - 15 * (j + 1)].box_color == 2 \
                                        or stage1_state.block[i - 15 * (j + 1)].box_color == 3 or stage1_state.block[i - 15 * (j + 1)].box_color == 4 \
                                        or stage1_state.block[i - 15 * (j + 1)].box_color == 5 or stage1_state.block[i - 15 * (j + 1)].box_color == 6 \
                                        or stage1_state.block[i - 15 * (j + 1)].box_color == 7:
                                    if stage1_state.block[i - 15 * (j + 1)].box_color == 1 or stage1_state.block[i - 15 * (j + 1)].box_color == 2 \
                                            or stage1_state.block[i - 15 * (j + 1)].box_color == 3:
                                        stage1_state.block[i - 15 * (j + 1)].box_broken = 0
                                    bubble.range_up = j
                                    break
                            else:
                                bubble.range_up = j
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
                                if stage2_state.block[i - j - 1].box_color == 1 or stage2_state.block[i - j - 1].box_color == 2 \
                                        or stage2_state.block[i - j - 1].box_color == 3 or stage2_state.block[i - j - 1].box_color == 4\
                                        or stage2_state.block[i - j - 1].box_color == 5:
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
                                if stage2_state.block[i + j + 1].box_color == 1 or stage2_state.block[i + j + 1].box_color == 2 \
                                        or stage2_state.block[i + j + 1].box_color == 3 or stage2_state.block[i + j + 1].box_color == 4\
                                        or stage2_state.block[i + j + 1].box_color == 5:
                                    if stage2_state.block[i + j + 1].box_color == 1 or stage2_state.block[i + j + 1].box_color == 2 \
                                            or stage2_state.block[i + j + 1].box_color == 3:
                                        stage2_state.block[i + j + 1].box_broken = 0
                                    bubble.range_right = j
                                    break

                        for j in range(bubble.range_down):
                            if i + 15 * (j + 1) < 195:
                                if stage2_state.block[i + 15 * (j + 1)].box_color == 1 or stage2_state.block[i + 15 * (j + 1)].box_color == 2 \
                                        or stage2_state.block[i + 15 * (j + 1)].box_color == 3 or stage2_state.block[i + 15 * (j + 1)].box_color == 4 \
                                        or stage2_state.block[i + 15 * (j + 1)].box_color == 5:
                                    if stage2_state.block[i + 15 * (j + 1)].box_color == 1 or stage2_state.block[i + 15 * (j + 1)].box_color == 2 \
                                            or stage2_state.block[i + 15 * (j + 1)].box_color == 3:
                                        stage2_state.block[i + 15 * (j + 1)].box_broken = 0
                                    bubble.range_down = j
                                    break
                            else:
                                bubble.range_down = j
                                break

                        for j in range(bubble.range_up):
                            if i - 15 * (j + 1) >= 0:
                                if stage2_state.block[i - 15 * (j + 1)].box_color == 1 or stage2_state.block[i - 15 * (j + 1)].box_color == 2 \
                                        or stage2_state.block[i - 15 * (j + 1)].box_color == 3 or stage2_state.block[i - 15 * (j + 1)].box_color == 4 \
                                        or stage2_state.block[i - 15 * (j + 1)].box_color == 5:
                                    if stage2_state.block[i - 15 * (j + 1)].box_color == 1 or stage2_state.block[i - 15 * (j + 1)].box_color == 2 \
                                            or stage2_state.block[i - 15 * (j + 1)].box_color == 3:
                                        stage2_state.block[i - 15 * (j + 1)].box_broken = 0
                                    bubble.range_up = j
                                    break
                            else:
                                bubble.range_up = j
                                break

                        break

        elif bubble.stage == 3:
            for i in range(195):
                if boss_stage.block[i].block_x <= bubble.x < boss_stage.block[i].block_x + 40.2:
                    if boss_stage.block[i].block_y <= bubble.y < boss_stage.block[i].block_y + 40:
                        for j in range(bubble.range_left):
                            if (i - j - 1) == -1 or i % 15 == 0:
                                bubble.range_left = 0
                                break
                            elif ((i - j - 1) % 15) - 14 == 0:
                                bubble.range_left = j
                                break
                            else:
                                if boss_stage.block[i - j - 1].box_color != 0:
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
                                if boss_stage.block[i + j + 1].box_color != 0:
                                    bubble.range_right = j
                                    break

                        for j in range(bubble.range_down):
                            if i + 15 * (j + 1) < 195:
                                if boss_stage.block[i + 15 * (j + 1)].box_color != 0:
                                    bubble.range_down = j
                                    break
                            else:
                                bubble.range_down = j
                                break

                        for j in range(bubble.range_up):
                            if i - 15 * (j + 1) >= 0:
                                if boss_stage.block[i - 15 * (j + 1)].box_color != 0:
                                    bubble.range_up = j
                                    break
                            else:
                                bubble.range_up = j
                                break

                        break

        # Bomb animation
        for i in range(bubble.range_left):
            if i == bubble.range_left - 1:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 160, 40, 40, bubble.x - 40.2 * (i + 1), bubble.y - 7)
                # Delete Enemy
                for enemy in game_world.objects[2]:
                    if collide(bubble.x - 40.2 * (bubble.range_left + 1) + 20.1, bubble.y - 28, bubble.x - 20.1, bubble.y + 12, enemy):
                        game_world.remove_object(enemy)
                        break
                for bazzi_check in game_world.objects[3]:
                    if collide(bubble.x - 40.2 * (bubble.range_left + 1) + 20.1, bubble.y - 28, bubble.x - 20.1, bubble.y + 12, bazzi_check):
                        bazzi.Bazzi.in_bubble = 1
                        break
            else:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 0, 40, 40, bubble.x - 40.2 * (i + 1), bubble.y - 7)

        for i in range(bubble.range_right):
            if i == bubble.range_right - 1:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 200, 40, 40, bubble.x + 40.2 * (i + 1), bubble.y - 7)
                # Delete Enemy
                for enemy in game_world.objects[2]:
                    if collide(bubble.x + 20.1, bubble.y - 28, bubble.x + 40.2 * (bubble.range_right + 1) - 20.1, bubble.y + 12, enemy):
                        game_world.remove_object(enemy)
                        break
                for bazzi_check in game_world.objects[3]:
                    if collide(bubble.x + 20.1, bubble.y - 28, bubble.x + 40.2 * (bubble.range_right + 1) - 20.1, bubble.y + 12, bazzi_check):
                        bazzi.Bazzi.in_bubble = 1
                        break
            else:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 40, 40, 40, bubble.x + 40.2 * (i + 1), bubble.y - 7)

        for i in range(bubble.range_down):
            if i == bubble.range_down - 1:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 240, 40, 40, bubble.x, bubble.y - 7 - 40 * (i + 1))
                # Delete Enemy
                for enemy in game_world.objects[2]:
                    if collide(bubble.x - 20.1, bubble.y - 7 - 40 * (bubble.range_down + 1) + 20, bubble.x + 20.1, bubble.y - 28, enemy):
                        game_world.remove_object(enemy)
                        break
                for bazzi_check in game_world.objects[3]:
                    if collide(bubble.x - 20.1, bubble.y - 7 - 40 * (bubble.range_down + 1) + 20, bubble.x + 20.1, bubble.y - 28, bazzi_check):
                        bazzi.Bazzi.in_bubble = 1
                        break
            else:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 80, 40, 40, bubble.x, bubble.y - 7 - 40 * (i + 1))

        for i in range(bubble.range_up):
            if i == bubble.range_up - 1:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 280, 40, 40, bubble.x, bubble.y - 7 + 40 * (i + 1))
                # Delete Enemy
                for enemy in game_world.objects[2]:
                    if collide(bubble.x - 20.1, bubble.y + 12, bubble.x + 20.1, bubble.y - 7 + 40 * (bubble.range_up + 1) - 20, enemy):
                        game_world.remove_object(enemy)
                        break
                for bazzi_check in game_world.objects[3]:
                    if collide(bubble.x - 20.1, bubble.y + 12, bubble.x + 20.1, bubble.y - 7 + 40 * (bubble.range_up + 1) - 20, bazzi_check):
                        bazzi.Bazzi.in_bubble = 1
                        break
            else:
                bubble.pop_image.clip_draw(int(bubble.frame) * 40, 120, 40, 40, bubble.x, bubble.y - 7 + 40 * (i + 1))


next_state_table = {
    IdleState: {POP_TIMER: PopState}
}


class Bubble:
    image = None
    pop_image = None
    def __init__(self, x = 9999, y = 9999, bubble_range = 0, stage = 0):
        self.timer = 15
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