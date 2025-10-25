from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.database import get_db
from app.schemas import (
    AvailabilityCreate,
    AvailabilityResponse,
    WeeklyAvailabilityResponse
)
from app.services.availability_service import (
    create_or_update_availability,
    get_my_availability,
    get_availability_by_date,
)
from app.auth_utils import get_current_referee


router = APIRouter()


# ==========================================================
# 🧩 POST /availability
# ==========================================================
@router.post(
    "/",
    summary="Crear o actualizar disponibilidad diaria",
    response_model=AvailabilityResponse,
    response_description="Devuelve la disponibilidad creada o actualizada.",
    status_code=status.HTTP_200_OK
)
def post_availability(
    data: AvailabilityCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_referee)
):
    """
    Permite a un árbitro crear o modificar su disponibilidad para una fecha específica.
    Si ya existe un registro para ese día, se actualiza.
    """
    try:
        result = create_or_update_availability(db, user["id"], data)
        return result["data"]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# 📅 GET /availability/me
# ==========================================================
@router.get(
    "/me",
    summary="Consultar disponibilidad semanal del árbitro autenticado",
    response_model=WeeklyAvailabilityResponse,
    response_description="Devuelve la disponibilidad semanal completa del árbitro.",
)
def get_my_weekly_availability(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_referee)
):
    """
    Retorna todas las disponibilidades de la semana actual del árbitro autenticado.
    """
    try:
        return get_my_availability(db, user["id"])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# 📆 GET /availability/date/{yyyy-mm-dd}
# ==========================================================
@router.get(
    "/date/{target_date}",
    summary="Consultar árbitros disponibles en una fecha específica",
    response_model=List[AvailabilityResponse],
    response_description="Devuelve la lista de árbitros con disponibilidad activa para la fecha indicada."
)
def get_availability_by_specific_date(
    target_date: date,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_referee)
):
    """
    Devuelve todos los árbitros disponibles para una fecha específica.
    Puede ser utilizada por coordinadores para realizar designaciones.
    """
    try:
        result = get_availability_by_date(db, target_date)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
