import game_framework
import menu_state
from pico2d import *

WIDTH, HEIGHT = 800, 600
help = None


def enter():
    global help
    help = load_image('resource/Help_key.png')
    pass


def exit():
    global help
    del(help)
    pass


def update():
    pass


def draw():
    global help, WIDTH, HEIGHT
    clear_canvas()

    menu_state.menu.draw(WIDTH // 2, HEIGHT // 2)
    menu_state.game_start.clip_draw(0, 0, 192, 55, 400, 195)
    menu_state.out.clip_draw(0, 0, 140, 55, 405, 145)
    help.clip_draw(0, 0, 594, 264, 400, 400)

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
            elif event.key == SDLK_h:
                game_framework.pop_state()
    pass