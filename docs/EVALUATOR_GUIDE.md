# Guia para evaluadores

## Estructura del repositorio

- `README.md`: entrada principal.
- `app/`: prototipo local.
- `app/frontend/`: HTML, CSS y JavaScript.
- `app/mocks/`: datos ficticios.
- `docs/`: evidencia, QA, trazabilidad, riesgos y cierre.
- `tests/`: pruebas estaticas.
- `factory/` y `project/`: fabrica ARNES SDD y runs.

## Como levantar el prototipo

Desde `app/`:

```powershell
python -m http.server 8000
```

Abrir:

```text
http://127.0.0.1:8000/frontend/
```

## Credenciales demo

- Usuario: `demo.claveunica`
- Clave: `DemoLocal2026`
- OTP / factor demo: `123456`

## Recorrido funcional recomendado

1. Revisar portal publico, ayuda y novedades.
2. Iniciar sesion con credenciales incorrectas y luego correctas.
3. Probar OTP incorrecto y luego `123456`.
4. Revisar dashboard.
5. Editar datos personales ficticios con factor demo.
6. Revisar sesiones y cerrar una remota simulada.
7. Ejecutar DDU: cancelar, volver y completar configuracion demo.
8. Revisar notificaciones: bloqueo por DDU pendiente, listado, detalle y lectura.
9. Revisar autorizaciones: aprobar/rechazar/revocar con factor demo.
10. Cerrar sesion.

## Como revisar evidencias

- Estado y alcance: `docs/FINAL_PROTOTYPE_REPORT.md`.
- Evidencia de flujos: `docs/PROTOTYPE_EVIDENCE.md`.
- Checklist: `docs/FINAL_CHECKLIST.md`.
- QA/accesibilidad: `docs/QA_ACCESSIBILITY_REPORT.md`.
- Trazabilidad: `docs/FINAL_TRACEABILITY_MATRIX.md`.
- Riesgos: `docs/FINAL_RISK_REGISTER.md`.

## Como ejecutar pruebas

Desde la raiz:

```powershell
python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp
node --check app/frontend/app.js
```

## Que no debe interpretarse como produccion

- Login y OTP no son reales.
- DDU no se configura realmente.
- Notificaciones no provienen de CasillaUnica real.
- Autorizaciones no tienen validez legal.
- `sessionStorage` no es persistencia productiva.
- No hay backend, API, integracion externa ni seguridad productiva.
- No hay cumplimiento WCAG/legal/regulatorio completo validado.

## Criterios de revision sugeridos

- Coherencia entre run base, backlog y prototipo.
- Completitud del recorrido funcional local.
- Uso exclusivo de datos ficticios.
- Claridad de advertencias sandbox/no produccion.
- Pruebas estaticas pasando.
- Riesgos residuales visibles.
- Trazabilidad entre fuentes, modulos, archivos, pruebas y evidencia.
