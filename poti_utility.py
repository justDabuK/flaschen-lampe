from hsv_to_rgb import hsv_to_rgb


def poti_white(val):
    return [int(255 * c) for c in hsv_to_rgb(0, 0.0, val)]


def poti_warm_white(val):
    return [int(255 * c) for c in hsv_to_rgb(0.08, 0.5, val)]


def poti_cold_white(val):
    return [int(255 * c) for c in hsv_to_rgb(0.67, 0.3, val)]


def poti_red(val):
    return [int(255 * c) for c in hsv_to_rgb(0, 1.0, val)]


def poti_blue(val):
    return [int(255 * c) for c in hsv_to_rgb(0.67, 1.0, val)]


def poti_green(val):
    return [int(255 * c) for c in hsv_to_rgb(0.33, 1.0, val)]


def poti_magenta(val):
    return [int(255 * c) for c in hsv_to_rgb(0.83, 1.0, val)]


def poti_cyan(val):
    return [int(255 * c) for c in hsv_to_rgb(0.5, 1.0, val)]


def poti_yellow(val):
    return [int(255 * c) for c in hsv_to_rgb(0.167, 1.0, val)]


def poti_color_cycle(val, hue):
    hue += 0.01
    if hue > 1.0:
        hue = 0
    return [int(c * 255) for c in hsv_to_rgb(hue, 1.0, val)], hue


def poti_fire(val, t):
    return [int(c * 255) for c in hsv_to_rgb((t / 10) % 0.08, 1.0, val)]


def get_color_codes(poti_value, current_mode, color_cycle_value, t):
    red = 0
    green = 0
    blue = 0

    if current_mode == "white":
        red, green, blue = poti_white(poti_value)
    elif current_mode == "warm_white":
        red, green, blue = poti_warm_white(poti_value)
    elif current_mode == "cold_white":
        red, green, blue = poti_cold_white(poti_value)
    elif current_mode == "red":
        red, green, blue = poti_red(poti_value)
    elif current_mode == "blue":
        red, green, blue = poti_blue(poti_value)
    elif current_mode == "green":
        red, green, blue = poti_green(poti_value)
    elif current_mode == "magenta":
        red, green, blue = poti_magenta(poti_value)
    elif current_mode == "cyan":
        red, green, blue = poti_cyan(poti_value)
    elif current_mode == "yellow":
        red, green, blue = poti_yellow(poti_value)
    elif current_mode == "color_cycle" or current_mode == "rainbow":
        [red, green, blue], color_cycle_value = poti_color_cycle(poti_value, color_cycle_value)
    elif current_mode == "fire":
        red, green, blue = poti_fire(poti_value, t)
    else:
        red, green, blue = poti_white(poti_value)

    return [red, green, blue], color_cycle_value
