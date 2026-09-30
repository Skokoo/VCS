import os

# filesystem.py my goat (pls laugh)

_exe_cache = {}

def is_exe(p):
    if p in _exe_cache:
        return _exe_cache[p]
    r = os.path.isfile(p) and os.access(p, os.X_OK)
    _exe_cache[p] = r
    return r

def get_tree(p):
    try:
        a = os.path.abspath(p)
        d, f = [], []
        with os.scandir(a) as it:
            for e in it:
                n = e.name
                if n.startswith('.'):
                    continue
                if e.is_dir(follow_symlinks=False):
                    d.append(n)
                elif e.is_file(follow_symlinks=False):
                    f.append(n)
        d.sort()
        f.sort()
        return [".."] + d + f if a != "/" else d + f
    except:
        return [".."]

def fsize(b):
    if b < 1024:
        return f"{b} B"
    if b < 1048576:
        return f"{b/1024:.1f} KB"
    return f"{b/1048576:.1f} MB"