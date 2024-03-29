import game_framework
import game_world
from pico2d import *
import menu_state

from stage2_block import Block
from bazzi import Bazzi
from boss import Boss

WIDTH, HEIGHT = 800, 600
stage2_map = None

ingame_word = None

enemy_count = 0
screen_timer = 0
screen_timer_2 = 0
gameover_timer = 0

running = True
bazzi = None
bazzi_running = False
block = None
enemy = None
bgm = None

# x 80.4 , y 81
# x : left 39 ~ 601 right
# y : bottom 148 ~ 540 top
block_x, block_y = 39, 540


def enter():
    global stage2_map, ingame_word, screen_timer, screen_timer_2, cursor, gameover_timer, bgm
    global bazzi, block, enemy
    global block_y, block_x

    screen_timer = 0
    screen_timer_2 = 0

    stage2_map = load_image('resource/stage2.png')
    ingame_word = load_image('resource/InGame_Image_Word.png')
    cursor = load_image('resource/hand_arrow.png')
    bgm = load_music('sound/piratebgm.mp3')
    bgm.set_volume(80)
    bgm.repeat_play()

    bazzi = Bazzi()
    bazzi.stage = 3
    bazzi.x, bazzi.y = 180, 140
    game_world.add_object(bazzi, 3)

    enemy = Boss()
    game_world.add_object(enemy, 2)

    block = []
    for i in range(195):
        if block_x > 610:
            block_y -= 40
            block_x = 39
        # no broken1
        if i == 82:
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
    pass


def exit():
    global block_x, block_y, enemy_count, screen_timer_2, screen_timer, gameover_timer, bgm
    enemy_count = 0
    screen_timer = 0
    screen_timer_2 = 0
    gameover_timer = 0
    block_x, block_y = 39, 540
    Bazzi.in_bubble = 0
    Boss.hp = 4
    bgm.stop()


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    global stage2_map, ingame_word, screen_timer, screen_timer_2, gameover_timer

    clear_canvas()
    screen_timer += game_framework.frame_time
    stage2_map.draw(WIDTH // 2, HEIGHT // 2)

    for game_object in game_world.all_objects():
        game_object.draw()

    if screen_timer < 2:
        if enemy_count == 0:
            ingame_word.clip_draw(0, 300, 405, 72, WIDTH // 2 - 50, HEIGHT // 2)
    if screen_timer_2 > 2:
        if enemy_count == 1:
            game_framework.change_state(menu_state)
            Bazzi.bubble_limit = 1
            bazzi.bubble_count = 0
            game_world.remove_object(bazzi)
            for n in range(len(block)):
                game_world.remove_object(block[n])
            game_world.remove_object(enemy)
    if enemy_count == 1:
        ingame_word.clip_draw(0, 125, 405, 62, WIDTH // 2 - 50, HEIGHT // 2)
        screen_timer_2 += game_framework.frame_time
    if bazzi.go_main == 1:
        ingame_word.clip_draw(0, 0, 405, 62, WIDTH // 2 - 50, HEIGHT // 2)
        gameover_timer += game_framework.frame_time
        if gameover_timer > 3:
            game_framework.change_state(menu_state)
            Bazzi.bubble_limit = 1
            bazzi.bubble_count = 0
            bazzi.go_main = 0
            game_world.remove_object(bazzi)
            for n in range(len(block)):
                game_world.remove_object(block[n])
            game_world.remove_object(enemy)
    update_canvas()
    pass


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
            game_world.remove_object(enemy)
        elif event.key == SDLK_4:
            game_framework.change_state(menu_state)
            Bazzi.bubble_limit = 1
            bazzi.bubble_count = 0
            game_world.remove_object(bazzi)
            for n in range(len(block)):
                game_world.remove_object(block[n])
            game_world.remove_object(enemy)
        else:
            bazzi.handle_event(event)