from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional

app = FastAPI(title="VisorPoint Backend")

class Pin(BaseModel):
    pin_id: str
    name: str
    lat: float
    lon: float
    alt: Optional[float] = None
    color: Optional[str] = None
    updated_at: Optional[str] = None
    source: str = "unknown"

class ActiveTarget(BaseModel):
    pin_id: str
    name: str
    lat: float
    lon: float
    alt: Optional[float] = None
    selected_at: str
    source: str

pins_db: dict[str, Pin] = {}

active_target: Optional[ActiveTarget] = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/pins")
def get_pins():
    return list(pins_db.values())


@app.post("/pins/upsert")
def upsert_pin(pin: Pin):
    if not pin.updated_at:
        pin.updated_at = now_iso()

    pins_db[pin.pin_id] = pin
    return {
        "status": "upserted",
        "pin_id": pin.pin_id
    }


@app.post("/target/activate")
def activate_target(payload: dict):
    global active_target

    pin_id = payload.get("pin_id")
    if not pin_id:
        raise HTTPException(status_code=400, detail="pin_id is required")

    pin = pins_db.get(pin_id)
    if not pin:
        raise HTTPException(status_code=404, detail="pin not found")

    active_target = ActiveTarget(
        pin_id=pin.pin_id,
        name=pin.name,
        lat=pin.lat,
        lon=pin.lon,
        alt=pin.alt,
        selected_at=now_iso(),
        source=pin.source
    )

    return {
        "status": "activated",
        "pin_id": pin.pin_id,
        "name": pin.name
    }


@app.get("/target/current")
def get_current_target():
    if active_target is None:
        raise HTTPException(status_code=404, detail="no active target")
    return active_target