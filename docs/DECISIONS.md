# Decisiones finales

## D001 - Cierre de prototipo local

Se cierra la etapa como prototipo funcional local/sandbox, no como producto.

## D002 - Frontend estatico

Se mantiene frontend estatico en `app/frontend/` para reducir dependencias y facilitar demo local.

## D003 - Uso de mocks

Los datos del prototipo se obtienen desde `app/mocks/*.json` y son ficticios.

## D004 - sessionStorage solo demo

`sessionStorage` se usa solo para estado local de demo. No representa persistencia real.

## D005 - Sin backend real

No se implementa backend real en esta etapa.

## D006 - Sin servicios reales

No se conecta ClaveUnica, CasillaUnica, Plataforma de Notificaciones ni servicios externos reales.

## D007 - No produccion

La entrega no debe presentarse como readiness productivo ni como cumplimiento legal, regulatorio o WCAG completo.

## D008 - Pruebas estaticas como evidencia inicial

Las pruebas estaticas y `node --check` son evidencia inicial suficiente para este cierre, dejando E2E y auditorias como pendientes.

## D009 - Riesgos aceptados para entrega academica/prototipo

Se aceptan riesgos residuales de accesibilidad formal, E2E, backend, integracion, seguridad productiva y validacion legal solo para fines de entrega academica/prototipo.
