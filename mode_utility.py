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
