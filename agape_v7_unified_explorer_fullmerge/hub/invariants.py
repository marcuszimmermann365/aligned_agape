from .models import AgapeCoreState
from copy import deepcopy

def enforce_ahimsa(state: AgapeCoreState) -> AgapeCoreState:
    s = deepcopy(state)
    if s.jMetrics.j5 < -0.5:
        s.hardwareAnchors.throttle = 0.0
        s.hardwareAnchors.ahimsaAlarm = True
    return s

def enforce_sync_growth(prev: AgapeCoreState, cur: AgapeCoreState) -> AgapeCoreState:
    s = deepcopy(cur)
    dj4 = s.jMetrics.j4 - prev.jMetrics.j4
    if dj4 > 0.0 and s.worldState.baseline.scm < 0.7:
        # clamp growth
        s.jMetrics.j4 = prev.jMetrics.j4
    return s

def clamp_numeric(state: AgapeCoreState) -> AgapeCoreState:
    s = deepcopy(state)
    # Basic anti-hacking clamps: keep J-metrics and baseline reasonable
    s.jMetrics.j1 = float(max(-10.0, min(10.0, s.jMetrics.j1)))
    s.jMetrics.j2 = float(max(-10.0, min(10.0, s.jMetrics.j2)))
    s.jMetrics.j3 = float(max(-10.0, min(10.0, s.jMetrics.j3)))
    s.jMetrics.j4 = float(max(-10.0, min(10.0, s.jMetrics.j4)))
    s.jMetrics.j5 = float(max(-10.0, min(10.0, s.jMetrics.j5)))
    s.worldState.baseline.gws = float(max(0.0, min(1.0, s.worldState.baseline.gws)))
    s.worldState.baseline.scm = float(max(0.0, min(1.0, s.worldState.baseline.scm)))
    s.hardwareAnchors.throttle = float(max(0.0, min(1.0, s.hardwareAnchors.throttle)))
    return s

def enforce_all(prev: AgapeCoreState, cur: AgapeCoreState) -> AgapeCoreState:
    s = clamp_numeric(cur)
    s = enforce_ahimsa(s)
    s = enforce_sync_growth(prev, s)
    return s
