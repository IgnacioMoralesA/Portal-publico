# Aprendizaje de la Fábrica

## Reglas permanentes

1. No reinyectar documentos completos en cada ciclo.
2. Usar `source-manifest.json`, `context-pack.json` y `evidence-register.json` como memoria objetiva.
3. Priorizar salida en JSON estricto y markdown breve.
4. Mantener trazabilidad entre caso de uso, funcionalidad, evidencia y artefacto generado.
5. Antes de ejecutar un agente, validar presupuesto de tokens.
6. Cuando un agente necesite más contexto, pedir IDs de evidencia específicos, no documentos completos.

## Decisiones de diseño

- El stack tecnológico se mantiene fuera del núcleo de la fábrica.
- La fábrica modela el trabajo, no reemplaza la aprobación humana.
- Los agentes se ejecutan en ruta fija para reproducibilidad.
