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
    global stage1_tree_state, stage1_tree_x, stage1_tree_y
    global stage1, stage1_box1, stage1_box2, stage1_box3, stage1_tree
    global stage1_house1, stage1_house2, stage1_house3
    clear_canvas()

    stage1.draw(WIDTH // 2, HEIGHT // 2)
    for n in range(16):
        stage1_tree.draw(stage1_tree_x[n], stage1_tree_y[n])

    update_canvas()
    pass


open_canvas(WIDTH, HEIGHT)

menu = load_image('Main.png')
Help = load_image('Help_key.png')
stage1 = load_image('Stage1.png')
stage2 = load_image('Stage2.png')
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
dir = 0

tree_x, tree_y = 0, 0
stage1_tree_state = []
stage1_tree_x = []
stage1_tree_y = []
for i in range(16):
    if i <= 5:
        tree_x += 80.4
        if i == 3:
            tree_x = 441.4
        if i == 0:
            tree_x, tree_y = 40, 315
    elif 5 < i <= 10:
        if i == 6:
            tree_x = 241
            tree_y = 595
        elif i == 9:
            tree_x = 401.8
            tree_y = 595
        tree_y -= 80
    elif 10 < i <= 16:
        if i == 11:
            tree_x = 241
            tree_y = 275
        elif i == 13:
            tree_x = 401.8
            tree_y = 355
        tree_y -= 80
    stage1_tree_state.append(1)
    stage1_tree_x.append(tree_x)
    stage1_tree_y.append(tree_y)

block_x, block_y = 0, 0
stage1_block_state = []
stage1_block_x = []
stage1_block_y = []
for i in range(112):
    stage1_block_state.append(0)
    stage1_block_x.append(block_x)
    stage1_block_y.append(block_y)

while running:

    if stage == 0:
        menu.draw(WIDTH // 2, HEIGHT // 2)
    # bazzi.clip_draw(bazzi_frame_x * 100, bazzi_frame_y * 119, 60, 60, bazzi_x, 90)
    elif stage == 1:
        make_stage1()
    elif stage == 2:
        stage2.draw(WIDTH // 2, HEIGHT // 2)

    handle_events()
    # frame = (frame + 1) % 8
    # bazzi_x += dir * 15

    delay(0.02)

close_canvas()
