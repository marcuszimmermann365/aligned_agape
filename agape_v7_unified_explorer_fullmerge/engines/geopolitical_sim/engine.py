from typing import Dict, Any
from datetime import datetime
import math, random
from ...hub.models import AgapeCoreState
from ...hub.utils_anti import estimate_jacobian_proxy, compute_inertia_proxy
from ...hub.utils_conservation import compute_conservation_energy
from ...hub.runtime_metrics import push_anti, push_energy

def _toy_turn_lines():
    lines = [
        "Actor A: proposes limited monitoring.",
        "Actor B: accepts monitoring, requests phased sanctions relief.",
        "Actor C: requests maritime safety corridor and seasonal quotas."
    ]
    return lines

def step(state: AgapeCoreState, payload: Dict[str, Any]) -> AgapeCoreState:
    """
    Simulate one lightweight 'turn' in a geopolitical scenario:
    - Slightly improve integration and diversity if dialogue progresses.
    - Compute a proxy harm (negative values) with noise; j5 nudges towards mild positive.
    - Keep changes small; hub invariants will clamp/gate.
    """
    s = state.model_copy(deep=True)
    dlg = s.engineStates.geopoliticalSimulator.dialogueLog
    dlg.extend(_toy_turn_lines())

    # toy hidden "progress" flag
    prog = 0.03 + 0.02 * random.random()
    s.jMetrics.j1 += prog            # integration
    s.jMetrics.j2 += 0.5 * prog      # diversity
    s.jMetrics.j3 += 0.2 * prog      # robustness

    # empowerment changes only a tad (hub will clamp if SCM < 0.7)
    s.jMetrics.j4 += 0.05 * prog

    # j5 causal-proxy (higher is less harm). keep around small positive with noise
    s.jMetrics.j5 += 0.03 - 0.06 * random.random()

    # SCM gently improves with successful talk
    s.worldState.baseline.scm += 0.02

    s.timestamp = datetime.utcnow()
    # push metrics
    try:
        vec = (s.worldState.agents[0].internalState if s.worldState.agents else [])
        push_energy(compute_conservation_energy(vec))
        push_anti(estimate_jacobian_proxy(vec))
    except Exception:
        pass
    return s
