# Guion seguro de demo

## Advertencias antes de iniciar

- Demo con datos ficticios.
- Sin ClaveUnica real.
- Sin CasillaUnica real.
- Sin backend real.
- Sin servicios externos reales.
- No ingresar datos personales reales.
- No usar en produccion.

## Preparar entorno

1. Desde la raiz del repositorio, entrar a `app/`.
2. Ejecutar:

```powershell
python -m http.server 8000
```

3. Abrir:

```text
http://127.0.0.1:8000/frontend/
```

## Portal publico

1. Revisar inicio del Portal Ciudadano.
2. Verificar accesos a Ayuda y Novedades.
3. Probar botones de activar, recuperar e iniciar sesion como flujo visual/local.

## Login y 2FA

1. Abrir `Iniciar sesion`.
2. Probar usuario o clave incorrecta y verificar mensaje de error.
3. Usar usuario `demo.claveunica` y clave `DemoLocal2026`.
4. Probar OTP incorrecto y verificar mensaje de error.
5. Usar OTP `123456`.
6. Confirmar acceso al dashboard privado.

## Dashboard

1. Revisar resumen de persona mock.
2. Revisar estado DDU, 2FA, notificaciones y autorizaciones.
3. Usar accesos privados a cada modulo.

## Datos personales

1. Entrar a `Datos personales`.
2. Cambiar correo o telefono con valores ficticios.
3. Probar factor incorrecto.
4. Usar factor demo `123456`.
5. Confirmar mensaje de exito local.

## Sesiones

1. Entrar a `Sesiones`.
2. Revisar sesion actual y sesiones remotas mock.
3. Cerrar una sesion remota.
4. Confirmar estado `cerrada demo`.

## DDU

1. Entrar a `DDU`.
2. Verificar alerta pendiente/no configurado.
3. Iniciar configuracion y cancelar desde el modal.
4. Iniciar nuevamente y continuar a pasarela simulada.
5. Cancelar y confirmar que el estado sigue pendiente.
6. Repetir y completar configuracion demo.
7. Confirmar retorno y estado configurado.

## Notificaciones

1. Con DDU pendiente, entrar a `Notificaciones` y verificar bloqueo.
2. Configurar DDU demo.
3. Volver a `Notificaciones`.
4. Abrir detalle de una notificacion.
5. Confirmar aviso de derivacion simulada/local.
6. Marcar como leida.
7. Verificar actualizacion local de contador/estado.

## Autorizaciones

1. Entrar a `Autorizaciones`.
2. Revisar resumen por pendientes, aprobadas/vigentes, rechazadas y revocadas.
3. Abrir autorizacion pendiente.
4. Probar aprobar/rechazar con factor incorrecto.
5. Usar factor demo `123456` para aprobar o rechazar.
6. Abrir autorizacion aprobada/vigente.
7. Revocar con factor demo `123456`.
8. Verificar que rechazadas/revocadas quedan en solo lectura.

## Cierre de sesion

1. Usar `Cerrar sesion`.
2. Confirmar retorno al portal publico.

## Registro de evidencia

Solo registrar evidencia manual si el navegador local carga correctamente. Si Codex bloquea o expira localhost, anotar la limitacion del entorno y no inventar evidencia visual.
