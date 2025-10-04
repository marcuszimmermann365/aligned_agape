from collections import deque
from typing import Deque, Dict, Any
ANTI_SERIES: Deque[float] = deque(maxlen=256)
ENERGY_SERIES: Deque[float] = deque(maxlen=256)
def push_anti(x: float): ANTI_SERIES.append(float(x))
def push_energy(x: float): ENERGY_SERIES.append(float(x))
def get_anti_series(): return list(ANTI_SERIES)
def get_energy_series(): return list(ENERGY_SERIES)
