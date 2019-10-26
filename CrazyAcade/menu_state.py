import game_framework
import stage1_state
from pico2d import *

WIDTH, HEIGHT = 800, 600
game_frame = 0
running = True
menu = None
Help = None
game_start = None
out = None

def enter():
    global menu, Help, game_start, out
    menu = load_image('Main.png')
    Help = load_image('Help_key.png')
    game_start = load_image('Game_start.png')
    out = load_image('InGame_Button_Out.png')
    pass


def exit():
    global menu, Help, game_start, out
    del(menu)
    del(Help)
    del(game_start)
    del(out)
    pass


def update():
    pass


def draw():
    global menu, Help, game_start, out
    global game_frame
    clear_canvas()

    menu.draw(WIDTH // 2, HEIGHT // 2)
    game_start.clip_draw(game_frame * 192, 0, 192, 55, 400, 195)
    out.clip_draw(game_frame * 140, 0, 140, 55, 405, 145)
    game_frame = (game_frame + 1) % 2
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass


def make_menu():
    global menu, Help, game_start, out
    global game_frame
    clear_canvas()

    menu.draw(WIDTH // 2, HEIGHT // 2)
    game_start.clip_draw(game_frame * 192, 0, 192, 55, 400, 195)
    out.clip_draw(game_frame * 140, 0, 140, 55, 405, 145)
    game_frame = (game_frame + 1) % 2

    handle_events()
    update_canvas()
    pass


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_1:
                game_framework.change_state(stage1_state)
    pass


open_canvas(WIDTH, HEIGHT)

while running:
    make_menu()
    delay(0.2)

    handle_events()

close_canvas()
