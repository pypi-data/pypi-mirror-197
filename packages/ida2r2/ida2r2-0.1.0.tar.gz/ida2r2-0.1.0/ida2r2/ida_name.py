import logging

from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj
from .ida_idaapi import BADADDR

LOG_FORMAT = "%(asctime)-15s [%(levelname)s] - %(message)s"
log = logging.getLogger("ida2r2.ida_name")
log.setLevel(logging.WARN)

def set_name(ea, new_name, flags = 0):
    log_exec_r2_cmd(f"s {ea}")
    log_exec_r2_cmd(f"fr {new_name}")

def force_name(ea, new_name, flags = 0):
    return set_name(ea, new_name, flags)

def show_name(ea):
    return log_exec_r2_cmdj(f"fdj. @ {ea}").get("realname")