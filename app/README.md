# Prototipo web local

Prototipo estático del Portal Ciudadano de ClaveÚnica, basado en `project/runs/RUN-22673eb11025`.

## Abrir localmente

Desde `app/`:

```powershell
python -m http.server 8000
```

Luego abrir:

```text
http://localhost:8000/frontend/
```

El prototipo carga mocks locales desde `app/mocks/`. Por restricciones normales del navegador, debe abrirse mediante un servidor HTTP local para que `fetch()` pueda leer esos archivos.

## Acceso demo

- Usuario demo: `demo.claveunica`
- Clave demo: `DemoLocal2026`
- Codigo OTP demo: `123456`

## Datos personales demo

Para probar el modulo privado:

1. Iniciar sesion con las credenciales demo.
2. Completar el OTP demo `123456`.
3. Entrar a `Datos personales` desde el dashboard.
4. Cambiar correo y/o telefono.
5. Probar un factor incorrecto y verificar que no se guarden cambios.
6. Usar el factor de seguridad demo `123456` y verificar el mensaje de exito.
7. Volver al dashboard y cerrar sesion.

El cambio de correo y telefono es local y simulado en la vista del prototipo. No se guarda en backend, no usa servicios reales de ClaveUnica y no debe utilizar datos personales reales.

## Sesiones demo

Para probar el modulo privado:

1. Iniciar sesion con las credenciales demo.
2. Completar el OTP demo `123456`.
3. Entrar a `Sesiones` desde el dashboard.
4. Revisar la sesion actual y las sesiones remotas mock.
5. Cerrar una sesion remota y verificar el mensaje de exito.
6. Confirmar que la sesion remota cambia a estado `cerrada demo`.
7. Volver al dashboard y cerrar sesion con el boton general.

Las sesiones son simuladas y se cargan desde `app/mocks/sessions.json`. La gestion es local del prototipo: no persiste sesiones reales, no usa ubicaciones reales, no usa IPs reales, no usa servicios reales de ClaveUnica y no hay proteccion real productiva contra secuestro de sesion. La pantalla solo representa una simulacion de politica de multisesion para validacion visual/local.

## DDU demo

Estado inicial demo: Domicilio Digital Unico pendiente/no configurado, cargado desde `app/mocks/ddu.json`.

Para probar el modulo privado:

1. Iniciar sesion con las credenciales demo.
2. Completar el OTP demo `123456`.
3. Entrar a `DDU` desde el dashboard.
4. Verificar la alerta de configuracion pendiente.
5. Presionar `Iniciar configuracion DDU` y cancelar desde el modal; el estado debe seguir pendiente.
6. Iniciar configuracion nuevamente y continuar a la pasarela simulada.
7. Cancelar dentro de la pasarela y confirmar la cancelacion; se retorna a DDU y el estado sigue pendiente.
8. Iniciar configuracion nuevamente y completar la configuracion demo.
9. Verificar el mensaje de retorno al portal y que el dashboard muestra DDU configurado.
10. Abrir DDU configurado y revisar el acceso preparado hacia Notificaciones.

El flujo DDU es visual/mock y usa solo estado demo/local del navegador mediante `sessionStorage`. No usa CasillaUnica real, no configura DDU real, no conecta Plataforma de Notificaciones real, no usa backend productivo y no debe probarse con domicilio, correo o telefono reales. No es una funcionalidad lista para produccion.

## Notificaciones demo

Para probar el modulo privado:

1. Iniciar sesion con las credenciales demo.
2. Completar el OTP demo `123456`.
3. Entrar a `Notificaciones` desde el dashboard con DDU pendiente y verificar la alerta que exige configurar DDU.
4. Usar el acceso `Ir a DDU`, completar la configuracion DDU demo y volver al dashboard.
5. Entrar nuevamente a `Notificaciones`.
6. Ver el listado mock de notificaciones pendientes de lectura con fecha ficticia, institucion ficticia, titulo, estado, prioridad y categoria.
7. Abrir el detalle de una notificacion.
8. Verificar el aviso de derivacion simulada/local a CasillaUnica.
9. Marcar la notificacion como leida y volver al listado.
10. Verificar que el contador/estado visual de pendientes se actualiza en el listado y dashboard.

Las notificaciones se cargan desde `app/mocks/notifications.json` y el marcado como leida usa solo `sessionStorage` del navegador. No usa CasillaUnica real, no usa Plataforma de Notificaciones real, no usa notificaciones reales, no abre URLs productivas, no guarda cambios en backend y no es una funcionalidad lista para produccion.

## Autorizaciones demo

Para probar el modulo privado:

1. Iniciar sesion con las credenciales demo.
2. Completar el OTP demo `123456`.
3. Entrar a `Autorizaciones` desde el dashboard.
4. Revisar el resumen por estados: pendientes, aprobadas/vigentes, rechazadas y revocadas.
5. Abrir el detalle de una autorizacion pendiente.
6. Intentar aprobar o rechazar con un factor incorrecto y verificar el mensaje de error.
7. Usar el factor demo `123456` para aprobar o rechazar y verificar el cambio de estado e historial local.
8. Abrir una autorizacion aprobada/vigente, usar el factor demo `123456` y revocarla.
9. Verificar que las autorizaciones rechazadas o revocadas quedan en solo lectura.
10. Volver al dashboard y cerrar sesion.

Estados disponibles: `pendiente`, `aprobada`, `rechazada` y `revocada`. Las acciones de aprobar, rechazar y revocar exigen factor demo obligatorio `123456`.

Las autorizaciones se cargan desde `app/mocks/authorizations.json` y los cambios de estado usan solo `sessionStorage` del navegador. No usa autorizaciones reales, no muestra datos sensibles reales, no tiene validez legal, no conecta servicios reales del Estado, no guarda cambios en backend y no es una funcionalidad lista para produccion.

## Alcance y seguridad

- La autenticación es simulada y sólo sirve para validar el flujo visual/local.
- No usa ClaveÚnica real.
- No usa backend real.
- No conecta servicios externos, Plataforma de Notificaciones ni CasillaÚnica real.
- No debe usarse ni presentarse como sistema listo para producción.
- El uso de `sessionStorage` corresponde sólo a estado demo/local del navegador.
