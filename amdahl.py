import math
K = 0.9 # TODO: change by your system model

def amdahl(c: int, core: int) -> int:
    return math.ceil(K*math.ceil(c/core))+math.ceil((1-K)*c)