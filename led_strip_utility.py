from common_utility import increase_color_index

NUM_LEDS = 144


def set_strip_color(led_strip, led_rainbow_codes, current_mode, poti_value, red, green, blue, led_step):
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
    return led_step


def get_led_rainbow_codes(led_strip):
    delta_hue = 65536 / NUM_LEDS
    led_rainbow_codes = []
    for led_index in range(NUM_LEDS):
        r, g, b = led_strip.colorHSV(int(delta_hue * led_index), 255, 150)
        led_rainbow_codes.append((r, g, b))

    return led_rainbow_codes
