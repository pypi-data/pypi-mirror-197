from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj
from .ida_idaapi import BADADDR
from .common import get_func_info, Function, FlowGraph

def get_func(ea):
    finfo = get_func_info(ea)
    if not finfo:
        return None
    return Function(finfo)

def FlowChart(f: Function):
    return FlowGraph(f)