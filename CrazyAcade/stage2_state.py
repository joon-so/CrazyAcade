import game_framework
import menu_state
from pico2d import *
import boss_stage
import game_world

from stage2_block import Block
from bazzi import Bazzi
from stage2_enemy import Enemy

WIDTH, HEIGHT = 800, 600
stage2_map = None
ingame_word = None

enemy_count = 0
screen_timer = 0
screen_timer_2 = 0

running = True
bazzi = None
block = None
enemy_count = 0

enemy = None

box_frame_x, box_frame_y = 0, 2

# x 80.4 , y 81
# x : left 39 ~ 601 right
# y : bottom 148 ~ 540 top
block_x, block_y = 39, 540
box_color, box_broken = 0, 0


def enter():
    global stage2_map, ingame_word, screen_timer_2, screen_timer
    global bazzi, block, enemy
    global block_y, block_x, box_color, box_broken

    screen_timer = 0
    screen_timer_2 = 0

    stage2_map = load_image('resource/Stage2.png')
    ingame_word = load_image('resource/InGame_Image_Word.png')

    enemy = []
    block = []
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

        block.append(Block(block_x, block_y, box_color, box_broken))
        block_x += 40.2
    game_world.add_objects(block, 0)

    x, y, dir = 200, 395, 3
    enemy.append(Enemy(x, y, dir))

    x, y, dir = 282, 200, 4
    enemy.append(Enemy(x, y, dir))


    x, y, dir = 480, 310, 2
    enemy.append(Enemy(x, y, dir))

    x, y, dir = 362, 450, 1
    enemy.append(Enemy(x, y, dir))
    game_world.add_objects(enemy, 2)

    bazzi = Bazzi()
    bazzi.stage = 2
    bazzi.x,bazzi.y = 80, 80
    game_world.add_object(bazzi, 3)
    pass


def exit():
    global block_x, block_y, enemy_count, screen_timer, screen_timer_2
    enemy_count = 0
    screen_timer = 0
    screen_timer_2 = 0
    block_x, block_y = 39, 540
    pass


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    global stage2_map, screen_timer, screen_timer_2

    hide_cursor()
    clear_canvas()
    screen_timer += game_framework.frame_time
    stage2_map.draw(WIDTH // 2, HEIGHT // 2)

    for game_object in game_world.all_objects():
        game_object.draw()

    if screen_timer < 2:
        if enemy_count == 0:
            ingame_word.clip_draw(0, 300, 405, 72, WIDTH // 2 - 50, HEIGHT // 2)
    if screen_timer_2 > 2:
        if enemy_count == 4:
            game_framework.change_state(boss_stage)
            Bazzi.bubble_limit = 1
            bazzi.bubble_count = 0
            game_world.remove_object(bazzi)
            for n in range(len(block)):
                game_world.remove_object(block[n])
            for n in range(len(enemy)):
                game_world.remove_object(enemy[n])
    if enemy_count == 4:
        ingame_word.clip_draw(0, 125, 405, 62, WIDTH // 2 - 50, HEIGHT // 2)
        screen_timer_2 += game_framework.frame_time

    update_canvas()


def handle_events():
    global bazzi, block, enemy
    events = get_events()
    for event in events:
        if event.key == SDLK_ESCAPE:
            game_framework.change_state(menu_state)
            Bazzi.bubble_limit = 1
            bazzi.bubble_count = 0
            game_world.remove_object(bazzi)
            for n in range(len(block)):
                game_world.remove_object(block[n])
            for n in range(len(enemy)):
                game_world.remove_object(enemy[n])
        elif event.key == SDLK_3:
            game_framework.change_state(boss_stage)
            Bazzi.bubble_limit = 1
            bazzi.bubble_count = 0
            game_world.remove_object(bazzi)
            for n in range(len(block)):
                game_world.remove_object(block[n])
            for n in range(len(enemy)):
                game_world.remove_object(enemy[n])
        else:
            bazzi.handle_event(event)