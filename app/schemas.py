from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


# ==============================================
# 🧩 ENUM DE ESTADO (para mantener coherencia con el modelo)
# ==============================================
class AvailabilityStatus(str, Enum):
    active = "active"
    closed = "closed"
    expired = "expired"


# ==============================================
# 📥 MODELO DE ENTRADA (POST /availability)
# ==============================================
class AvailabilityCreate(BaseModel):
    date: date = Field(..., description="Fecha específica (YYYY-MM-DD)")
    slot_morning: bool = Field(default=False, description="Disponible en la mañana (07:00–12:00)")
    slot_afternoon: bool = Field(default=False, description="Disponible en la tarde (12:01–17:00)")
    slot_evening: bool = Field(default=False, description="Disponible en la noche (17:01–20:00)")

    @validator("date")
    def validar_fecha(cls, v):
        if v < date.today():
            raise ValueError("La fecha no puede estar en el pasado.")
        return v

    class Config:
        schema_extra = {
            "example": {
                "date": "2025-10-25",
                "slot_morning": True,
                "slot_afternoon": False,
                "slot_evening": True
            }
        }


# ==============================================
# 📤 MODELO DE RESPUESTA INDIVIDUAL
# ==============================================
class AvailabilityResponse(BaseModel):
    id: int
    referee_id: int
    date: date
    week_start: date
    slot_morning: bool
    slot_afternoon: bool
    slot_evening: bool
    status: AvailabilityStatus
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 15,
                "referee_id": 3,
                "date": "2025-10-25",
                "week_start": "2025-10-20",
                "slot_morning": True,
                "slot_afternoon": False,
                "slot_evening": True,
                "status": "active",
                "created_at": "2025-10-24T14:10:23Z"
            }
        }


# ==============================================
# 📅 MODELO DE RESPUESTA SEMANAL (GET /availability/me)
# ==============================================
class WeeklyAvailabilityResponse(BaseModel):
    referee_id: int
    week_start: date
    availability: List[AvailabilityResponse]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "referee_id": 3,
                "week_start": "2025-10-20",
                "availability": [
                    {
                        "id": 15,
                        "date": "2025-10-25",
                        "slot_morning": True,
                        "slot_afternoon": False,
                        "slot_evening": True,
                        "status": "active"
                    },
                    {
                        "id": 16,
                        "date": "2025-10-26",
                        "slot_morning": False,
                        "slot_afternoon": True,
                        "slot_evening": False,
                        "status": "active"
                    }
                ]
            }
        }
