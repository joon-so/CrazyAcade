import game_framework
from pico2d import *
import boss_stage
import game_world

WIDTH, HEIGHT = 800, 600
stage2_map = None
stage2_box1 = None
stage2_box2 = None
stage2_box3 = None
stage2_box4 = None
stage2_box5 = None


running = True
bazzi = None
bazzi_dir = 0
bazzi_dir_x = 0
bazzi_dir_y = 0
bazzi_running = False

monster_team = None
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
        self.x, self.y = 80, 80
        self.frame_x, self.frame_y = 0, 420
        self.image = load_image('resource/Character1_edit.png')

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
        self.x, self.y = 200, 200
        self.frame_x, self.frame_y = 1, 0
        self.dir = 1
        self.timer = 0
        self.image = load_image('resource/Monster_Normal.png')

    def update(self):
        self.timer += 1
        if self.timer == 2:
            if self.dir == 1:
                self.frame_y = 195
                self.y -= 1
            elif self.dir == 2:
                self.frame_y = 156
                self.x -= 1
            elif self.dir == 3:
                self.frame_y = 117
                self.x += 1
            elif self.dir == 4:
                self.frame_y = 78
                self.y += 1

            if self.frame_x == 1:
                self.frame_x = 0
            else:
                self.frame_x = 1
            self.timer = 0

    def draw(self):
        self.image.clip_draw(self.frame_x * 41, self.frame_y, 41, 39, self.x, self.y)


class Bubble:
    image = None
    def __init__(self):
        self.time, self.state = 0, 0
        self.frame = 0
        self.x, self.y = 9999, 9999
        if Bubble.image == None:
            Bubble.image = load_image('resource/Bubble.png')

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
    global stage2_map, stage2_box1, stage2_box2, stage2_box3, stage2_box4, stage2_box5
    global bazzi, bubble_team, monster_team
    global block_y, block_x, stage2_block_state, stage2_block_broken, stage2_block_x, stage2_block_y

    stage2_map = load_image('resource/Stage2.png')
    stage2_box1 = load_image('resource/pirate_Box_0.png')
    stage2_box2 = load_image('resource/pirate_Box_1.png')
    stage2_box3 = load_image('resource/pirate_Box_2.png')
    stage2_box4 = load_image('resource/pirate_Box_3.png')
    stage2_box5 = load_image('resource/pirate_Box_4.png')
    bazzi = Bazzi()
    bubble_team = [Bubble() for i in range(195)]
    monster_team = [Monster() for i in range(4)]
    monster_team[0].x, monster_team[0].y = 200, 395
    monster_team[0].dir = 3
    monster_team[1].x, monster_team[1].y = 282, 200
    monster_team[1].dir = 4
    monster_team[2].x, monster_team[2].y = 480, 310
    monster_team[2].dir = 2
    monster_team[3].x, monster_team[3].y = 362, 480

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
                or i == 15 or i == 17 or i == 27 or i == 29 or i == 30 or i == 44 \
                or i == 59 or i == 60 or i == 74 or i == 80 or i == 85 \
                or i == 84 or i == 86 or i == 89 or i == 90 or i == 106 \
                or i == 118 or i == 121 or i == 132 or i == 134 or i == 135 or i == 136 \
                or i == 138 or i == 148 or i == 151 or i == 153 or i == 161 or i == 163 or i == 169 \
                or i == 170 or i == 176 or i == 179 or i == 183 or i == 184 or i == 186 or i == 189 or i == 191:
            box_color = 2
            box_broken = 1
        # box2
        elif i == 31 or i == 43 or i == 45 or i == 52 \
                or i == 75 or i == 78 \
                or i == 79 or i == 104 or i == 105 or i == 112\
                or i == 119 or i == 120 or i == 122 or i == 127 or i == 133 \
                or i == 137 or i == 142 or i == 146 or i == 147 or i == 149 or i == 150 or i == 154 or i == 160 or i == 164 \
                or i == 165 or i == 168 or i == 174 or i == 175 or i == 180 or i == 185 or i == 187 or i == 188 \
                or i == 190 or i == 194:
            box_color = 3
            box_broken = 1
        # no broken1
        elif i == 67 or i == 81 or i == 82 or i == 83 or i == 97:
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
    global stage2_map, stage2_box1, stage2_box2, stage2_box3, stage2_box4, stage2_box5
    global bazzi, bubble_team, monster_team
    global block_y, block_x, stage2_block_state, stage2_block_broken, stage2_block_x, stage2_block_y

    del(stage2_map)
    del(stage2_box1)
    del(stage2_box2)
    del(stage2_box3)
    del(stage2_box4)
    del(stage2_box5)
    del(bazzi)
    del(bubble_team)
    del(monster_team)
    del(block_x)
    del(block_y)
    del(stage2_block_state)
    del(stage2_block_broken)
    del(stage2_block_x)
    del(stage2_block_y)
    pass


def update():
    global bazzi, bubble_team, monster_team

    for bubble in bubble_team:
        bubble.update()
    for monster in monster_team:
        monster.update()
    bazzi.update()
    delay(0.03)
    pass


def draw():
    global stage2_map, stage2_box1, stage2_box2, stage2_box3, stage2_box4, stage2_box5
    global bazzi, bubble_team
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

    for bubble in bubble_team:
        bubble.draw()
    for monster in monster_team:
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
            if event.key == SDLK_3:
                game_framework.change_state(boss_stage)

            elif event.key == SDLK_d:
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