import os
from dotenv import load_dotenv
from datetime import time

# Cargar variables desde archivo .env
load_dotenv()


class Settings:
    """
    Configuración global del microservicio de disponibilidad SGAD.
    Se cargan desde el entorno o desde .env.
    """

    # --- Información general del servicio ---
    SERVICE_NAME: str = "SGAD Availability Service"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # --- Base de datos ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@db:5432/sgad_availability"
    )

    # --- Conexión con Auth Service ---
    AUTH_URL: str = os.getenv(
        "AUTH_URL",
        "http://sgad-auth-service:4000/validate"
    )

    # --- Ventana de edición de disponibilidad ---
    OPEN_DAY: str = os.getenv("OPEN_DAY", "thursday")    # Día de apertura (jueves)
    OPEN_HOUR: int = int(os.getenv("OPEN_HOUR", 8))      # Hora apertura (08:00)
    CLOSE_DAY: str = os.getenv("CLOSE_DAY", "friday")    # Día de cierre (viernes)
    CLOSE_HOUR: int = int(os.getenv("CLOSE_HOUR", 14))   # Hora cierre (14:00)
    RESET_HOUR: int = int(os.getenv("RESET_HOUR", 15))   # Hora de limpieza (15:00)

    # --- Franjas horarias estándar ---
    MORNING_START: time = time(7, 0)
    MORNING_END: time = time(12, 0)
    AFTERNOON_START: time = time(12, 1)
    AFTERNOON_END: time = time(17, 0)
    EVENING_START: time = time(17, 1)
    EVENING_END: time = time(20, 0)

    # --- Seguridad ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")

    def __repr__(self):
        return f"<Settings env={self.ENVIRONMENT}, db={self.DATABASE_URL}, auth={self.AUTH_URL}>"


# Instancia global accesible desde otros módulos
settings = Settings()
