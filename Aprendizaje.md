# Aprendizaje de la Fabrica

## Reglas permanentes

1. No reinyectar documentos completos en cada ciclo.
2. Usar `source-manifest.json`, `context-pack.json` y `evidence-register.json` como memoria objetiva.
3. Priorizar salida en JSON estricto y markdown breve cuando se ejecutan agentes de fabrica.
4. Mantener trazabilidad entre caso de uso, funcionalidad, evidencia y artefacto generado.
5. Antes de ejecutar un agente, validar presupuesto de tokens.
6. Cuando un agente necesite mas contexto, pedir IDs de evidencia especificos, no documentos completos.
7. Priorizar siempre economizar tokens: leer solo el contexto necesario, resumir resultados y evitar reinyecciones extensas.
8. Si se levanta el proyecto, servidor o proceso local para verificar algo, bajarlo al terminar para no dejar consumo activo.

## Decisiones de diseno

- El stack tecnologico se mantiene fuera del nucleo de la fabrica.
- La fabrica modela el trabajo, no reemplaza la aprobacion humana.
- Los agentes se ejecutan en ruta fija para reproducibilidad.

## Aprendizaje del cierre documental

- El prototipo final debe presentarse como demo local/sandbox, no como sistema productivo.
- La evidencia final debe separar claramente pruebas estaticas, validacion manual y pendientes.
- Los riesgos residuales deben quedar visibles: WCAG formal, E2E, backend, persistencia, hardening, integraciones reales y validacion legal/regulatoria.
- `sessionStorage` y mocks son decisiones validas para demo, pero no deben confundirse con persistencia ni integracion real.
