from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj
from .ida_idaapi import BADADDR
from .common import Segment

def get_segm_by_name(n):
    # IDA segments are what's commonly called sections
    sections = log_exec_r2_cmdj("iSj")
    section = None
    for s in sections:
        if s["name"] == n:
            section = s

    return Segment(section)

def SegmByName(name):
    return get_segm_by_name(name)