from .models import AgapeCoreState

# simple in-memory store (single-session)
_STATE = AgapeCoreState()

def get_state() -> AgapeCoreState:
    return _STATE

def set_state(new_state: AgapeCoreState) -> AgapeCoreState:
    global _STATE
    _STATE = new_state
    return _STATE
