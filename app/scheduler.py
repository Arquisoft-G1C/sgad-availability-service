from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.database import SessionLocal
from app.services.availability_service import close_and_expire_availability

# Instancia global del programador
scheduler = BackgroundScheduler()
scheduler_started = False  # Evita inicialización múltiple en modo reload

# ==========================================================
# 🕓 TAREA AUTOMÁTICA: CIERRE Y EXPIRACIÓN SEMANAL
# ==========================================================
def job_close_and_expire():
    """
    Marca las disponibilidades activas de la semana actual como 'closed'
    y las anteriores como 'expired'.
    Se ejecuta automáticamente todos los viernes a las 15:00.
    """
    print(f"⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ejecutando tarea semanal de cierre...")

    db = SessionLocal()
    try:
        result = close_and_expire_availability(db)
        print(f"✅ Cierre completado → Cerradas: {result['closed']}, Expiradas: {result['expired']}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error en la tarea de cierre semanal: {e}")
    finally:
        db.close()


# ==========================================================
# 🚀 INICIALIZACIÓN DEL SCHEDULER
# ==========================================================
def start_scheduler():
    """
    Inicia el programador en segundo plano.
    Se llama automáticamente desde main.py al evento startup.
    Previene inicialización múltiple en modo reload.
    """
    global scheduler_started
    if scheduler_started:
        print("⚠️ Scheduler ya estaba en ejecución, se omite reinicio.")
        return

    scheduler.add_job(job_close_and_expire, "cron", day_of_week="fri", hour=15, minute=0)
    scheduler.start()
    scheduler_started = True
    print("🗓️ Scheduler iniciado: cierre automático cada viernes a las 15:00.")
