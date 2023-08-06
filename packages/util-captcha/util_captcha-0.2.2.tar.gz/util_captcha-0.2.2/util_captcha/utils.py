# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:url: https://punk_lee.gitee.io/
:copyright: © 2023 Punk Lee <punklee333@gmail.com>
"""
from random import randint, choice


def random_char():
    """Generate random characters"""
    random_num = str(randint(0, 9))
    random_lower = chr(randint(97, 122))  # a-z
    random_upper = chr(randint(65, 90))  # A-Z
    return choice([random_num, random_lower, random_upper])


def random_color(rgb: bool = True):
    """Generate random colors (rgb or hex)"""
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)

    if rgb:
        return r, g, b
    else:
        return rgb_to_hex(r, g, b)


def hex_to_rgb(hex_value: str):
    """HEX to RGB"""
    hex_value = hex_value.replace("#", "")
    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)
    return r, g, b


def rgb_to_hex(r: int = 0, g: int = 0, b: int = 0):
    """RGB to HEX"""
    return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()
