import game_framework
import stage2_state
import random
import game_world
from pico2d import *

from stage1_block import Block
from bazzi import Bazzi
from stage1_enemy import Enemy

WIDTH, HEIGHT = 800, 600
stage1_map = None
running = True

bazzi = None
block = None
enemy = None

bazzi_running = False

# x 80.4 , y 81
# x : left 39 ~ 601 right
# y : bottom 148 ~ 540 top

block_x, block_y = 39, 540
box_color = 0
box_broken = 0


def enter():
    global stage1_map
    global bazzi, block, enemy
    global block_x, block_y, box_color, box_broken

    stage1_map = load_image('resource/Stage1.png')

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
        elif n == 5 or n == 9 or n == 17 or n == 19 or n == 35 or n == 39 or n == 41 \
                or n == 43 or n == 45 or n == 47 or n == 49 or n == 65 or n == 66 or n == 67 \
                or n == 68 or n == 69 or n == 71 or n == 73 or n == 91 or n == 93 or n == 95 \
                or n == 99 or n == 101 or n == 103 or n == 121 or n == 123 or n == 125 \
                or n == 126 or n == 127 or n == 128 or n == 129 or n == 145 or n == 147 \
                or n == 149 or n == 153 or n == 155 or n == 159 or n == 175 or n == 177 \
                or n == 185 or n == 189:
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

        block = Block(block_x, block_y, box_color, box_broken)
        game_world.add_object(block, 1)

        block_x += 40.2

    x, y, dir = 280, 500, 1
    enemy = Enemy(x, y, dir)
    game_world.add_object(enemy, 1)

    x, y, dir = 350, 300, 4
    enemy = Enemy(x, y, dir)
    game_world.add_object(enemy, 1)


    x, y, dir = 300, 100, 3
    enemy = Enemy(x, y, dir)
    game_world.add_object(enemy, 1)

    x, y, dir = 600, 510, 2
    enemy = Enemy(x, y, dir)
    game_world.add_object(enemy, 1)

    bazzi = Bazzi()
    game_world.add_object(bazzi, 1)
    pass


def exit():
    global stage1_map
    global bazzi, enemy, block
    del(stage1_map)
    del(enemy)
    del(block)
    del(bazzi)
    game_world.clear()
    pass


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    delay(0.01)
    pass


def draw():
    global stage1_map

    clear_canvas()
    stage1_map.draw(WIDTH // 2, HEIGHT // 2)

    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.key == SDLK_2:
            game_framework.change_state(stage2_state)
        elif event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            bazzi.handle_event(event)


def makeBubble(x, y):
    global stage1_block_state, stage1_block_x, stage1_block_y
    global bubble_team

    for i in range(195):
        if stage1_block_x[i] <= x + 20.1 < stage1_block_x[i] + 40.2:
            if stage1_block_y[i] <= y < stage1_block_y[i] + 40:
                if stage1_block_state[i] == 0:
                    stage1_block_state[i] = 8
                    for k in range(195):
                        if bubble_team[k].state == 0:
                            bubble_team[k].state = 1
                            bubble_team[k].x = stage1_block_x[i]
                            bubble_team[k].y = stage1_block_y[i]
                            break
                else:
                    break