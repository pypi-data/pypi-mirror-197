import logging

from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj
from .ida_idaapi import BADADDR
from .idc import get_prev_func as idc_get_prev_func
from .idc import get_next_func as idc_get_next_func

def get_prev_func(ea):
    return idc_get_prev_func(ea)

def get_next_func(ea):
    return idc_get_next_func(ea)