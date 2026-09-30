import re, math, random, os, sys, ctypes, mmap, platform

x86 = platform.machine().lower() in ("x86_64", "amd64")

'''
a_rgb:
mov    eax, edi
shr    eax, 16
mov    ecx, 51
xor    edx, edx
div    ecx
imul   eax, eax, 36
mov    r8d, eax

mov    eax, edi
shr    eax, 8
and    eax, 255
xor    edx, edx
div    ecx
imul   eax, eax, 6
add    eax, r8d
mov    r8d, eax

mov    eax, edi
and    eax, 255
xor    edx, edx
div    ecx
add    eax, r8d
add    eax, 16
ret
'''
a_rgb = b"\x89\xf8\xc1\xe8\x10\xb9\x33\x00\x00\x00\x31\xd2\xf7\xf1\x6b\xc0\x24\x44\x89\xc0\x89\xf8\xc1\xe8\x08\x25\xff\x00\x00\x00\x31\xd2\xf7\xf1\x6b\xc0\x06\x41\x01\xc0\x89\xf8\x25\xff\x00\x00\x00\x31\xd2\xf7\xf1\x44\x01\xc0\x83\xc0\x10\xc3"

'''
a_scan:
xor    eax, eax
test   rsi, rsi
jle    not_found

loop_start:
 cmp    byte ptr [rdi + rax], dl
 je     found
 inc    rax
 dec    rsi
 jnz    loop_start

not_found:
 mov    rax, -1
 ret

found:
 ret
'''
a_scan = b"\x31\xc0\x48\x85\xf6\x7e\x0d\x38\x14\x07\x74\x09\x48\xff\xc0\x48\xff\xce\x75\xf3\x48\xc7\xc0\xff\xff\xff\xff\xc3"

def _init_asm_f1(code):
    if not x86: return None
    try:
        b = mmap.mmap(-1, len(code), flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS, prot=7)
        b.write(code)
        a = ctypes.addressof(ctypes.c_char.from_buffer(b))
        return ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_uint64)(a)
    except: return None

def _init_asm_f3(code):
    if not x86: return None
    try:
        b = mmap.mmap(-1, len(code), flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS, prot=7)
        b.write(code)
        a = ctypes.addressof(ctypes.c_char.from_buffer(b))
        return ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_uint64, ctypes.c_int64, ctypes.c_uint64)(a)
    except: return None

f_rgb_asm = _init_asm_f1(a_rgb)
f_scan_asm = _init_asm_f3(a_scan)

def fast_rgb256(r, g, b):
    if f_rgb_asm:
        return f_rgb_asm((r << 16) | (g << 8) | b)
    return 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)

msin = math.sin
rint = random.randint
runi = random.uniform
rsub = re.sub
pi2 = 6.283185307179586
rst = "\033[0m"

sint = tuple(msin(i * 0.01) for i in range(630))

def fsin(x):
    k = int((x % pi2) * 100)
    return sint[k] if 0 <= k < 630 else 0.0

themes = {
    "fart": {"pk": "\033[38;5;142m", "rg": "\033[38;5;100m", "pl": "\033[38;5;137m", "cn": "\033[38;5;94m", "cm": "\033[38;5;58m", "bg": ""},
    "monokrom": {"pk": "\033[38;5;231m", "rg": "\033[38;5;246m", "pl": "\033[38;5;250m", "cn": "\033[38;5;244m", "cm": "\033[38;5;239m", "bg": ""},
    "cxx": {"pk": "\033[38;5;75m", "rg": "\033[38;5;32m", "pl": "\033[38;5;221m", "cn": "\033[38;5;215m", "cm": "\033[38;5;242m", "bg": ""},
    "pastel": {"pk": "\033[38;5;204m", "rg": "\033[38;5;162m", "pl": "\033[38;5;141m", "cn": "\033[38;5;75m", "cm": "\033[38;5;242m", "bg": ""},
    "hacker": {"pk": "\033[38;5;82m", "rg": "\033[38;5;34m", "pl": "\033[38;5;46m", "cn": "\033[38;5;28m", "cm": "\033[38;5;22m", "bg": ""},
    "crimson": {"pk": "\033[38;5;196m", "rg": "\033[38;5;124m", "pl": "\033[38;5;160m", "cn": "\033[38;5;88m", "cm": "\033[38;5;52m", "bg": ""},
    "defiance": {"pk": "\033[38;5;39m", "rg": "\033[38;5;24m", "pl": "\033[38;5;252m", "cn": "\033[38;5;110m", "cm": "\033[38;5;240m", "bg": ""}
}

thms = list(themes.keys()) + ["rgb", "hardcore"]
thstr = ", ".join(thms)

kw_cpp = {
    'static','inline','unsigned','char','short','void','const','if','else','while','for','switch','case','default',
    'return','int','float','double','bool','long','signed','class','struct','public','private','protected','union',
    'enum','typedef','using','typename','template','namespace','std','cout','cin','auto','virtual','override','final',
    'explicit','friend','mutable','constexpr','consteval','constinit','noexcept','nullptr','decltype','static_assert',
    'concept','requires','co_await','co_return','co_yield','try','catch','throw','__asm__','volatile','sizeof',
    'alignas','alignof','uint8_t','uint16_t','uint32_t','uint64_t','int8_t','int16_t','int32_t','int64_t','size_t'
}

kw_py = {
    'def','class','return','if','elif','else','while','for','in','import','from','as','try','except','finally','raise',
    'assert','and','or','not','is','lambda','with','pass','break','continue','None','True','False','global','nonlocal',
    'async','await','yield','self','cls','match','case','type'
}

kw_asm = {
    'bits','mov','movl','movq','movb','movw','lea','xchg','push','pop','pusha','popa','add','sub','mul','imul','div','idiv',
    'inc','dec','neg','and','or','xor','not','shl','shr','sal','sar','rol','ror','cmp','test','jmp','je','jne','jg','jge',
    'jl','jle','ja','jb','jae','jbe','jz','jnz','call','ret','int','syscall','sysret','nop','hlt','cli','sti','leave','enter',
    'loop','rdtsc','cpuid','vmovdqu','vaddps','vsubps','vmulps','vdivps',
    'ldr','str','ldp','stp','ldur','stur','subs','udiv','sdiv','b','bl','blx','bx','cbz','cbnz','tbz','tbnz','svc',
    'adr','adrp','movz','movk','orr','eor','bic','lsl','lsr','asr'
}

regs_asm = {
    'rax','rbx','rcx','rdx','rsi','rdi','rsp','rbp','r8','r9','r10','r11','r12','r13','r14','r15',
    'eax','ebx','ecx','edx','esi','edi','esp','ebp','r8d','r9d','r10d','r11d','r12d','r13d','r14d','r15d',
    'ax','bx','cx','dx','si','di','sp','bp','r8w','r9w','r10w','r11w','r12w','r13w','r14w','r15w',
    'al','ah','bl','bh','cl','ch','dl','dh','r8b','r9b','r10b','r11b','r12b','r13b','r14b','r15b',
    'xmm0','xmm1','xmm2','xmm3','xmm4','xmm5','xmm6','xmm7','xmm8','xmm9','xmm10','xmm11','xmm12','xmm13','xmm14','xmm15',
    'ymm0','ymm1','ymm2','ymm3','ymm4','ymm5','ymm6','ymm7','ymm8','ymm9','ymm10','ymm11','ymm12','ymm13','ymm14','ymm15',
    'x0','x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11','x12','x13','x14','x15',
    'x16','x17','x18','x19','x20','x21','x22','x23','x24','x25','x26','x27','x28','x29','x30',
    'w0','w1','w2','w3','w4','w5','w6','w7','w8','w9','w10','w11','w12','w13','w14','w15',
    'lr','xzr','wzr','zero','ra','gp','tp','t0','t1','t2','t3','t4','t5','t6','s0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','a0','a1','a2','a3','a4','a5','a6','a7'
}

kw_sh = {
    'if','then','else','elif','fi','case','esac','for','select','while','until','do','done','in','function','export',
    'alias','unset','local','readonly','return','exit','echo','printf','cd','pwd','set','shift','exec','eval','source','read','trap'
}

re_cpp = re.compile(
    r'(?P<cm>//.*?$|/\*[\s\S]*?\*/)|'
    r'(?P<s>R"(?P<d>[^()\s\\]*)\([\s\S]*?\)(?P=d)"|"(?:\\.|[^"\n\\])*"|\'(?:\\.|[^\'\n\\])*\')|'
    r'(?P<inc>#include\s+[<"][^>"]+[>"])|'
    r'(?P<pr>#\w+\b)|'
    r'(?P<num>\b0x[0-9a-fA-F]+\b|\b0b[01]+\b|\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[fFlUu]*\b)|'
    r'(?P<w>\b[a-zA-Z_]\w*\b)|'
    r'(?P<sy>[\s\S])',
    re.MULTILINE
)

re_py = re.compile(
    r'(?P<cm>#.*?$)|'
    r'(?P<s>[fFrRbBuU]?\'\'\'[\s\S]*?\'\'\'|[fFrRbBuU]?"""[\s\S]*?"""|[fFrRbBuU]?"(?:\\.|[^"\n\\])*"|[fFrRbBuU]\'(?:\\.|[^\'\n\\])*\')|'
    r'(?P<pr>@[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*)|'
    r'(?P<num>\b0x[0-9a-fA-F_]+\b|\b0b[01_]+\b|\b\d[0-9_]*(?:\.\d[0-9_]*)?(?:[eE][+-]?\d+)?j?\b)|'
    r'(?P<w>\b[a-zA-Z_]\w*\b)|'
    r'(?P<sy>[\s\S])',
    re.MULTILINE
)

re_asm = re.compile(
    r'(?P<cm>//.*?$|;.*?$|/\*[\s\S]*?\*/|@.*?$)|'
    r'(?P<s>"(?:\\.|[^"\n\\])*"|\'(?:\\.|[^\'\n\\])*\')|'
    r'(?P<label>^\s*[a-zA-Z_.][a-zA-Z0-9_.]*:)|'
    r'(?P<sec>\.[a-zA-Z_][a-zA-Z0-9_.]*\b)|'
    r'(?P<num>\b0x[0-9a-fA-F]+\b|\b0b[01]+\b|#[0-9-]+\b|\b[0-9]+\b)|'
    r'(?P<w>\b[a-zA-Z_][a-zA-Z0-9_]*\b)|'
    r'(?P<sy>[\s\S])',
    re.MULTILINE
)

re_sh = re.compile(
    r'(?P<cm>#.*?$)|'
    r'(?P<s>"(?:\\.|[^"\n\\])*"|\'(?:\\.|[^\'\n\\])*\')|'
    r'(?P<var>\$[a-zA-Z_]\w*|\$\{[^}]+\}|\$\d+|\$[\@\*\#\?\!\$])|'
    r'(?P<num>\b\d+(?:\.\d+)?\b)|'
    r'(?P<w>\b[a-zA-Z_]\w*\b)|'
    r'(?P<sy>[\s\S])',
    re.MULTILINE
)

ext_map = {
    '.py': (re_py, kw_py), '.pyw': (re_py, kw_py),
    '.c': (re_cpp, kw_cpp), '.cpp': (re_cpp, kw_cpp), '.h': (re_cpp, kw_cpp), '.hpp': (re_cpp, kw_cpp), '.cc': (re_cpp, kw_cpp), '.cxx': (re_cpp, kw_cpp),
    '.asm': (re_asm, kw_asm), '.s': (re_asm, kw_asm), '.S': (re_asm, kw_asm),
    '.sh': (re_sh, kw_sh), '.bash': (re_sh, kw_sh), '.zsh': (re_sh, kw_sh),
}

def run(code, th, ext):
    ext_l = ext.lower()
    if ext_l not in ext_map:
        return code

    if th == "rgb":
        o = runi(0, pi2)
        fs = fsin
        return "".join(c if c in (' ','\t','\n','\r') else f"\033[38;2;{int(fs(0.3*i+o)*127+128)};{int(fs(0.3*i+2+o)*127+128)};{int(fs(0.3*i+4+o)*127+128)}m{c}" for i,c in enumerate(code)) + rst
    if th == "hardcore":
        return "".join(t if not t or t.isspace() else f"\033[38;5;{rint(16,231)}m{t}{rst}" for t in re.split(r'(\w+|\s+|.)', code))

    t = themes.get(th, themes["cxx"])
    pk, cn, cm, bg = t["pk"], t["cn"], t["cm"], t.get("bg","")
    pl = t.get("pl", pk)
    rg = t.get("rg", pk)
    rc = bg if bg else rst
    idx = 0
    ona = runi(0, pi2)

    re_e, kws = ext_map[ext_l]

    def rgbs(txt):
        nonlocal idx
        b = []
        fs = fsin
        for c in txt:
            if c in (' ','\t','\n','\r'):
                b.append(c)
            else:
                b.append(f"\033[38;2;{int(fs(0.3*idx+ona)*127+128)};{int(fs(0.3*idx+2+ona)*127+128)};{int(fs(0.3*idx+4+ona)*127+128)}m{c}")
                idx += 1
        return "".join(b) + rst

    mats = list(re_e.finditer(code))
    n = len(mats)
    if n == 0:
        return code

    nxt_val = [""] * n
    curr = ""
    for i in range(n - 1, -1, -1):
        nxt_val[i] = curr
        st = mats[i].group(mats[i].lastgroup).strip()
        if st:
            curr = st

    out = []
    pw = ""
    is_py = ext_l in ('.py', '.pyw')
    is_sh = ext_l in ('.sh', '.bash', '.zsh')

    for i, m in enumerate(mats):
        k = m.lastgroup
        v = m.group(k)

        if k in ('w', 'label'):
            vl = v.strip(':').lower()
            if vl in regs_asm:
                item = f"{rg}{v}{rc}"
            elif vl in kws:
                item = rgbs(v) if th == "rgbNA" else f"{pk}{v}{rc}"
            else:
                fdec = False
                if is_py and pw in ('def', 'class'):
                    fdec = True
                elif is_sh and (pw == 'function' or nxt_val[i].startswith('(')):
                    fdec = True

                item = f"{pl}{v}{rc}" if fdec else v
        elif k == 'var':
            item = v
        elif k in ('sec', 'pr'):
            item = f"{pk}{v}{rc}"
        elif k == 'cm':
            item = f"{cm}{v}{rc}"
        elif k in ('s', 'num'):
            item = f"{cn}{v}{rc}"
        elif k == 'inc':
            item = rsub(r'(#include\s+)([<"][^>"]+[>"])', rf"{pk}\1{cn}\2{rc}", v)
        else:
            item = v

        out.append(item)

        vt = v.strip()
        if vt:
            pw = vl if k == 'w' else vt

    return "".join(out)

def parse_ansi_to_curses_segments(txt):   
    out = []
    cur = []
    cfg, cbg = -1, -1
    i = 0
    n = len(txt)
    rgb_fn = fast_rgb256

    while i < n:
        ch = txt[i]
        if ch == '\033':
            if i + 1 < n and txt[i + 1] == '[':
                end = txt.find('m', i + 2)
                if end != -1:
                    esc = txt[i + 2:end]
                    i = end + 1
                    if not esc or esc == '0':
                        cfg, cbg = -1, -1
                    else:
                        p = esc.split(';')
                        lp = len(p)
                        if lp >= 5 and p[0] == '38' and p[1] == '2':
                            cfg = rgb_fn(int(p[2]), int(p[3]), int(p[4]))
                        elif lp >= 3 and p[0] == '38' and p[1] == '5':
                            cfg = int(p[2])
                        elif lp >= 3 and p[0] == '48' and p[1] == '5':
                            cbg = int(p[2])
                    continue
            i += 1
        elif ch == '\n':
            out.append(cur)
            cur = []
            i += 1
        else:
            e1 = txt.find('\033', i)
            e2 = txt.find('\n', i)
            if e1 == -1: end = e2
            elif e2 == -1: end = e1
            else: end = e1 if e1 < e2 else e2

            if end == -1: end = n

            t = txt[i:end]
            i = end
            if cur and cur[-1][1] == cfg and cur[-1][2] == cbg:
                cur[-1] = (cur[-1][0] + t, cfg, cbg)
            else:
                cur.append((t, cfg, cbg))

    out.append(cur)
    return out