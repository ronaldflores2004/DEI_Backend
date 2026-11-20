# DEI · Documentación del proyecto (PUDS)

| | |
|---|---|
| **Proyecto** | DEI, Diario Emocional Inteligente |
| **Metodología** | Proceso Unificado de Desarrollo de Software (PUDS / RUP) |
| **Elaborado por** | Ronald |
| **Versión del documento** | 1.0 |
| **Fecha** | 20 de noviembre de 2026 |
| **Repositorios** | `dei_backend` (API), `dei_ai` (IA local), `dei_app` (aplicación Flutter) |

## Historial de versiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0 | 20/11/2026 | Documento completo: inicio, requerimientos, análisis, diseño, implementación, pruebas y anexos. |

## Cómo está organizado este documento

El Proceso Unificado organiza el trabajo en **cuatro fases** (Inicio,
Elaboración, Construcción y Transición) y en **flujos de trabajo** que se
repiten en cada iteración (Requerimientos, Análisis, Diseño, Implementación y
Pruebas). Este documento sigue esos flujos de trabajo y produce sus artefactos:

| Capítulo | Flujo de trabajo / fase | Artefactos principales |
|---|---|---|
| 1 | Inicio | Documento de visión, interesados, alcance, factibilidad, cronograma, riesgos |
| 2 | Requerimientos | Requerimientos funcionales y no funcionales, actores, modelo de casos de uso, especificación de cada caso de uso |
| 3 | Análisis | Clases de análisis (interfaz, control y entidad), diagramas de comunicación y de secuencia por caso de uso, actividad |
| 4 | Diseño | Arquitectura, paquetes, clases de diseño, modelo de datos, estados, diseño de interfaz |
| 5 | Implementación | Componentes, despliegue, tecnologías, estructura del código |
| 6 | Pruebas | Plan de pruebas, casos de prueba y resultados reales |
| 7 | Anexos | Manual de usuario por rol, manual técnico de instalación, glosario |

Los diagramas UML están en PlantUML (fuente editable), PNG y SVG, y el modelo
UML 2.1 en XMI se puede importar en Enterprise Architect (ver el manual técnico,
sección 7.2.6).


# 1. Fase de Inicio

## 1.1 Documento de visión

### 1.1.1 Planteamiento del problema

El seguimiento emocional entre sesiones de terapia suele depender de la memoria
del paciente. Lo que siente durante la semana se pierde o llega a la consulta
resumido y sesgado. Los diarios en papel o en notas del teléfono no ayudan a ver
patrones, no avisan cuando aparecen señales de riesgo y no se pueden compartir
de forma controlada con el psicólogo. Por otra parte, las aplicaciones de
bienestar que usan IA suelen enviar textos muy sensibles a servicios en la nube
sin control del paciente sobre quién ve qué.

### 1.1.2 Propuesta de solución

DEI es una plataforma con aplicación móvil y web donde:

- El **paciente** registra su diario emocional por **texto o voz**.
- Una **IA** analiza cada entrada (emoción principal, intensidad, nivel de riesgo
  y temas), genera un **resumen semanal** y propone **recomendaciones**.
- La IA corre **primero en local** (Ollama y Whisper en una máquina con GPU) y
  solo usa **Gemini** en la nube como respaldo.
- Un **filtro determinista** de frases de riesgo complementa a la IA, y ante un
  riesgo alto el paciente recibe al instante las **líneas de crisis** de su país
  y su psicólogo una **alerta**.
- El paciente decide **con qué psicólogo** se vincula, **qué comparte** (todo el
  historial, desde una fecha o solo lo nuevo) y puede **revocar** el acceso.
- El **psicólogo** ve solo lo compartido, atiende alertas, agenda sesiones con
  notas clínicas y revisa las recomendaciones de la IA antes de que lleguen al
  paciente.
- El **administrador** verifica las licencias de los psicólogos, gestiona
  usuarios, elige el orden de los proveedores de IA y mantiene las líneas de
  crisis.

### 1.1.3 Objetivos

**Objetivo general.** Desarrollar una plataforma de diario emocional inteligente
que apoye el seguimiento psicológico entre sesiones mediante análisis con IA,
con detección de riesgo y control del paciente sobre su información.

**Objetivos específicos.**

1. Permitir registrar entradas de diario por texto y por voz, con transcripción
   automática.
2. Analizar cada entrada con IA para obtener emoción principal, intensidad,
   nivel de riesgo y temas, priorizando la IA local para reducir costos y
   exposición de datos.
3. Detectar situaciones de riesgo con un mecanismo que no dependa solo de la IA y
   activar una respuesta de crisis inmediata.
4. Gestionar el vínculo paciente-psicólogo con consentimientos explícitos,
   revocables y auditados.
5. Ofrecer al psicólogo un panel con pacientes, alertas, sesiones, notas
   clínicas e insights.
6. Proteger los datos clínicos con cifrado en reposo, control de acceso por rol y
   auditoría.
7. Entregar una única aplicación multiplataforma (Android, iOS y web) para los
   tres roles.

### 1.1.4 Alcance

**Incluye:**

- Registro e inicio de sesión con roles (paciente, psicólogo, administrador) y
  recuperación de contraseña por correo.
- Consentimiento informado y consentimiento de procesamiento con IA.
- Diario de texto y voz; transcripción; análisis emocional; resumen semanal;
  recomendaciones con revisión profesional.
- Detección de riesgo, líneas de crisis y alertas al psicólogo.
- Vinculación paciente-psicólogo, sesiones y notas clínicas.
- Notificaciones dentro de la aplicación.
- Panel de administración: usuarios, verificación de psicólogos, estadísticas,
  cadena de proveedores de IA y líneas de crisis.
- Exportación y borrado de datos del paciente; registro de accesos.

**No incluye (fuera de alcance de esta versión):**

- Diagnóstico clínico automático. DEI apoya al profesional, no lo reemplaza.
- Servicio de emergencias: DEI informa líneas de crisis, pero no llama ni
  despacha ayuda.
- Videollamadas, chat en tiempo real o pagos.
- Notificaciones push (solo notificaciones dentro de la aplicación).

### 1.1.5 Interesados (stakeholders)

| Interesado | Descripción | Interés principal | Responsabilidad en el proyecto |
|---|---|---|---|
| Pacientes | Personas en acompañamiento psicológico | Registrar cómo se sienten, recibir apoyo, controlar su privacidad | Usuarios finales; validan la usabilidad |
| Psicólogos | Profesionales con licencia verificada | Seguimiento entre sesiones, alertas oportunas, menos carga administrativa | Usuarios finales; validan criterios clínicos |
| Administrador de la plataforma | Responsable de la operación | Usuarios válidos, IA disponible, líneas de crisis correctas | Opera y configura el sistema |
| Desarrollador | Ronald | Producto funcional, mantenible y documentado | Análisis, diseño, implementación y pruebas |
| Docente / evaluador | Revisión académica | Aplicación correcta del Proceso Unificado | Evalúa los artefactos |

### 1.1.6 Perfil de usuarios y entorno

| Usuario | Conocimientos | Dispositivo | Frecuencia de uso |
|---|---|---|---|
| Paciente | Uso básico de teléfono | Android, iOS o navegador | Diario o varias veces por semana |
| Psicólogo | Uso de computadora y teléfono | Navegador (pantalla ancha) o tableta | Diario, durante su jornada |
| Administrador | Conocimientos técnicos básicos | Navegador | Semanal o ante incidencias |

### 1.1.7 Características del producto (resumen)

| Característica | Beneficio |
|---|---|
| Diario por texto y voz | Registrar en el momento, sin fricción |
| Análisis emocional con IA local primero | Información útil sin costo por token y con menos exposición de datos |
| Filtro determinista de riesgo | La seguridad no depende solo de la IA |
| Respuesta de crisis | Ayuda inmediata y aviso al profesional |
| Compartir controlado | El paciente decide qué y con quién |
| Revisión profesional de recomendaciones | Ningún consejo de IA llega sin supervisión cuando hay psicólogo |
| Cifrado y auditoría | Confianza y cumplimiento |

## 1.2 Estudio de factibilidad

### 1.2.1 Factibilidad técnica

| Recurso | Disponibilidad | Conclusión |
|---|---|---|
| Lenguajes y frameworks | Python + FastAPI, Flutter, PostgreSQL: libres y maduros | Factible |
| IA local | Ollama con `llama3.1:8b` y Faster-Whisper en una laptop con GPU (Nitro 5) | Factible en red local |
| IA en la nube | Gemini con clave de API como respaldo | Factible, con costo por uso |
| Servidor de aplicación | Laptop ThinkPad con PostgreSQL | Factible para desarrollo y pruebas |
| Conocimientos | Desarrollo web, móvil y uso de modelos de lenguaje | Disponibles |

### 1.2.2 Factibilidad económica

| Concepto | Costo estimado | Observación |
|---|---|---|
| Software (FastAPI, Flutter, PostgreSQL, Ollama, Whisper) | 0 | Código abierto |
| Hardware (dos laptops existentes) | 0 adicional | Equipos propios |
| Gemini (respaldo) | Bajo | Solo cuando la IA local no responde |
| Publicación en tiendas | Pago único (Google Play) y anual (Apple) | Solo si se publica |
| Dominio y hosting para producción | Variable | Fase de transición |

La decisión de usar **IA local primero** es la que hace viable el proyecto: el
análisis de cada entrada no genera costo por token salvo que la IA local falle.

### 1.2.3 Factibilidad operativa

Los usuarios ya usan teléfonos y aplicaciones de mensajería; la app sigue
patrones conocidos (barra inferior en móvil, menú lateral en web). El
psicólogo no necesita instalar nada: puede usar la versión web. El
administrador configura la IA y las líneas de crisis desde la propia app.

### 1.2.4 Factibilidad legal y ética

DEI maneja datos de salud mental, que son datos sensibles. Por eso el diseño
incluye consentimiento informado obligatorio, consentimiento separado para la
IA, cifrado en reposo, mínimo privilegio para el psicólogo, auditoría de
accesos, derecho a exportar y borrar datos, y avisos de que DEI no es un
servicio de emergencias. Antes de un uso real con pacientes conviene revisar la
normativa local de protección de datos y la ética profesional del país.

## 1.3 Cronograma (fases e iteraciones)

Las iteraciones de Elaboración y Construcción se reconstruyeron a partir del
historial de commits de los repositorios. La iteración de Inicio y la de
Transición son estimadas.

![Cronograma](diagramas/png/15-cronograma.png)

| Fase | Iteración | Fechas | Resultado |
|---|---|---|---|
| Inicio | I1 | jun 2026 (estimado) | Visión, actores, casos de uso principales, factibilidad |
| Elaboración | E1 | 8–17 jun 2026 | Arquitectura base: módulos Identity y Therapy |
| Elaboración | E2 | 18–22 jun 2026 | Análisis con Gemini, dashboards, recomendaciones, sesiones, notificaciones |
| Construcción | C1 | 30 jun–14 jul 2026 | Patrón Repository y capa de servicios en todos los módulos |
| Construcción | C2 | 14–25 jul 2026 | Arquitectura de providers de IA, enums, logging, endurecimiento de seguridad |
| Construcción | C3 | 1–5 ago 2026 | Servicio de IA local `dei_ai` con Ollama y Faster-Whisper |
| Construcción | C4 | oct–nov 2026 | Cadena Ollama → Gemini → Fake, Whisper por HTTP, migraciones Alembic |
| Construcción | C5 | nov 2026 | Seguridad clínica, panel de administración, recuperación de contraseña, panel del psicólogo, catálogo único de emociones |
| Construcción | C6 | nov 2026 | Aplicación Flutter para los tres roles |
| Transición | T1 | nov–dic 2026 (estimado) | Documentación, pruebas en dispositivos, despliegue |

## 1.4 Análisis de riesgos

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | La IA subestima una situación de riesgo | Media | Muy alto | Filtro determinista de frases que siempre corre y prevalece si detecta más riesgo; criterios de riesgo explícitos en el prompt |
| R2 | La IA local no está disponible (laptop apagada) | Alta | Medio | Cadena de proveedores: Gemini como respaldo; la entrada se guarda y se puede analizar después |
| R3 | Fuga de datos clínicos | Baja | Muy alto | Cifrado de campos, JWT con expiración, control de acceso por relación y consentimiento, auditoría |
| R4 | Pérdida de la clave de cifrado | Baja | Muy alto | Copia fuera del servidor y rotación con varias claves |
| R5 | La IA inventa resultados en producción | Baja | Alto | El proveedor `FAKE` está prohibido con `APP_ENV=production` |
| R6 | Un psicólogo sin licencia accede a pacientes | Baja | Alto | Verificación por el administrador; el directorio solo muestra verificados |
| R7 | Recomendación de IA dañina para un paciente en riesgo | Media | Alto | Revisión profesional obligatoria si hay psicólogo; sin psicólogo y con riesgo alto no se generan |
| R8 | Costos de Gemini | Media | Bajo | IA local primero; el administrador controla el orden |
| R9 | Retraso en el desarrollo de la app | Media | Medio | Arquitectura por features; la app tolera endpoints faltantes |
| R10 | Diferencias entre el backend y el servicio de IA | Media | Medio | Catálogo único de 22 emociones y pruebas de contrato en ambos repositorios |

# 2. Flujo de trabajo: Requerimientos

## 2.1 Requerimientos funcionales

| Código | Requerimiento | Prioridad | Caso de uso |
|---|---|---|---|
| RF01 | El sistema debe permitir registrarse como paciente o psicólogo con correo y contraseña (8 a 128 caracteres). No se permite registrar administradores. | Alta | CU01 |
| RF02 | El sistema debe autenticar con correo y contraseña y emitir un token JWT que vence en 30 minutos. | Alta | CU01 |
| RF03 | El sistema debe permitir recuperar la contraseña con un código de 6 dígitos enviado por correo (válido 15 minutos, 5 intentos). | Alta | CU02 |
| RF04 | El sistema debe exigir al paciente un perfil (nombre, apellido, fecha de nacimiento, género) y al psicólogo un perfil profesional (licencia, especialidades). | Alta | CU01 |
| RF05 | El sistema debe exigir el consentimiento informado vigente antes de usar el diario. | Alta | CU03 |
| RF06 | El sistema debe pedir un consentimiento separado y revocable para procesar entradas con IA. | Alta | CU03 |
| RF07 | El paciente debe poder crear entradas de texto. | Alta | CU04 |
| RF08 | El paciente debe poder crear entradas de voz y el sistema debe transcribirlas. | Alta | CU05, CU06 |
| RF09 | El paciente debe poder corregir la transcripción. | Media | CU06 |
| RF10 | El sistema debe analizar una entrada con IA y obtener emoción principal, intensidad, nivel de riesgo y un análisis detallado. | Alta | CU07 |
| RF11 | El sistema debe aplicar un filtro determinista de frases de riesgo y quedarse con el nivel más alto entre IA y filtro. | Alta | CU07 |
| RF12 | Ante riesgo HIGH o CRITICAL, el sistema debe mostrar las líneas de crisis del país y alertar a los psicólogos autorizados. | Alta | CU08 |
| RF13 | El sistema debe generar un resumen semanal (con IA solo si hay consentimiento). | Media | CU09 |
| RF14 | El sistema debe generar recomendaciones con IA; si el paciente tiene psicólogo, quedan pendientes de revisión. | Media | CU10, CU23 |
| RF15 | El paciente debe poder buscar psicólogos verificados y enviar una solicitud indicando qué comparte (todo, desde una fecha o solo lo nuevo). | Alta | CU11 |
| RF16 | El paciente debe poder otorgar y revocar el acceso a un psicólogo. | Alta | CU11 |
| RF17 | El paciente debe poder exportar todos sus datos y borrarlos. | Media | CU12 |
| RF18 | El paciente debe poder ver qué psicólogo accedió a sus datos y cuándo. | Media | CU13 |
| RF19 | El psicólogo debe poder aceptar o rechazar solicitudes de vínculo. | Alta | CU20 |
| RF20 | El psicólogo debe ver solo las entradas que cada paciente le comparte, con su análisis. | Alta | CU21 |
| RF21 | El psicólogo debe poder ver su bandeja de alertas, marcarlas como vistas y resolverlas con una nota. | Alta | CU22 |
| RF22 | El psicólogo debe poder aprobar (editando) o rechazar recomendaciones de IA. | Media | CU23 |
| RF23 | El psicólogo debe poder agendar, completar y cancelar sesiones, y registrar notas clínicas. | Media | CU24 |
| RF24 | El psicólogo debe poder ver insights calculados de cada paciente. | Media | CU25 |
| RF25 | El administrador debe poder verificar psicólogos. | Alta | CU30 |
| RF26 | El administrador debe poder activar y desactivar usuarios. | Alta | CU31 |
| RF27 | El administrador debe poder elegir el orden de los proveedores de IA. | Media | CU32 |
| RF28 | El administrador debe poder gestionar las líneas de crisis por país. | Media | CU33 |
| RF29 | El administrador debe poder ver estadísticas de uso. | Baja | CU34 |
| RF30 | El sistema debe enviar notificaciones dentro de la aplicación (alertas, sesiones, recomendaciones). | Media | Transversal |

## 2.2 Requerimientos no funcionales

| Código | Categoría | Requerimiento |
|---|---|---|
| RNF01 | Seguridad | Las contraseñas se guardan con bcrypt; nunca en texto plano. |
| RNF02 | Seguridad | El texto del diario, las transcripciones, el análisis detallado, las recomendaciones y las notas clínicas se cifran en reposo (Fernet). El sistema no arranca sin clave de cifrado. |
| RNF03 | Seguridad | Todas las rutas, salvo registro, login y recuperación, requieren JWT. Cambiar la contraseña invalida todas las sesiones. |
| RNF04 | Seguridad | Límite de intentos por IP y por cuenta en la recuperación de contraseña; la respuesta no revela si el correo existe. |
| RNF05 | Privacidad | Un psicólogo solo accede a datos de pacientes con relación activa, consentimiento vigente y dentro del periodo compartido. |
| RNF06 | Privacidad | Cada acceso de un psicólogo a datos de un paciente queda auditado. |
| RNF07 | Privacidad | Las notificaciones de riesgo no incluyen el texto del diario. Los logs de red de la app no imprimen cuerpos. |
| RNF08 | Disponibilidad | Si un proveedor de IA falla, se usa el siguiente de la cadena; si fallan todos, se responde 503 sin perder la entrada. |
| RNF09 | Rendimiento | El análisis con IA local debe responder en menos de 120 s (tiempo máximo configurable); el resto de operaciones en menos de 2 s en red local. |
| RNF10 | Usabilidad | Una sola app para los tres roles, con navegación adaptada a móvil (barra inferior) y pantallas anchas (menú lateral). Mensajes de error en español. |
| RNF11 | Portabilidad | La app funciona en Android, iOS y web desde un mismo código. |
| RNF12 | Mantenibilidad | Backend por módulos con capas router-service-repository; app por features con capas domain-data-presentation; esquema de base de datos versionado con Alembic. |
| RNF13 | Extensibilidad | Agregar un proveedor de IA requiere implementar su clase y registrarlo en la fábrica, sin tocar los servicios. |
| RNF14 | Confiabilidad | El proveedor simulado (FAKE) está prohibido en producción. |
| RNF15 | Verificabilidad | Pruebas automáticas en backend, servicio de IA y app que no requieren servicios externos. |

## 2.3 Actores

| Actor | Tipo | Descripción |
|---|---|---|
| Paciente | Principal | Persona que registra su diario y recibe apoyo. Rol `PATIENT`. |
| Psicólogo | Principal | Profesional verificado que acompaña a pacientes. Rol `PROFESSIONAL`. |
| Administrador | Principal | Opera la plataforma. Rol `ADMIN`; se crea directamente en la base de datos. |
| IA (Ollama / Gemini / Whisper) | Secundario (sistema) | Servicios que transcriben audio y generan análisis, resúmenes y recomendaciones. |
| Servidor de correo (SMTP) | Secundario (sistema) | Envía los códigos de recuperación de contraseña. |

## 2.4 Diagrama de casos de uso

![Casos de uso](diagramas/png/03-casos-de-uso.png)

| Código | Caso de uso | Actor | Prioridad |
|---|---|---|---|
| CU01 | Registrarse e iniciar sesión | Paciente, Psicólogo, Administrador | Alta |
| CU02 | Recuperar contraseña | Paciente, Psicólogo, Administrador | Alta |
| CU03 | Aceptar consentimientos | Paciente | Alta |
| CU04 | Escribir entrada de texto | Paciente | Alta |
| CU05 | Grabar entrada de voz | Paciente | Alta |
| CU06 | Transcribir audio | IA (Whisper) | Alta |
| CU07 | Analizar entrada con IA | Paciente, IA | Alta |
| CU08 | Recibir ayuda en crisis | Paciente | Alta |
| CU09 | Ver resumen semanal | Paciente | Media |
| CU10 | Ver y pedir recomendaciones | Paciente | Media |
| CU11 | Solicitar vínculo con psicólogo | Paciente | Alta |
| CU12 | Exportar o borrar mis datos | Paciente | Media |
| CU13 | Ver quién accedió a mis datos | Paciente | Media |
| CU20 | Aceptar o rechazar pacientes | Psicólogo | Alta |
| CU21 | Ver entradas compartidas | Psicólogo | Alta |
| CU22 | Atender alertas de riesgo | Psicólogo | Alta |
| CU23 | Revisar recomendaciones de IA | Psicólogo | Media |
| CU24 | Gestionar sesiones y notas | Psicólogo | Media |
| CU25 | Ver insights del paciente | Psicólogo | Media |
| CU30 | Verificar psicólogos | Administrador | Alta |
| CU31 | Activar o desactivar usuarios | Administrador | Alta |
| CU32 | Configurar cadena de IA | Administrador | Media |
| CU33 | Gestionar líneas de crisis | Administrador | Media |
| CU34 | Ver estadísticas | Administrador | Baja |

## 2.5 Especificación de casos de uso

### CU01 · Registrarse e iniciar sesión

| | |
|---|---|
| **Actor principal** | Paciente o Psicólogo (el Administrador solo inicia sesión) |
| **Descripción** | El usuario crea su cuenta y accede a la aplicación según su rol. |
| **Precondiciones** | El usuario tiene la app instalada o abierta en el navegador. |
| **Postcondiciones** | El usuario tiene una sesión válida (JWT guardado de forma segura) y ve la pantalla de inicio de su rol, o la de completar perfil o consentimiento si le falta. |
| **Requerimientos** | RF01, RF02, RF04, RNF01, RNF03 |

**Flujo básico**

1. El usuario elige "Regístrate" e indica si es paciente o psicólogo.
2. Ingresa correo y contraseña.
3. El sistema valida los datos, guarda la contraseña con bcrypt y crea la cuenta.
4. El usuario ingresa correo y contraseña en "Iniciar sesión".
5. El sistema verifica las credenciales y emite un JWT.
6. La app guarda el token, consulta los datos del usuario y su perfil.
7. La app muestra la pantalla de inicio de su rol.

**Flujos alternos**

- **3a. Correo ya registrado:** el sistema responde "Email ya registrado" y el usuario corrige el correo.
- **3b. Contraseña inválida (menos de 8 caracteres):** la app muestra el error de validación.
- **3c. Intento de registrar un administrador:** el sistema lo rechaza.
- **5a. Credenciales inválidas:** el sistema responde "Credenciales inválidas".
- **5b. Usuario desactivado:** el sistema responde "Usuario desactivado".
- **6a. Sin perfil:** la app lleva a completar el perfil de paciente o el perfil profesional.
- **6b. Paciente sin consentimiento informado:** la app lleva a CU03.
- **En cualquier momento, token vencido (401):** la app cierra la sesión y vuelve al login.

### CU02 · Recuperar contraseña

| | |
|---|---|
| **Actor principal** | Cualquier usuario registrado |
| **Actor secundario** | Servidor de correo |
| **Precondiciones** | El usuario tiene una cuenta activa y acceso a su correo. |
| **Postcondiciones** | La contraseña cambió, el código quedó consumido y todas las sesiones anteriores quedaron cerradas. |
| **Requerimientos** | RF03, RNF04 |

**Flujo básico**

1. El usuario elige "¿Olvidaste tu contraseña?" e ingresa su correo.
2. El sistema genera un código de 6 dígitos, guarda su hash con vencimiento de 15 minutos y lo envía por correo.
3. El sistema muestra un mensaje genérico (no revela si el correo existe).
4. El usuario ingresa el código.
5. El sistema verifica el código.
6. El usuario ingresa la nueva contraseña.
7. El sistema cambia la contraseña, consume el código e incrementa la versión del token.
8. La app vuelve al login.

**Flujos alternos**

- **2a. Correo inexistente o cuenta inactiva:** no se envía código, pero la respuesta es la misma.
- **2b. Se superó el límite de 3 códigos por hora o el límite por IP:** el sistema responde 429 con el tiempo de espera.
- **5a. Código incorrecto:** se cuenta el intento; al quinto el código se anula.
- **5b. Código vencido o ya usado:** se pide un código nuevo.
- **6a. Contraseña débil:** el sistema la rechaza.

### CU03 · Aceptar consentimientos

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | El paciente inició sesión y tiene perfil. |
| **Postcondiciones** | Queda registrado el consentimiento informado con su versión; opcionalmente, el de IA. |
| **Requerimientos** | RF05, RF06 |

**Flujo básico**

1. La app muestra el documento de consentimiento informado vigente (qué es DEI, que no es un servicio de emergencias, límites de la confidencialidad).
2. El paciente lo acepta.
3. El sistema registra el consentimiento con su versión y fecha.
4. La app ofrece el consentimiento de procesamiento con IA.
5. El paciente lo acepta.
6. El sistema lo registra y la app muestra el inicio.

**Flujos alternos**

- **2a. El paciente no acepta:** no puede usar el diario.
- **3a. Versión desactualizada:** el sistema rechaza y la app muestra la versión nueva.
- **5a. El paciente no acepta la IA:** puede usar el diario, pero sus entradas no se analizan con IA y el resumen semanal se calcula sin IA.
- **Más tarde, revocar IA:** desde Ajustes → Privacidad, el paciente revoca; desde ese momento el análisis automático responde 403.

### CU04 · Escribir entrada de texto

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | Consentimiento informado vigente. |
| **Postcondiciones** | La entrada queda guardada con el texto cifrado. |
| **Puntos de extensión** | CU07 (analizar con IA) |
| **Requerimientos** | RF07, RNF02 |

**Flujo básico**

1. El paciente abre "Nueva entrada" y elige texto.
2. Escribe cómo se siente y guarda.
3. El sistema guarda la entrada cifrada.
4. Si hay consentimiento de IA, la app ofrece analizarla (CU07).
5. La app muestra el detalle de la entrada.

**Flujos alternos**

- **3a. Sin consentimiento informado:** 403; la app lleva a CU03.
- **3b. Texto vacío:** error de validación.

### CU05 · Grabar entrada de voz

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | Consentimiento informado vigente; permiso de micrófono. |
| **Postcondiciones** | La entrada de audio queda guardada y, si la transcripción funciona, con su texto. |
| **Incluye** | CU06 (transcribir audio) |
| **Requerimientos** | RF08 |

**Flujo básico**

1. El paciente abre "Nueva entrada" y elige voz.
2. Graba y detiene la grabación.
3. La app sube el audio.
4. El sistema guarda el archivo y crea la entrada de tipo audio.
5. Se ejecuta CU06.
6. La app muestra la transcripción y ofrece analizar (CU07).

**Flujos alternos**

- **2a. Permiso de micrófono denegado:** la app explica cómo activarlo.
- **3a. Archivo no válido o demasiado grande:** el sistema lo rechaza.

### CU06 · Transcribir audio

| | |
|---|---|
| **Actor principal** | IA (Whisper), iniciado por el Paciente |
| **Precondiciones** | Existe una entrada de audio del paciente. |
| **Postcondiciones** | Existe una transcripción cifrada asociada a la entrada. |
| **Requerimientos** | RF08, RF09 |

**Flujo básico**

1. El sistema lee el audio de la entrada.
2. Lo envía al servidor Whisper configurado (idioma español).
3. Recibe el texto y lo guarda cifrado con el nombre del proveedor y modelo.

**Flujos alternos**

- **2a. Whisper no responde:** 503 "El servicio de transcripción no está disponible"; la entrada queda guardada y el paciente puede reintentar o escribir la transcripción a mano.
- **3a. El paciente corrige el texto:** la transcripción queda marcada como manual.

### CU07 · Analizar entrada con IA

| | |
|---|---|
| **Actor principal** | Paciente |
| **Actor secundario** | IA (Ollama, Gemini) |
| **Precondiciones** | La entrada existe, es del paciente y tiene texto (o transcripción); consentimiento de IA vigente. |
| **Postcondiciones** | Existe un análisis guardado con emoción, intensidad, riesgo y detalle cifrado. Si el riesgo es HIGH o CRITICAL se ejecutó CU08. |
| **Puntos de extensión** | CU08 [riesgo HIGH o CRITICAL] |
| **Requerimientos** | RF10, RF11, RNF08, RNF13 |

**Flujo básico**

1. El paciente pide "Analizar con IA".
2. El sistema verifica el consentimiento de IA y que la entrada sea suya.
3. El sistema obtiene el texto (o la transcripción) descifrado.
4. El sistema pide el análisis al primer proveedor de la cadena (por defecto Ollama).
5. El proveedor responde un JSON válido con emoción, intensidad, riesgo y análisis.
6. El sistema aplica el filtro de frases de riesgo y se queda con el nivel mayor.
7. El sistema guarda el análisis (el detalle cifrado).
8. La app muestra el resultado.

**Flujos alternos**

- **2a. Sin consentimiento de IA:** 403.
- **3a. Audio sin transcripción:** 400 "El audio aún no tiene transcripción".
- **5a. El proveedor falla o responde algo inválido:** se intenta con el siguiente proveedor (Gemini).
- **5b. Ningún proveedor responde:** 503; la entrada queda guardada.
- **6a. El filtro detecta HIGH o CRITICAL:** se ejecuta CU08.
- **Reanalizar:** el paciente puede pedir un nuevo análisis; se reemplaza el anterior.

### CU08 · Recibir ayuda en crisis

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | Un análisis tiene riesgo HIGH o CRITICAL. |
| **Postcondiciones** | El paciente vio las líneas de crisis; cada psicólogo autorizado tiene una alerta NEW y una notificación. |
| **Requerimientos** | RF12, RNF05, RNF07 |

**Flujo básico**

1. El sistema obtiene las líneas de crisis activas del país configurado.
2. El sistema busca los psicólogos con relación activa, consentimiento vigente y acceso a la fecha de la entrada.
3. Por cada uno crea una alerta de riesgo (si no existe para ese análisis y nivel) y una notificación sin el texto del diario.
4. La app muestra una tarjeta de ayuda con las líneas y un botón para llamar, e indica si se avisó a su psicólogo.

**Flujos alternos**

- **2a. Sin psicólogos autorizados:** solo se muestran las líneas de crisis.
- **3a. Falla al guardar la notificación:** se revierte y se informa que no se pudo avisar; las líneas se muestran igual.

### CU09 · Ver resumen semanal

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | Sesión iniciada. |
| **Postcondiciones** | Ninguna (consulta). |
| **Requerimientos** | RF13 |

**Flujo básico**

1. El paciente abre "Inicio".
2. El sistema calcula los datos de la semana (número de entradas, emociones frecuentes, intensidad promedio, niveles de riesgo).
3. Si hay consentimiento de IA, pide a la cadena un resumen en texto.
4. La app muestra el resumen.

**Flujos alternos**

- **2a. Sin entradas en la semana:** se muestra un resumen vacío.
- **3a. Sin consentimiento de IA o IA no disponible:** se muestra solo el resumen calculado.

### CU10 · Ver y pedir recomendaciones

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | Existe al menos un análisis del paciente. |
| **Postcondiciones** | Se creó una recomendación APPROVED (sin psicólogo) o PENDING_REVIEW (con psicólogo). |
| **Requerimientos** | RF14 |

**Flujo básico**

1. El paciente abre "Recomendaciones" y pide una nueva para un análisis.
2. El sistema verifica que el análisis sea suyo y que no tenga ya recomendación.
3. Pide a la cadena de IA un título y un contenido.
4. Si el paciente tiene psicólogo, la guarda como pendiente de revisión; si no, como aprobada.
5. La app muestra la lista; las pendientes aparecen "en revisión".

**Flujos alternos**

- **2a. Riesgo HIGH o CRITICAL y sin psicólogo:** 409; no se genera y se sugiere buscar apoyo profesional o una línea de crisis.
- **3a. IA no disponible:** 503.

### CU11 · Solicitar vínculo con psicólogo

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | El paciente tiene perfil y consentimiento informado. |
| **Postcondiciones** | Existe una solicitud PENDING con el modo de compartir elegido. Tras ser aceptada, el paciente puede otorgar acceso. |
| **Requerimientos** | RF15, RF16 |

**Flujo básico**

1. El paciente abre "Mi psicólogo" y ve el directorio de psicólogos verificados.
2. Elige uno y el modo de compartir: todo el historial, desde una fecha o solo entradas nuevas.
3. Envía la solicitud.
4. El sistema valida y crea la solicitud pendiente.
5. Cuando el psicólogo la acepta (CU20), el paciente otorga el acceso.
6. El sistema registra el consentimiento por psicólogo.

**Flujos alternos**

- **4a. Psicólogo no verificado o inexistente:** 400 o 404.
- **4b. Ya hay una solicitud pendiente o una relación activa:** 400.
- **2a. Modo "desde una fecha" sin fecha:** error de validación.
- **Revocar:** el paciente revoca el acceso y el psicólogo deja de ver sus datos.

### CU12 · Exportar o borrar mis datos

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | Sesión iniciada. |
| **Postcondiciones** | Exportar: el paciente recibe sus datos en JSON. Borrar: sus datos clínicos fueron eliminados. |
| **Requerimientos** | RF17 |
| **Estado** | Implementado en la API (`/patients/me/data/export` y `/erase`). La pantalla en la app está pendiente. |

**Flujo básico (exportar)**

1. El paciente elige "Exportar mis datos".
2. El sistema reúne perfil, entradas, transcripciones, análisis, recomendaciones, sesiones, consentimientos y vínculos, descifrados.
3. La app entrega el archivo.

**Flujo básico (borrar)**

1. El paciente elige "Borrar mis datos" y escribe `ELIMINAR` para confirmar.
2. El sistema elimina su información clínica.

**Flujos alternos**

- **1a. Confirmación distinta de `ELIMINAR`:** 400, no se borra nada.

### CU13 · Ver quién accedió a mis datos

| | |
|---|---|
| **Actor principal** | Paciente |
| **Precondiciones** | Sesión iniciada. |
| **Postcondiciones** | Ninguna (consulta). |
| **Requerimientos** | RF18, RNF06 |
| **Estado** | Implementado en la API (`GET /audit/my-access-log`). La pantalla en la app está pendiente. |

**Flujo básico**

1. El paciente abre la consulta de accesos.
2. El sistema lista los registros de auditoría: psicólogo, acción (ver entradas, ver alertas, revisar recomendación, notas clínicas…) y fecha.

### CU20 · Aceptar o rechazar pacientes

| | |
|---|---|
| **Actor principal** | Psicólogo |
| **Precondiciones** | Psicólogo con perfil; existe una solicitud pendiente dirigida a él. |
| **Postcondiciones** | Aceptar: solicitud ACCEPTED y relación terapéutica activa con el modo elegido por el paciente. Rechazar: solicitud REJECTED. |
| **Requerimientos** | RF19 |

**Flujo básico**

1. El psicólogo abre "Pacientes" y ve las solicitudes con nombre del paciente y modo de compartir.
2. Elige "Aceptar".
3. El sistema marca la solicitud como aceptada y crea la relación terapéutica.
4. El paciente aparece en "Mis pacientes".

**Flujos alternos**

- **2a. Rechazar:** la solicitud queda rechazada.
- **3a. La solicitud no es suya:** 403. **Ya procesada:** 400. **Relación ya existente:** 400.

### CU21 · Ver entradas compartidas

| | |
|---|---|
| **Actor principal** | Psicólogo |
| **Precondiciones** | Relación activa y consentimiento vigente con el paciente. |
| **Postcondiciones** | Se registró el acceso en la auditoría. |
| **Requerimientos** | RF20, RNF05, RNF06 |

**Flujo básico**

1. El psicólogo abre la ficha de un paciente.
2. El sistema verifica relación, consentimiento y periodo compartido.
3. Devuelve las entradas permitidas con su análisis.
4. Registra el acceso en la auditoría.

**Flujos alternos**

- **2a. Sin relación o sin consentimiento:** 403.
- **3a. Modo "solo nuevas":** solo aparecen entradas posteriores a la aceptación.

### CU22 · Atender alertas de riesgo

| | |
|---|---|
| **Actor principal** | Psicólogo |
| **Precondiciones** | Existen alertas dirigidas al psicólogo. |
| **Postcondiciones** | La alerta pasó a SEEN o RESOLVED; cada paso quedó auditado. |
| **Requerimientos** | RF21 |

**Flujo básico**

1. El psicólogo abre "Alertas" y filtra por estado (nuevas, vistas, resueltas).
2. Abre una alerta; el sistema la marca como vista.
3. Contacta al paciente por los medios que corresponda.
4. Escribe una nota de resolución y resuelve.
5. El sistema guarda la nota, la fecha y la auditoría.

**Flujos alternos**

- **2a. La alerta no es suya:** 404.
- **4a. Resolver sin haberla marcado vista:** se marca vista y resuelta a la vez.

### CU23 · Revisar recomendaciones de IA

| | |
|---|---|
| **Actor principal** | Psicólogo |
| **Precondiciones** | Hay recomendaciones PENDING_REVIEW de sus pacientes. |
| **Postcondiciones** | La recomendación quedó APPROVED (posiblemente editada) o REJECTED; el paciente fue notificado. |
| **Requerimientos** | RF22 |

**Flujo básico**

1. El psicólogo abre "Revisar".
2. Lee la recomendación y el análisis que la originó.
3. Edita el texto si hace falta y la aprueba.
4. El sistema la marca aprobada, registra quién y cuándo, audita y notifica al paciente.

**Flujos alternos**

- **3a. Rechazar:** la recomendación no llega al paciente.
- **4a. Ya revisada:** 400.

### CU24 · Gestionar sesiones y notas

| | |
|---|---|
| **Actor principal** | Psicólogo |
| **Precondiciones** | Relación activa con el paciente. |
| **Postcondiciones** | Sesión creada, completada o cancelada; notas clínicas cifradas guardadas. |
| **Requerimientos** | RF23, RNF02 |

**Flujo básico**

1. El psicólogo agenda una sesión con fecha y hora para un paciente.
2. El sistema la crea como SCHEDULED y notifica al paciente.
3. Después de la sesión, el psicólogo la marca como completada.
4. Escribe notas clínicas, que se guardan cifradas y se auditan.

**Flujos alternos**

- **3a. Cancelar:** la sesión pasa a CANCELLED.
- **1a. Sin relación activa:** 403.

### CU25 · Ver insights del paciente

| | |
|---|---|
| **Actor principal** | Psicólogo |
| **Precondiciones** | Relación activa y consentimiento. |
| **Postcondiciones** | Acceso auditado. |
| **Requerimientos** | RF24 |

**Flujo básico**

1. El psicólogo abre la ficha del paciente.
2. El sistema calcula insights por reglas, con prioridad: patrón emocional recurrente (la misma emoción negativa 3 o más veces), tema recurrente y desencadenante frecuente (2 o más veces en el análisis).
3. La app los muestra junto al historial.

### CU30 · Verificar psicólogos

| | |
|---|---|
| **Actor principal** | Administrador |
| **Precondiciones** | Existen psicólogos con perfil sin verificar. |
| **Postcondiciones** | El psicólogo queda verificado (quién y cuándo) y aparece en el directorio. |
| **Requerimientos** | RF25 |

**Flujo básico**

1. El administrador abre "Psicólogos" y ve los pendientes con su número de licencia.
2. Comprueba la licencia por fuera del sistema.
3. Elige "Verificar".
4. El sistema registra la verificación.

### CU31 · Activar o desactivar usuarios

| | |
|---|---|
| **Actor principal** | Administrador |
| **Precondiciones** | Sesión de administrador. |
| **Postcondiciones** | El usuario quedó activo o inactivo. Un usuario inactivo no puede iniciar sesión. |
| **Requerimientos** | RF26 |

**Flujo básico**

1. El administrador abre "Usuarios", busca por correo y filtra por rol.
2. Cambia el interruptor del usuario.
3. El sistema actualiza el estado.

### CU32 · Configurar cadena de IA

| | |
|---|---|
| **Actor principal** | Administrador |
| **Precondiciones** | Sesión de administrador. |
| **Postcondiciones** | La cadena queda guardada y se aplica en menos de 30 s. |
| **Requerimientos** | RF27, RNF14 |

**Flujo básico**

1. El administrador abre Ajustes → Proveedor de IA.
2. El sistema muestra la cadena actual y su origen (archivo `.env` o elegida por el administrador).
3. El administrador reordena los proveedores arrastrándolos y guarda.
4. El sistema valida y guarda la cadena.

**Flujos alternos**

- **4a. Cadena vacía, con repetidos, con proveedores desconocidos o con FAKE en producción:** 400.
- **Restablecer:** el administrador elimina su elección y se vuelve a usar la del `.env`.

### CU33 · Gestionar líneas de crisis

| | |
|---|---|
| **Actor principal** | Administrador |
| **Precondiciones** | Sesión de administrador. |
| **Postcondiciones** | Las líneas activas del país son las que verá el paciente en CU08. |
| **Requerimientos** | RF28 |

**Flujo básico**

1. El administrador abre Ajustes → Líneas de crisis.
2. Agrega una línea (país, ciudad opcional, nombre, teléfono, orden) o edita una existente.
3. Activa o desactiva líneas.
4. El sistema guarda los cambios.

**Flujos alternos**

- **Sin líneas cargadas para el país:** el sistema usa la lista fija incluida en el código.

### CU34 · Ver estadísticas

| | |
|---|---|
| **Actor principal** | Administrador |
| **Precondiciones** | Sesión de administrador. |
| **Postcondiciones** | Ninguna (consulta). |
| **Requerimientos** | RF29 |

**Flujo básico**

1. El administrador abre el panel.
2. El sistema muestra totales de usuarios, pacientes, psicólogos verificados, usuarios desactivados, entradas, análisis con IA, sesiones, recomendaciones, notificaciones y entradas archivadas.

## 2.6 Matriz de trazabilidad (requerimientos → casos de uso → pruebas)

| Requerimiento | Caso de uso | Prueba automática que lo verifica |
|---|---|---|
| RF01–RF02 | CU01 | `test_app_starts_without_gemini_key`, `test_ai_health_requires_authentication` |
| RF03, RNF04 | CU02 | 15 pruebas de `test_password_reset.py` |
| RF05–RF06 | CU03 | `test_diary_requires_informed_consent`, `test_outdated_consent_version_is_rejected`, `test_ai_analysis_requires_ai_consent_and_can_be_revoked` |
| RF10 | CU07 | `test_analysis_sends_json_request_to_configured_server`, `test_parses_markdown_wrapped_json`, `test_invalid_responses_trigger_fallback` |
| RF11 | CU07 | `test_screen_risk_phrases` (9 casos), `test_highest_risk_keeps_the_most_severe`, `test_auto_analysis_never_below_phrase_filter`, `test_patient_cannot_set_own_risk` |
| RF12 | CU08 | `test_high_risk_gives_crisis_support_and_alerts_professional` |
| RF13 | CU09 | `test_weekly_summary_skips_ai_without_consent`, `test_summary_returns_plain_text` |
| RF14, RF22 | CU10, CU23 | `test_ai_recommendation_waits_for_professional_review`, `test_no_ai_recommendation_for_high_risk_without_professional` |
| RF15–RF16, RF19–RF20 | CU11, CU20, CU21 | `test_sharing_mode_limits_what_professional_sees`, `test_from_date_requires_share_from`, 8 pruebas de `test_professional_portal.py` |
| RF17 | CU12 | `test_export_and_erase_my_data` |
| RF21 | CU22 | `test_risk_alert_lifecycle_and_audit` |
| RF27, RNF14 | CU32 | `test_admin_chooses_ai_provider_chain`, `test_invalid_ai_chain_is_rejected`, `test_fake_provider_rejected_in_production` |
| RF28 | CU33 | `test_admin_manages_crisis_lines_shown_to_patient`, `test_without_managed_lines_the_fixed_list_is_used` |
| RNF02 | Transversal | `test_clinical_text_is_encrypted_at_rest` |
| RNF08 | CU07 | `test_falls_back_in_order`, `test_raises_when_every_provider_fails` |

# 3. Flujo de trabajo: Análisis

El análisis refina los casos de uso en términos del sistema, sin decidir aún la
tecnología. Se usan las tres clases de análisis del Proceso Unificado:

| Estereotipo | Símbolo | Responsabilidad | Ejemplos en DEI |
|---|---|---|---|
| Interfaz (`boundary`) | Círculo con línea vertical | Comunicación con actores o sistemas externos | Pantalla Nueva entrada, Servicio de IA, Servicio Whisper |
| Control (`control`) | Círculo con flecha | Coordinación y reglas de un caso de uso | Gestor de análisis, Evaluador de riesgo, Gestor de vínculos |
| Entidad (`entity`) | Círculo con línea inferior | Información persistente del dominio | Entrada emocional, Análisis, Alerta, Consentimiento |

## 3.1 Clases de análisis por caso de uso

### Registrar y analizar una entrada (CU04, CU05, CU06, CU07, CU08)

![Clases de análisis: registrar y analizar](diagramas/png/16-analisis-registrar-analizar.png)

| Clase | Tipo | Responsabilidad |
|---|---|---|
| Pantalla Nueva entrada | Interfaz | Capturar texto o grabar audio |
| Pantalla Detalle y análisis | Interfaz | Pedir el análisis y mostrar el resultado y la ayuda en crisis |
| Servicio de IA | Interfaz | Comunicación con Ollama o Gemini |
| Servicio Whisper | Interfaz | Comunicación con el servidor de transcripción |
| Gestor de entradas | Control | Validar consentimiento informado y guardar la entrada |
| Gestor de transcripción | Control | Obtener el texto del audio |
| Gestor de análisis | Control | Pedir el análisis con la cadena de proveedores y guardarlo |
| Evaluador de riesgo | Control | Filtro determinista; decidir el nivel final |
| Gestor de crisis | Control | Líneas de crisis, alertas y notificaciones |
| Entrada emocional, Transcripción, Análisis emocional, Alerta de riesgo, Consentimiento de plataforma | Entidad | Información persistente |

### Vincular paciente y psicólogo (CU11, CU20, CU21)

![Clases de análisis: vinculación](diagramas/png/17-analisis-vinculacion.png)

### Atender alertas y revisar recomendaciones (CU22, CU23)

![Clases de análisis: alertas y recomendaciones](diagramas/png/18-analisis-alertas.png)

## 3.2 Diagramas de comunicación

Muestran los mensajes numerados entre objetos de análisis para realizar un caso
de uso.

![Comunicación: analizar entrada](diagramas/png/19-comunicacion-analisis.png)

![Comunicación: vinculación](diagramas/png/20-comunicacion-vinculacion.png)

## 3.3 Diagramas de secuencia por caso de uso

### CU01 · Registrarse e iniciar sesión

![Secuencia CU01](diagramas/png/21-secuencia-login.png)

### CU02 · Recuperar contraseña

![Secuencia CU02](diagramas/png/09-secuencia-recuperar-contrasena.png)

### CU03 · Aceptar consentimientos

![Secuencia CU03](diagramas/png/22-secuencia-consentimiento.png)

### CU05 y CU06 · Entrada de voz y transcripción

![Secuencia CU05-CU06](diagramas/png/07-secuencia-entrada-audio.png)

### CU07 · Analizar entrada con IA

![Secuencia CU07](diagramas/png/05-secuencia-analisis-ia.png)

### CU08 y CU22 · Crisis y atención de la alerta

![Secuencia CU08-CU22](diagramas/png/06-secuencia-alerta-crisis.png)

### CU11 y CU20 · Vinculación

![Secuencia CU11-CU20](diagramas/png/23-secuencia-vinculacion.png)

### CU10 y CU23 · Recomendaciones y revisión

![Secuencia CU10-CU23](diagramas/png/24-secuencia-revision-recomendacion.png)

### CU32 · Configurar cadena de IA

![Secuencia CU32](diagramas/png/25-secuencia-config-ia.png)

## 3.4 Diagrama de actividad

Flujo completo de una entrada del diario, desde que el paciente la escribe o
graba hasta que ve el análisis, con las decisiones de consentimiento,
disponibilidad de IA y riesgo.

![Actividad: diario](diagramas/png/26-actividad-diario.png)


# 4. Flujo de trabajo: Diseño

## 4.1 Arquitectura del sistema

DEI es un sistema **cliente-servidor en tres niveles** con servicios de IA
externos:

1. **Presentación:** aplicación Flutter (Android, iOS, web).
2. **Lógica de negocio:** API REST en FastAPI (`dei_backend`).
3. **Datos:** PostgreSQL.
4. **Servicios de IA:** Ollama y Whisper en la red local (directamente o a través
   de `dei_ai`), y Gemini en la nube como respaldo.

![Componentes del sistema](diagramas/png/02-componentes-sistema.png)

### 4.1.1 Decisiones de arquitectura

| Decisión | Alternativas consideradas | Motivo |
|---|---|---|
| API REST con FastAPI | Django, Node.js | Tipado con Pydantic, documentación automática (Swagger), rendimiento y facilidad con Python para IA |
| Arquitectura por módulos con capas router-service-repository | Capas globales | Cada módulo de negocio es independiente y fácil de ubicar |
| Patrón Repository | Consultas en los servicios | Aísla SQLAlchemy y facilita pruebas |
| Patrón Strategy + Factory para la IA | Llamadas directas a cada API | Cambiar o sumar proveedores sin tocar los servicios |
| Cadena de responsabilidad (`AIProviderChain`) | Un solo proveedor | Disponibilidad: si falla uno se usa el siguiente |
| IA local primero | Solo Gemini | Costo cero por token y menos exposición de datos |
| Filtro de riesgo determinista | Solo IA | La seguridad no puede depender de un modelo probabilístico |
| JWT sin estado + `token_version` | Sesiones en servidor | Escala y permite invalidar todas las sesiones |
| Cifrado de campos (Fernet) | Cifrado de disco | Protege los datos aunque se filtre un respaldo de la base |
| Flutter con Riverpod y go_router | Apps nativas, React Native | Un código para Android, iOS y web; estado y navegación declarativos |
| App por features con capas domain/data/presentation | Por tipo de archivo | Cohesión por funcionalidad |
| Alembic | `create_all` | Esquema versionado y migraciones reproducibles |

## 4.2 Diagrama de paquetes

![Paquetes del backend](diagramas/png/29-diseno-paquetes.png)

## 4.3 Clases de diseño

### 4.3.1 Módulo de análisis (backend)

![Clases de diseño: análisis](diagramas/png/28-diseno-clases-analisis.png)

Cada módulo del backend repite la misma estructura:

| Capa | Clase | Responsabilidad |
|---|---|---|
| Router | `EmotionalAnalysisRouter` | Endpoints HTTP, dependencias de autenticación, rol y consentimiento |
| Servicio | `EmotionalAnalysisService` | Reglas de negocio del caso de uso |
| Repositorio | `EmotionalAnalysisRepository` | Consultas a la base de datos |
| Modelo | `EmotionalAnalysis` | Tabla `emotional_analyses` |
| Esquemas | `EmotionalAnalysisCreate`, `EmotionalAnalysisResponse` | Validación de entrada y salida |
| Proveedores | `BaseAnalysisProvider` y sus implementaciones | Estrategia de IA |

### 4.3.2 Aplicación Flutter

![Clases de diseño: app](diagramas/png/10-app-capas.png)

### 4.3.3 Servicio de IA local

![Clases de diseño: dei_ai](diagramas/png/12-ia-componentes.png)

### 4.3.4 Patrones de diseño aplicados

| Patrón | Dónde | Para qué |
|---|---|---|
| Repository | `app/*/repositories` | Separar el acceso a datos de la lógica |
| Service Layer | `app/*/services` | Centralizar reglas de negocio |
| Strategy | `providers/*` (análisis, resumen, recomendaciones, transcripción) | Intercambiar proveedores de IA |
| Factory | `provider_factory.py` | Crear el proveedor por nombre |
| Chain of Responsibility | `AIProviderChain` | Probar proveedores en orden |
| Dependency Injection | `Depends()` de FastAPI, `ref.watch` de Riverpod | Desacoplar y facilitar pruebas |
| Pipeline | `AnalysisPipeline` en `dei_ai` | Parsear, validar y normalizar la respuesta |
| Singleton | `WhisperClient` en `dei_ai` | Cargar el modelo una sola vez |
| Interceptor | `AuthInterceptor` (Dio) | Agregar el token y reaccionar a un 401 |

## 4.4 Modelo de datos

19 tablas en PostgreSQL. Los campos marcados *cifrado* se guardan con Fernet.

![Modelo de datos](diagramas/png/04-modelo-datos.png)

### 4.4.1 Diccionario de datos (tablas principales)

| Tabla | Descripción | Campos clave |
|---|---|---|
| `users` | Cuentas | `email` (único), `password_hash`, `role`, `is_active`, `token_version` |
| `patient_profiles` | Perfil del paciente | `user_id` (único), nombre, apellido, `birth_date`, `gender` |
| `professional_profiles` | Perfil del psicólogo | `user_id` (único), `license_number`, `specialties`, `is_verified`, `verified_at` |
| `emotional_entries` | Entradas del diario | `patient_id`, `entry_type` (TEXT/AUDIO), `text_content` (cifrado), `audio_path`, `is_archived` |
| `audio_transcriptions` | Transcripción de una entrada de audio | `entry_id` (único), `transcription_text` (cifrado), `provider` |
| `emotional_analyses` | Análisis de una entrada | `entry_id` (único), `primary_emotion`, `emotion_intensity`, `risk_level`, `provider`, `model`, `analysis_json` (cifrado) |
| `patient_recommendations` | Recomendaciones | `analysis_id`, `title`, `content` (cifrado), `status`, `reviewed_by_professional_id` |
| `risk_alerts` | Alertas de riesgo | `patient_id`, `professional_id`, `analysis_id`, `risk_level`, `status`, `resolution_note` |
| `link_requests` | Solicitudes de vínculo | `patient_id`, `professional_id`, `status`, `sharing_mode`, `share_from` |
| `patient_professionals` | Relación terapéutica | `sharing_mode`, `share_from`, `active`, `ended_at` |
| `consents` | Permiso del paciente a un psicólogo | `granted`, `granted_at`, `revoked_at` |
| `platform_consents` | Consentimiento informado y de IA | `consent_type`, `version`, `granted_at`, `revoked_at` |
| `therapy_sessions` | Sesiones | `session_date`, `status` |
| `clinical_notes` | Notas clínicas | `session_id`, `note` (cifrado) |
| `notifications` | Notificaciones en la app | `user_id`, `title`, `message`, `type`, `is_read` |
| `access_audit_logs` | Auditoría | `professional_id`, `patient_id`, `action`, `created_at` |
| `password_reset_codes` | Códigos de recuperación | `code_hash`, `expires_at`, `failed_attempts`, `consumed_at` |
| `crisis_lines` | Líneas de crisis | `country_code`, `city`, `name`, `phone`, `sort_order`, `is_active` |
| `system_settings` | Configuración (cadena de IA) | `key`, `value`, `updated_by_user_id` |

### 4.4.2 Catálogos (enumeraciones)

| Catálogo | Valores |
|---|---|
| Rol | PATIENT, PROFESSIONAL, ADMIN |
| Tipo de entrada | TEXT, AUDIO |
| Intensidad | LOW, MEDIUM, HIGH |
| Nivel de riesgo | LOW, MEDIUM, HIGH, CRITICAL |
| Emociones (22) | Alegría, Tristeza, Ansiedad, Miedo, Ira, Asco, Sorpresa, Calma, Estrés, Desánimo, Culpa, Vergüenza, Soledad, Frustración, Confusión, Esperanza, Confianza, Gratitud, Agotamiento, Amor, Preocupación, Desesperanza |
| Modo de compartir | FULL_HISTORY, FROM_DATE, NEW_ONLY |
| Estado de solicitud | PENDING, ACCEPTED, REJECTED |
| Estado de sesión | SCHEDULED, COMPLETED, CANCELLED |
| Estado de recomendación | PENDING_REVIEW, APPROVED, REJECTED |
| Estado de alerta | NEW, SEEN, RESOLVED |
| Consentimiento de plataforma | INFORMED_CONSENT, AI_PROCESSING |
| Tipo de notificación | SESSION, RISK_ALERT, RECOMMENDATION |
| Acción auditada | VIEW_INSIGHTS, VIEW_RISK_ALERTS, REVIEW_RISK_ALERT, VIEW_CLINICAL_NOTES, CREATE_CLINICAL_NOTE, CREATE_SESSION, REVIEW_RECOMMENDATION, PATIENT_ACCESS, VIEW_ENTRIES |

## 4.5 Diagramas de estados

![Estados de la alerta](diagramas/png/08-estados-alerta.png)

![Estados del dominio](diagramas/png/27-estados-dominio.png)

![Estados de la sesión de la app](diagramas/png/11-app-navegacion.png)

## 4.6 Diseño de la interfaz

La interfaz usa Material Design con una paleta verde azulada. En teléfonos la
navegación es una barra inferior; en pantallas anchas (web, tableta), un menú
lateral. Cada rol tiene su propio menú.

| Rol | Menú |
|---|---|
| Paciente | Inicio, Diario, Consejos (recomendaciones), Ajustes |
| Psicólogo | Panel, Pacientes, Alertas, Revisar, Cuenta |
| Administrador | Panel, Usuarios, Psicólogos, Ajustes, Cuenta |

**Inicio de sesión y recuperación de contraseña**

![Login](diagramas/capturas/login.png)

![Recuperar contraseña](diagramas/capturas/recuperar-codigo.png)

**Panel del psicólogo:** pacientes activos, pacientes con riesgo (resaltado en
rojo), solicitudes pendientes e insights; accesos a sesiones y a
recomendaciones por revisar.

![Panel del psicólogo](diagramas/capturas/pro-panel.png)

**Pacientes del psicólogo:** solicitudes con el modo de compartir elegido
(aceptar o rechazar) y lista de pacientes con desde cuándo comparten.

![Pacientes](diagramas/capturas/pro-pacientes.png)

**Panel de administración:** aviso de psicólogos por verificar y métricas de
usuarios y actividad.

![Panel de administración](diagramas/capturas/admin-panel.png)

**Usuarios (vista móvil):** búsqueda por correo, filtro por rol e interruptor
para activar o desactivar.

![Usuarios](diagramas/capturas/admin-usuarios.png)

### 4.6.1 Mapa de navegación

| Ruta | Pantalla | Rol |
|---|---|---|
| `/login`, `/register`, `/forgot-password`, `/reset-password` | Autenticación | Público |
| `/onboarding/profile`, `/onboarding/consent`, `/onboarding/professional` | Primer ingreso | Paciente / psicólogo |
| `/home` | Inicio con resumen semanal | Paciente |
| `/entries`, `/entries/new`, `/entries/{id}` | Diario, nueva entrada, detalle y análisis | Paciente |
| `/recommendations` | Recomendaciones | Paciente |
| `/settings`, `/settings/privacy`, `/settings/professional` | Ajustes, consentimientos, mi psicólogo | Paciente |
| `/pro`, `/pro/patients`, `/pro/patients/{id}` | Panel, pacientes, ficha | Psicólogo |
| `/pro/alerts`, `/pro/reviews`, `/pro/sessions`, `/pro/sessions/{id}` | Alertas, revisión, sesiones | Psicólogo |
| `/admin`, `/admin/users`, `/admin/professionals`, `/admin/settings` | Administración | Administrador |
| `/notifications` | Notificaciones | Paciente y psicólogo |


# 5. Flujo de trabajo: Implementación

## 5.1 Diagrama de componentes

![Componentes](diagramas/png/02-componentes-sistema.png)

## 5.2 Diagrama de despliegue

![Despliegue](diagramas/png/01-despliegue.png)

| Nodo | Software | Puerto |
|---|---|---|
| Dispositivo del usuario | App DEI (APK, IPA o web estática) | — |
| ThinkPad | Uvicorn + FastAPI (`dei_backend`), PostgreSQL, carpeta `uploads/` | 8000, 5432 |
| Nitro 5 | Ollama (`llama3.1:8b`), servidor Whisper compatible con OpenAI, `dei_ai` | 11434, 8000, 8001 |
| Google Cloud | Gemini API | 443 |
| Proveedor SMTP | Correo saliente | 587 / 465 |

## 5.3 Tecnologías

| Capa | Tecnología | Versión |
|---|---|---|
| App | Flutter (fijado con FVM) / Dart | 3.50 / 3.14 |
| App | flutter_riverpod, go_router, dio, flutter_secure_storage, record, url_launcher | 3.5, 18.1, 5.11, 11.2, 7.2, 6.3 |
| Backend | Python, FastAPI, Uvicorn | 3.12+, 0.136, 0.49 |
| Backend | SQLAlchemy, Alembic, psycopg2 | 2.0, 1.18, 2.9 |
| Backend | python-jose (JWT), passlib + bcrypt, cryptography (Fernet) | 3.5, 1.7 / 4.0, 48 |
| Backend | httpx, google-genai | 0.28, 2.9 |
| Base de datos | PostgreSQL | 14+ |
| IA local | FastAPI, pydantic-settings, faster-whisper, ctranslate2 | 0.141, 2.14, 1.2, 4.8 |
| IA local | Ollama con `llama3.1:8b` | — |
| Pruebas | pytest; flutter_test + mocktail | 9.1; SDK, 1.0 |

## 5.4 Estructura del código

**Backend (`dei_backend`)**

```
app/
  main.py                FastAPI, CORS, manejador 503 de IA, registro de routers
  core/                  config, database, dependencies, security, rate_limit, logging
  identity/ therapy/ platform_consents/ entries/ analysis/ recommendations/
  risk_alerts/ sessions/ notifications/ dashboard/ therapy_insights/
  administration/ audit/ health/
    routers/ services/ repositories/ models/ schemas/ [providers/]
  shared/  ai/ safety/ security/ email/ enums/ emotions.py
alembic/   migraciones
tests/     pruebas automáticas
```

**Aplicación (`dei_app`)**

```
lib/
  core/       config, network, storage, router, theme, widgets, utils
  features/   auth, profile, consents, entries, analysis, home, recommendations,
              therapy, notifications, professional, admin
    domain/ data/ presentation/
test/         pruebas
```

**IA local (`dei_ai`)**

```
app/
  analysis/ transcription/   api, services, pipeline, schemas
  providers/                 factory, registry y proveedores por tarea
  clients/                   ollama, whisper
  prompts/                   prompt del análisis
  shared/                    enums, normalizadores, parser, validador
  tests/
```

## 5.5 API REST (resumen)

| Prefijo | Endpoints principales | Rol |
|---|---|---|
| `/auth` | register, login, me, forgot-password, verify-reset-code, reset-password | Público / todos |
| `/patients` | profile, profile/me, me/data/export, me/data/erase | Paciente |
| `/professionals` | profile, profile/me, me/patients, me/patients/{id}/entries, directory, pending, {id}/verify | Psicólogo / admin |
| `/platform-consents` | documents, crear, listar, {tipo}/revoke | Paciente |
| `/therapy/link-requests` | crear, pending, {id}/accept, {id}/reject | Paciente / psicólogo |
| `/therapy/consents` | crear, listar, {id}/revoke | Paciente |
| `/entries` | crear, audio, listar, {id}, {id}/archive | Paciente |
| `/analysis` | transcriptions/…, entries/{id}, entries/{id}/auto, entries/{id}/reanalyze, weekly-summary | Paciente |
| `/recommendations` | listar, generate/{id}, review/pending, review/{id}/approve, review/{id}/reject | Paciente / psicólogo |
| `/risk-alerts` | listar, inbox, {id}/seen, {id}/resolve | Psicólogo |
| `/sessions` | crear, listar, {id}/complete, {id}/cancel, {id}/notes | Psicólogo / paciente |
| `/notifications` | listar, summary, {id}/read | Paciente / psicólogo |
| `/dashboard`, `/therapy-insights` | patient, professional, patient/{id} | Según rol |
| `/audit` | my-access-log | Paciente |
| `/admin` | dashboard, statistics, users, professionals, crisis-lines, ai-settings | Administrador |
| `/health` | ai | Administrador |

La documentación interactiva completa está en `/docs` (Swagger) al levantar el
backend.

## 5.6 Integración con la IA

| Tarea | Proveedores | Detalle |
|---|---|---|
| Análisis emocional | Ollama → Gemini → (Fake en desarrollo) | JSON con emoción, intensidad, riesgo y análisis; validado y normalizado al catálogo de 22 emociones |
| Resumen semanal | Ollama → Gemini | Texto libre, solo con consentimiento de IA |
| Recomendaciones | Ollama | Título y contenido; revisión profesional si hay psicólogo |
| Transcripción | Whisper por HTTP o en proceso | Español; el backend envía el audio por multipart |

El servicio `dei_ai` implementa el mismo contrato de análisis
(`primary_emotion`, `emotion_intensity`, `risk_level`, `provider`, `model`,
`analysis_json`) y el mismo catálogo de emociones. Su integración como un
proveedor más de la cadena es el siguiente paso planificado.

![Integración backend e IA](diagramas/png/14-integracion-backend-ia.png)

# 6. Flujo de trabajo: Pruebas

## 6.1 Plan de pruebas

### 6.1.1 Objetivo

Verificar que DEI cumple los requerimientos funcionales y no funcionales, con
énfasis en la **seguridad clínica** (detección de riesgo, consentimientos,
acceso del psicólogo) y la **privacidad** (cifrado, auditoría), y que la
integración con la IA tolera fallas.

### 6.1.2 Alcance y niveles

| Nivel | Qué se prueba | Herramienta | Dónde |
|---|---|---|---|
| Unitarias | Filtro de riesgo, normalizadores de emociones e intensidad, parser de respuestas de IA, cadena de proveedores, validadores, modelos | pytest, flutter_test | Los tres repositorios |
| Integración | Endpoints de la API con base de datos en memoria y proveedores de IA simulados | pytest + TestClient de FastAPI | `dei_backend` |
| Contrato | El backend y `dei_ai` usan el mismo catálogo de emociones y sinónimos | pytest | `dei_backend`, `dei_ai` |
| Componentes de UI | Pantalla y controlador de recuperación de contraseña, redirección por rol | flutter_test + mocktail | `dei_app` |
| Sistema (manual) | Recorridos completos por rol en dispositivo | Manual | Pendiente (fase de Transición) |

### 6.1.3 Estrategia

- Las pruebas **no necesitan** Ollama, Whisper, Gemini ni PostgreSQL: usan SQLite
  en memoria y respuestas HTTP simuladas. Se pueden correr en cualquier equipo y
  no gastan tokens.
- Cada requerimiento de seguridad tiene al menos una prueba (ver la matriz de
  trazabilidad, sección 2.6).
- Las pruebas de riesgo usan frases reales que deben detectarse y frases
  parecidas que **no** deben detectarse ("Me corté el pelo", "Me mató de risa el
  chiste") para evitar falsos positivos obvios.

### 6.1.4 Criterios de aceptación

- El 100 % de las pruebas automáticas pasan.
- Ninguna prueba se omite ni se desactiva.
- Ningún caso de riesgo HIGH o CRITICAL del conjunto de prueba queda sin detectar.

### 6.1.5 Entorno de ejecución

| Elemento | Valor |
|---|---|
| Fecha de ejecución | 20 de noviembre de 2026 |
| Python | 3.13 |
| Base de datos de prueba | SQLite en memoria |
| Versión probada | Backend con las PR #1 a #6; `dei_ai` con las PR #1 y #3 |
| Comandos | `pytest` en `dei_backend` y en `dei_ai`; `fvm flutter test` en `dei_app` |

## 6.2 Resultados

| Componente | Pruebas | Pasaron | Fallaron | Observación |
|---|---|---|---|---|
| Backend (`dei_backend`) | 88 | 88 | 0 | Ejecutadas para este documento |
| Servicio de IA (`dei_ai`) | 42 | 42 | 0 | Ejecutadas para este documento |
| App (`dei_app`) | 27 | 27 | 0 | Resultado reportado por el proyecto (`fvm flutter test`); no se volvió a ejecutar para este documento |
| **Total** | **157** | **157** | **0** | |

| Archivo de pruebas (backend) | Pruebas | Área |
|---|---|---|
| `test_clinical_safety.py` | 26 | Riesgo, crisis, consentimientos, compartir, alertas, recomendaciones, cifrado, exportar/borrar |
| `test_password_reset.py` | 15 | Recuperación de contraseña |
| `test_emotions.py` | 14 | Catálogo de emociones y contrato con `dei_ai` |
| `test_professional_portal.py` | 8 | Panel del psicólogo y acceso a entradas |
| `test_admin_settings.py` | 6 | Líneas de crisis y cadena de IA |
| `test_ollama_providers.py` | 6 | Proveedores Ollama |
| `test_analysis_parser.py` | 5 | Parser de respuestas de IA |
| `test_provider_chain.py` | 4 | Cadena de proveedores |
| `test_app.py`, `test_whisper_provider.py` | 4 | Arranque, salud de IA, Whisper |

La lista completa de las 130 pruebas de Python con su resultado está en el
anexo 7.3.

## 6.3 Casos de prueba

| ID | Caso de uso | Descripción | Entrada / pasos | Resultado esperado | Resultado obtenido |
|---|---|---|---|---|---|
| CP01 | CU07 | Frase de ideación suicida | "Tengo ganas de morir" | Riesgo HIGH | HIGH. Pasó |
| CP02 | CU07 | Frase con plan explícito | "Ya compré las pastillas, esta noche lo hago" | Riesgo CRITICAL | CRITICAL. Pasó |
| CP03 | CU07 | Frase cotidiana parecida | "Me corté el pelo" / "Me mató de risa el chiste" | Sin riesgo | Sin riesgo. Pasó |
| CP04 | CU07 | La IA subestima el riesgo | IA responde LOW para un texto con frase HIGH | Nivel final HIGH | HIGH. Pasó |
| CP05 | CU07 | El paciente intenta fijar su riesgo | Análisis manual con `risk_level` del paciente | Se ignora; solo el filtro asigna | Ignorado. Pasó |
| CP06 | CU08 | Crisis con psicólogo vinculado | Análisis HIGH de paciente con relación y consentimiento | Respuesta con líneas de crisis, `professional_notified=true`, alerta NEW y notificación | Correcto. Pasó |
| CP07 | CU03 | Diario sin consentimiento informado | Crear entrada sin consentimiento | 403 | 403. Pasó |
| CP08 | CU03 | Consentimiento con versión vieja | Aceptar versión anterior | 400 | 400. Pasó |
| CP09 | CU03, CU07 | Consentimiento de IA | Analizar sin consentimiento, aceptarlo y analizar, revocarlo y reanalizar | 403, luego 200, luego 403 | Correcto. Pasó |
| CP10 | CU09 | Resumen sin consentimiento de IA | Pedir resumen semanal | Resumen sin llamar a la IA | Correcto. Pasó |
| CP11 | CU21 | Modo "solo nuevas" | Paciente con 1 entrada previa y 1 nueva | El psicólogo ve 1 | 1. Pasó |
| CP12 | CU21 | Modo "todo el historial" | Igual que CP11 | El psicólogo ve 2 | 2. Pasó |
| CP13 | CU21 | Sin relación o sin consentimiento | Psicólogo pide entradas | 403 | 403. Pasó |
| CP14 | CU22 | Ciclo de una alerta | Ver bandeja, marcar vista, resolver con nota | NEW → SEEN → RESOLVED, con auditoría | Correcto. Pasó |
| CP15 | CU10, CU23 | Recomendación con psicólogo | Generar recomendación | Estado PENDING_REVIEW, no visible al paciente hasta aprobar | Correcto. Pasó |
| CP16 | CU10 | Riesgo alto sin psicólogo | Generar recomendación de un análisis HIGH | 409, no se genera | 409. Pasó |
| CP17 | RNF02 | Cifrado en reposo | Guardar entrada y leer la columna en la base | El texto no aparece en claro | Cifrado. Pasó |
| CP18 | CU12 | Exportar y borrar | Exportar, borrar con `ELIMINAR` | JSON completo; luego sin datos | Correcto. Pasó |
| CP19 | CU02 | Recuperación completa | Pedir código, verificar, cambiar | Contraseña nueva válida y sesiones anteriores cerradas | Correcto. Pasó |
| CP20 | CU02 | No revelar si el correo existe | Pedir código para correo inexistente | Misma respuesta que uno existente | Correcto. Pasó |
| CP21 | CU02 | Código agotado | 5 intentos fallidos | El código se anula | Correcto. Pasó |
| CP22 | CU02 | Límite por IP | Superar el límite de solicitudes | 429 con `Retry-After` | 429. Pasó |
| CP23 | CU07, RNF08 | Ollama caído | Servidor Ollama no responde | Se usa Gemini | Correcto. Pasó |
| CP24 | RNF08 | Todos los proveedores fallan | Cadena sin respuesta | `AIProviderException` → 503 | Correcto. Pasó |
| CP25 | CU07 | Respuesta de IA inválida | "no es json", campos faltantes, intensidad "ALTA" | Se descarta y se pasa al siguiente proveedor | Correcto. Pasó |
| CP26 | CU32 | Cadena de IA inválida | Cadena vacía o con proveedor desconocido | 400 | 400. Pasó |
| CP27 | CU32, RNF14 | FAKE en producción | `APP_ENV=production` con FAKE | Rechazado | Rechazado. Pasó |
| CP28 | CU33 | Líneas de crisis del administrador | Crear línea y provocar crisis | El paciente ve la línea nueva | Correcto. Pasó |
| CP29 | CU06 | Whisper caído | Servidor de transcripción no responde | 503 claro | Correcto. Pasó |
| CP30 | Contrato | Catálogo de emociones | Comparar backend y `dei_ai` | Mismas 22 emociones y sinónimos | Iguales. Pasó |

## 6.4 Pruebas pendientes (fase de Transición)

| Prueba | Motivo |
|---|---|
| Recorridos completos en Android, iOS y web contra el backend real | La app se validó con análisis estático, pruebas y compilación web |
| Rendimiento del análisis con la IA local (tiempos en la Nitro 5) | Depende del hardware |
| Usabilidad con pacientes y psicólogos reales | Requiere participantes y consentimiento |
| Revisión clínica de las frases de riesgo y del prompt | Requiere un profesional de salud mental |


# 7. Anexos

## 7.1 Manual de usuario

### 7.1.1 Paciente

**Primer ingreso**

1. Abre DEI y toca **¿No tienes cuenta? Regístrate**. Elige **Soy paciente**,
   escribe tu correo y una contraseña de al menos 8 caracteres.
2. Inicia sesión con tu correo y contraseña.
3. Completa tu perfil: nombre, apellido, fecha de nacimiento y género.
4. Lee y acepta el **consentimiento informado**. DEI no es un servicio de
   emergencias.
5. Decide si aceptas el **procesamiento con IA**. Si no lo aceptas, puedes usar
   el diario igual, pero tus entradas no se analizarán.

**Escribir o grabar una entrada**

1. Ve a **Diario** y toca **Escribir**.
2. Elige la pestaña **Escribir** y cuenta cómo te sientes, o la pestaña
   **Grabar** para dejar una nota de voz.
3. Guarda. Si grabaste, verás la transcripción y podrás corregirla.
4. Toca **Analizar con IA** para ver tu emoción principal, su intensidad, el
   nivel de riesgo y los temas detectados. Si la IA no está disponible, tu
   entrada queda guardada y puedes analizarla más tarde.

**Si aparece la tarjeta de ayuda.** Cuando una entrada muestra señales de
riesgo, DEI te muestra líneas de ayuda de tu país con un botón para llamar, y
avisa a tu psicólogo si tienes uno vinculado. Si estás en peligro inmediato,
llama a emergencias.

**Resumen y consejos**

- En **Inicio** verás el resumen de tu semana.
- En **Consejos** puedes pedir una recomendación sobre una entrada analizada.
  Si tienes psicólogo, aparecerá "en revisión" hasta que la apruebe.

**Vincularte con tu psicólogo**

1. Ve a **Ajustes → Mi psicólogo** y busca en el directorio.
2. Elige qué compartir: **todo tu historial**, **desde una fecha** o **solo
   entradas nuevas**, y envía la solicitud.
3. Cuando el psicólogo acepte, toca **Dar acceso**. Puedes quitar el acceso
   cuando quieras.

**Privacidad.** En **Ajustes → Privacidad** puedes revocar el consentimiento de
IA. La exportación y el borrado de tus datos, y la consulta de accesos, ya
están disponibles en el servidor; su pantalla en la app está pendiente.

**Olvidé mi contraseña.** En el inicio de sesión toca **¿Olvidaste tu
contraseña?**, escribe tu correo, ingresa el código de 6 dígitos que te llega
(vence en 15 minutos) y elige una contraseña nueva. Se cerrarán tus otras
sesiones.

### 7.1.2 Psicólogo

1. **Registro:** elige **Soy psicólogo**, inicia sesión y completa tu perfil
   profesional (número de licencia y especialidades). Hasta que el
   administrador te verifique verás un aviso y no aparecerás en el directorio.
2. **Panel:** pacientes activos, pacientes con riesgo, solicitudes pendientes e
   insights.
3. **Pacientes:** acepta o rechaza solicitudes (verás qué eligió compartir cada
   paciente). Abre la ficha de un paciente para ver el resumen, sus entradas
   compartidas con análisis y sus sesiones. Cada consulta queda registrada.
4. **Alertas:** revisa las alertas nuevas, márcalas como vistas y, después de
   contactar al paciente, resuélvelas con una nota.
5. **Revisar:** aprueba (puedes editar el texto) o rechaza las recomendaciones
   que propone la IA para tus pacientes.
6. **Sesiones:** agenda sesiones, márcalas como completadas o canceladas, y
   escribe notas clínicas (se guardan cifradas).

### 7.1.3 Administrador

1. **Acceso:** el administrador no se registra desde la app; se crea en la base
   de datos (ver el manual técnico, 7.2.5).
2. **Panel:** métricas de usuarios y de actividad, y aviso de psicólogos por
   verificar.
3. **Psicólogos:** revisa la licencia de cada psicólogo pendiente y toca
   **Verificar**.
4. **Usuarios:** busca por correo, filtra por rol y activa o desactiva cuentas.
5. **Ajustes → Proveedor de IA:** arrastra para ordenar la cadena (por ejemplo,
   Ollama primero y Gemini después). Puedes volver a la configuración del
   servidor.
6. **Ajustes → Líneas de crisis:** agrega, edita, ordena y activa las líneas de
   ayuda por país.

## 7.2 Manual técnico de instalación

### 7.2.1 Requisitos

| Componente | Requisito |
|---|---|
| Backend | Python 3.12 o superior, PostgreSQL 14 o superior, Git |
| IA local | Equipo con GPU recomendada, Ollama, Python 3.12 o superior |
| App | Flutter con FVM (versión en `.fvmrc`), Android Studio o Xcode o Chrome |
| Red | Backend e IA en la misma red local; puertos 8000, 8001, 11434 abiertos solo para la red local |

### 7.2.2 Backend (`dei_backend`)

```bash
git clone https://github.com/ronaldflores2004/dei_backend.git
cd dei_backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

Completa en `.env`:

| Variable | Valor |
|---|---|
| `DATABASE_URL` | `postgresql://usuario:clave@localhost:5432/dei` |
| `SECRET_KEY` | Texto aleatorio de 32 o más caracteres |
| `DATA_ENCRYPTION_KEYS` | Generar con `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` y guardar una copia fuera del servidor |
| `AI_PROVIDER_CHAIN` | `OLLAMA,GEMINI` |
| `OLLAMA_BASE_URL` | `http://<ip-de-la-nitro>:11434` |
| `WHISPER_API_URL` | `http://<ip-de-la-nitro>:8000` |
| `GEMINI_API_KEY` | Clave de Gemini (opcional) |
| `SMTP_*` | Datos del correo saliente (sin `SMTP_HOST`, en desarrollo el código se escribe en el log) |
| `CORS_ORIGINS` | Origen de la app web, por ejemplo `http://localhost:5000` |

```bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Comprueba en `http://localhost:8000/docs`.

### 7.2.3 IA local (Nitro 5)

```bash
# Ollama escuchando en la red (Windows)
setx OLLAMA_HOST 0.0.0.0
ollama pull llama3.1:8b

# Servicio dei_ai
git clone https://github.com/ronaldflores2004/dei_ai.git
cd dei_ai
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Para la transcripción que usa hoy el backend, levanta un servidor Whisper
compatible con la API de OpenAI (por ejemplo speaches o faster-whisper-server)
en el puerto 8000. Verifica con un administrador: `GET /health/ai`.

### 7.2.4 App (`dei_app`)

```bash
fvm install
fvm flutter pub get
# Emulador Android
fvm flutter run --dart-define-from-file=config/android-emulator.json
# Web
fvm flutter run -d chrome --web-port 5000 --dart-define-from-file=config/local.json
# Teléfono físico: copiar config/device.example.json a config/device.local.json con la IP de la PC
fvm flutter run --dart-define-from-file=config/device.local.json
```

Compilar para publicar:

```bash
fvm flutter build apk --release --dart-define=API_BASE_URL=https://api.tu-dominio
fvm flutter build web --release --dart-define=API_BASE_URL=https://api.tu-dominio
```

### 7.2.5 Crear el primer administrador

Regístrate como paciente desde la app y cambia el rol en la base de datos:

```sql
UPDATE users SET role = 'ADMIN' WHERE email = 'tu-correo@ejemplo.com';
```

### 7.2.6 Importar los diagramas en Enterprise Architect

1. **Modelo UML:** en el *Project Browser* selecciona un paquete y usa
   *Publish → Import/Export → Import Package from XMI*. Elige
   `diagramas/enterprise-architect/dei-modelo.xmi`. Se importan actores, casos
   de uso, componentes, nodos y las 19 entidades con sus relaciones. Luego crea
   los diagramas arrastrando los elementos (el XMI no guarda posiciones).
2. **Secuencias, actividad, estados y análisis:** importa los archivos
   `diagramas/plantuml/*.puml` con la opción de importar PlantUML de tu versión
   de Enterprise Architect, o redibújalos usando los PNG como referencia.

### 7.2.7 Pruebas

```bash
cd dei_backend && pytest
cd dei_ai && pytest
cd dei_app && fvm flutter analyze && fvm flutter test
```

### 7.2.8 Checklist antes de producción

- `APP_ENV=production` y sin `FAKE` en la cadena.
- `SECRET_KEY` y `DATA_ENCRYPTION_KEYS` únicas, con copia segura de la clave de
  cifrado.
- HTTPS delante del backend; `CORS_ORIGINS` solo con los dominios reales.
- SMTP configurado.
- Líneas de crisis del país revisadas por el administrador.
- Respaldos de PostgreSQL y de la carpeta de audios.

## 7.3 Lista completa de pruebas automáticas

Resultado de la ejecución del 20 de noviembre de 2026.

### 7.3.1 Backend (`dei_backend`): 88 pruebas

| # | Archivo | Prueba | Resultado |
|---|---|---|---|
| 1 | `test_admin_settings.py` | `test_admin_manages_crisis_lines_shown_to_patient` | Pasó |
| 2 | `test_admin_settings.py` | `test_without_managed_lines_the_fixed_list_is_used` | Pasó |
| 3 | `test_admin_settings.py` | `test_only_admin_manages_settings` | Pasó |
| 4 | `test_admin_settings.py` | `test_admin_chooses_ai_provider_chain` | Pasó |
| 5 | `test_admin_settings.py` | `test_invalid_ai_chain_is_rejected` | Pasó |
| 6 | `test_admin_settings.py` | `test_fake_provider_rejected_in_production` | Pasó |
| 7 | `test_analysis_parser.py` | `test_parses_markdown_wrapped_json` | Pasó |
| 8 | `test_analysis_parser.py` | `test_invalid_responses_trigger_fallback[no es json]` | Pasó |
| 9 | `test_analysis_parser.py` | `test_invalid_responses_trigger_fallback[{"primary_emotion": "Calma"}]` | Pasó |
| 10 | `test_analysis_parser.py` | `test_invalid_responses_trigger_fallback[{"primary_emotion": "Calma", "emotion_intensity": "ALTA", "risk_level": "LOW"}]` | Pasó |
| 11 | `test_analysis_parser.py` | `test_invalid_responses_trigger_fallback[{"primary_emotion": "", "emotion_intensity": "LOW", "risk_level": "LOW"}]` | Pasó |
| 12 | `test_app.py` | `test_app_starts_without_gemini_key` | Pasó |
| 13 | `test_app.py` | `test_ai_health_requires_authentication` | Pasó |
| 14 | `test_clinical_safety.py` | `test_screen_risk_phrases[Tengo ganas de morir-HIGH]` | Pasó |
| 15 | `test_clinical_safety.py` | `test_screen_risk_phrases[A veces pienso que estarían mejor sin mí-HIGH]` | Pasó |
| 16 | `test_clinical_safety.py` | `test_screen_risk_phrases[Anoche me corté los brazos-HIGH]` | Pasó |
| 17 | `test_clinical_safety.py` | `test_screen_risk_phrases[Me voy a matar-CRITICAL]` | Pasó |
| 18 | `test_clinical_safety.py` | `test_screen_risk_phrases[Ya compré las pastillas, esta noche lo hago-CRITICAL]` | Pasó |
| 19 | `test_clinical_safety.py` | `test_screen_risk_phrases[Hoy salí a caminar con mi perro-None]` | Pasó |
| 20 | `test_clinical_safety.py` | `test_screen_risk_phrases[Me corté el pelo-None]` | Pasó |
| 21 | `test_clinical_safety.py` | `test_screen_risk_phrases[Me mató de risa el chiste-None]` | Pasó |
| 22 | `test_clinical_safety.py` | `test_screen_risk_phrases[None-None]` | Pasó |
| 23 | `test_clinical_safety.py` | `test_highest_risk_keeps_the_most_severe` | Pasó |
| 24 | `test_clinical_safety.py` | `test_patient_cannot_set_own_risk` | Pasó |
| 25 | `test_clinical_safety.py` | `test_high_risk_gives_crisis_support_and_alerts_professional` | Pasó |
| 26 | `test_clinical_safety.py` | `test_auto_analysis_never_below_phrase_filter` | Pasó |
| 27 | `test_clinical_safety.py` | `test_diary_requires_informed_consent` | Pasó |
| 28 | `test_clinical_safety.py` | `test_outdated_consent_version_is_rejected` | Pasó |
| 29 | `test_clinical_safety.py` | `test_ai_analysis_requires_ai_consent_and_can_be_revoked` | Pasó |
| 30 | `test_clinical_safety.py` | `test_weekly_summary_skips_ai_without_consent` | Pasó |
| 31 | `test_clinical_safety.py` | `test_sharing_mode_limits_what_professional_sees[NEW_ONLY-1]` | Pasó |
| 32 | `test_clinical_safety.py` | `test_sharing_mode_limits_what_professional_sees[FULL_HISTORY-2]` | Pasó |
| 33 | `test_clinical_safety.py` | `test_from_date_requires_share_from` | Pasó |
| 34 | `test_clinical_safety.py` | `test_risk_alert_lifecycle_and_audit` | Pasó |
| 35 | `test_clinical_safety.py` | `test_ai_recommendation_waits_for_professional_review` | Pasó |
| 36 | `test_clinical_safety.py` | `test_no_ai_recommendation_for_high_risk_without_professional` | Pasó |
| 37 | `test_clinical_safety.py` | `test_clinical_text_is_encrypted_at_rest` | Pasó |
| 38 | `test_clinical_safety.py` | `test_export_and_erase_my_data` | Pasó |
| 39 | `test_clinical_safety.py` | `test_production_rejects_fake_provider` | Pasó |
| 40 | `test_emotions.py` | `test_normalize_emotion[TRISTEZA-Tristeza]` | Pasó |
| 41 | `test_emotions.py` | `test_normalize_emotion[estres-Estrés]` | Pasó |
| 42 | `test_emotions.py` | `test_normalize_emotion[  Ansiedad -Ansiedad]` | Pasó |
| 43 | `test_emotions.py` | `test_normalize_emotion[nostalgia-Nostalgia]` | Pasó |
| 44 | `test_emotions.py` | `test_normalize_emotion[-None]` | Pasó |
| 45 | `test_emotions.py` | `test_negative_emotions_match_any_spelling` | Pasó |
| 46 | `test_emotions.py` | `test_parser_stores_canonical_emotion` | Pasó |
| 47 | `test_emotions.py` | `test_analysis_prompt_defines_risk_levels_and_emotions` | Pasó |
| 48 | `test_emotions.py` | `test_catalog_matches_dei_ai` | Pasó |
| 49 | `test_emotions.py` | `test_every_emotion_has_a_valence_or_is_neutral` | Pasó |
| 50 | `test_emotions.py` | `test_aliases_shared_with_dei_ai[enojo-Ira]` | Pasó |
| 51 | `test_emotions.py` | `test_aliases_shared_with_dei_ai[Melancolía-Tristeza]` | Pasó |
| 52 | `test_emotions.py` | `test_aliases_shared_with_dei_ai[inquietud-Preocupación]` | Pasó |
| 53 | `test_emotions.py` | `test_aliases_shared_with_dei_ai[CANSANCIO-Agotamiento]` | Pasó |
| 54 | `test_ollama_providers.py` | `test_analysis_sends_json_request_to_configured_server` | Pasó |
| 55 | `test_ollama_providers.py` | `test_unreachable_ollama_raises_provider_exception` | Pasó |
| 56 | `test_ollama_providers.py` | `test_server_error_raises_provider_exception` | Pasó |
| 57 | `test_ollama_providers.py` | `test_summary_returns_plain_text` | Pasó |
| 58 | `test_ollama_providers.py` | `test_recommendation_requires_title_and_content` | Pasó |
| 59 | `test_ollama_providers.py` | `test_health_reports_model_availability` | Pasó |
| 60 | `test_password_reset.py` | `test_full_flow_changes_password` | Pasó |
| 61 | `test_password_reset.py` | `test_response_does_not_reveal_if_email_exists` | Pasó |
| 62 | `test_password_reset.py` | `test_inactive_user_gets_no_code` | Pasó |
| 63 | `test_password_reset.py` | `test_code_is_stored_hashed` | Pasó |
| 64 | `test_password_reset.py` | `test_code_is_single_use` | Pasó |
| 65 | `test_password_reset.py` | `test_expired_code_is_rejected` | Pasó |
| 66 | `test_password_reset.py` | `test_new_code_invalidates_previous` | Pasó |
| 67 | `test_password_reset.py` | `test_code_is_voided_after_max_failed_attempts` | Pasó |
| 68 | `test_password_reset.py` | `test_code_from_another_account_does_not_work` | Pasó |
| 69 | `test_password_reset.py` | `test_reset_closes_existing_sessions` | Pasó |
| 70 | `test_password_reset.py` | `test_weak_password_is_rejected` | Pasó |
| 71 | `test_password_reset.py` | `test_codes_per_account_are_limited` | Pasó |
| 72 | `test_password_reset.py` | `test_forgot_password_is_rate_limited_by_ip` | Pasó |
| 73 | `test_password_reset.py` | `test_reset_attempts_are_rate_limited_by_ip` | Pasó |
| 74 | `test_password_reset.py` | `test_malformed_code_is_rejected` | Pasó |
| 75 | `test_professional_portal.py` | `test_profile_me` | Pasó |
| 76 | `test_professional_portal.py` | `test_profile_me_404_without_profile` | Pasó |
| 77 | `test_professional_portal.py` | `test_directory_lists_only_verified` | Pasó |
| 78 | `test_professional_portal.py` | `test_link_request_shows_patient_name_and_can_be_rejected` | Pasó |
| 79 | `test_professional_portal.py` | `test_reject_requires_owner` | Pasó |
| 80 | `test_professional_portal.py` | `test_my_patients_and_entries_respect_sharing_and_audit` | Pasó |
| 81 | `test_professional_portal.py` | `test_entries_full_history` | Pasó |
| 82 | `test_professional_portal.py` | `test_entries_forbidden_without_relation_or_consent` | Pasó |
| 83 | `test_provider_chain.py` | `test_uses_first_provider_when_it_works` | Pasó |
| 84 | `test_provider_chain.py` | `test_falls_back_in_order` | Pasó |
| 85 | `test_provider_chain.py` | `test_raises_when_every_provider_fails` | Pasó |
| 86 | `test_provider_chain.py` | `test_default_chain_comes_from_settings` | Pasó |
| 87 | `test_whisper_provider.py` | `test_whisper_api_uploads_audio` | Pasó |
| 88 | `test_whisper_provider.py` | `test_whisper_api_unreachable` | Pasó |

### 7.3.2 Servicio de IA (`dei_ai`): 42 pruebas

| # | Archivo | Prueba | Resultado |
|---|---|---|---|
| 1 | `test_analysis_prompt.py` | `test_prompt_does_not_ask_to_diagnose_or_guess` | Pasó |
| 2 | `test_analysis_prompt.py` | `test_prompt_defines_every_risk_level` | Pasó |
| 3 | `test_analysis_prompt.py` | `test_prompt_lists_every_emotion` | Pasó |
| 4 | `test_analysis_prompt.py` | `test_risk_synonyms` | Pasó |
| 5 | `test_emotion_normalizer.py` | `test_normalize_tristeza` | Pasó |
| 6 | `test_emotion_normalizer.py` | `test_normalize_desanimo` | Pasó |
| 7 | `test_emotion_normalizer.py` | `test_normalize_furia` | Pasó |
| 8 | `test_emotion_normalizer.py` | `test_unknown_emotion_returns_confusion` | Pasó |
| 9 | `test_emotion_normalizer.py` | `test_catalog_matches_backend` | Pasó |
| 10 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Alegría]` | Pasó |
| 11 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Tristeza]` | Pasó |
| 12 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Ansiedad]` | Pasó |
| 13 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Miedo]` | Pasó |
| 14 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Ira]` | Pasó |
| 15 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Asco]` | Pasó |
| 16 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Sorpresa]` | Pasó |
| 17 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Calma]` | Pasó |
| 18 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Estrés]` | Pasó |
| 19 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Desánimo]` | Pasó |
| 20 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Culpa]` | Pasó |
| 21 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Vergüenza]` | Pasó |
| 22 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Soledad]` | Pasó |
| 23 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Frustración]` | Pasó |
| 24 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Confusión]` | Pasó |
| 25 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Esperanza]` | Pasó |
| 26 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Confianza]` | Pasó |
| 27 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Gratitud]` | Pasó |
| 28 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Agotamiento]` | Pasó |
| 29 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Amor]` | Pasó |
| 30 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Preocupación]` | Pasó |
| 31 | `test_emotion_normalizer.py` | `test_backend_names_normalize_to_same_emotion[Desesperanza]` | Pasó |
| 32 | `test_emotion_normalizer.py` | `test_desesperanza_is_not_desanimo` | Pasó |
| 33 | `test_emotion_normalizer.py` | `test_preocupacion[preocupación]` | Pasó |
| 34 | `test_emotion_normalizer.py` | `test_preocupacion[PREOCUPACION]` | Pasó |
| 35 | `test_emotion_normalizer.py` | `test_preocupacion[inquietud]` | Pasó |
| 36 | `test_emotion_normalizer.py` | `test_preocupacion[preocupado]` | Pasó |
| 37 | `test_emotion_normalizer.py` | `test_accents_and_case_are_ignored` | Pasó |
| 38 | `test_emotion_normalizer.py` | `test_empty_emotion_returns_confusion` | Pasó |
| 39 | `test_intensity_normalizer.py` | `test_low` | Pasó |
| 40 | `test_intensity_normalizer.py` | `test_media` | Pasó |
| 41 | `test_intensity_normalizer.py` | `test_alta` | Pasó |
| 42 | `test_intensity_normalizer.py` | `test_unknown_returns_medium` | Pasó |

## 7.4 Glosario

| Término | Definición |
|---|---|
| Análisis emocional | Resultado de la IA sobre una entrada: emoción principal, intensidad, nivel de riesgo y detalle (sentimientos, pensamientos, patrones, posibles causas, resumen). |
| Cadena de proveedores | Orden en que el sistema prueba los proveedores de IA (por ejemplo, Ollama y luego Gemini). |
| Consentimiento informado | Aceptación obligatoria de qué es DEI, sus límites y el manejo de la información. |
| Consentimiento por psicólogo | Permiso revocable que el paciente da a un psicólogo concreto para ver su información. |
| Entrada | Registro del diario, de texto o de audio. |
| Filtro de frases de riesgo | Reglas fijas (expresiones regulares) que detectan ideación suicida, autolesión o planes, sin depender de la IA. |
| Fernet | Esquema de cifrado simétrico usado para los campos clínicos. |
| JWT | Token firmado que identifica al usuario en cada petición. |
| Línea de crisis | Teléfono de ayuda emocional o de emergencia de un país o ciudad. |
| Modo de compartir | Qué entradas ve el psicólogo: todo el historial, desde una fecha o solo las nuevas. |
| Ollama | Servidor que ejecuta modelos de lenguaje en un equipo local. |
| PUDS | Proceso Unificado de Desarrollo de Software: iterativo, incremental, dirigido por casos de uso y centrado en la arquitectura. |
| Whisper | Modelo de reconocimiento de voz que convierte audio en texto. |
| XMI | Formato estándar para intercambiar modelos UML entre herramientas como Enterprise Architect. |
