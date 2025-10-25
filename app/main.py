from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.availability_routes import router as availability_router
from app.scheduler import start_scheduler
from app.database import init_db
from app.config import settings

# ================================================
# 🚀 CONFIGURACIÓN INICIAL DEL SERVICIO
# ================================================
app = FastAPI(
    title=settings.SERVICE_NAME,
    version=settings.VERSION,
    description=(
        "SGAD Availability Service 🕓\n"
        "Microservicio encargado de gestionar la disponibilidad semanal y horaria de los árbitros."
    ),
)

# ================================================
# 🌐 CORS (ajusta allow_origins en producción)
# ================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # ← sustituir por dominios del frontend en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================
# 📦 RUTAS PRINCIPALES
# ================================================
app.include_router(availability_router, prefix="/availability", tags=["Availability"])

# ================================================
# ⚙️ EVENTOS DE CICLO DE VIDA
# ================================================
@app.on_event("startup")
async def startup_event():
    print("🚀 Iniciando SGAD Availability Service...")
    init_db()          # Crear tablas si no existen
    start_scheduler()  # Programar cierre/expiración viernes 15:00
    print("✅ Servicio y scheduler listos.")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Apagando SGAD Availability Service...")

# ================================================
# 🧪 ENDPOINT DE SALUD
# ================================================
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": settings.SERVICE_NAME, "version": settings.VERSION}
