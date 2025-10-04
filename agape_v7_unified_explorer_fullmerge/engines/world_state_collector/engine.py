from typing import Dict, Any
from datetime import datetime
from ...hub.models import AgapeCoreState
from ...hub.utils_anti import estimate_jacobian_proxy, compute_inertia_proxy
from ...hub.utils_conservation import compute_conservation_energy
from ...hub.runtime_metrics import push_anti, push_energy

def step(state: AgapeCoreState) -> AgapeCoreState:
    """
    Simulate fetching a new world baseline snapshot and gently move
    GWS and SCM towards slightly improved values (bounded).
    """
    s = state.model_copy(deep=True)
    bl = s.worldState.baseline
    # tiny smoothing towards 0.55/0.6
    target_gws, target_scm = 0.55, 0.60
    bl.gws = bl.gws + 0.1 * (target_gws - bl.gws)
    bl.scm = bl.scm + 0.1 * (target_scm - bl.scm)
    # meta: mark updatedBaseline in engine state
    s.engineStates.empiricalGrounder.updatedBaseline = {
        "as_of": datetime.utcnow().isoformat(),
        "gws": bl.gws,
        "scm": bl.scm,
        "sources": ["mock://worldbank", "mock://gpi"]
    }
    s.timestamp = datetime.utcnow()
    # push metrics
    try:
        vec = (s.worldState.agents[0].internalState if s.worldState.agents else [])
        push_energy(compute_conservation_energy(vec))
        push_anti(estimate_jacobian_proxy(vec))
    except Exception:
        pass
    return s
