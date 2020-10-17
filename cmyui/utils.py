# -*- coding: utf-8 -*-

import sys
from enum import IntEnum
from typing import overload
from string import ascii_letters, digits
from random import choice
from datetime import (
    datetime as dt,
    timezone as tz,
    timedelta as td
)

__all__ = ('get_timestamp', '_isdecimal', 'rstring',
           'Ansi', 'AnsiRGB', 'printc')

ts_fmt = ('%I:%M:%S%p', '%d/%m/%Y %I:%M:%S%p')
tz_est = tz(td(hours = -4), 'EDT')
def get_timestamp(full: bool = False) -> str:
    return f'{dt.now(tz = tz_est):{ts_fmt[full]}}'

def _isdecimal(s: str, _float: bool = False,
               _negative: bool = False) -> None:
    if _float:
        s = s.replace('.', '', 1)

    if _negative:
        s = s.replace('-', '', 1)

    return s.isdecimal()

def isfloat(s: str) -> bool:
    return s.replace('.', '', 1).isdecimal()

__chars = ascii_letters + digits
def rstring(l: int, seq: str = __chars) -> str:
    return ''.join((choice(seq) for _ in range(l)))

class Ansi(IntEnum):
    # Default colours
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37

    # Light colours
    GRAY          = 90
    LRED     = 91
    LGREEN   = 92
    LYELLOW  = 93
    LBLUE    = 94
    LMAGENTA = 95
    LCYAN    = 96
    LWHITE   = 97

    RESET = 0

    def __repr__(self) -> str:
        return f'\x1b[{self.value}m'

class AnsiRGB:
    @overload
    def __init__(self, rgb: int) -> None: ...
    @overload
    def __init__(self, r: int, g: int, b: int) -> None: ...

    def __init__(self, *args) -> None:
        largs = len(args)

        if largs == 3:
            # r, g, b passed.
            self.r, self.g, self.b = args
        elif largs == 1:
            # passed as single argument
            rgb = args[0]
            self.b = rgb & 0xff
            self.g = (rgb >> 8) & 0xff
            self.r = (rgb >> 16) & 0xff
        else:
            raise ValueError('Incorrect params for AnsiRGB.')

    def __repr__(self) -> str:
        return f'\x1b[38;2;{self.r};{self.g};{self.b}m'

def printc(s: str, col: Ansi) -> None:
    # abstract the ugliness of colour codes away a bit.
    sys.stdout.write(f'{col!r}{s}{Ansi.RESET!r}\n')
