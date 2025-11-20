from pydantic import BaseModel, Field, field_validator
from datetime import date as DateType, datetime as DateTimeType
from typing import Optional, List
from enum import Enum

# ==============================================
# 🧩 ENUM DE ESTADO
# ==============================================
class AvailabilityStatus(str, Enum):
    active = "active"
    closed = "closed"
    expired = "expired"


# ==============================================
# 📥 MODELO DE ENTRADA
# ==============================================
class AvailabilityCreate(BaseModel):
    availability_date: DateType = Field(..., description="Fecha específica (YYYY-MM-DD)")
    slot_morning: bool = Field(default=False, description="Disponible en la mañana (07:00–12:00)")
    slot_afternoon: bool = Field(default=False, description="Disponible en la tarde (12:01–17:00)")
    slot_evening: bool = Field(default=False, description="Disponible en la noche (17:01–20:00)")

    @field_validator("availability_date")
    def validar_fecha(cls, v):
        if v < DateType.today():
            raise ValueError("La fecha no puede estar en el pasado.")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "availability_date": "2025-10-25",
                "slot_morning": True,
                "slot_afternoon": False,
                "slot_evening": True
            }
        }
    }


# ==============================================
# 📤 MODELO DE RESPUESTA INDIVIDUAL
# ==============================================
class AvailabilityResponse(BaseModel):
    id: int
    referee_id: int
    availability_date: DateType
    week_start_date: DateType
    slot_morning: bool
    slot_afternoon: bool
    slot_evening: bool
    status: AvailabilityStatus
    created_timestamp: DateTimeType

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 15,
                "referee_id": 3,
                "availability_date": "2025-10-25",
                "week_start_date": "2025-10-20",
                "slot_morning": True,
                "slot_afternoon": False,
                "slot_evening": True,
                "status": "active",
                "created_timestamp": "2025-10-24T14:10:23Z"
            }
        }
    }


# ==============================================
# 📅 MODELO DE RESPUESTA SEMANAL
# ==============================================
class WeeklyAvailabilityResponse(BaseModel):
    referee_id: int
    week_start_date: DateType
    availability: List[AvailabilityResponse]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "referee_id": 3,
                "week_start_date": "2025-10-20",
                "availability": [
                    {
                        "id": 15,
                        "availability_date": "2025-10-25",
                        "slot_morning": True,
                        "slot_afternoon": False,
                        "slot_evening": True,
                        "status": "active"
                    },
                    {
                        "id": 16,
                        "availability_date": "2025-10-26",
                        "slot_morning": False,
                        "slot_afternoon": True,
                        "slot_evening": False,
                        "status": "active"
                    }
                ]
            }
        }
    }
