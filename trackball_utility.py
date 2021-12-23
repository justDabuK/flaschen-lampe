from breakout_trackball import BreakoutTrackball

from mode_utility import decrease_mode, increase_mode, possible_modes

sensitivity = 1


def set_tb_color(trackball, current_mode, red, green, blue):
    if current_mode == "white":
        trackball.set_rgbw(0, 0, 0, 255)
    elif current_mode == "warm_white":
        trackball.set_rgbw(255, 0, 0, 0)
    elif current_mode == "cold_white":
        trackball.set_rgbw(0, 0, 255, 0)
    elif current_mode == "color_cycle" or current_mode == "rainbow":
        trackball.set_rgbw(red, green, blue, 0)
    elif current_mode == "fire":
        trackball.set_rgbw(red, green, blue, 0)
    else:
        trackball.set_rgbw(0, 0, 0, 255)


def get_current_mode(trackball, current_mode):
    if current_mode is None:
        current_mode = possible_modes[1]
    state = trackball.read()
    if state[BreakoutTrackball.LEFT] > sensitivity:  # 0
        current_mode = decrease_mode(current_mode)
    elif state[BreakoutTrackball.RIGHT] > sensitivity:  # 1
        current_mode = increase_mode(current_mode)

    return current_mode
