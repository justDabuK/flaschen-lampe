import time
from neopixel import Neopixel
import random

NONE = "NONE"
RAINBOW = "RAINBOW"
COLOR_CYCLE = "COLOR_CYCLE"
FIRE = "FIRE"
WHITE = "WHITE"
WARM_WHITE = "WARM_WHITE"
COLD_WHITE = "COLD_WHITE"

possible_modes = [NONE, RAINBOW, COLOR_CYCLE, FIRE, WHITE, WARM_WHITE, COLD_WHITE]

NUM_LEDS = 144

BRIGHTNESS = 150

led_strip = Neopixel(NUM_LEDS, 0, 28, "GRB")

led_strip.brightness(BRIGHTNESS)

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


def rainbow_cycle(wait):
    print("rainbow not implemented yet")
    return
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            #led_strip[i] = colorwheel(rc_index & 255)
        led_strip.show()
        time.sleep(wait)

def color_cycle(wait):
    print("colory_cycle not implemented yet")
    return
    for i in range(256):
        #led_strip.fill(colorwheel(i))
        led_strip.show()
        time.sleep(wait)

def fire(wait, old_value):
    """
    try to emulate a fire effect. We take an "old" random birgthness value and create a new one. The idea is to not just give
    all LEDs a random hue, but either the old brightness, if it's an even LED, or the new brightness if it's an odd one.
    """
    # pick a random new brightness value
    new_value = random.randint(1, 255)
    mid_value = int((new_value + old_value) / 2)

    # first go for a brightness for all pixels that lies in the middle between the two values
    for i in range(NUM_LEDS):
        # pick a random hue between orange that is more redish and orange that is more yellowish
        hue = random.randint(2, 5) /100
        brightness = mid_value
        # combine them to a color
        r, g, b = hsv_to_rgb(hue, 1.0, brightness)
        # and apply it
        led_strip.set_pixel(i, (r, g, b))
    led_strip.show()
    time.sleep(wait)

    # second go for the actual values
    for i in range(NUM_LEDS):
        # pick a random hue between orange that is more redish and orange that is more yellowish
        hue = random.randint(2, 5) /100
        brightness = 0.0
        if (i % 2) == 0:
            brightness = new_value
        else:
            brightness = old_value
        # combine them to a color
        r, g, b = hsv_to_rgb(hue, 1.0, brightness)
        # and apply it
        led_strip.set_pixel(i, (r, g, b))
    led_strip.show()
    time.sleep(wait)
    return new_value

# starting mode is rainbow
mode = COLD_WHITE
# starting brightness value for the fire is 0.0
value = 0.0

while True:
    # execute mode
    if mode == RAINBOW:
        rainbow_cycle(0)
    elif mode == COLOR_CYCLE:
        color_cycle(0.1)
    elif mode == FIRE:
        value = fire(0, value)
    elif mode == WHITE:
        r, g, b = hsv_to_rgb(0, 0.0, 0.5)
        led_strip.fill((int(r * 255), int(g * 255), int(b * 255)))
        led_strip.show()
    elif mode == WARM_WHITE:
        r, g, b = hsv_to_rgb(0.08, 0.5, 0.5)
        led_strip.fill((int(r * 255), int(g * 255), int(b * 255)))
        led_strip.show()
        led_strip.show()
    elif mode == COLD_WHITE:
        r, g, b = hsv_to_rgb(0.67, 0.3, 0.5)
        led_strip.fill((int(r * 255), int(g * 255), int(b * 255)))
        led_strip.show()
        led_strip.show()
    else:
        led_strip.fill((0, 0, 0))
        led_strip.show()
    time.sleep(1)
