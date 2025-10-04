PY?=python
PIP?=$(PY) -m pip

venv:
	$(PY) -m venv .venv && . .venv/bin/activate && $(PIP) install --upgrade pip

install: venv
	. .venv/bin/activate && $(PIP) install -r requirements.txt

run:
	. .venv/bin/activate && uvicorn hub.app:app --host 127.0.0.1 --port 8000 --reload

test:
	. .venv/bin/activate && pytest -q
