#!/usr/bin/env python3
import sys

# dumb constants so that you don't have to type quotes
black = "\033[30m",
red = "\033[31m",
green = "\033[32m",
yellow = "\033[33m",
blue = "\033[34m",
magenta = "\033[35m",
cyan = "\033[36m",
white = "\033[37m",
reset = "\033[0m",
bright_black = "\033[30;1m",
bright_red = "\033[31;1m",
bright_green = "\033[32;1m",
bright_yellow = "\033[33;1m",
bright_blue = "\033[34;1m",
bright_magenta = "\033[35;1m",
bright_cyan = "\033[36;1m",
bright_white = "\033[37;1m",

color_dict = {
        "BLACK": "\033[30m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
        "MAGENTA": "\033[35m",
        "CYAN": "\033[36m",
        "WHITE": "\033[37m",
        "RESET": "\033[0m",
        "BRIGHT_BLACK": "\033[30;1m",
        "BRIGHT_RED": "\033[31;1m",
        "BRIGHT_RED_UL": "\033[31;1;4m",
        "BRIGHT_GREEN": "\033[32;1m",
        "BRIGHT_YELLOW": "\033[33;1m",
        "BRIGHT_BLUE": "\033[34;1m",
        "BRIGHT_MAGENTA": "\033[35;1m",
        "BRIGHT_CYAN": "\033[36;1m",
        "BRIGHT_WHITE": "\033[37;1m",
        }

def TERM_RED(s):
    return "\033[31;1;4m" + s + "\033[0m"

def TERM_GREEN(s):
    return "\033[32m" + s + "\033[0m"

def color_string(s,color):
    return color_dict[color.upper()] + s + color_dict["RESET"]

def color_print(s,color):
    print(color_dict[color.upper()] + s + color_dict["RESET"])



if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(TERM_RED(arg))
        print(TERM_GREEN(arg))

    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            print(("\033[38;5;" + code + "m " + code.ljust(4)),end="")
        print("\033[0m")
    print("no colors?")
    for key in color_dict:
        color_print(key,key)
        print("reset?")

