import game_framework
import menu_state
from pico2d import *

WIDTH, HEIGHT = 800, 600
help = None
cursor = None
mouse_x, mouse_y = 0, 0
click_x, click_y = 0, 0


def enter():
    global help, cursor
    help = load_image('resource/Help_key.png')
    cursor = load_image('resource/hand_arrow.png')
    pass


def exit():
    global help
    del(help)
    pass


def update():
    pass


def draw():
    global help, WIDTH, HEIGHT, cursor
    clear_canvas()

    menu_state.menu.draw(WIDTH // 2, HEIGHT // 2)
    menu_state.game_start.clip_draw(0, 0, 192, 55, 400, 195)
    menu_state.out.clip_draw(0, 0, 140, 55, 405, 145)
    help.clip_draw(0, 0, 594, 264, 400, 400)
    cursor.draw_now(mouse_x + 18, mouse_y - 20)
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global mouse_y, mouse_x, click_x, click_y
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_state()
        if event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, HEIGHT - 1 - event.y
        if event.type == SDL_MOUSEBUTTONDOWN:
            click_x, click_y = mouse_x, mouse_y
            if 514 <= click_x <= 561 and 172 <= click_y <= 217:
                game_framework.pop_state()