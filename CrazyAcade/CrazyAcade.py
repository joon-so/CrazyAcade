from pico2d import *

WIDTH, HEIGHT = 800, 600


def handle_events():
    global running
    global dir
    global frame
    global bazzi_frame_y
    global bazzi_frame_x
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
                bazzi_frame_y = 3
                bazzi_frame_x = (bazzi_frame_x + 1) % 4
            elif event.key == SDLK_LEFT:
                dir -= 1
                bazzi_frame_y = 2
                bazzi_frame_x = (bazzi_frame_x + 1) % 4
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1
    pass


open_canvas(WIDTH, HEIGHT)
#ackground = load_image('InGame_Bg')
#bmp png로 변경
bazzi = load_image('Character1_edit.png')

running = True
bazzi_x = 800 // 2
bazzi_frame_y = 2
bazzi_frame_x = 0
dir = 0

while running:
    clear_canvas()
    #background.draw(WIDTH // 2, HEIGHT // 2)
    bazzi.clip_draw(bazzi_frame_x * 100, bazzi_frame_y * 119, 60, 60, bazzi_x, 90)
    update_canvas()

    handle_events()
    #frame = (frame + 1) % 8
    bazzi_x += dir * 15

    delay(0.02)

close_canvas()
