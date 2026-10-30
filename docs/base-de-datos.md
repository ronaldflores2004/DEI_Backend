# Base de datos y migraciones

El esquema se administra **solo con Alembic**. La app no usa
`Base.metadata.create_all`, porque ese método no modifica tablas existentes
ni lleva control de versiones.

## Instalación nueva (base vacía)

```bash
# DATABASE_URL apuntando a una base PostgreSQL vacía
alembic upgrade head
```

La primera migración (`0f2a6c1d9b3e_initial_schema`) crea todas las tablas,
y las siguientes agregan índices, columnas y restricciones.

## Base existente

- **Si tu base ya está en `dffe805a0f64`** (revísalo con `alembic current`):
  no tienes que hacer nada, porque sigue siendo la versión más reciente.
- **Si la base se creó con `create_all` y nunca se migró** (no existe la tabla
  `alembic_version`): márcala con la revisión inicial y aplica el resto:

  ```bash
  alembic stamp 0f2a6c1d9b3e
  alembic upgrade head
  ```

## Cambios en los modelos

```bash
alembic revision --autogenerate -m "describe el cambio"
# revisa el archivo generado antes de aplicarlo
alembic upgrade head
```
