import os
import logging

from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj
from .ida_idaapi import BADADDR
from .common import get_func_info

LOG_FORMAT = "%(asctime)-15s [%(levelname)s] - %(message)s"
log = logging.getLogger("ida2r2.idc")
log.setLevel(logging.WARN)

# -------------------------------------------
# Constants
# -------------------------------------------
FUNCATTR_START  = 0
FUNCATTR_END    = 4
FUNCATTR_FLAGS  = 8
FUNCATTR_FRAME  = 16
FUNCATTR_FRSIZE = 20
FUNCATTR_FRREGS = 24


INF_SHORT_DN = 0
INF_LONG_DN  = 1
# -------------------------------------------
# Functions
# -------------------------------------------
def get_func_attr(ea, attr):
    if attr == FUNCATTR_START:
        return get_func_start(ea)
    elif attr == FUNCATTR_END:
        return get_func_end(ea)
    
    return BADADDR

def get_func_name(ea):
    try:
        return log_exec_r2_cmdj(f"fdj @ {ea}").get("realname", 0)
    except Exception:
        return 0

def get_func_start(ea):
    finfo = get_func_info(ea)
    if not finfo:
        return BADADDR
    return finfo["offset"]

def get_func_end(ea):
    finfo = get_func_info(ea)
    if not finfo:
        return BADADDR
    return finfo["offset"] + finfo["size"]

def NextFunction(x):
    next_fn   = {}
    all_fns   = log_exec_r2_cmdj("aflj")
    cur_fn_ea = log_exec_r2_cmdj(f"fdj @ {x}").get("offset", x)
    for fn in all_fns:
        if (
            fn["offset"] > cur_fn_ea and
            (not next_fn or fn["offset"] < next_fn["offset"])
        ):
            next_fn = fn

    return next_fn.get("offset", BADADDR)

def get_next_func(ea):
    return NextFunction(ea)

def PrevFunction(x):
    prev_fn   = {}
    all_fns   = log_exec_r2_cmdj("aflj")
    cur_fn_ea = log_exec_r2_cmdj(f"fdj @ {x}").get("offset", x)
    for fn in all_fns:
        if (
            fn["offset"] < cur_fn_ea and
            (not prev_fn or fn["offset"] > prev_fn["offset"])
        ):
            prev_fn = fn

    return prev_fn.get("offset", BADADDR)

def get_prev_func(ea):
    return PrevFunction(ea)

# ----------------------------------------------------------------------
def GetFunctionName(x):
    return get_func_name()

def get_root_filename():
    return os.path.basename(
        log_exec_r2_cmdj("ij").get("core", {}).get("file", "")
    )

def get_idb_path():
    return "YOU HAVE NO POWER HERE FOOL"


def get_sourcefile(ea):
    log_exec_r2_cmd(f"s {ea}")
    source_info = log_exec_r2_cmd(f"CL.")
    if not source_info:
        return None
    
    return source_info.split("\n")[0][6:]

def demangle_name(name, disable_mask):
    lang = "c++"
    demangled = log_exec_r2_cmd(f"iD {lang} {name}")
    if demangled:
        return demangled
    else:
        return name

# TODO Implement
# Get linear address of a name
#      from - the referring address.
#             Allows to retrieve local label addresses in functions.
#             If a local name is not found, then address of a global name is returned.
#      name - name of program byte
# returns: address of the name
#          BADADDR - no such name
# Dummy names (like byte_xxxx where xxxx are hex digits) are parsed by this
# function to obtain the address. The database is not consulted for them.

# long get_name_ea(long from, string name);
# #define get_name_ea_simple(name)  get_name_ea(BADADDR, name)
def get_name_ea(_from, name):
    return ""

# TODO Implement
def get_name_ea_simple(name):
    return ""

MAX_OPCODE_LEN = 15
def PrevInstr(ea):
    prev_instr_ea = BADADDR
    try:
        cur_ins = log_exec_r2_cmdj(f"aoj @ ea")[0]
        prev_instr_ea = cur_ins["addr"] - cur_ins["size"]
    except:
        log.exception("Could not decode previous instruction to %d", ea)
    return prev_instr_ea

# ----------------------------------------------------------
def NFuncUp( fun, n ) :
    i = 0
    f = fun
    while ((i < n) and (f != BADADDR)):
        f = PrevFunction(f)
        i = i+1
    return f


def NFuncDown( fun, n ) :
    i = 0
    f = fun
    while ((i < n) and (f != BADADDR)):
        f = NextFunction(f)
        i = i+1
    return f


def MemCopy( dest, src, length ) :
    log_exec_r2_cmd("oo+")
    log_exec_r2_cmd(f"s {dest}")
    log_exec_r2_cmd(f"wd {src} {length}")

#The "canonical" name format (for now) is <module name>_<func name>_<address>
#where <module_name> and <func_name> are in camel case.
#This is not ideal for a number of reasons but this is a workaround for now

#Return just the "function name" part of the canonical name
def GetCanonicalName(f):
    n = get_func_name(f)
    parts = n.split("_")
    if len(parts) == 3:
        return parts[1]
    else:
        return None

#Put function in canonical format, given the function name and module name
def NameCanonical(f,mod_name,func_name):
    n = "%s_%s_%08x" % (mod_name, func_name, f)
    log.info("Renaming %s to %s", get_func_name(f), n)
    log_exec_r2_cmd(f"afn {n} @ {f}")

#Put function in canonical format when it doesn't have a name, but you know the module name
def RenameFuncWithAddr(f,s):
    func_name = "unk"
    NameCanonical(f,s,func_name)

#Use this if you have pre-existing named functions in the DB that are in non-canonical format
def RenameRangeWithAddr(start,end,s):
    x = start
    while (x<=end):
        n = get_func_name(x)
        if (n.startswith("sub_")):
            RenameFuncWithAddr(x,s)
        else:
            NameCanonical(x,s,n)
        x = NextFunction(x)

#Rename a function in canonical format without changing the module name
def CanonicalFuncRename(f,name):
    n = get_func_name(f)
    parts = n.split("_")
    new_name = "%s_%s_%08x" % (parts[0],name,f)
    log.info("Renaming %s to %s", n, new_name)
    log_exec_r2_cmd(f"afn {new_name} @ {f}")

#Rename the module name without changing the function name
def RenameFuncWithNewMod(f,mod):
    n = get_func_name(f)
    parts = n.split("_")
    new_name = "%s_%s_%08x" % (mod,parts[1],f)
    log.info("Renaming %s to %s", n, new_name)
    log_exec_r2_cmd(f"afn {new_name} @ {f}")

#Rename a module (all functions that start with <mod>_)
def RenameMod(orig, new):
    i = NextFunction(0)
    while (i != BADADDR):
        n = get_func_name(i)
        if n.startswith(orig + "_"):
            RenameFuncWithNewMod(i,new)
        i = NextFunction(i)

#Just rename the module over a given range (can be used to split a module and give part a new name)
def RenameModRange(start, end, new):
    x = start
    while (x<=end):
        n = get_func_name(x)
        RenameFuncWithNewMod(x,new)
        x = NextFunction(x)


# -------------------------------------------
# Strings
# -------------------------------------------
def GetStrLitContents(ea):
    # make sure there is a string at ea
    if not log_exec_r2_cmd(f"fd. @ {ea}").startswith("str."):
        return ""
    
    return log_exec_r2_cmd(f"ps @ {ea}")

def get_strlit_contents(ea):
    return GetStrLitContents(ea)