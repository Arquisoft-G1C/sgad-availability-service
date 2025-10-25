from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    Date,
    DateTime,
    String,
    Enum,
    UniqueConstraint,
    Index
)
from datetime import datetime
from app.database import Base
import enum


# ===============================================
# 🧱 ENUMS Y MODELOS
# ===============================================
class AvailabilityStatus(str, enum.Enum):
    """Estados válidos de una disponibilidad semanal."""
    active = "active"
    closed = "closed"
    expired = "expired"


class DailyAvailability(Base):
    """
    Representa la disponibilidad horaria de un árbitro en un día específico.
    Cada registro es único por árbitro y fecha.
    """

    __tablename__ = "daily_availability"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Identificador del árbitro (desde auth-service)
    referee_id = Column(Integer, nullable=False, index=True)

    # Fecha específica (día)
    date = Column(Date, nullable=False, index=True)

    # Lunes correspondiente a esa semana
    week_start = Column(Date, nullable=False)

    # Franjas horarias
    slot_morning = Column(Boolean, default=False)   # 07:00–12:00
    slot_afternoon = Column(Boolean, default=False) # 12:01–17:00
    slot_evening = Column(Boolean, default=False)   # 17:01–20:00

    # Estado del registro (active, closed, expired)
    status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.active)

    # Fecha de creación
    created_at = Column(DateTime, default=datetime.utcnow)

    # ===============================================
    # 🔒 Restricciones y optimización
    # ===============================================
    __table_args__ = (
        UniqueConstraint("referee_id", "date", name="uq_referee_date"),
        Index("ix_referee_week", "referee_id", "week_start"),
    )

    # ===============================================
    # 🧠 Representación para depuración
    # ===============================================
    def __repr__(self):
        return (
            f"<DailyAvailability("
            f"id={self.id}, referee_id={self.referee_id}, date={self.date}, "
            f"morning={self.slot_morning}, afternoon={self.slot_afternoon}, "
            f"evening={self.slot_evening}, status={self.status.value})>"
        )
