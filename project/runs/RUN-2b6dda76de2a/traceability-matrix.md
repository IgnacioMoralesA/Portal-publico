# Matriz de trazabilidad

| Bloque | Cobertura esperada | Evidencia base | Agentes responsables |
|---|---|---|---|
| Portal público | Accesos activar, autenticar, recuperar, ayuda y novedades | S06:HU01, S08:CU_001 | spec, ui, qa |
| Datos personales | Cambio de teléfono/correo con factor de seguridad | S06:HU02, S08:CU_002 | spec, security, tests |
| 2FA | Activación opcional y exigencia al login si está activo | S06:HU03, S08:CU_003 | spec, security, tests |
| Sesiones | Política de multisesión y mitigación de secuestro | S06:HU04, S08:CU_004 | security, qa |
| DDU | Derivación, cancelación, retorno y alerta pendiente | S06:HU05-HU12, S07, S08:CU_005-CU_012 | architect, api, tests |
| Notificaciones | Listado y detalle desde CasillaÚnica | S06:HU09-HU11, S07 | ui, api, tests |
| Autorizaciones | Historial, pendientes, aprobación, rechazo y revocación | S06:HU13-HU16, S08:CU_013-CU_016 | architect, security, tests |
| Calidad | Pruebas frontend, prototipo, accesibilidad y evidencia | S05 | tests, qa |
| Garantía | Cobertura mínima de calidad, funcionamiento, compatibilidad, rendimiento, seguridad y estabilidad | S05 | doc, qa |
