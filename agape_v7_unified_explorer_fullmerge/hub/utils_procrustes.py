from typing import List
def coherence_procrustes_score(h1: List[float], h2: List[float]) -> float:
    # toy basis-invariant-ish similarity: normalized dot
    if not h1 or not h2 or len(h1)!=len(h2): return 0.0
    import math
    n1 = math.sqrt(sum(x*x for x in h1)); n2 = math.sqrt(sum(x*x for x in h2))
    if n1==0 or n2==0: return 0.0
    dot = sum(a*b for a,b in zip(h1,h2))
    c = dot/(n1*n2)
    return float(max(0.0, min(1.0, 0.5*(c+1.0))))
