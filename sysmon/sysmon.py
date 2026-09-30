import os

_f_stat = open("/proc/stat", "r") if os.path.exists("/proc/stat") else None
_f_status = open("/proc/self/status", "r") if os.path.exists("/proc/self/status") else None
_prev_total = 0
_prev_idle = 0

def get_ram_mb():
    if not _f_status: return 0.0
    try:
        _f_status.seek(0)
        for line in _f_status:
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024
    except:
        pass
    return 0.0

def get_cpu_percent():
    global _prev_total, _prev_idle
    if not _f_stat: return 0.0
    try:
        _f_stat.seek(0)
        vals = list(map(int, _f_stat.readline().split()[1:8]))
        tot = sum(vals)
        idl = vals[3] + vals[4]
        if _prev_total == 0:
            _prev_total, _prev_idle = tot, idl
            return 0.0
        tot_d = tot - _prev_total
        idl_d = idl - _prev_idle
        _prev_total, _prev_idle = tot, idl
        return (1.0 - idl_d / tot_d) * 100 if tot_d else 0.0
    except:
        pass
    return 0.0

def cleanup():
    if _f_stat:
        _f_stat.close()
    if _f_status:
        _f_status.close()