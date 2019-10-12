from pico2d import *

WIDTH, HEIGHT = 800, 600


def handle_events():
    global running
    global dir
    global frame
    global bazzi_frame_y
    global bazzi_frame_x
    global stage
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
                dir += 1
                bazzi_frame_y = 3
                bazzi_frame_x = (bazzi_frame_x + 1) % 4

            elif event.key == SDLK_LEFT:
                dir -= 1
                bazzi_frame_y = 2
                bazzi_frame_x = (bazzi_frame_x + 1) % 4

            elif event.key == SDLK_ESCAPE:
                running = False

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1
    pass


def make_stage1():
    global stage1_block_state, stage1_block_x, stage1_block_y
    #global stage1_tree_state, stage1_tree_x, stage1_tree_y
    #global stage1_house_state, stage1_house_x, stage1_house_y
    global stage1_map, stage1_box1, stage1_box2, stage1_box3, stage1_tree
    global stage1_house1, stage1_house2, stage1_house3
    global box_frame_x, box_frame_y
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
    update_canvas()
    pass


open_canvas(WIDTH, HEIGHT)

menu = load_image('Main.png')
Help = load_image('Help_key.png')
stage1_map = load_image('Stage1.png')
stage2_map = load_image('Stage2.png')
stage1_box1 = load_image('vilige_Box_0_M1.png')
stage1_box2 = load_image('vilige_Box_1_M1.png')
stage1_box3 = load_image('vilige_Box_2_M1.png')
stage1_house1 = load_image('vilige_House_0.png')
stage1_house2 = load_image('vilige_House_1.png')
stage1_house3 = load_image('vilige_House_2.png')
stage1_tree = load_image('vilige_Tree.png')
bazzi = load_image('Character1_edit.png')

running = True
stage = 1
bazzi_x = 800 // 2
bazzi_frame_y = 2
bazzi_frame_x = 0
box_frame_x, box_frame_y = 0, 2
dir = 0


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
    #red block
    if n == 2 or n == 4 or n == 11 or n == 25 or n == 33 or n == 56 or n == 58 or n == 60\
            or n == 62 or n == 64 or n == 85 or n == 87 or n == 89 or n == 105 or n == 107\
            or n == 109 or n == 115 or n == 117 or n == 119 or n == 131 or n == 133or n == 136 or n == 138\
            or n == 160 or n == 162 or n == 167 or n == 169 or n == 183 or n == 191:
        box_color = 1
        box_broken = 1
    #yellow block
    elif n == 1 or n == 3 or n == 26 or n == 32 or n == 34 or n == 55 or n == 57 or n == 59\
            or n == 61 or n == 63 or n == 75 or n == 77 or n == 79 or n == 86 or n == 88 \
            or n == 106 or n == 108 or n == 130 or n == 132 or n == 134 or n == 135 or n == 137 \
            or n == 139 or n == 161 or n == 163 or n == 168 or n == 190 or n == 192:
        box_color = 2
        box_broken = 1
    #box
    elif n == 5 or n == 8 or n == 9 or n == 17 or n == 19 or n == 21 or n == 35 or n == 37\
            or n == 38 or n == 39 or n == 41 or n == 43 or n == 45 or n == 47 or n == 49\
            or n == 51 or n == 65 or n == 68 or n == 69 or n == 71 or n == 73 or n == 81\
            or n == 82 or n == 91 or n == 93 or n == 95 or n == 98 or n == 99 or n == 101 \
            or n == 103 or n == 111 or n == 121 or n == 123 or n == 125 or n == 127 or n == 128\
            or n == 129 or n == 141 or n == 145 or n == 147 or n == 149 or n == 153 or n == 155 \
            or n == 158 or n == 159 or n == 171 or n == 172 or n == 175 or n == 177 or n == 185 \
            or n == 188 or n == 189:
        box_color = 3
        box_broken = 1
    #red box
    elif n == 16 or n == 18 or n == 46 or n == 48 or n == 76 or n == 78 or n == 116 or n == 118\
            or n == 146 or n == 148 or n == 176 or n == 178:
        box_color = 4
        box_broken = 1
    #yellow house
    elif n == 10 or n == 12 or n == 14 or n == 40 or n == 42 or n == 44 or n == 70 or n == 72\
            or n == 74:
        box_color = 5
        box_broken = 1
    #blue house
    elif n == 120 or n == 122 or n == 124 or n == 150 or n == 152 or n == 154 or n == 180 \
            or n == 180 or n == 182 or n == 184:
        box_color = 6
        box_broken = 1
    #tree
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

while running:

    if stage == 0:
        menu.draw(WIDTH // 2, HEIGHT // 2)
    # bazzi.clip_draw(bazzi_frame_x * 100, bazzi_frame_y * 119, 60, 60, bazzi_x, 90)
    elif stage == 1:
        make_stage1()
    elif stage == 2:
        stage2_map.draw(WIDTH // 2, HEIGHT // 2)

    handle_events()
    # frame = (frame + 1) % 8
    # bazzi_x += dir * 15

    delay(0.02)

close_canvas()
