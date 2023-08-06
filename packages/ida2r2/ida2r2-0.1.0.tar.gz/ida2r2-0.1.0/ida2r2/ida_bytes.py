import logging

from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj, invalidate_cache
from .ida_idaapi import BADADDR

LOG_FORMAT = "%(asctime)-15s [%(levelname)s] - %(message)s"
log = logging.getLogger("ida2r2.ida_bytes")
log.setLevel(logging.WARN)

def patch_byte(ea, x):
    if x > 0xFF:
        return
    log_exec_r2_cmd("oo+")
    log_exec_r2_cmd(f"s {ea}")
    log_exec_r2_cmd(f"wx 0x{x:02x}")
    invalidate_cache()

def copy_bytes(src, dest, length):
    log_exec_r2_cmd("oo+")
    log_exec_r2_cmd(f"s {dest}")
    log_exec_r2_cmd(f"wd {src} {length}")
    invalidate_cache()

def get_byte(ea):
    return log_exec_r2_cmdj(f"pxj 1 @ {ea}")[0]

def get_max_strlit_length(ea, str_type):
    # make sure there is a string at ea
    if not log_exec_r2_cmd(f"fd. @ {ea}").startswith("str."):
        return 0
    _str = log_exec_r2_cmdj(f"psj @ {ea}")
    return _str["length"]

def get_strlit_contents(ea, potential_len, str_type):
    if not log_exec_r2_cmd(f"fd. @ {ea}").startswith("str."):
        return b""
    return log_exec_r2_cmd(f"ps @ {ea}").encode("utf-8")