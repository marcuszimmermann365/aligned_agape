import math
from typing import Dict, Any, List
def estimate_jacobian_proxy(hidden: List[float]) -> float:
    # A lightweight proxy: sum of absolute differences between neighbors
    if not hidden or len(hidden)<2: return 0.0
    return float(sum(abs(hidden[i+1]-hidden[i]) for i in range(len(hidden)-1)))

def compute_inertia_proxy(series: List[float], window:int=10) -> float:
    if not series: return 1.0
    tail = series[-window:] if len(series)>window else series[:]
    if len(tail)<2: return 1.0
    diffs = [abs(tail[i+1]-tail[i]) for i in range(len(tail)-1)]
    avg = sum(diffs)/max(1,len(diffs))
    # normalize: larger diffs -> lower inertia
    return float(max(0.0, min(1.0, 1.0/(1.0+avg))))
