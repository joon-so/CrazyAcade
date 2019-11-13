import game_framework
import menu_state
import pico2d

pico2d.open_canvas(sync=True)
game_framework.run(menu_state)
pico2d.close_canvas()