# Agape V7.0 — Unified Explorer (Monorepo)

This repository is a runnable skeleton that implements the **Agape Core State Hub**, three engines
(**WorldStateCollector**, **CausalExplorerEngine**, **GeopoliticalSimulatorEngine**), a minimal
**Unified Dashboard**, and a basic **test-suite**. It follows the **StateContract V1.0** and
enforces the key invariants (Ahimsa Alarm, Synchronous Growth, Anti-Hacking clamps).

> Target: Python 3.11, CPU-only. Works with `uvicorn` + `fastapi`.

## 1) Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Run the Hub (API + static dashboard)
```bash
uvicorn hub.app:app --host 127.0.0.1 --port 8000 --reload
# open dashboard:
# http://127.0.0.1:8000/static/index.html
```

## 3) Try the flow
- Health: `GET /health`
- Get state: `GET /state/get`
- Step engines (order is flexible):
  - `POST /engine/world/step`
  - `POST /engine/causal/step`   (with a small causal spec JSON)
  - `POST /engine/geo/step`

## 4) Tests
```bash
pytest -q
```
