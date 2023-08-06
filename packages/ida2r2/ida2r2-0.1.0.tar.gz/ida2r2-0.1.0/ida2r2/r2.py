import time
import r2pipe
import logging

#-----------------------------------------------------------------------
r2 = None

LOG_FORMAT = "%(asctime)-15s [%(levelname)s] - %(message)s"
log = logging.getLogger("ida2r2")
log.setLevel(logging.WARN)

#-----------------------------------------------------------------------
def get_r2():
    return r2

def set_r2_instance(r2_inst):
    global r2
    r2 = r2_inst

def invalidate_cache():
    r2.invalidate_cache()

def log_exec_r2_cmdj(cmd):
    s = time.time()
    r = r2.cmdj(cmd)
    log.debug("R2 CMDJ: %s: %.6fs", cmd, time.time() - s)
    return r

def log_exec_r2_cmd(cmd):
    s = time.time()
    r = r2.cmd(cmd)
    log.debug("R2 CMD: %s: %.6fs", cmd, time.time() - s)
    return r