import time
from pimoroni_i2c import PimoroniI2C
from breakout_potentiometer import BreakoutPotentiometer
from breakout_trackball import BreakoutTrackball
from breakout_roundlcd import BreakoutRoundLCD
from neopixel import Neopixel

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5, "baudrate": 100000}

sensitivity = 1

i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)


# From CPython Lib/colorsys.py
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


# --- Potentiometer ---
pot = BreakoutPotentiometer(i2c)
pot.set_brightness(1.0)
poti_value = 0


def poti_white(val):
    return [int(255 * c) for c in hsv_to_rgb(0, 0.0, val)]


def poti_warm_white(val):
    return [int(255 * c) for c in hsv_to_rgb(0.08, 0.5, val)]


def poti_cold_white(val):
    return [int(255 * c) for c in hsv_to_rgb(0.67, 0.3, val)]


def poti_color_cycle(val, hue):
    hue += 0.01
    if hue > 1.0:
        hue = 0
    return [int(c * 255) for c in hsv_to_rgb(hue, 1.0, val)], hue


def poti_fire(val, t):
    return [int(c * 255) for c in hsv_to_rgb((t / 10) % 0.08, 1.0, val)]


# --- Trackball ---
trackball = BreakoutTrackball(i2c)
trackball.set_rgbw(0, 0, 0, 64)
direction = "none"
print("Roll the trackball to change colour!")

# --- LEDs ---
NUM_LEDS = 144
BRIGHTNESS = 150
led_strip = Neopixel(NUM_LEDS, 0, 28, "GRB")
led_strip.brightness(BRIGHTNESS)

max_hue = 1.0
delta_hue = 65536 / NUM_LEDS

led_rainbow_codes = []
for led_index in range(NUM_LEDS):
    r, g, b = led_strip.colorHSV(int(delta_hue * led_index), 255, 150)
    led_rainbow_codes.append((r, g, b))
led_step = 0

# --- Round LCD ---
width = BreakoutRoundLCD.WIDTH
height = BreakoutRoundLCD.HEIGHT

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display = BreakoutRoundLCD(display_buffer)

display.set_backlight(1.0)

RADIUS = width // 2
t = 0

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


def increase_color_index(origin, step, max_value=6):
    value = origin + step
    if value >= max_value:
        value -= max_value
    return value


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


def get_mode_name(mode):
    if mode == "white":
        return "white"
    elif mode == "warm_white":
        return "warm-white"
    elif mode == "cold_white":
        return "cold-white"
    elif mode == "color_cycle":
        return "color-cycle"
    elif mode == "rainbow":
        return "rainbow"
    elif mode == "fire":
        return "fire"
    else:
        return "ERROR"


# --- mode magic ---

possible_modes = [
    "rainbow",
    "color_cycle",
    # "fire", TODO: implement the fire animation for the LEDs
    "white",
    "warm_white",
    "cold_white"
]


def increase_mode(current_mode):
    curr_index = possible_modes.index(current_mode)
    new_index = curr_index + 1
    if new_index >= len(possible_modes):
        new_index = 0
    return possible_modes[new_index]


def decrease_mode(current_mode):
    curr_index = possible_modes.index(current_mode)
    new_index = curr_index - 1
    if new_index < 0:
        new_index = len(possible_modes) - 1
    return possible_modes[new_index]


current_mode = possible_modes[1]
color_cycle_value = 0
while True:
    # --- POTENTIOMETER ----
    poti_value = pot.read()

    red = 0
    green = 0
    blue = 0

    if current_mode == "white":
        red, green, blue = poti_white(poti_value)
    elif current_mode == "warm_white":
        red, green, blue = poti_warm_white(poti_value)
    elif current_mode == "cold_white":
        red, green, blue = poti_cold_white(poti_value)
    elif current_mode == "color_cycle" or current_mode == "rainbow":
        [red, green, blue], color_cycle_value = poti_color_cycle(poti_value, color_cycle_value)
    elif current_mode == "fire":
        red, green, blue = poti_fire(poti_value, t)
    else:
        red, green, blue = poti_white(poti_value)

    pot.set_led(red, green, blue)

    # --- TRACKBALL ---
    # TODO: find a nice way to get what state it is
    state = trackball.read()
    if state[BreakoutTrackball.SW_PRESSED]:  # 5
        direction = "pressed"
    elif state[BreakoutTrackball.LEFT] > sensitivity:  # 0
        direction = "left"
        current_mode = decrease_mode(current_mode)
    elif state[BreakoutTrackball.RIGHT] > sensitivity:  # 1
        direction = "right"
        current_mode = increase_mode(current_mode)
    elif state[BreakoutTrackball.UP] > sensitivity:  # 2
        direction = "up"
    elif state[BreakoutTrackball.DOWN] > sensitivity:  # 3
        direction = "down"
    elif state[BreakoutTrackball.SW_CHANGED]:  # 4
        direction = "changed?"
    else:
        direction = "none"

    if current_mode == "white":
        trackball.set_rgbw(0, 0, 0, 255)
    elif current_mode == "warm_white":
        trackball.set_rgbw(255, 0, 0, 0)
    elif current_mode == "cold_white":
        trackball.set_rgbw(0, 0, 255, 0)
    elif current_mode == "color_cycle" or current_mode == "rainbow":
        trackball.set_rgbw(red, green, blue, 0)
    elif current_mode == "fire":
        red, green, blue = poti_fire(1.0, t)
        trackball.set_rgbw(red, green, blue, 0)
    else:
        trackball.set_rgbw(0, 0, 0, 255)

    # --- ROUND LCD ---
    # clear the screen first
    display.set_pen(0, 0, 0)
    display.clear()

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

    # status message
    display.set_pen(0, 0, 0)
    # RADIUS, RADIUS is the middle
    # x + = right
    # x - = left
    # y + = down
    # y - = up

    display.text(f"{get_mode_name(current_mode)}", int(width * 3 / 8), int(height / 3), 0)
    display.text(f"{int(poti_value * 100)}%", RADIUS, int(height * 2 / 3), 0)
    display.update()
    display.update()

    # --- LEDS ---
    if current_mode in ["white", "warm_white", "cold_white", "color_cycle"]:
        led_strip.fill((int(red), int(green), int(blue)))
        led_strip.show()
    elif current_mode == "rainbow":
        led_step += 1
        if led_step >= NUM_LEDS:
            led_step = 0
        for led_index in range(NUM_LEDS):
            color_code = led_rainbow_codes[increase_color_index(led_index, led_step, NUM_LEDS)]
            led_strip.set_pixel(led_index, (
                int(color_code[0] * poti_value), int(color_code[1] * poti_value), int(color_code[2] * poti_value)))

        led_strip.show()
    else:
        led_strip.fill((0, 0, 0))
        led_strip.show()

    time.sleep(0.02)
    t += 0.02
