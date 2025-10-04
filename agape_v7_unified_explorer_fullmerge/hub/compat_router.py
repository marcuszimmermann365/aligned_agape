
from fastapi import APIRouter, Body
from typing import Any, Dict
from .storage import get_state, set_state
from .invariants import enforce_all
from engines.world_state_collector.engine import step as world_step
from engines.causal_explorer.engine import step as causal_step
from engines.geopolitical_sim.engine import step as geo_step

router = APIRouter()

@router.get("/dashboard/state/compact")
def compact_state():
    s = get_state()
    return {
        "j": s.jMetrics.model_dump(),
        "baseline": s.worldState.baseline.model_dump(),
        "hw": s.hardwareAnchors.model_dump(),
        "ts": s.timestamp.isoformat()
    }

@router.get("/metrics/current")
def metrics_current():
    s = get_state()
    return s.jMetrics.model_dump()

@router.get("/metrics/scm_live")
def scm_live():
    s = get_state()
    return {"scm": s.worldState.baseline.scm}

@router.post("/engines/route")
def engines_route(payload: Dict[str, Any] = Body(default_factory=dict)):
    # naive router: engine: v4|v5|v6
    engine = (payload.get("engine") or "").lower()
    prev = get_state()
    if engine == "v5" or engine == "world":
        cur = world_step(prev)
    elif engine == "v4" or engine == "causal":
        cur = causal_step(prev, payload.get("spec") or {})
    elif engine == "v6" or engine == "geo":
        cur = geo_step(prev, payload.get("spec") or {})
    else:
        cur = prev
    cur = enforce_all(prev, cur)
    set_state(cur)
    return cur

@router.post("/engines/{name}/tick")
def engines_tick(name: str, payload: Dict[str, Any] = Body(default_factory=dict)):
    return engines_route({"engine": name, "spec": payload})




from fastapi import Response
from .runtime_metrics import get_anti_series, get_energy_series
from .storage import get_state
from datetime import datetime

@router.get("/metrics/anti")
def metrics_anti():
    s = get_state()
    series = get_anti_series()
    return {"anti_series": series, "latest": series[-1] if series else 0.0, "scm": s.worldState.baseline.scm}

@router.get("/metrics/conservation")
def metrics_conservation():
    series = get_energy_series()
    return {"energy_series": series, "latest": series[-1] if series else 0.0}

@router.get("/engines/status")
def engines_status():
    s = get_state()
    return {
        "ts": s.timestamp.isoformat(),
        "last_j": s.jMetrics.model_dump(),
        "baseline": s.worldState.baseline.model_dump(),
        "geo_log_len": len(s.engineStates.geopoliticalSimulator.dialogueLog or [])
    }

@router.get("/export/csv/snapshots")
def export_csv_snapshots():
    s = get_state()
    rows = [
        "ts,j1,j2,j3,j4,j5,gws,scm,throttle,alarm",
        f"{s.timestamp.isoformat()},{s.jMetrics.j1:.6f},{s.jMetrics.j2:.6f},{s.jMetrics.j3:.6f},{s.jMetrics.j4:.6f},{s.jMetrics.j5:.6f},{s.worldState.baseline.gws:.6f},{s.worldState.baseline.scm:.6f},{s.hardwareAnchors.throttle:.6f},{int(s.hardwareAnchors.ahimsaAlarm)}"
    ]
    data = "\n".join(rows)
    return Response(content=data, media_type="text/csv")

@router.get("/export/csv/series")
def export_csv_series():
    e = get_energy_series()
    a = get_anti_series()
    rows = ["idx,energy,anti"]
    n = max(len(e), len(a))
    for i in range(n):
        ei = e[i] if i < len(e) else ""
        ai = a[i] if i < len(a) else ""
        rows.append(f"{i},{ei},{ai}")
    data = "\n".join(rows)
    return Response(content=data, media_type="text/csv")
