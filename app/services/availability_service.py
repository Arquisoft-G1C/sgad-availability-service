from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
from fastapi import HTTPException
from app.models import DailyAvailability, AvailabilityStatus
from app.schemas import AvailabilityCreate, AvailabilityResponse, WeeklyAvailabilityResponse

# =====================================================
# 🧩 CREAR O ACTUALIZAR DISPONIBILIDAD
# =====================================================
def create_or_update_availability(db: Session, referee_id: int, data: AvailabilityCreate) -> dict:
    """
    Crea o actualiza la disponibilidad diaria de un árbitro.
    Si ya existe un registro para esa fecha, se actualiza.
    """

    week_start = data.date - timedelta(days=data.date.weekday())

    try:
        existing = (
            db.query(DailyAvailability)
            .filter(
                DailyAvailability.referee_id == referee_id,
                DailyAvailability.date == data.date,
            )
            .first()
        )

        if existing:
            existing.slot_morning = data.slot_morning
            existing.slot_afternoon = data.slot_afternoon
            existing.slot_evening = data.slot_evening
            existing.status = AvailabilityStatus.active
            db.commit()
            db.refresh(existing)
            print(f"🟡 Disponibilidad actualizada: árbitro={referee_id}, fecha={data.date}")
            return {"message": "Disponibilidad actualizada", "data": existing}

        new_record = DailyAvailability(
            referee_id=referee_id,
            date=data.date,
            week_start=week_start,
            slot_morning=data.slot_morning,
            slot_afternoon=data.slot_afternoon,
            slot_evening=data.slot_evening,
            status=AvailabilityStatus.active,
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        print(f"🟢 Nueva disponibilidad creada: árbitro={referee_id}, fecha={data.date}")
        return {"message": "Disponibilidad creada", "data": new_record}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una disponibilidad registrada para la fecha {data.date}."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# 📅 OBTENER DISPONIBILIDAD SEMANAL DEL ÁRBITRO
# =====================================================
def get_my_availability(db: Session, referee_id: int) -> WeeklyAvailabilityResponse:
    """
    Devuelve la disponibilidad del árbitro para la semana actual.
    """
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    records = (
        db.query(DailyAvailability)
        .filter(
            DailyAvailability.referee_id == referee_id,
            DailyAvailability.date.between(week_start, week_end),
        )
        .order_by(DailyAvailability.date)
        .all()
    )

    if not records:
        return {"referee_id": referee_id, "week_start": week_start, "availability": []}

    return {
        "referee_id": referee_id,
        "week_start": week_start,
        "availability": [
            {
                "id": r.id,
                "date": r.date,
                "slot_morning": r.slot_morning,
                "slot_afternoon": r.slot_afternoon,
                "slot_evening": r.slot_evening,
                "status": r.status,
                "created_at": r.created_at
            }
            for r in records
        ],
    }


# =====================================================
# 📆 CONSULTAR DISPONIBILIDAD POR FECHA
# =====================================================
def get_availability_by_date(db: Session, target_date: date) -> list[AvailabilityResponse]:
    """
    Devuelve todos los árbitros disponibles en una fecha específica.
    """
    records = (
        db.query(DailyAvailability)
        .filter(
            DailyAvailability.date == target_date,
            DailyAvailability.status == AvailabilityStatus.active,
        )
        .all()
    )

    if not records:
        print(f"ℹ️ No hay árbitros disponibles para {target_date}")
        return []

    return [
        {
            "referee_id": r.referee_id,
            "date": r.date,
            "slot_morning": r.slot_morning,
            "slot_afternoon": r.slot_afternoon,
            "slot_evening": r.slot_evening,
            "status": r.status
        }
        for r in records
    ]


# =====================================================
# 🕓 CERRAR Y EXPIRAR DISPONIBILIDADES (SCHEDULER)
# =====================================================
def close_and_expire_availability(db: Session) -> dict:
    """
    Marca las disponibilidades activas de la semana actual como 'closed'
    y las anteriores como 'expired'.
    """
    today = date.today()
    current_week_start = today - timedelta(days=today.weekday())

    # Cerrar activas de la semana actual
    closed_count = (
        db.query(DailyAvailability)
        .filter(
            DailyAvailability.week_start == current_week_start,
            DailyAvailability.status == AvailabilityStatus.active,
        )
        .update({DailyAvailability.status: AvailabilityStatus.closed})
    )

    # Expirar semanas anteriores
    expired_count = (
        db.query(DailyAvailability)
        .filter(DailyAvailability.week_start < current_week_start)
        .update({DailyAvailability.status: AvailabilityStatus.expired})
    )

    db.commit()
    print(f"🔁 Cierre semanal: {closed_count} cerradas, {expired_count} expiradas.")
    return {"closed": closed_count, "expired": expired_count}
