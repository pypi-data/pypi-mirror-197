from sys import stderr
from typing import Callable, Optional, Any

class ANSIcodes:
    """Console colors and utilities."""
    class fg:
        default = "\u001b[39m"
        black = "\u001b[30m"
        red = "\u001b[31m"
        green = "\u001b[32m"
        yellow = "\u001b[33m"
        blue = "\u001b[34m"
        magenta = "\u001b[35m"
        cyan = "\u001b[36m"
        white = "\u001b[37m"
        rgb: Callable[[int, int, int], str] = lambda r, g, b: f"\u001b[38;2;{r};{g};{b}m"

    class bg:
        black = "\u001b[40m"
        red = "\u001b[41m"
        green = "\u001b[42m"
        yellow = "\u001b[43m"
        blue = "\u001b[44m"
        magenta = "\u001b[45m"
        cyan = "\u001b[46m"
        white = "\u001b[47m"
        rgb: Callable[[int, int, int], str] = lambda r, g, b: f"\u001b[48;2;{r};{g};{b}m"

    reset = "\u001b[0m"
    bold = "\u001b[1m"
    italic = "\u001b[3m"
    underline = "\u001b[4m"
    reverse = "\u001b[7m"

    clear = "\u001b[2J"
    clearline = "\u001b[2K"

    up = "\u001b[1A"
    down = "\u001b[1B"
    right = "\u001b[1C"
    left = "\u001b[1D"

    nextline = "\u001b[1E"
    prevline = "\u001b[1F"

    top = "\u001b[0;0H"
    goto: Callable[[int, int], str] = lambda x, y: f"\u001b[{y};{x}H"

# Colors scheme
DEVI_COLORS: dict[str, Callable[[str], str]] = {
    'default':   lambda str: ANSIcodes.fg.default + str + ANSIcodes.reset,
    'primary':   lambda str: ANSIcodes.fg.green   + str + ANSIcodes.reset,
    'secondary': lambda str: ANSIcodes.fg.blue    + str + ANSIcodes.reset,
    'error':     lambda str: ANSIcodes.fg.red     + str + ANSIcodes.reset,
    'warning':   lambda str: ANSIcodes.fg.yellow  + str + ANSIcodes.reset,
    'info':      lambda str: ANSIcodes.fg.blue    + str + ANSIcodes.reset,
    'success':   lambda str: ANSIcodes.fg.green   + str + ANSIcodes.reset,
}

class Log:
    def __init__(self):
        pass

    def __call__(self, msg: Optional[Any]="", end="\n"):
        print(msg, end=end)

    def err(self, msg: Optional[Any]="", end='\n'):
        print(f"{DEVI_COLORS['error']('[!]')} {msg}", file=stderr, end=end)

    def warn(self, msg: Optional[Any]="", end='\n'):
        print(f"{DEVI_COLORS['warning']('[!]')} {msg}", file=stderr, end=end)

    def info(self, msg: Optional[Any]="", end='\n'):
        print(f"{DEVI_COLORS['secondary']('[i]')} {msg}", file=stderr, end=end)

    def success(self, msg: Optional[Any]="", end='\n'):
        print(f"{DEVI_COLORS['success']('[-]')} {msg}", file=stderr, end=end)

deviprint = Log()
