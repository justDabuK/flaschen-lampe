import time
from pimoroni_i2c import PimoroniI2C
from breakout_potentiometer import BreakoutPotentiometer
from breakout_trackball import BreakoutTrackball
from breakout_roundlcd import BreakoutRoundLCD
from breakout_colourlcd240x240 import BreakoutColourLCD240x240

from lcd_utility import set_display_color, set_display_message, square_width, square_height, round_height, \
    round_width, SQUARE, LCD_MODE
from led_strip_utility import NUM_LEDS, set_strip_color, get_led_rainbow_codes
from neopixel import Neopixel
from poti_utility import get_color_codes
from trackball_utility import set_tb_color, get_current_mode

print("Initialize components")

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5, "baudrate": 100000}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
print("i2c bus is setup")
# --- Potentiometer ---
pot = BreakoutPotentiometer(i2c)
pot.set_brightness(1.0)
poti_value = 0
print("poti is setup")

# --- Trackball ---
trackball = BreakoutTrackball(i2c)
print("trackball is setup")
# --- LEDs ---
MAX_BRIGHTNESS = 150
led_strip = Neopixel(NUM_LEDS, 0, 28, "GRB")
led_strip.brightness(MAX_BRIGHTNESS)

led_rainbow_codes = get_led_rainbow_codes(led_strip)
led_step = 0
print("leds are setup")
# --- Round LCD ---
display = None

if LCD_MODE == SQUARE:
    display_buffer = bytearray(square_width * square_height * 2)  # 2-bytes per pixel (RGB565)
    display = BreakoutColourLCD240x240(display_buffer)
else:
    display_buffer = bytearray(round_width * round_height * 2)  # 2-bytes per pixel (RGB565)
    display = BreakoutRoundLCD(display_buffer)

display.set_backlight(1.0)
print("display is setup")

t = 0

current_mode = None
color_cycle_value = 0

while True:
    # --- POTENTIOMETER ----
    poti_value = pot.read()

    [red, green, blue], color_cycle_value = get_color_codes(poti_value, current_mode, color_cycle_value, t)

    pot.set_led(red, green, blue)

    # --- TRACKBALL ---
    current_mode = get_current_mode(trackball, current_mode)

    set_tb_color(trackball, current_mode, red, green, blue)

    # --- ROUND LCD ---
    set_display_color(display, current_mode, red, green, blue, t)
    set_display_message(display, current_mode, poti_value)
    display.update()

    # --- LEDS ---
    led_step = set_strip_color(led_strip, led_rainbow_codes, current_mode, poti_value, red, green, blue, led_step)
    time.sleep(0.02)
    t += 0.02
