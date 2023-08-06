from .r2 import log_exec_r2_cmd, log_exec_r2_cmdj

def get_func_info(ea):
    fns = log_exec_r2_cmdj("aflj")
    for fn in fns:
        if ea >= fn["offset"] and ea <= fn["offset"] + fn["size"]:
            return fn
    return {}

# -------------------------------------------
#                   Classes
# -------------------------------------------

class String:
    def __init__(self, sinfo):
        self.r2_info = sinfo
        self.ea      = sinfo["vaddr"]
        self.length  = sinfo["length"]
        self.content = sinfo["string"]
        self.type    = sinfo["type"]

    def __repr__(self) -> str:
        return f"{self.content} @ 0x{self.ea:x}"
    
    def __str__(self):
        return self.content


class Function:
    def __init__(self, finfo):
        self.r2_info = finfo
        self.name    = finfo["name"]
        self.startEA = finfo["offset"]
        self.endEA   = finfo["offset"] + finfo["size"]
        self.start_ea = self.startEA
        self.end_ea   = self.endEA

    def __repr__(self) -> str:
        return f"Function '{self.name}' @ 0x{self.ea:x}"


class FlowGraph:
    def __init__(self, f: Function):
        self.f   = f
        self.bbs = []
        self.build_flowchart()

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._bb_index < len(self.bbs):
            bb = self.bbs[self._bb_index]
            self._bb_index += 1
            return bb
        else:
            raise StopIteration()

    def build_flowchart(self):
        self.bbs = [
            Block(bb) for bb in log_exec_r2_cmdj(f"afbj @ {self.f.startEA}")
        ]
        self._bb_index = 0

class Block:
    def __init__(self, binfo):
        self.r2_info  = binfo
        self.start_ea = binfo["addr"]
        self.end_ea   = binfo["addr"] + binfo["size"]

    def __repr__(self):
        return f"BB @ 0x{self.start_ea:x} - 0x{self.end_ea:x}"
    

class Segment:
    def __init__(self, sinfo):
        self.r2_info  = sinfo
        self.name     = sinfo["name"]
        self.start_ea = int(sinfo["vaddr"])
        self.end_ea   = self.start_ea + int(sinfo["vsize"])

    def __repr__(self):
        return f"Segment {self.name} @ 0x{self.start_ea:x} - 0x{self.end_ea:x}"