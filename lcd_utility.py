from common_utility import increase_color_index
from hsv_to_rgb import hsv_to_rgb
from breakout_roundlcd import BreakoutRoundLCD

from mode_utility import get_mode_name
from poti_utility import poti_warm_white, poti_cold_white

width = BreakoutRoundLCD.WIDTH
height = BreakoutRoundLCD.HEIGHT

RADIUS = width // 2

display_rainbow_codes = [
    [int(c * 255) for c in hsv_to_rgb(0, 1.0, 1.0)],  # red
    [int(c * 255) for c in hsv_to_rgb(0.083, 1.0, 1.0)],  # orange
    [int(c * 255) for c in hsv_to_rgb(0.167, 1.0, 1.0)],  # yellow
    [int(c * 255) for c in hsv_to_rgb(0.33, 1.0, 1.0)],  # green
    [int(c * 255) for c in hsv_to_rgb(0.67, 1.0, 1.0)],  # blue
    [int(c * 255) for c in hsv_to_rgb(0.75, 1.0, 1.0)]  # purple
]


def white(display):
    display.set_pen(255, 255, 255)
    display.circle(RADIUS, RADIUS, RADIUS)


def warm_white(display):
    r, g, b = poti_warm_white(1.0)
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, RADIUS)


def cold_white(display):
    r, g, b = poti_cold_white(1.0)
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, RADIUS)


def color_cycle(display, r, g, b):
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, RADIUS)


def rainbow_circles(display, t):
    step = int((t % 0.6) * 10)

    # 1. red
    r, g, b = display_rainbow_codes[increase_color_index(0, step)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS))

    # 2. orange
    r, g, b = display_rainbow_codes[increase_color_index(1, step)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * 5 / 6))

    # 3. yellow
    r, g, b = display_rainbow_codes[increase_color_index(2, step)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * 4 / 6))

    # 4. green
    r, g, b = display_rainbow_codes[increase_color_index(3, step)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * 3 / 6))

    # 5. blue
    r, g, b = display_rainbow_codes[increase_color_index(4, step)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * 2 / 6))

    # 6. purple
    r, g, b = display_rainbow_codes[increase_color_index(5, step)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * 1 / 6))


def rainbow_bars(display, t):
    # colors i want to use
    bar_height = int(height / 6)

    # 1. red
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.rectangle(int(RADIUS - width / 2), 0, width, bar_height)

    # 2. orange
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0.083, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.rectangle(int(RADIUS - width / 2), bar_height, width, bar_height)

    # 3. yellow
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0.167, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.rectangle(int(RADIUS - width / 2), 2 * bar_height, width, bar_height)

    # 4. green
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0.33, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.rectangle(int(RADIUS - width / 2), 3 * bar_height, width, bar_height)

    # 5. blue
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0.67, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.rectangle(int(RADIUS - width / 2), 4 * bar_height, width, bar_height)

    # 6. purple
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0.75, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.rectangle(int(RADIUS - width / 2), 5 * bar_height, width, bar_height)


def fire(display, t):
    value = (t % 0.3)
    scale = 1 / 3
    if value <= 0.1:
        scale = 1 / 3
    elif 0.1 <= value <= 0.2:
        scale = 2 / 3
    elif value > 0.2:
        scale = 1
    else:
        scale = 1

    # outer yellow circle
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0.167, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * scale))

    # middle orange circle
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0.083, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * 2 / 3 * scale))

    # inner red circle
    r, g, b = [int(c * 255) for c in hsv_to_rgb(0, 1.0, 1.0)]
    display.set_pen(r, g, b)
    display.circle(RADIUS, RADIUS, int(RADIUS * 1 / 3 * scale))


def set_display_color(display, current_mode, red, green, blue, t):
    # background magic
    if current_mode == "white":
        white(display)
    elif current_mode == "warm_white":
        warm_white(display)
    elif current_mode == "cold_white":
        cold_white(display)
    elif current_mode == "color_cycle":
        color_cycle(display, red, green, blue)
    elif current_mode == "rainbow":
        rainbow_circles(display, t)
    elif current_mode == "fire":
        fire(display, t)
    else:
        white(display)


def set_display_message(display, current_mode, poti_value):
    # status message
    display.set_pen(0, 0, 0)
    # RADIUS, RADIUS is the middle
    # x + = right
    # x - = left
    # y + = down
    # y - = up
    display.text(f"{get_mode_name(current_mode)}", int(width * 3 / 8), int(height / 3), 0)
    display.text(f"{int(poti_value * 100)}%", RADIUS, int(height * 2 / 3), 0)
