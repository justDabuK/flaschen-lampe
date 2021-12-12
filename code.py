import board
import digitalio
import busio
import neopixel
from rainbowio import colorwheel
import time
import adafruit_fancyled.adafruit_fancyled as fancy
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

BRIGHTNESS = 1

led_strip = neopixel.NeoPixel(board.DATA, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

button_boot = digitalio.DigitalInOut(board.USER_SW)
button_boot.direction = digitalio.Direction.INPUT
button_boot.pull = digitalio.Pull.UP

button_a = digitalio.DigitalInOut(board.SW_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.SW_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP



def rainbow_cycle(wait):
    mode = RAINBOW
    for j in range(255):
        # early exit, if the mode is not rainbow anymore
        mode = get_mode(RAINBOW)
        if mode != RAINBOW:
            return mode
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            led_strip[i] = colorwheel(rc_index & 255)
        led_strip.show()
        time.sleep(wait)
    return mode

def color_cycle(wait):
    mode = COLOR_CYCLE
    for i in range(256):
        # early exit, if the mode is not rainbow anymore
        mode = get_mode(COLOR_CYCLE )
        if mode != COLOR_CYCLE:
            return mode
        led_strip.fill(colorwheel(i))
        led_strip.show()
        time.sleep(wait)
    return mode

def fire(wait, old_value):
    """
    try to emulate a fire effect. We take an "old" random birgthness value and create a new one. The idea is to not just give
    all LEDs a random hue, but either the old brightness, if it's an even LED, or the new brightness if it's an odd one.
    """
    # pick a random new brightness value
    new_value = random.randint(10, 100) / 100
    mid_value = (new_value + old_value) / 2
    mode = FIRE

    # first go for a brightness for all pixels that lies in the middle between the two values
    for i in range(NUM_LEDS):
        mode = get_mode(FIRE)
        if mode != FIRE:
            return mode, new_value
        # pick a random hue between orange that is more redish and orange that is more yellowish
        hue = random.randint(2, 5) /100
        brightness = mid_value
        # combine them to a color
        color = fancy.CHSV(hue, 1.0, brightness).pack()
        # and apply it
        led_strip[i] = color
    led_strip.show()
    time.sleep(wait)

    # second go for the actual values
    for i in range(NUM_LEDS):
        mode = get_mode(FIRE)
        if mode != FIRE:
            return mode, new_value
        # pick a random hue between orange that is more redish and orange that is more yellowish
        hue = random.randint(2, 5) /100
        brightness = 0.0
        if (i % 2) == 0:
            brightness = new_value
        else:
            brightness = old_value
        # combine them to a color
        color = fancy.CHSV(hue, 1.0, brightness).pack()
        # and apply it
        led_strip[i] = color
    led_strip.show()
    time.sleep(wait)
    return mode, new_value

def white(wait):
    led_strip.fill((255, 255, 255))
    led_strip.show()
    time.sleep(wait)
    return WHITE

def button_read(button):
    return not button.value

def get_mode(old_mode):
    mode = old_mode
    if button_read(button_a):
        print("a was pressed")
        while button_read(button_a):
            pass
        curr_index = possible_modes.index(old_mode)
        print("current index", curr_index)
        new_index = curr_index - 1
        print("new index", new_index)
        if new_index <= -1:
            new_index = len(possible_modes) - 1
        print("actual new index", new_index)
        mode = possible_modes[new_index]
        print ("switched to mode", mode)
    if button_read(button_b):
        print("b was pressed")
        while button_read(button_b):
            pass
        curr_index = possible_modes.index(old_mode)
        print("current index", curr_index)
        new_index = curr_index + 1
        print("new index", new_index)
        if new_index >= len(possible_modes):
            new_index = 0
        print("actual new index", new_index)
        mode = possible_modes[new_index]
        print ("switched to mode", mode)
    if button_read(button_boot):
        print("boot was pressed")
        while button_read(button_boot):
            pass
        mode = NONE
        print ("switched to mode", mode)
    return mode

# starting mode is rainbow
mode = COLOR_CYCLE
# starting brightness value for the fire is 0.0
value = 0.0

while True:
    # execute mode
    if mode == RAINBOW:
        mode = rainbow_cycle(0)
    elif mode == COLOR_CYCLE:
        mode = color_cycle(0.1)
    elif mode == FIRE:
        mode,value = fire(0, value)
    elif mode == WHITE:
        color = fancy.CHSV(0, 0.0, 0.5).pack()
        led_strip.fill(color)
        led_strip.show()
        mode = get_mode(mode)
    elif mode == WARM_WHITE:
        color = fancy.CHSV(0.08, 0.5, 0.5).pack()
        led_strip.fill(color)
        led_strip.show()
        mode = get_mode(mode)
    elif mode == COLD_WHITE:
        color = fancy.CHSV(0.67, 0.3, 0.5).pack()
        led_strip.fill(color)
        led_strip.show()
        mode = get_mode(mode)
    else:
        led_strip.fill((0, 0, 0))
        led_strip.show()
        mode = get_mode(mode)
