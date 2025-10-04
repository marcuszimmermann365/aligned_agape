from typing import Dict, Any
from datetime import datetime
from ...hub.models import AgapeCoreState
from ...hub.utils_anti import estimate_jacobian_proxy, compute_inertia_proxy
from ...hub.utils_conservation import compute_conservation_energy
from ...hub.runtime_metrics import push_anti, push_energy

def step(state: AgapeCoreState, causal_spec: Dict[str, Any]) -> AgapeCoreState:
    """
    Apply a small what-if causal spec. We support keys:
      - 'j4_delta' (float): desired empowerment delta
      - 'scm_delta' (float): desired SCM change
      - 'gws_delta' (float): desired GWS change
      - 'notes' (str): human-readable
    Synchronous Growth will clamp positive j4 growth if SCM < 0.7 (enforced by hub).
    """
    s = state.model_copy(deep=True)

    j4d = float(causal_spec.get("j4_delta", 0.0))
    scmd = float(causal_spec.get("scm_delta", 0.0))
    gwsd = float(causal_spec.get("gws_delta", 0.0))

    # apply naive deltas
    s.jMetrics.j4 += j4d
    s.worldState.baseline.scm += scmd
    s.worldState.baseline.gws += gwsd

    # annotate
    s.engineStates.causalExplorer.causalMap = {"inputs": causal_spec}
    s.engineStates.causalExplorer.simulationOutput = {
        "applied": {"j4_delta": j4d, "scm_delta": scmd, "gws_delta": gwsd},
        "note": causal_spec.get("notes", "n/a")
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
