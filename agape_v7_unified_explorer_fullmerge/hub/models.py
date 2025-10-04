from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class Agent(BaseModel):
    id: str
    internalState: List[float] = Field(default_factory=list, description="H_i vector")
    actions: List[str] = Field(default_factory=list)

class Baseline(BaseModel):
    gws: float = Field(ge=0.0, le=1.0, default=0.5)
    scm: float = Field(ge=0.0, le=1.0, default=0.5)
    dataSources: List[str] = Field(default_factory=list)

class WorldState(BaseModel):
    baseline: Baseline = Field(default_factory=Baseline)
    agents: List[Agent] = Field(default_factory=lambda: [Agent(id="A", internalState=[0.1,0.0,0.0])])

class JMetrics(BaseModel):
    j1: float = 0.0
    j2: float = 0.0
    j3: float = 0.0
    j4: float = 0.0
    j5: float = 0.0

class CausalExplorerState(BaseModel):
    causalMap: Dict[str, Any] = Field(default_factory=dict)
    simulationOutput: Dict[str, Any] = Field(default_factory=dict)

class EmpiricalGrounderState(BaseModel):
    updatedBaseline: Dict[str, Any] = Field(default_factory=dict)

class GeopoliticalSimulatorState(BaseModel):
    scenario: Dict[str, Any] = Field(default_factory=dict)
    dialogueLog: List[str] = Field(default_factory=list)

class EngineStates(BaseModel):
    causalExplorer: CausalExplorerState = Field(default_factory=CausalExplorerState)
    empiricalGrounder: EmpiricalGrounderState = Field(default_factory=EmpiricalGrounderState)
    geopoliticalSimulator: GeopoliticalSimulatorState = Field(default_factory=GeopoliticalSimulatorState)

class HardwareAnchors(BaseModel):
    throttle: float = Field(ge=0.0, le=1.0, default=1.0)
    ahimsaAlarm: bool = False

class AgapeCoreState(BaseModel):
    sessionId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userQuery: str = ""
    worldState: WorldState = Field(default_factory=WorldState)
    jMetrics: JMetrics = Field(default_factory=JMetrics)
    engineStates: EngineStates = Field(default_factory=EngineStates)
    hardwareAnchors: HardwareAnchors = Field(default_factory=HardwareAnchors)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

    @field_validator("version")
    @classmethod
    def _check_version(cls, v):
        if v != "1.0":
            raise ValueError("StateContract version must be '1.0'")
        return v
