# Seguridad clínica y privacidad

Esta guía explica cómo DEI protege a los pacientes y sus datos, qué
configuración necesita el servidor y qué tiene que mostrar el frontend.

## 1. Configuración obligatoria

Variables de `.env` nuevas:

| Variable | Valor | Para qué |
|---|---|---|
| `DATA_ENCRYPTION_KEYS` | clave Fernet (ver sección 2) | Cifra diarios, audios y notas. **Sin ella la app no arranca.** |
| `APP_ENV` | `development` o `production` | En `production` la app no arranca si `AI_PROVIDER_CHAIN` incluye `FAKE`. |
| `CRISIS_COUNTRY` | `BO` (por defecto) | País cuyas líneas de crisis ve el paciente. |
| `AI_PROVIDER_CHAIN` | `OLLAMA,GEMINI` (por defecto) | Orden inicial de proveedores de IA. El admin puede cambiarlo desde el panel (sección 8). `FAKE` solo en desarrollo. |

## 2. La clave de cifrado

### Generarla

En la máquina del backend, con el entorno virtual activado:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Imprime una clave de 44 caracteres que termina en `=`, por ejemplo
`M2Q4ZTFjYjJhZjVkNGU3ZjkwYjFjM2Q1ZTdmOWExYjM=`. **No uses esa clave de
ejemplo**: la usan los tests y es pública.

### Configurarla

En el `.env` del servidor:

```env
DATA_ENCRYPTION_KEYS=la-clave-que-generaste
```

Luego aplica las migraciones. La migración `d2f6a8c1e4b7` cifra los datos
que ya existían, por eso necesita la clave:

```bash
alembic upgrade head
```

### Guardarla

- **Si se pierde la clave, los diarios no se pueden recuperar.** No hay
  forma de descifrarlos sin ella.
- Guarda una copia fuera del servidor, por ejemplo en un gestor de
  contraseñas (Bitwarden, 1Password) o impresa en un lugar seguro.
- No la subas a git ni la compartas por chat o correo.
- Usa una clave distinta para desarrollo y para producción.

### Rotarla

Si sospechas que la clave se filtró, o como rutina anual:

1. Genera una clave nueva con el mismo comando.
2. Pon la nueva primero y la anterior después, separadas por coma:
   ```env
   DATA_ENCRYPTION_KEYS=CLAVE_NUEVA,CLAVE_ANTERIOR
   ```
3. Reinicia el backend. Lo nuevo se cifra con la clave nueva y lo antiguo
   se sigue leyendo con la anterior.
4. Conserva la clave anterior en la lista mientras existan datos cifrados
   con ella.

### Qué se cifra

| Dato | Dónde |
|---|---|
| Texto de las entradas | `emotional_entries.text_content` |
| Transcripciones | `audio_transcriptions.transcription_text` |
| Análisis de la IA | `emotional_analyses.analysis_json` |
| Notas clínicas | `clinical_notes.note` |
| Recomendaciones | `patient_recommendations.content` |
| Audios | archivos en `uploads/audio` |

El resto del código trabaja con el texto en claro. El cifrado y el
descifrado ocurren al guardar y al leer (`app/shared/security/field_encryption.py`).
Los datos anteriores al cifrado se siguen leyendo aunque estén en texto plano.

## 3. Detección de riesgo y crisis

- **El paciente no fija su nivel de riesgo.** Lo calcula el sistema.
- **Filtro de frases** (`app/shared/safety/risk_phrase_screening.py`):
  detecta ideación suicida, autolesión y planes explícitos sin depender de
  la IA. En el análisis automático gana el nivel más alto entre la IA y el
  filtro.
- **Ante riesgo HIGH o CRITICAL:**
  - El paciente recibe al instante `crisis_support`: un mensaje de
    contención, las líneas de crisis de su país y la aclaración de que DEI
    no es un servicio de emergencias.
  - Cada psicólogo vinculado y con consentimiento recibe una notificación
    `RISK_ALERT`, sin el texto de la entrada.
  - Se crea una alerta con estado en la bandeja del psicólogo.

La migración carga las líneas de Bolivia:
- Familia Segura: 800 11 30 40 (de 6:00 a 24:00) y WhatsApp 77797667.
- Policía: 110.
- Ambulancia en La Paz: 165.

**Confírmalas llamando antes de salir a producción.** El administrador
las gestiona desde el panel (sección 8).

### Bandeja de alertas del psicólogo

| Endpoint | Uso |
|---|---|
| `GET /risk-alerts/inbox?status=NEW` | Alertas nuevas, vistas o resueltas |
| `PATCH /risk-alerts/{id}/seen` | Marcar como vista |
| `PATCH /risk-alerts/{id}/resolve` | Resolver con `resolution_note` (qué se hizo) |

Si el reanálisis de una entrada da el mismo nivel, no se notifica de
nuevo. Si sube de HIGH a CRITICAL, la alerta se reabre.

## 4. Consentimientos del paciente

| Tipo | Obligatorio para | ¿Revocable? |
|---|---|---|
| `INFORMED_CONSENT` | Escribir en el diario y hacer análisis manuales | No; para dejar DEI se eliminan los datos (sección 7) |
| `AI_PROCESSING` | Análisis automático, transcripción, recomendaciones y resumen con IA | Sí |

| Endpoint | Uso |
|---|---|
| `GET /platform-consents/documents` | Textos vigentes y si el paciente ya los aceptó |
| `POST /platform-consents` | Aceptar: `{"consent_type": "...", "version": "1.0"}` |
| `PATCH /platform-consents/AI_PROCESSING/revoke` | Retirar el consentimiento de IA |

Los textos están en `app/platform_consents/documents.py`. Si cambias un
texto, **sube su `version`**: los pacientes tendrán que aceptarlo de
nuevo. Conviene revisar los textos con un abogado y un psicólogo.

Sin el consentimiento correspondiente, la API responde **403**. El
frontend debe mostrar los textos y pedir la aceptación antes de dejar
escribir.

## 5. Qué ve el psicólogo

- Al pedir el vínculo, el paciente elige `sharing_mode`:
  - `NEW_ONLY` (por defecto): solo las entradas creadas desde que se
    acepta el vínculo.
  - `FROM_DATE`: desde la fecha indicada en `share_from`.
  - `FULL_HISTORY`: todo el historial.
- Siempre hace falta, además, una relación activa y un consentimiento
  vigente hacia ese psicólogo.

### Recomendaciones revisadas

- Si el paciente tiene psicólogo, las recomendaciones de IA quedan en
  `PENDING_REVIEW` y el paciente no ve el texto hasta que se aprueban.
- El psicólogo las revisa en `GET /recommendations/review/pending` y las
  aprueba con `PATCH /recommendations/review/{id}/approve` (puede editar
  el texto) o las rechaza con `.../reject`.
- Si el paciente no tiene psicólogo y el riesgo es HIGH o CRITICAL, no se
  generan recomendaciones automáticas.

## 6. Auditoría

Se registra cada vez que un psicólogo consulta insights, notas o alertas,
revisa alertas o recomendaciones, o crea sesiones y notas. El paciente lo
ve en `GET /audit/my-access-log`.

## 7. Derechos del paciente sobre sus datos

| Endpoint | Qué hace |
|---|---|
| `GET /patients/me/data/export` | Descarga todos sus datos en JSON |
| `POST /patients/me/data/erase` con `{"confirmation": "ELIMINAR"}` | Ver lista abajo |

Al eliminar los datos:
- Se borran las entradas, audios, transcripciones, análisis,
  recomendaciones, alertas y notificaciones.
- Se revocan los consentimientos y se cierran los vínculos.
- Se anonimiza el perfil y se desactiva la cuenta.

Se conservan, sin datos personales, las sesiones y notas clínicas (son el
registro del psicólogo), el historial de consentimientos y la auditoría.
Valida este criterio con un abogado según la Ley de Bolivia.

## 8. Panel del administrador

### Líneas de crisis

| Endpoint | Uso |
|---|---|
| `GET /admin/crisis-lines?country_code=BO` | Ver las líneas |
| `POST /admin/crisis-lines` | Crear: `{"country_code": "BO", "city": "Santa Cruz", "name": "Ambulancia", "phone": "161"}` |
| `PATCH /admin/crisis-lines/{id}` | Editar o desactivar (`{"is_active": false}`) |

- Una línea sin `city` es nacional.
- `sort_order` define el orden en que aparecen.
- El paciente ve las líneas activas del país de `CRISIS_COUNTRY`.
- Si no hay ninguna activa, se usa la lista fija de
  `app/shared/safety/crisis_resources.py`.

### Proveedor de IA

| Endpoint | Uso |
|---|---|
| `GET /admin/ai-settings` | Ver la cadena actual y si viene del admin o del `.env` |
| `PUT /admin/ai-settings` | Elegir el orden: `{"provider_chain": ["OLLAMA", "GEMINI"]}` |
| `DELETE /admin/ai-settings` | Volver a lo que diga el `.env` |

Ejemplos:
- `["OLLAMA"]`: solo la IA local, sin costo de tokens.
- `["GEMINI", "OLLAMA"]`: Gemini primero y la IA local de respaldo.

El cambio se aplica en hasta 30 segundos y no hace falta reiniciar el
backend. Se rechazan los proveedores no implementados, los repetidos y,
en producción, `FAKE`.

**Agregar otra IA en línea** (por ejemplo, otra API distinta de Gemini):
1. Implementa su proveedor de análisis, resumen y recomendaciones, igual
   que los de Gemini.
2. Regístralo en las tres fábricas (`provider_factory.py`).
3. Agrega su nombre a `SUPPORTED_PROVIDERS` en
   `app/shared/ai/runtime_settings.py`.

Desde ese momento el admin ya puede elegirla.

## 9. Checklist antes de producción

- [ ] Clave generada, en el `.env` y con copia fuera del servidor.
- [ ] `APP_ENV=production` y `AI_PROVIDER_CHAIN` sin `FAKE`.
- [ ] `alembic upgrade head` aplicado.
- [ ] Líneas de crisis confirmadas por teléfono y cargadas las de otras
      ciudades (`/admin/crisis-lines`).
- [ ] Textos de consentimiento revisados por un abogado y un psicólogo.
- [ ] Si usas Gemini, contratar un plan que no use los datos para
      entrenar y que tenga acuerdo de tratamiento de datos.
- [ ] El frontend muestra los consentimientos, `crisis_support` y la
      bandeja de alertas.

## 10. Tests

```bash
pip install -r requirements-dev.txt
pytest
```

`tests/test_clinical_safety.py`, `tests/test_admin_settings.py` y
`tests/test_emotions.py` cubren todo lo anterior. Usan una base en memoria
y el proveedor de IA simulado.
