from pico2d import *
import random

WIDTH, HEIGHT = 800, 600


class Bazzi:
    global bazzi_dir
    global bazzi_running
    global bazzi_dir_x, bazzi_dir_y

    def __init__(self):
        self.x, self.y = 400, 400
        self.frame_x, self.frame_y = 0, 0
        self.image = load_image('Character1_edit.png')

    def update(self):
        if bazzi_dir == 1:
            self.frame_x = (self.frame_x + 1) % 4
            self.frame_y = 350
        elif bazzi_dir == 2:
            self.frame_x = (self.frame_x + 1) % 4
            self.frame_y = 280
        elif bazzi_dir == 3:
            self.frame_x = (self.frame_x + 1) % 5
            self.frame_y = 490
        elif bazzi_dir == 4:
            self.frame_x = (self.frame_x + 1) % 5
            self.frame_y = 420

        self.x += bazzi_dir_x * 8
        self.y += bazzi_dir_y * 8

    def draw(self):
        self.image.clip_draw(self.frame_x * 70, self.frame_y, 70, 70, self.x, self.y)


class Bubble:
    def __init__(self):
        self.time, self.state = 0, 0
        self.frame = 0
        self.x, self.y = 9999, 9999
        self.image = load_image('Bubble.png')

    def update(self):
        if self.state == 1:
            #if self.state == 2000:
                #self.frame = (self.frame + 1) % 3
            self.time += 1
        if self.time == 10000:
            self.state = 2

    def draw(self):
        self.image.clip_draw(self.frame * 50, 0, 40, 40, self.x, self.y + 5)


def handle_events():
    global running
    global bazzi_dir, bazzi_dir_x, bazzi_dir_y
    global bazzi_running
    global stage
    global bazzi

    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_0:
                stage = 0
            elif event.key == SDLK_1:
                stage = 1
            elif event.key == SDLK_2:
                stage = 2
            elif event.key == SDLK_3:
                stage = 3

            elif event.key == SDLK_RIGHT:
                bazzi_dir = 1
                bazzi_dir_x += 1
            elif event.key == SDLK_LEFT:
                bazzi_dir = 2
                bazzi_dir_x -= 1
            elif event.key == SDLK_UP:
                bazzi_dir = 3
                bazzi_dir_y += 1
            elif event.key == SDLK_DOWN:
                bazzi_dir = 4
                bazzi_dir_y -= 1

            elif event.key == SDLK_k:
                makeBubble(bazzi.x, bazzi.y)

            elif event.key == SDLK_ESCAPE:
                running = False

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                bazzi_dir_x -= 1
            elif event.key == SDLK_LEFT:
                bazzi_dir_x += 1
            elif event.key == SDLK_UP:
                bazzi_dir_y -= 1
            elif event.key == SDLK_DOWN:
                bazzi_dir_y += 1
            bazzi_dir = 0
    pass


def makeBubble(x, y):
    global stage2_block_state, stage2_block_x, stage2_block_y
    global stage1_block_state, stage1_block_x, stage1_block_y
    global stage
    global bubble_team

    if stage == 1:
        for i in range(195):
            if stage1_block_x[i] <= x < stage1_block_x[i] + 40.2:
                if stage1_block_y[i] <= y < stage1_block_y[i] + 40:
                    if stage1_block_state[i] == 0:
                        stage1_block_state[i] = 8
                        for k in range(100):
                            if bubble_team[k].state == 0:
                                bubble_team[k].state = 1
                                bubble_team[k].x = stage1_block_x[i]
                                bubble_team[k].y = stage1_block_y[i]
                                break
                    else:
                        break

    else:
        for i in range(195):
            if stage2_block_x[i] <= x < stage2_block_x[i] + 40.2:
                if stage2_block_y[i] <= y < stage2_block_y[i] + 40:
                    if stage2_block_state[i] == 0:
                        stage2_block_state[i] = 8
                        for k in range(100):
                            if bubble_team[k].state == 0:
                                bubble_team[k].state = 1
                                bubble_team[k].x = stage2_block_x[i]
                                bubble_team[k].y = stage2_block_y[i]
                    else:
                        break


def make_menu():
    global menu, Help, game_start, out
    global game_frame
    clear_canvas()

    menu.draw(WIDTH // 2, HEIGHT // 2)
    game_start.clip_draw(game_frame * 192, 0, 192, 55, 400, 195)
    out.clip_draw(game_frame * 140, 0, 140, 55, 405, 145)
    game_frame = (game_frame + 1) % 2
    update_canvas()
    pass


def make_stage1():
    global stage1_block_state, stage1_block_x, stage1_block_y
    global stage1_map, stage1_box1, stage1_box2, stage1_box3, stage1_tree
    global stage1_house1, stage1_house2, stage1_house3
    global box_frame_x, box_frame_y
    global bazzi, bubble_team

    for bubble in bubble_team:
        bubble.update()
    bazzi.update()
    clear_canvas()

    stage1_map.draw(WIDTH // 2, HEIGHT // 2)
    # stage1_block_state
    # 0: NULL
    # 1: red block
    # 2: yellow block
    # 3: box
    # 4: red house
    # 5: yellow house
    # 6: blue house
    # 7: tree
    # 8: bubble
    # x 80.4 , y 81
    for n in range(195):
        if stage1_block_state[n] == 1:
            stage1_box2.clip_draw(box_frame_x * 40, box_frame_y * 45, 41, 45, stage1_block_x[n], stage1_block_y[n])
        elif stage1_block_state[n] == 2:
            stage1_box3.clip_draw(box_frame_x * 40, box_frame_y * 45, 41, 45, stage1_block_x[n], stage1_block_y[n])
        elif stage1_block_state[n] == 3:
            stage1_box1.clip_draw(box_frame_x * 40, box_frame_y * 45, 41, 45, stage1_block_x[n], stage1_block_y[n])
        elif stage1_block_state[n] == 4:
            stage1_house1.clip_draw(0, 0, 41, 57, stage1_block_x[n], stage1_block_y[n] + 7)
        elif stage1_block_state[n] == 5:
            stage1_house2.clip_draw(0, 0, 41, 57, stage1_block_x[n], stage1_block_y[n] + 7)
        elif stage1_block_state[n] == 6:
            stage1_house3.clip_draw(0, 0, 41, 57, stage1_block_x[n], stage1_block_y[n] + 7)
        elif stage1_block_state[n] == 7:
            stage1_tree.clip_draw(0, 0, 40, 70, stage1_block_x[n], stage1_block_y[n] + 12)

    for bubble in bubble_team:
        bubble.draw()
    bazzi.draw()

    update_canvas()
    pass


def make_stage2():
    global stage2_block_state, stage2_block_x, stage2_block_y
    global stage2_map, stage2_box1, stage2_box2, stage2_box3, stage2_box4, stage2_box5
    global box_frame_x, box_frame_y
    clear_canvas()

    stage2_map.draw(WIDTH // 2, HEIGHT // 2)
    # stage2_block_state
    # 0: NULL
    # 1: wood block
    # 2: block1
    # 3: block2
    # 4: no broken1
    # 5: no broken2
    # x 80.4 , y 81
    for n in range(195):
        if stage2_block_state[n] == 1:
            stage2_box1.clip_draw(box_frame_x * 40, box_frame_y * 45, 41, 45, stage2_block_x[n], stage2_block_y[n])
        elif stage2_block_state[n] == 2:
            stage2_box2.clip_draw(box_frame_x * 40, box_frame_y * 45, 41, 45, stage2_block_x[n], stage2_block_y[n])
        elif stage2_block_state[n] == 3:
            stage2_box3.clip_draw(box_frame_x * 40, box_frame_y * 45, 41, 45, stage2_block_x[n], stage2_block_y[n])
        elif stage2_block_state[n] == 4:
            stage2_box4.clip_draw(0, 0, 41, 57, stage2_block_x[n], stage2_block_y[n] + 7)
        elif stage2_block_state[n] == 5:
            stage2_box5.clip_draw(0, 0, 40, 70, stage2_block_x[n], stage2_block_y[n] + 15)
    update_canvas()
    pass


open_canvas(WIDTH, HEIGHT)

menu = load_image('Main.png')
Help = load_image('Help_key.png')
game_start = load_image('Game_start.png')
out = load_image('InGame_Button_Out.png')
game_frame = 0

stage1_map = load_image('Stage1.png')
stage1_box1 = load_image('vilige_Box_0_M1.png')
stage1_box2 = load_image('vilige_Box_1_M1.png')
stage1_box3 = load_image('vilige_Box_2_M1.png')
stage1_house1 = load_image('vilige_House_0.png')
stage1_house2 = load_image('vilige_House_1.png')
stage1_house3 = load_image('vilige_House_2.png')
stage1_tree = load_image('vilige_Tree.png')

stage2_map = load_image('Stage2.png')
stage2_box1 = load_image('pirate_Box_0.png')
stage2_box2 = load_image('pirate_Box_1.png')
stage2_box3 = load_image('pirate_Box_2.png')
stage2_box4 = load_image('pirate_Box_3.png')
stage2_box5 = load_image('pirate_Box_4.png')

running = True
stage = 2
bazzi = Bazzi()
bazzi_dir = 0
bazzi_dir_x = 0
bazzi_dir_y = 0
bazzi_running = False

bubble_team = [Bubble() for i in range(100)]

box_frame_x, box_frame_y = 0, 2

# x 80.4 , y 81
# x : left 39 ~ 601 right
# y : bottom 148 ~ 540 top

block_x, block_y = 39, 540
box_color = 0
box_broken = 0
stage1_block_state = []
stage1_block_broken = []
stage1_block_x = []
stage1_block_y = []
for n in range(195):
    if block_x > 610:
        block_y -= 40
        block_x = 39
    # red block
    if n == 2 or n == 4 or n == 11 or n == 25 or n == 33 or n == 56 or n == 58 or n == 60 \
            or n == 62 or n == 64 or n == 85 or n == 87 or n == 89 or n == 105 or n == 107 \
            or n == 109 or n == 115 or n == 117 or n == 119 or n == 131 or n == 133 or n == 136 or n == 138 \
            or n == 160 or n == 162 or n == 167 or n == 169 or n == 183 or n == 191:
        box_color = 1
        box_broken = 1
    # yellow block
    elif n == 1 or n == 3 or n == 26 or n == 32 or n == 34 or n == 55 or n == 57 or n == 59 \
            or n == 61 or n == 63 or n == 75 or n == 77 or n == 79 or n == 86 or n == 88 \
            or n == 106 or n == 108 or n == 130 or n == 132 or n == 134 or n == 135 or n == 137 \
            or n == 139 or n == 161 or n == 163 or n == 168 or n == 190 or n == 192:
        box_color = 2
        box_broken = 1
    # box
    elif n == 5 or n == 8 or n == 9 or n == 17 or n == 19 or n == 21 or n == 35 or n == 37 \
            or n == 38 or n == 39 or n == 41 or n == 43 or n == 45 or n == 47 or n == 49 \
            or n == 51 or n == 65 or n == 68 or n == 69 or n == 71 or n == 73 or n == 81 \
            or n == 82 or n == 91 or n == 93 or n == 95 or n == 98 or n == 99 or n == 101 \
            or n == 103 or n == 111 or n == 121 or n == 123 or n == 125 or n == 127 or n == 128 \
            or n == 129 or n == 141 or n == 145 or n == 147 or n == 149 or n == 153 or n == 155 \
            or n == 158 or n == 159 or n == 171 or n == 172 or n == 175 or n == 177 or n == 185 \
            or n == 188 or n == 189:
        box_color = 3
        box_broken = 1
    # red box
    elif n == 16 or n == 18 or n == 46 or n == 48 or n == 76 or n == 78 or n == 116 or n == 118 \
            or n == 146 or n == 148 or n == 176 or n == 178:
        box_color = 4
        box_broken = 1
    # yellow house
    elif n == 10 or n == 12 or n == 14 or n == 40 or n == 42 or n == 44 or n == 70 or n == 72 \
            or n == 74:
        box_color = 5
        box_broken = 1
    # blue house
    elif n == 120 or n == 122 or n == 124 or n == 150 or n == 152 or n == 154 or n == 180 \
            or n == 180 or n == 182 or n == 184:
        box_color = 6
        box_broken = 1
    # tree
    elif n == 20 or n == 24 or n == 50 or n == 54 or n == 80 or n == 90 or n == 92 or n == 94 \
            or n == 100 or n == 102 or n == 104 or n == 114 or n == 140 or n == 144 or n == 170 \
            or n == 174:
        box_color = 7
        box_broken = 1
    else:
        box_color = 0
        box_broken = 0
    stage1_block_state.append(box_color)
    stage1_block_broken.append(box_broken)
    stage1_block_x.append(block_x)
    stage1_block_y.append(block_y)
    block_x += 40.2

block_x, block_y = 39, 540
stage2_block_state = []
stage2_block_broken = []
stage2_block_x = []
stage2_block_y = []
for i in range(195):
    if block_x > 610:
        block_y -= 40
        block_x = 39
    # wood box
    if i == 19 or i == 20 or i == 21 or i == 23 or i == 24 or i == 25 or i == 33 or i == 37 or i == 41 \
            or i == 47 or i == 57 or i == 62 or i == 72 or i == 77 or i == 87 or i == 92 or i == 102 \
            or i == 108 or i == 116 or i == 124 or i == 130 or i == 140 or i == 144 or i == 156 or i == 157 \
            or i == 158:
        box_color = 1
        box_broken = 1
    # box1
    elif i == 0 or i == 1 or i == 2 or i == 3 or i == 7 or i == 11 or i == 12 or i == 13 or i == 14 \
            or i == 15 or i == 17 or i == 27 or i == 29 or i == 30 or i == 39 or i == 44 or i == 50 \
            or i == 54 or i == 59 or i == 60 or i == 64 or i == 71 or i == 74 or i == 80 or i == 85 \
            or i == 84 or i == 89 or i == 90 or i == 94 or i == 100 or i == 106 or i == 81 or i == 111 \
            or i == 113 or i == 118 or i == 121 or i == 127 or i == 132 or i == 134 or i == 135 or i == 136 \
            or i == 138 or i == 142 or i == 148 or i == 151 or i == 153 or i == 161 or i == 163 or i == 169 \
            or i == 170 or i == 176 or i == 179 or i == 183 or i == 184 or i == 186 or i == 189 or i == 191:
        box_color = 2
        box_broken = 1
    # box2
    elif i == 31 or i == 35 or i == 43 or i == 45 or i == 49 or i == 51 or i == 52 or i == 53 or i == 55 \
            or i == 63 or i == 65 or i == 66 or i == 67 or i == 68 or i == 69 or i == 70 or i == 75 \
            or i == 79 or i == 93 or i == 95 or i == 99 or i == 101 or i == 104 or i == 105 or i == 110 \
            or i == 83 or i == 114 or i == 119 or i == 120 or i == 122 or i == 126 or i == 128 or i == 133 \
            or i == 137 or i == 146 or i == 147 or i == 149 or i == 150 or i == 154 or i == 160 or i == 164 \
            or i == 165 or i == 168 or i == 174 or i == 175 or i == 180 or i == 185 or i == 187 or i == 188 \
            or i == 190 or i == 194:
        box_color = 3
        box_broken = 1
    # no broken1
    elif i == 82 or i == 96 or i == 97 or i == 98 or i == 112:
        box_color = 4
        box_broken = 1
    # no broken2
    elif i == 16 or i == 28 or i == 166 or i == 178:
        box_color = 5
        box_broken = 1
    else:
        box_color = 0
        box_broken = 0
    stage2_block_state.append(box_color)
    stage2_block_broken.append(box_broken)
    stage2_block_x.append(block_x)
    stage2_block_y.append(block_y)
    block_x += 40.2

while running:
    if stage == 0:
        make_menu()
        delay(0.2)
    elif stage == 1:
        make_stage1()
        delay(0.01)
    elif stage == 2:
        make_stage2()
        delay(0.01)

    handle_events()

close_canvas()
