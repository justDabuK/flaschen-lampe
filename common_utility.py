def increase_color_index(origin, step, max_value=6):
    value = origin + step
    if value >= max_value:
        value -= max_value
    return value

