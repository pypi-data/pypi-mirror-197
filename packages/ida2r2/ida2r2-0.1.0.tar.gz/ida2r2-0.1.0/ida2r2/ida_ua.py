import logging

from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj
from .ida_idaapi import BADADDR

LOG_FORMAT = "%(asctime)-15s [%(levelname)s] - %(message)s"
log = logging.getLogger("ida2r2.ida_ua")
log.setLevel(logging.WARN)

def decode_prev_insn(out, ea):
    prev_instr_ea = BADADDR
    try:
        cur_ins = log_exec_r2_cmdj(f"aoj 1 @ {ea}")[0]
        prev_instr_ea = cur_ins["addr"] - cur_ins["size"]
    except:
        log.exception("Could not decode previous instruction to %d", ea)

    out = log_exec_r2_cmdj(f"aoj 1 @ {prev_instr_ea}")[0]
    return prev_instr_ea