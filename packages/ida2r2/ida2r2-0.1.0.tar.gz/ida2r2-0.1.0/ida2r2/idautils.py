from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj
from .ida_idaapi import BADADDR
from .common import get_func_info, String

def CodeRefsTo(target, flow = 1):
    # Return a list of code references to address 'x'. The value 'y',
    # in IDA, is used to consider the previous instruction (y=1) as a valid
    # code reference or if it should be ignored (y=0).
    xrefs = log_exec_r2_cmdj(f"axtj @ {target}")
    return [x["from"] for x in xrefs if x["type"] == "CALL" or x["type"] == "CODE"]


def CodeRefsFrom(ea, flow = 1):
    xrefs = log_exec_r2_cmdj(f"axfj @ {ea}")
    return [x["to"] for x in xrefs if x["type"] == "CALL" or x["type"] == "CODE"]

# This function is not part of idautils
# It is added just for convenience
def CodeRefsFromFn(ea):
    xrefs = log_exec_r2_cmdj(f"axffj @ {ea}")
    return [x["ref"] for x in xrefs if x["type"] == "CALL"]


def DataRefsFrom(ea, flow = 1):
    xrefs = log_exec_r2_cmdj(f"axfj @ {ea}")
    return [x["to"] for x in xrefs if x["type"] == "DATA" or x["type"] == "STRN"]


def DataRefsTo(ea, flow = 1):
    xrefs = log_exec_r2_cmdj(f"axtj @ {ea}")
    return [x["from"] for x in xrefs if x["type"] == "DATA" or x["type"] == "STRN"]

# -------------------------------------------
def FuncItems(ea):
    finfo = get_func_info(ea)
    if not finfo:
        return []
    
    instrs = log_exec_r2_cmdj(f"aoj {finfo['size']} @ {finfo['offset']}")
    return [int(i["addr"]) for i in instrs]

def Functions():
    functions = log_exec_r2_cmdj("aflj")
    return [f["offset"] for f in functions]

def Heads(start, end):
    # res = log_exec_r2_cmd(f"pid {size} @ {ea}~[0]").strip()
    # addrs = filter(None, [int16(x) for x in res.split("\n")])
    # # Remove duplicates
    # return list(dict.fromkeys(addrs))
    ops = log_exec_r2_cmdj(f"aoj {end - start} @ {start}")
    return [op["addr"] for op in ops]

def Names():
    names = log_exec_r2_cmdj("fj")
    for name in names:
        yield (name["offset"], name["name"].split(".")[-1])

def Strings():
    strings = log_exec_r2_cmdj("izzzj")
    return [String(s) for s in strings]