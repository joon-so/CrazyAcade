import game_framework
import stage1_state
from pico2d import *

WIDTH, HEIGHT = 800, 600
game_frame = 0
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
    global game_frame
    game_frame = (game_frame + 1) % 2
    delay(0.2)
    pass


def draw():
    global menu, Help, game_start, out
    global game_frame, WIDTH, HEIGHT
    clear_canvas()

    menu.draw(WIDTH // 2, HEIGHT // 2)
    game_start.clip_draw(game_frame * 192, 0, 192, 55, 400, 195)
    out.clip_draw(game_frame * 140, 0, 140, 55, 405, 145)
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_1:
                game_framework.change_state(stage1_state)
    pass