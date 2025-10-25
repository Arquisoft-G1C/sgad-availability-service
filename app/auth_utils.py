import os
import requests
from fastapi import Depends, HTTPException, Header, status
from app.config import settings

# ===========================================
# 🔐 VALIDACIÓN JWT CON AUTH-SERVICE
# ===========================================
def validate_token_with_auth_service(token: str) -> dict:
    """
    Envía el token al auth-service para validarlo y obtener información del usuario.
    Retorna un diccionario con los datos del usuario si el token es válido.
    """
    url = f"{settings.AUTH_URL}"

    try:
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado.",
            )

        user_data = response.json()

        # Validar campos mínimos esperados
        if "id" not in user_data or "role" not in user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Respuesta inválida del servicio de autenticación.",
            )

        return user_data

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo contactar con el servicio de autenticación (auth-service).",
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Tiempo de espera agotado al comunicarse con el servicio de autenticación.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# 👤 DEPENDENCIA FASTAPI PARA ÁRBITROS
# ===========================================
def get_current_referee(authorization: str = Header(None)) -> dict:
    """
    Extrae y valida el token JWT desde el header Authorization.
    Retorna los datos del árbitro autenticado.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere un token Bearer válido en el encabezado Authorization.",
        )

    token = authorization.split(" ")[1]
    user_data = validate_token_with_auth_service(token)

    if user_data["role"] != "referee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido: solo los árbitros pueden usar este servicio.",
        )

    print(f"✅ Árbitro autenticado: ID={user_data['id']}")
    return user_data
