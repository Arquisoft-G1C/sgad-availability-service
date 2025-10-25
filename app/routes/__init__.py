"""
Inicializador del paquete de rutas de SGAD Availability Service.

Expone directamente el router principal (availability_router)
para permitir una importación más limpia en app/main.py:
    from app.routes import availability_router
"""

from .availability_routes import router as availability_router
