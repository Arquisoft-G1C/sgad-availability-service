
# ⚙️ SGAD Availability Service

Microservicio del sistema **SGAD (Sistema de Gestión de Árbitros y Designaciones)** encargado de gestionar la **disponibilidad semanal y horaria de los árbitros**.  
Permite registrar, consultar y cerrar automáticamente las disponibilidades cada semana, integrándose con los microservicios de autenticación y designación.

---

## 🧩 Arquitectura del Microservicio

Este servicio hace parte del ecosistema de microservicios **SGAD**, junto con:

- `sgad-auth-service` → Autenticación y validación JWT.  
- `sgad-referee-management` → Gestión de árbitros.  
- `sgad-match-management` → Gestión de partidos.  
- `sgad-api-gateway` → Enrutamiento y comunicación interna.  
- `sgad-frontend` → Interfaz SSR/Next.js.  
- `sgad-infraestructure` → Configuración de red y base de datos.

---

## 📁 Estructura del Proyecto

```
sgad-availability-service/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth_utils.py
│   ├── scheduler.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── availability_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── availability_service.py
├── tests/
│   └── test_availability.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Instalación Local (Modo Desarrollo)

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/<tu-organizacion>/sgad-availability-service.git
cd sgad-availability-service
```

### 2️⃣ Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # En Linux / Mac
venv\Scripts\activate    # En Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno
```bash
cp .env.example .env
```
Luego edita `.env` con tus credenciales de base de datos y URL del auth-service.

### 5️⃣ Ejecutar la aplicación
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en:
🔗 **http://localhost:8000/docs**

---

## 🐳 Despliegue con Docker

### 1️⃣ Construir la imagen
```bash
docker build -t sgad-availability-service .
```

### 2️⃣ Ejecutar el contenedor
```bash
docker run -d -p 8003:8000 --name sgad-availability     --env-file .env sgad-availability-service
```

### 3️⃣ Verificar estado
```bash
docker logs -f sgad-availability
```

El microservicio estará disponible en:
🔗 **http://localhost:8003/docs**

---

## 🧠 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|-----------|--------------|
| `POST` | `/availability/` | Crear o actualizar disponibilidad diaria. |
| `GET`  | `/availability/me` | Consultar disponibilidad semanal del árbitro autenticado. |
| `GET`  | `/availability/date/{yyyy-mm-dd}` | Listar árbitros disponibles en una fecha específica. |
| `GET`  | `/health` | Verificar estado del servicio. |

---

## 🔒 Autenticación

Todos los endpoints (excepto `/health`) requieren un **token JWT** válido emitido por el `sgad-auth-service`.
Debe enviarse en el encabezado HTTP:

```http
Authorization: Bearer <token>
```

---

## 🕓 Scheduler (Tarea Automática)

El **cierre y expiración semanal** de disponibilidades se ejecuta automáticamente todos los **viernes a las 15:00**, mediante el módulo `APScheduler`.

- Las disponibilidades activas de la semana actual → pasan a **`closed`**.  
- Las de semanas anteriores → pasan a **`expired`**.

Puedes ejecutar manualmente la tarea:
```bash
python -m app.scheduler
```

---

## 🧪 Pruebas Automáticas

Ejecutar todos los tests:
```bash
pytest -v
```

Ejecutar con salida detallada:
```bash
pytest -s
```

---

## 🧱 Variables de Entorno (.env)

| Variable | Descripción | Ejemplo |
|-----------|--------------|----------|
| `DATABASE_URL` | Conexión PostgreSQL | `postgresql://postgres:postgres@sgad-db:5432/sgad_availability` |
| `AUTH_URL` | Endpoint del auth-service | `http://sgad-auth-service:4000/validate` |
| `OPEN_DAY` / `CLOSE_DAY` | Control de ventana de disponibilidad | `thursday` / `friday` |
| `OPEN_HOUR` / `CLOSE_HOUR` | Horarios límite | `8` / `14` |
| `RESET_HOUR` | Hora del cierre semanal | `15` |
| `SECRET_KEY` | Clave interna de servicio | `supersecretkey` |

---

## 🧰 Tecnologías Principales

- 🐍 **Python 3.11**
- ⚡ **FastAPI**
- 🧱 **SQLAlchemy 2.0**
- 🕓 **APScheduler**
- 🧩 **Docker & Docker Compose**
- 🧪 **pytest + httpx**

---

## 👨‍💻 Desarrollado por

**Equipo SGAD – Arquitectura de Software (UNAL, 2025-II)**  
Proyecto académico de Arquitectura de Software: *Sistema de Gestión de Árbitros y Designaciones.*

> 📘 **Nota:** Este microservicio depende del `sgad-auth-service` para la validación de tokens JWT.
