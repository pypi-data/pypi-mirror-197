from typing import NamedTuple


class Colors(NamedTuple):
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    magenta = "\x1b[35m"
    cyan = "\x1b[36m"
    white = "\x1b[37m"
    
    secondary_black = "\x1b[90m"
    secondary_red = "\x1b[91m"
    secondary_green = "\x1b[92m"
    secondary_yellow = "\x1b[93m"
    secondary_blue = "\x1b[94m"
    secondary_magenta = "\x1b[95m"
    secondary_cyan = "\x1b[96m"
    secondary_white = "\x1b[97m"
