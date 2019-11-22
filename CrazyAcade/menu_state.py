import game_framework
import stage1_state
import help_state
from pico2d import *

WIDTH, HEIGHT = 800, 600
game_frame = 0
menu = None
game_start = None
out = None
cursor = None
mouse_x, mouse_y = 0, 0
click_x, click_y = 0, 0

def enter():
    global menu, game_start, out, cursor, mouse_y, mouse_x
    mouse_y, mouse_x = 100, 100
    menu = load_image('resource/Main.png')
    game_start = load_image('resource/Game_start.png')
    out = load_image('resource/InGame_Button_Out.png')
    cursor = load_image('resource/hand_arrow.png')


def exit():
    global menu, game_start, out
    del(menu)
    del(game_start)
    del(out)


def update():
    global game_frame
    game_frame = (game_frame + game_framework.frame_time * 3) % 2


def handle_events():
    global mouse_y, mouse_x, click_x, click_y
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_1:
                game_framework.change_state(stage1_state)

        if event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, HEIGHT - 1 - event.y
        if event.type == SDL_MOUSEBUTTONDOWN:
            click_x, click_y = mouse_x, mouse_y
            if 290 <= click_x <= 507 and 172 <= click_y <= 217:
                game_framework.change_state(stage1_state)
            elif 514 <= click_x <= 561 and 172 <= click_y <= 217:
                game_framework.push_state(help_state)
            elif 290 <= click_x <= 507 and 122 <= click_y <= 167:
                game_framework.quit()




def draw():
    global menu, game_start, out, cursor
    global game_frame, WIDTH, HEIGHT, mouse_y, mouse_x
    hide_cursor()
    clear_canvas()

    menu.draw(WIDTH // 2, HEIGHT // 2)
    game_start.clip_draw(int(game_frame) * 192, 0, 192, 55, 400, 195)
    out.clip_draw(int(game_frame) * 140, 0, 140, 55, 405, 145)
    cursor.draw_now(mouse_x + 18, mouse_y - 20)

    update_canvas()


def pause():
    pass


def resume():
    pass