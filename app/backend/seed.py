from sqlalchemy.orm import Session

from app.backend.config import settings
from app.backend.database import Base, engine
from app.backend.models import (
    AuditEvent,
    AuthFactor,
    AuthorizationRequest,
    DduProfile,
    Notification,
    User,
    UserSession,
)


DEMO_USER_ID = "USR-001"


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_demo_data(db)


def seed_demo_data(db: Session) -> None:
    if db.get(User, DEMO_USER_ID):
        return

    user = User(
        id=DEMO_USER_ID,
        username=settings.demo_username,
        nombre="Persona de prueba",
        run_enmascarado="12.345.***-*",
        correo="persona@example.cl",
        telefono="+56 9 1234 5678",
        clave_unica_estado="activa demo",
        segundo_factor_activo=True,
    )
    db.add(user)
    db.add_all(
        [
            AuthFactor(user_id=DEMO_USER_ID, factor_type="otp_demo", demo_code=settings.demo_otp, enabled=True),
            AuthFactor(user_id=DEMO_USER_ID, factor_type="personal_code_demo", demo_code=settings.demo_otp, enabled=True),
            DduProfile(
                user_id=DEMO_USER_ID,
                estado="pendiente",
                domicilio="Domicilio Digital Unico pendiente de configuracion demo",
                alerta_pendiente=True,
            ),
        ]
    )
    db.add_all(
        [
            UserSession(
                id="SES-DEMO-001",
                user_id=DEMO_USER_ID,
                actual=True,
                dispositivo="Notebook institucional demo",
                navegador="Navegador local",
                ubicacion="Ubicacion generica demo",
                ultimo_acceso="2026-07-05 10:15",
                estado="activa",
                riesgo="",
            ),
            UserSession(
                id="SES-DEMO-002",
                user_id=DEMO_USER_ID,
                actual=False,
                dispositivo="Telefono demo",
                navegador="Navegador movil simulado",
                ubicacion="Zona generica norte",
                ultimo_acceso="2026-07-04 18:40",
                estado="activa",
                riesgo="revision recomendada",
            ),
            UserSession(
                id="SES-DEMO-003",
                user_id=DEMO_USER_ID,
                actual=False,
                dispositivo="Equipo compartido demo",
                navegador="Navegador de escritorio simulado",
                ubicacion="Zona generica centro",
                ultimo_acceso="2026-07-03 09:25",
                estado="activa",
                riesgo="riesgo medio demo",
            ),
        ]
    )
    db.add_all(
        [
            Notification(
                id="NOT-001",
                user_id=DEMO_USER_ID,
                institucion="Servicio Demo de Beneficios",
                titulo="Aviso de beneficio local disponible",
                estado="pendiente",
                fecha_recepcion="2026-07-05 09:30",
                prioridad="media",
                categoria="informativa",
                contenido="Contenido ficticio seguro para validar el detalle local de una notificacion demo.",
            ),
            Notification(
                id="NOT-002",
                user_id=DEMO_USER_ID,
                institucion="Unidad Demo de Tramites",
                titulo="Recordatorio de tramite simulado",
                estado="pendiente",
                fecha_recepcion="2026-07-04 16:20",
                prioridad="alta",
                categoria="recordatorio",
                contenido="Mensaje local de prueba sin documentos reales, datos personales reales ni enlaces productivos.",
            ),
        ]
    )
    db.add_all(
        [
            AuthorizationRequest(
                id="AUT-DEMO-001",
                user_id=DEMO_USER_ID,
                institucion="Instituto Demo de Estudios Sociales",
                finalidad="Validar postulacion ficticia a un beneficio local de prueba.",
                tipo_dato="Indicador sensible generico",
                fecha_solicitud="2026-07-02 09:15",
                estado="pendiente",
                historial="2026-07-02 09:15 solicitud demo recibida",
            ),
            AuthorizationRequest(
                id="AUT-DEMO-002",
                user_id=DEMO_USER_ID,
                institucion="Agencia Ficticia de Orientacion Ciudadana",
                finalidad="Preparar recomendacion simulada para un tramite ciudadano demo.",
                tipo_dato="Categoria sensible generica",
                fecha_solicitud="2026-07-03 11:40",
                estado="pendiente",
                historial="2026-07-03 11:40 solicitud demo recibida",
            ),
            AuthorizationRequest(
                id="AUT-DEMO-003",
                user_id=DEMO_USER_ID,
                institucion="Centro Demo de Apoyo Local",
                finalidad="Revisar elegibilidad ficticia de acompanamiento no productivo.",
                tipo_dato="Antecedente sensible representado de forma generica",
                fecha_solicitud="2026-06-28 15:05",
                estado="aprobada",
                fecha_decision="2026-06-29 10:00",
                historial="2026-06-28 15:05 solicitud demo recibida\n2026-06-29 10:00 aprobacion demo registrada",
            ),
            AuthorizationRequest(
                id="AUT-DEMO-004",
                user_id=DEMO_USER_ID,
                institucion="Unidad Simulada de Servicios Comunitarios",
                finalidad="Contrastar requisito ficticio para una atencion local de prueba.",
                tipo_dato="Dato sensible generico no revelado",
                fecha_solicitud="2026-06-25 13:30",
                estado="rechazada",
                fecha_decision="2026-06-25 18:20",
                historial="2026-06-25 13:30 solicitud demo recibida\n2026-06-25 18:20 rechazo demo registrado",
            ),
            AuthorizationRequest(
                id="AUT-DEMO-005",
                user_id=DEMO_USER_ID,
                institucion="Programa Ficticio de Asistencia Digital",
                finalidad="Mantener referencia simulada para una revision historica local.",
                tipo_dato="Grupo sensible generico",
                fecha_solicitud="2026-06-20 08:50",
                estado="revocada",
                fecha_decision="2026-06-30 16:10",
                historial="2026-06-20 08:50 solicitud demo recibida\n2026-06-21 09:25 aprobacion demo registrada\n2026-06-30 16:10 revocacion demo registrada",
            ),
            AuditEvent(user_id=DEMO_USER_ID, event_type="seed", severity="info", message="Seed local con datos ficticios creado."),
        ]
    )
    db.commit()
