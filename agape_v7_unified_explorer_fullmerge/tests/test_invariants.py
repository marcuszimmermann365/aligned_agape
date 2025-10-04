from hub.models import AgapeCoreState, JMetrics
from hub.invariants import enforce_all

def test_ahimsa_alarm():
    prev = AgapeCoreState()
    cur = prev.model_copy(deep=True)
    cur.jMetrics.j5 = -1.0
    out = enforce_all(prev, cur)
    assert out.hardwareAnchors.ahimsaAlarm is True
    assert out.hardwareAnchors.throttle == 0.0

def test_sync_growth_gate():
    prev = AgapeCoreState()
    cur = prev.model_copy(deep=True)
    cur.jMetrics.j4 = prev.jMetrics.j4 + 0.5
    cur.worldState.baseline.scm = 0.6
    out = enforce_all(prev, cur)
    # should clamp j4 back if scm<0.7
    assert abs(out.jMetrics.j4 - prev.jMetrics.j4) < 1e-9

def test_clamps():
    prev = AgapeCoreState()
    cur = prev.model_copy(deep=True)
    cur.jMetrics.j1 = 999
    cur.worldState.baseline.gws = -5
    out = enforce_all(prev, cur)
    assert out.jMetrics.j1 <= 10.0
    assert 0.0 <= out.worldState.baseline.gws <= 1.0
