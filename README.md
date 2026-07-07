# Fábrica ClaveÚnica ARNES SDD

Fábrica local y determinística para organizar el desarrollo del Portal Ciudadano de ClaveÚnica mediante un ciclo SDD controlado.

## Qué incluye

- Arnés `factory/` con orquestador, registro de agentes, política, validadores y ledger de tokens.
- Proyecto base `project/` con carpeta de entradas, memoria, runs, cache e índice.
- Modo de economía de tokens activado por defecto.
- Generación de artefactos trazables: `work_order.json`, `context-pack.json`, `evidence-register.json`, `traceability-matrix.md`, `validation-report.json` y `final-report.json`.

## Uso rápido

```bash
python -m factory.cli init --project project
python -m factory.cli run --project project --objective "Construir el Portal Ciudadano de ClaveÚnica según requerimientos funcionales y anexos" --economy
```

## Pruebas

```bash
python -m pytest tests
```

## Política de economía de tokens

La fábrica no pasa documentos completos a cada agente. Primero crea un inventario, luego usa `context-pack.json` con fragmentos relevantes, límite de tokens y referencias por `source_id`. Cada agente debe responder con salida acotada, evidencia y delta de archivos, evitando repetir contexto ya registrado.
