from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI(title="VisorPoint Backend")

class Target(BaseModel):
    target_id: str
    lat: float
    lon: float
    alt: float | None = None
    updated_at: str
    source: str

current_target = Target(
    target_id="pin_001",
    lat=-29.7600,
    lon=-51.1400,
    alt=35.2,
    updated_at=datetime.now(timezone.utc).isoformat(),
    source="mock"
)

@app.get("/target/current", response_model=Target)
def get_current_target():
    return current_target

@app.post("/target/update", response_model=Target)
def update_target(target: Target):
    global current_target
    current_target = target
    return current_target