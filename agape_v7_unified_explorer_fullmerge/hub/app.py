from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

from .models import AgapeCoreState, JMetrics
from .storage import get_state, set_state
from .invariants import enforce_all
from .runtime_metrics import push_anti, push_energy

from engines.world_state_collector.engine import step as world_step
from engines.causal_explorer.engine import step as causal_step
from engines.geopolitical_sim.engine import step as geo_step

app = FastAPI(title="Agape V7.0 - Unified Explorer")
from .compat_router import router as compat_router
app.include_router(compat_router)


# serve static dashboard
app.mount("/static", StaticFiles(directory="dashboard"), name="static")

@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

@app.get("/state/get", response_model=AgapeCoreState)
def get_current_state():
    return get_state()

class Delta(BaseModel):
    jMetrics: Dict[str, float] | None = None
    worldBaseline: Dict[str, float] | None = None
    hardware: Dict[str, Any] | None = None

@app.post("/state/update", response_model=AgapeCoreState)
def update_state(delta: Delta = Body(...)):
    prev = get_state()
    cur = prev.model_copy(deep=True)

    if delta.jMetrics:
        jm = cur.jMetrics
        for k, v in delta.jMetrics.items():
            if hasattr(jm, k):
                setattr(jm, k, float(v))

    if delta.worldBaseline:
        bl = cur.worldState.baseline
        for k, v in delta.worldBaseline.items():
            if hasattr(bl, k):
                setattr(bl, k, float(v))

    if delta.hardware:
        hw = cur.hardwareAnchors
        for k, v in delta.hardware.items():
            if hasattr(hw, k):
                setattr(hw, k, v)

    cur.timestamp = datetime.utcnow()
    cur = enforce_all(prev, cur)
    set_state(cur)
    return cur

@app.post("/engine/world/step", response_model=AgapeCoreState)
def step_world():
    prev = get_state()
    cur = world_step(prev)
    cur = enforce_all(prev, cur)
    set_state(cur)
    return cur

@app.post("/engine/causal/step", response_model=AgapeCoreState)
def step_causal(payload: Dict[str, Any] = Body(default_factory=dict)):
    prev = get_state()
    cur = causal_step(prev, payload or {})
    cur = enforce_all(prev, cur)
    set_state(cur)
    return cur

@app.post("/engine/geo/step", response_model=AgapeCoreState)
def step_geo(payload: Dict[str, Any] = Body(default_factory=dict)):
    prev = get_state()
    cur = geo_step(prev, payload or {})
    cur = enforce_all(prev, cur)
    set_state(cur)
    return cur
