import game_framework
from pico2d import *

WIDTH, HEIGHT = 800, 600
stage2_map = None
stage2_box4 = None
stage2_box5 = None


running = True
bazzi = None
bazzi_dir = 0
bazzi_dir_x = 0
bazzi_dir_y = 0
bazzi_running = False

monster = None
bubble_team = None

box_frame_x, box_frame_y = 0, 2

# x 80.4 , y 81
# x : left 39 ~ 601 right
# y : bottom 148 ~ 540 top
block_x, block_y = 39, 540
stage2_block_state = []
stage2_block_broken = []
stage2_block_x = []
stage2_block_y = []

class Bazzi:
    global bazzi_dir
    global bazzi_running
    global bazzi_dir_x, bazzi_dir_y

    def __init__(self):
        self.x, self.y = 400, 400
        self.frame_x, self.frame_y = 0, 420
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


class Monster:
    def __init__(self):
        self.x, self.y = 180, 500
        self.frame_x, self.frame_y = 0, 0
        self.dir = 1
        self.timer = 0
        self.image = load_image('Monster_Boss.png')

    def update(self):
        self.timer += 1
        if self.timer == 2:
            if self.dir == 1:
                self.frame_y = 2484
                self.y += 1
            elif self.dir == 2:
                self.frame_y = 2277
                self.y -= 1
            elif self.dir == 3:
                self.frame_y = 2070
                self.x += 1
            elif self.dir == 4:
                self.frame_y = 1863
                self.x -= 1

            self.frame_x = (self.frame_x + 1) % 6
            self.timer = 0

    def draw(self):
        self.image.clip_draw(self.frame_x * 120, self.frame_y, 120, 207, self.x, self.y)


class Bubble:
    image = None
    def __init__(self):
        self.time, self.state = 0, 0
        self.frame = 0
        self.x, self.y = 9999, 9999
        if Bubble.image == None:
            Bubble.image = load_image('Bubble.png')

    def update(self):
        if self.state == 1:
            #if self.time == 100:
            self.frame = (self.frame + 1) % 4
            self.time += 1
        if self.time == 10000:
            self.state = 2

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 40, self.x, self.y + 5)


def enter():
    global stage2_map, stage2_box4, stage2_box5
    global bazzi, bubble_team, monster
    global block_y, block_x, stage2_block_state, stage2_block_broken, stage2_block_x, stage2_block_y

    stage2_map = load_image('stage2.png')
    stage2_box4 = load_image('pirate_Box_3.png')
    stage2_box5 = load_image('pirate_Box_4.png')
    bazzi = Bazzi()

    bubble_team = [Bubble() for i in range(195)]
    monster = Monster()
    monster.dir = 2

    for i in range(195):
        if block_x > 610:
            block_y -= 40
            block_x = 39
        # no broken1
        if i == 67 or i == 81 or i == 82 or i == 83 or i == 97:
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
    pass


def exit():
    global stage2_map, stage2_box4, stage2_box5
    global bazzi, bubble_team, monster
    global block_y, block_x, stage2_block_state, stage2_block_broken, stage2_block_x, stage2_block_y

    del(stage2_map)
    del(stage2_box4)
    del(stage2_box5)
    del(bazzi)
    del(bubble_team)
    del(monster)
    del(block_x)
    del(block_y)
    del(stage2_block_state)
    del(stage2_block_broken)
    del(stage2_block_x)
    del(stage2_block_y)
    pass


def update():
    global bazzi, bubble_team, monster

    for bubble in bubble_team:
        bubble.update()
    monster.update()
    bazzi.update()
    delay(0.008)
    pass


def draw():
    global stage2_map, stage2_box4, stage2_box5
    global bazzi, bubble_team, monster
    global block_y, block_x, stage2_block_state, stage2_block_broken, stage2_block_x, stage2_block_y

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
        if stage2_block_state[n] == 4:
            stage2_box4.clip_draw(0, 0, 41, 57, stage2_block_x[n], stage2_block_y[n] + 7)
        elif stage2_block_state[n] == 5:
            stage2_box5.clip_draw(0, 0, 40, 70, stage2_block_x[n], stage2_block_y[n] + 15)

    for bubble in bubble_team:
        bubble.draw()
    monster.draw()
    bazzi.draw()

    update_canvas()
    pass


def makeBubble(x, y):
    global stage2_block_state, stage2_block_x, stage2_block_y
    global stage
    global bubble_team

    for i in range(195):
        if stage2_block_x[i] <= x + 20.1 < stage2_block_x[i] + 40.2:
            if stage2_block_y[i] <= y < stage2_block_y[i] + 40:
                if stage2_block_state[i] == 0:
                    stage2_block_state[i] = 8
                    for k in range(195):
                        if bubble_team[k].state == 0:
                            bubble_team[k].state = 1
                            bubble_team[k].x = stage2_block_x[i]
                            bubble_team[k].y = stage2_block_y[i]
                            break
                else:
                    break


def handle_events():
    global running
    global bazzi_dir, bazzi_dir_x, bazzi_dir_y
    global bazzi_running
    global bazzi

    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                bazzi_dir = 1
                bazzi_dir_x += 1
            elif event.key == SDLK_a:
                bazzi_dir = 2
                bazzi_dir_x -= 1
            elif event.key == SDLK_w:
                bazzi_dir = 3
                bazzi_dir_y += 1
            elif event.key == SDLK_s:
                bazzi_dir = 4
                bazzi_dir_y -= 1

            elif event.key == SDLK_g:
                makeBubble(bazzi.x, bazzi.y)

            elif event.key == SDLK_ESCAPE:
                game_framework.quit()

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                bazzi_dir_x -= 1
            elif event.key == SDLK_a:
                bazzi_dir_x += 1
            elif event.key == SDLK_w:
                bazzi_dir_y -= 1
            elif event.key == SDLK_s:
                bazzi_dir_y += 1
            bazzi_dir = 0
    pass