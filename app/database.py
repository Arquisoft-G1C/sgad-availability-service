import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ===============================================
# ⚙️ CONFIGURACIÓN DE LA CONEXIÓN
# ===============================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@db:5432/sgad_availability"
)

# Motor de conexión con ping automático (evita desconexiones)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # cambiar a True para depurar SQL
)

# Sesión de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base declarativa (para los modelos)
Base = declarative_base()

# ===============================================
# 🧩 DEPENDENCIA DE SESIÓN (para usar en FastAPI)
# ===============================================
def get_db():
    """
    Crea una sesión de base de datos por solicitud.
    Se cierra automáticamente al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===============================================
# 🧱 INICIALIZACIÓN DE TABLAS
# ===============================================
def init_db():
    """
    Crea todas las tablas si no existen.
    Se ejecuta automáticamente al iniciar la app (main.py).
    """
    from app.models import DailyAvailability  # Import local para evitar dependencias circulares
    print("🔧 Creando tablas en la base de datos si no existen...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos lista y operativa.")
