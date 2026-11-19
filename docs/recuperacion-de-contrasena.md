# Recuperación de contraseña

El usuario que olvidó su contraseña recibe por correo un **código de 6
dígitos**, lo escribe en la app y elige una contraseña nueva.

## Endpoints

| Método y ruta | Cuerpo | Respuestas |
|---|---|---|
| `POST /auth/forgot-password` | `{"email"}` | `202` siempre con el mismo mensaje, exista o no la cuenta. `429` si hay demasiadas solicitudes. |
| `POST /auth/verify-reset-code` | `{"email", "code"}` | `200 {"valid": true}` o `400 {"detail": "Código inválido o expirado"}`. Opcional: valida el código antes de pedir la contraseña nueva. No lo consume, pero los fallos cuentan. |
| `POST /auth/reset-password` | `{"email", "code", "new_password"}` | `200` con mensaje, `400` código inválido o expirado, `422` contraseña fuera de 8 a 128 caracteres, `429` demasiadas solicitudes. |

Las respuestas `429` traen la cabecera `Retry-After` en segundos.

### Flujo en la app

1. Pantalla "Olvidé mi contraseña": pide el correo y llama a
   `forgot-password`. Muestra siempre el mensaje de la respuesta.
2. Pantalla del código: el usuario escribe los 6 dígitos (opcionalmente se
   validan con `verify-reset-code`).
3. Pantalla de contraseña nueva: llama a `reset-password` con el correo, el
   código y la contraseña.
4. Al terminar, la app vuelve al login. **Todas las sesiones anteriores se
   cierran**: cualquier token viejo recibe `401`.

## Reglas de seguridad

- **No revela cuentas:** `forgot-password` responde igual si el correo no
  existe o la cuenta está desactivada, y el correo se envía en segundo plano
  para que la respuesta tarde lo mismo.
- **Código de un solo uso:** vence a los 15 minutos
  (`PASSWORD_RESET_CODE_TTL_MINUTES`) y se anula al usarlo.
- **Pedir uno nuevo anula el anterior.**
- **Intentos limitados:** tras 5 intentos fallidos
  (`PASSWORD_RESET_MAX_ATTEMPTS`) el código queda anulado y hay que pedir otro.
- **Guardado con hash:** en la base solo queda el HMAC-SHA256 del código,
  calculado con `SECRET_KEY` y ligado al usuario.
- **El código va con el correo:** `reset-password` exige el email, así un
  código no se puede probar contra todas las cuentas.
- **Límites de frecuencia:**
  - Por cuenta: 3 códigos por hora (`PASSWORD_RESET_MAX_REQUESTS_PER_HOUR`),
    contados en la base de datos.
  - Por IP: 5 solicitudes de código y 10 intentos de verificación o cambio
    cada 15 minutos. Este límite vive en memoria de cada proceso: con varios
    workers cada uno cuenta por separado, y detrás de un proxy hay que pasar la
    IP real a uvicorn (`--proxy-headers --forwarded-allow-ips=...`).
- **Cierre de sesiones:** cada usuario tiene `token_version`, que va dentro
  del JWT como `ver`. Restablecer la contraseña (o borrar los datos del
  paciente) la incrementa y los tokens anteriores dejan de valer. Los tokens
  emitidos antes de esta versión cuentan como `ver = 0`, así que nadie pierde
  la sesión al desplegar.
- **Aviso:** tras el cambio se envía un correo "tu contraseña fue cambiada".
- El código nunca se escribe en el log, salvo en `development` sin SMTP
  configurado (para poder probar).

## Configuración

Variables nuevas en `.env` (ver `.env.example`):

```env
PASSWORD_RESET_CODE_TTL_MINUTES=15
PASSWORD_RESET_MAX_ATTEMPTS=5
PASSWORD_RESET_MAX_REQUESTS_PER_HOUR=3

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURITY=STARTTLS   # STARTTLS, SSL (puerto 465) o NONE
SMTP_USERNAME=tu-cuenta@gmail.com
SMTP_PASSWORD=contraseña-de-aplicación
SMTP_FROM=DEI <tu-cuenta@gmail.com>
```

Con Gmail hay que activar la verificación en dos pasos y crear una
"contraseña de aplicación"; la contraseña normal no funciona.

Sin `SMTP_HOST`:

- en `development` el correo (con el código) aparece en el log del backend;
- en `production` no se envía nada y queda un error en el log.

Luego aplica la migración `a7d3e5f1c9b2`:

```bash
alembic upgrade head
```

## Pruebas

```bash
pytest tests/test_password_reset.py
```
