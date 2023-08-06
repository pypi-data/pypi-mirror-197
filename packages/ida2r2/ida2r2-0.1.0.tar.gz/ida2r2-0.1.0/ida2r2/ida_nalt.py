import logging

from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj, invalidate_cache
from .ida_idaapi import BADADDR

LOG_FORMAT = "%(asctime)-15s [%(levelname)s] - %(message)s"
log = logging.getLogger("ida2r2.ida_nalt")
log.setLevel(logging.WARN)

STRTYPE_TERMCHR   = 0
STRTYPE_C         = 0
STRTYPE_C_16      = 1
STRTYPE_C_32      = 2
STRTYPE_PASCAL    = 4
STRTYPE_PASCAL_16 = 5
STRTYPE_LEN2      = 8
STRTYPE_LEN2_16   = 9
STRTYPE_LEN4      = 0xC
STRTYPE_LEN4_16   = 0xD
NALT_STRTYPE      = 0x10

R2_STR_TYPE_TO_NALT = {
    "ascii": STRTYPE_C
}

def get_str_type(ea):
    # make sure there is a string at ea
    if not log_exec_r2_cmd(f"fd. @ {ea}").startswith("str."):
        return 0
    _str = log_exec_r2_cmdj(f"psj @ {ea}")
    return R2_STR_TYPE_TO_NALT[_str["type"]]