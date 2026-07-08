from sqlalchemy.orm import Session

from app.backend.config import settings
from app.backend.database import Base, engine
from app.backend.models import (
    AccessibilityCheck,
    AuditEvent,
    AuthFactor,
    AuthorizationDecision,
    AuthorizationHistory,
    AuthorizationRequest,
    BusinessRule,
    DeploymentTarget,
    DeviceRiskAssessment,
    DduActivationEvent,
    DduCancellationEvent,
    DduProfile,
    HelpArticle,
    HelpCategory,
    Institution,
    InstitutionIntegration,
    IntegrationStatusEvent,
    Notification,
    NotificationCategory,
    NotificationDeliveryAttempt,
    NotificationPriority,
    NotificationReadEvent,
    NotificationRecipient,
    OtpChallenge,
    PasswordRecoveryRequest,
    ProductChecklistItem,
    PrototypeScreen,
    PublicNews,
    PublicServiceCard,
    SecurityQuestion,
    SensitiveDataCategory,
    SessionEvent,
    TestEvidenceRecord,
    TrustedDevice,
    User,
    UserContactMethod,
    UserProfile,
    UserSession,
    ValidationRule,
)


DEMO_USER_ID = "USR-001"


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_demo_data(db)


def seed_demo_data(db: Session) -> None:
    if not db.get(User, DEMO_USER_ID):
        db.add(
            User(
                id=DEMO_USER_ID,
                username=settings.demo_username,
                nombre="Persona de prueba",
                run_enmascarado="12.345.***-*",
                correo="persona@example.cl",
                telefono="+56 9 1234 5678",
                clave_unica_estado="activa demo",
                segundo_factor_activo=True,
            )
        )
        db.flush()
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
        db.add_all(_base_authorizations())

    _seed_schema_expansion_data(db)
    db.commit()


def _base_authorizations() -> list[AuthorizationRequest | AuditEvent]:
    return [
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


def _add_if_missing(db: Session, model, primary_key, row) -> None:
    if not db.get(model, primary_key):
        db.add(row)


def _seed_schema_expansion_data(db: Session) -> None:
    rows = [
        (UserProfile, 1, UserProfile(id=1, user_id=DEMO_USER_ID, display_name="Perfil demo ciudadano", profile_status="activo", identity_level="verificado demo", completion_percent=80)),
        (UserContactMethod, 1, UserContactMethod(id=1, user_id=DEMO_USER_ID, contact_type="email", masked_value="p***@example.cl", verified=True, preferred=True)),
        (SecurityQuestion, 1, SecurityQuestion(id=1, user_id=DEMO_USER_ID, question_text="Pregunta generica de recuperacion demo", answer_hint="respuesta demo", question_status="activa", failed_attempts=0)),
        (PasswordRecoveryRequest, "REC-DEMO-001", PasswordRecoveryRequest(id="REC-DEMO-001", user_id=DEMO_USER_ID, request_status="solicitada", delivery_channel="email", attempt_count=0, requested_at="2026-07-05 08:00")),
        (OtpChallenge, "OTP-DEMO-001", OtpChallenge(id="OTP-DEMO-001", user_id=DEMO_USER_ID, challenge_status="aprobado", channel="app_demo", attempt_count=1, created_at="2026-07-05 10:16")),
        (SessionEvent, 1, SessionEvent(id=1, session_id="SES-DEMO-001", event_type="inicio", risk_level="bajo", requires_review=False, occurred_at="2026-07-05 10:15")),
        (TrustedDevice, "DEV-DEMO-001", TrustedDevice(id="DEV-DEMO-001", user_id=DEMO_USER_ID, device_label="Notebook demo", device_status="confiable", trust_score=75, remember_device=True)),
        (DeviceRiskAssessment, 1, DeviceRiskAssessment(id=1, device_id="DEV-DEMO-001", risk_level="bajo", signals_count=1, action="permitir", assessed_at="2026-07-05 10:14")),
        (DduActivationEvent, "DDU-ACT-001", DduActivationEvent(id="DDU-ACT-001", user_id=DEMO_USER_ID, activation_status="iniciada", origin_channel="portal", requires_confirmation=True, event_at="2026-07-05 11:00")),
        (DduCancellationEvent, "DDU-CAN-001", DduCancellationEvent(id="DDU-CAN-001", user_id=DEMO_USER_ID, cancellation_status="solicitada", reason_code="prueba_demo", restored_previous_state=False, event_at="2026-07-05 11:05")),
        (NotificationCategory, 1, NotificationCategory(id=1, category_code="informativa", label="Informativa demo", enabled=True, retention_days=365)),
        (NotificationPriority, 1, NotificationPriority(id=1, priority_code="media", label="Media", sort_order=2, requires_banner=False)),
        (NotificationRecipient, 1, NotificationRecipient(id=1, notification_id="NOT-001", user_id=DEMO_USER_ID, recipient_status="pendiente", recipient_type="titular", delivery_required=True)),
        (NotificationReadEvent, 1, NotificationReadEvent(id=1, notification_id="NOT-001", read_channel="portal", acknowledged=False, read_duration_seconds=0, read_at="2026-07-05 12:00")),
        (NotificationDeliveryAttempt, 1, NotificationDeliveryAttempt(id=1, notification_id="NOT-001", delivery_status="enviado demo", channel="portal", attempt_number=1, attempted_at="2026-07-05 09:30")),
        (AuthorizationDecision, 1, AuthorizationDecision(id=1, authorization_id="AUT-DEMO-003", decision="aprobar", factor_verified=True, decision_source="portal", decided_at="2026-06-29 10:00")),
        (AuthorizationHistory, 1, AuthorizationHistory(id=1, authorization_id="AUT-DEMO-001", history_event="creada", summary="Solicitud demo creada", visible_to_user=True, event_at="2026-07-02 09:15")),
        (SensitiveDataCategory, 1, SensitiveDataCategory(id=1, category_type="social_generica", label="Categoria social generica", requires_explicit_consent=True, retention_days=180)),
        (Institution, "INS-DEMO-001", Institution(id="INS-DEMO-001", display_name="Servicio Publico Demo", institution_type="servicio_publico_demo", active=True, support_label="Mesa demo")),
        (InstitutionIntegration, "INT-DEMO-001", InstitutionIntegration(id="INT-DEMO-001", institution_id="INS-DEMO-001", integration_type="api_mock", sync_enabled=False, timeout_seconds=30, endpoint_label="Integracion local mock")),
        (IntegrationStatusEvent, 1, IntegrationStatusEvent(id=1, integration_id="INT-DEMO-001", status="ok", severity="info", retry_count=0, event_at="2026-07-05 12:10")),
        (HelpCategory, 1, HelpCategory(id=1, slug="acceso-demo", label="Acceso demo", category_status="activa", sort_order=1, public_visible=True)),
        (HelpArticle, "HELP-DEMO-001", HelpArticle(id="HELP-DEMO-001", category_id=1, title="Como usar el acceso demo", article_status="publicado demo", audience="publico", view_count=0)),
        (PublicNews, "NEWS-DEMO-001", PublicNews(id="NEWS-DEMO-001", title="Novedad demo del portal local", news_status="publicada demo", importance="media", pinned=False, published_at="2026-07-05 08:30")),
        (PublicServiceCard, "CARD-DEMO-001", PublicServiceCard(id="CARD-DEMO-001", title="Iniciar sesion demo", card_status="activa", service_type="login", sort_order=1, action_label="Ingresar")),
        (AccessibilityCheck, "ACC-DEMO-001", AccessibilityCheck(id="ACC-DEMO-001", screen_id="SCR-DEMO-001", wcag_level="AA", result="pendiente", issue_count=0, checked_at="2026-07-05 13:00")),
        (PrototypeScreen, "SCR-DEMO-001", PrototypeScreen(id="SCR-DEMO-001", name="Dashboard demo", screen_area="privada", screen_status="implementada", requires_auth=True, route_hint="dashboard")),
        (BusinessRule, "RN-DEMO-001", BusinessRule(id="RN-DEMO-001", title="OTP demo requerido para acceso privado", rule_status="vigente", rule_domain="auth", priority="alta", source_ref="S08:CU_003")),
        (ValidationRule, "VAL-DEMO-001", ValidationRule(id="VAL-DEMO-001", target="otp_challenges", validation_type="check_sql", severity="error", automated=True, description="Limita intentos OTP demo entre cero y cinco.")),
        (ProductChecklistItem, "CHK-DEMO-001", ProductChecklistItem(id="CHK-DEMO-001", title="Completar minimo de tablas", item_status="cumplido", criterion_type="tecnico", evidence_required=True, owner_agent="agent.db_schema_expansion")),
        (TestEvidenceRecord, "EVD-DEMO-001", TestEvidenceRecord(id="EVD-DEMO-001", evidence_type="pytest", result="pending", duration_seconds=0, command="python -m pytest -q tests", recorded_at="2026-07-05 13:30")),
        (DeploymentTarget, "DEP-DEMO-001", DeploymentTarget(id="DEP-DEMO-001", environment="local", target_status="pendiente", external_network_enabled=False, deployment_note="Deploy EC2 pendiente; solo objetivo local mock.", owner_agent="agent.aws_ec2_deploy")),
    ]
    for model, primary_key, row in rows:
        _add_if_missing(db, model, primary_key, row)
