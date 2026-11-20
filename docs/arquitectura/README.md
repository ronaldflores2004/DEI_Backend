# Documentación de DEI

| Documento | Contenido |
|---|---|
| [arquitectura-general.md](arquitectura-general.md) | Visión del sistema, despliegue, flujos clave, integración con la IA local, seguridad y cómo importar los diagramas en Enterprise Architect. |
| [backend.md](backend.md) | `dei_backend`: módulos, API, modelo de datos, IA, seguridad, configuración. |
| [app.md](app.md) | `dei_app` (Flutter): capas, features, sesión y navegación, comunicación con la API. |
| [DEI-Documentacion-PUDS.md](DEI-Documentacion-PUDS.md) | Documento completo del proyecto según el Proceso Unificado (inicio, requerimientos, casos de uso, análisis, diseño, implementación, pruebas y anexos). Versión Word en `docx/DEI-Documentacion-PUDS.docx`. |
| [ia.md](ia.md) | `dei_ai`: API, pipeline de análisis, configuración y plan de integración con el backend. |

Diagramas en [`diagramas/`](diagramas/):

- `plantuml/`: fuente editable de los 29 diagramas.
- `png/` y `svg/`: imágenes.
- `capturas/`: pantallas de la app.
- `enterprise-architect/dei-modelo.xmi`: modelo UML 2.1 para importar en
  Enterprise Architect (casos de uso, componentes, despliegue y las 19 entidades).

`tools/gen_model.py` regenera el diagrama de datos y el XMI desde los modelos
SQLAlchemy del backend. `tools/to_docx.py` y `tools/to_docx_puds.py` generan los Word desde los Markdown.
