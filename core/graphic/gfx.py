import curses

_cc = [0] * 65536
_pid = 16
_mp = 0

HX = [f"{i:02x} " for i in range(256)]
AM = [chr(i) if 32 <= i < 127 else "." for i in range(256)]

def get_pair(fg, bg, fb):
    global _pid, _mp
    a = 255 if fg == -1 else fg
    b = fb if bg == -1 else bg
    k = (a << 8) | (b & 0xFF)
    v = _cc[k]
    if v:
        return v
    if _mp == 0:
        _mp = min(256, curses.COLOR_PAIRS - 1)
    if _pid < _mp:
        try:
            curses.init_pair(_pid, a, b)
            v = curses.color_pair(_pid)
            _cc[k] = v
            _pid += 1
            return v
        except:
            return 0
    return 0