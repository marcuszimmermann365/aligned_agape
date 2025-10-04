from typing import List
def compute_conservation_energy(vec: List[float]) -> float:
    # toy 'energy' = sum of squares
    return float(sum((x*x) for x in (vec or [])))
