from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("length(username) >= 5", name="ck_users_username_min"),
        CheckConstraint("clave_unica_estado IN ('activa demo', 'bloqueada demo')", name="ck_users_clave_estado"),
        CheckConstraint("segundo_factor_activo IN (0, 1)", name="ck_users_factor_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    run_enmascarado: Mapped[str] = mapped_column(String(32), nullable=False)
    correo: Mapped[str] = mapped_column(String(160), nullable=False)
    telefono: Mapped[str] = mapped_column(String(40), nullable=False)
    clave_unica_estado: Mapped[str] = mapped_column(String(32), nullable=False)
    segundo_factor_activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    factors: Mapped[list["AuthFactor"]] = relationship(back_populates="user")


class AuthFactor(Base):
    __tablename__ = "auth_factors"
    __table_args__ = (
        CheckConstraint("factor_type IN ('otp_demo', 'personal_code_demo')", name="ck_auth_factor_type"),
        CheckConstraint("enabled IN (0, 1)", name="ck_auth_factor_enabled_bool"),
        CheckConstraint("length(demo_code) = 6", name="ck_auth_factor_code_length"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    factor_type: Mapped[str] = mapped_column(String(32), nullable=False)
    demo_code: Mapped[str] = mapped_column(String(12), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped[User] = relationship(back_populates="factors")


class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    __table_args__ = (
        CheckConstraint("result IN ('success', 'failure')", name="ck_login_attempt_result"),
        CheckConstraint("channel IN ('local_mock')", name="ck_login_attempt_channel"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    result: Mapped[str] = mapped_column(String(16), nullable=False)
    channel: Mapped[str] = mapped_column(String(24), nullable=False, default="local_mock")
    detail: Mapped[str] = mapped_column(String(160), nullable=False)


class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = (
        CheckConstraint("actual IN (0, 1)", name="ck_user_sessions_actual_bool"),
        CheckConstraint("estado IN ('activa', 'cerrada demo')", name="ck_user_sessions_estado"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    actual: Mapped[bool] = mapped_column(Boolean, nullable=False)
    dispositivo: Mapped[str] = mapped_column(String(120), nullable=False)
    navegador: Mapped[str] = mapped_column(String(120), nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(120), nullable=False)
    ultimo_acceso: Mapped[str] = mapped_column(String(32), nullable=False)
    estado: Mapped[str] = mapped_column(String(24), nullable=False)
    riesgo: Mapped[str] = mapped_column(String(80), nullable=False, default="")


class DduProfile(Base):
    __tablename__ = "ddu_profiles"
    __table_args__ = (
        CheckConstraint("estado IN ('pendiente', 'configurado')", name="ck_ddu_estado"),
        CheckConstraint("alerta_pendiente IN (0, 1)", name="ck_ddu_alerta_bool"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    estado: Mapped[str] = mapped_column(String(24), nullable=False)
    domicilio: Mapped[str] = mapped_column(String(240), nullable=False)
    alerta_pendiente: Mapped[bool] = mapped_column(Boolean, nullable=False)
    fecha_configuracion: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    canal: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    casilla_demo: Mapped[str] = mapped_column(String(80), nullable=False, default="")


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        CheckConstraint("estado IN ('pendiente', 'leida demo')", name="ck_notifications_estado"),
        CheckConstraint("prioridad IN ('baja', 'media', 'alta')", name="ck_notifications_prioridad"),
        CheckConstraint("length(titulo) >= 5", name="ck_notifications_titulo_min"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    institucion: Mapped[str] = mapped_column(String(140), nullable=False)
    titulo: Mapped[str] = mapped_column(String(180), nullable=False)
    estado: Mapped[str] = mapped_column(String(24), nullable=False)
    fecha_recepcion: Mapped[str] = mapped_column(String(32), nullable=False)
    prioridad: Mapped[str] = mapped_column(String(16), nullable=False)
    categoria: Mapped[str] = mapped_column(String(40), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)


class AuthorizationRequest(Base):
    __tablename__ = "authorization_requests"
    __table_args__ = (
        CheckConstraint("estado IN ('pendiente', 'aprobada', 'rechazada', 'revocada')", name="ck_authorizations_estado"),
        CheckConstraint("length(finalidad) >= 10", name="ck_authorizations_finalidad_min"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    institucion: Mapped[str] = mapped_column(String(140), nullable=False)
    finalidad: Mapped[str] = mapped_column(String(260), nullable=False)
    tipo_dato: Mapped[str] = mapped_column(String(120), nullable=False)
    fecha_solicitud: Mapped[str] = mapped_column(String(32), nullable=False)
    estado: Mapped[str] = mapped_column(String(24), nullable=False)
    fecha_decision: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    historial: Mapped[str] = mapped_column(Text, nullable=False, default="")


class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = (
        CheckConstraint("event_type IN ('auth', 'read', 'seed')", name="ck_audit_event_type"),
        CheckConstraint("severity IN ('info', 'warning')", name="ck_audit_severity"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(32), nullable=False)
    event_type: Mapped[str] = mapped_column(String(24), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    message: Mapped[str] = mapped_column(String(240), nullable=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = (
        CheckConstraint("profile_status IN ('borrador', 'activo', 'suspendido demo')", name="ck_user_profiles_status"),
        CheckConstraint("identity_level IN ('basico', 'verificado demo', 'alto demo')", name="ck_user_profiles_identity_level"),
        CheckConstraint("completion_percent BETWEEN 0 AND 100", name="ck_user_profiles_completion_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    profile_status: Mapped[str] = mapped_column(String(32), nullable=False)
    identity_level: Mapped[str] = mapped_column(String(32), nullable=False)
    completion_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class UserContactMethod(Base):
    __tablename__ = "user_contact_methods"
    __table_args__ = (
        CheckConstraint("contact_type IN ('email', 'telefono', 'casilla_demo')", name="ck_user_contact_type"),
        CheckConstraint("verified IN (0, 1)", name="ck_user_contact_verified_bool"),
        CheckConstraint("preferred IN (0, 1)", name="ck_user_contact_preferred_bool"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    contact_type: Mapped[str] = mapped_column(String(24), nullable=False)
    masked_value: Mapped[str] = mapped_column(String(160), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    preferred: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class SecurityQuestion(Base):
    __tablename__ = "security_questions"
    __table_args__ = (
        CheckConstraint("question_status IN ('activa', 'inactiva demo')", name="ck_security_questions_status"),
        CheckConstraint("failed_attempts >= 0", name="ck_security_questions_failed_nonnegative"),
        CheckConstraint("length(question_text) >= 12", name="ck_security_questions_text_min"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(String(180), nullable=False)
    answer_hint: Mapped[str] = mapped_column(String(120), nullable=False)
    question_status: Mapped[str] = mapped_column(String(24), nullable=False)
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class PasswordRecoveryRequest(Base):
    __tablename__ = "password_recovery_requests"
    __table_args__ = (
        CheckConstraint("request_status IN ('solicitada', 'validada demo', 'expirada', 'cancelada')", name="ck_password_recovery_status"),
        CheckConstraint("delivery_channel IN ('email', 'sms', 'soporte_demo')", name="ck_password_recovery_channel"),
        CheckConstraint("attempt_count >= 0", name="ck_password_recovery_attempts_nonnegative"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    request_status: Mapped[str] = mapped_column(String(24), nullable=False)
    delivery_channel: Mapped[str] = mapped_column(String(24), nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    requested_at: Mapped[str] = mapped_column(String(32), nullable=False)


class OtpChallenge(Base):
    __tablename__ = "otp_challenges"
    __table_args__ = (
        CheckConstraint("challenge_status IN ('pendiente', 'aprobado', 'fallido', 'expirado')", name="ck_otp_challenges_status"),
        CheckConstraint("channel IN ('app_demo', 'sms_demo', 'email_demo')", name="ck_otp_challenges_channel"),
        CheckConstraint("attempt_count BETWEEN 0 AND 5", name="ck_otp_challenges_attempt_range"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    challenge_status: Mapped[str] = mapped_column(String(24), nullable=False)
    channel: Mapped[str] = mapped_column(String(24), nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)


class SessionEvent(Base):
    __tablename__ = "session_events"
    __table_args__ = (
        CheckConstraint("event_type IN ('inicio', 'renovacion', 'cierre', 'cierre_remoto_demo')", name="ck_session_events_type"),
        CheckConstraint("risk_level IN ('bajo', 'medio', 'alto')", name="ck_session_events_risk"),
        CheckConstraint("requires_review IN (0, 1)", name="ck_session_events_review_bool"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("user_sessions.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    requires_review: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    occurred_at: Mapped[str] = mapped_column(String(32), nullable=False)


class TrustedDevice(Base):
    __tablename__ = "trusted_devices"
    __table_args__ = (
        CheckConstraint("device_status IN ('confiable', 'revocado', 'pendiente')", name="ck_trusted_devices_status"),
        CheckConstraint("trust_score BETWEEN 0 AND 100", name="ck_trusted_devices_score_range"),
        CheckConstraint("remember_device IN (0, 1)", name="ck_trusted_devices_remember_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    device_label: Mapped[str] = mapped_column(String(120), nullable=False)
    device_status: Mapped[str] = mapped_column(String(24), nullable=False)
    trust_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    remember_device: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class DeviceRiskAssessment(Base):
    __tablename__ = "device_risk_assessments"
    __table_args__ = (
        CheckConstraint("risk_level IN ('bajo', 'medio', 'alto', 'critico demo')", name="ck_device_risk_level"),
        CheckConstraint("signals_count >= 0", name="ck_device_risk_signals_nonnegative"),
        CheckConstraint("action IN ('permitir', 'desafiar_otp', 'bloquear_demo')", name="ck_device_risk_action"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(ForeignKey("trusted_devices.id"), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(24), nullable=False)
    signals_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    action: Mapped[str] = mapped_column(String(24), nullable=False)
    assessed_at: Mapped[str] = mapped_column(String(32), nullable=False)


class DduActivationEvent(Base):
    __tablename__ = "ddu_activation_events"
    __table_args__ = (
        CheckConstraint("activation_status IN ('iniciada', 'completada demo', 'fallida demo')", name="ck_ddu_activation_status"),
        CheckConstraint("origin_channel IN ('portal', 'casilla_demo', 'soporte_demo')", name="ck_ddu_activation_channel"),
        CheckConstraint("requires_confirmation IN (0, 1)", name="ck_ddu_activation_confirmation_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    activation_status: Mapped[str] = mapped_column(String(24), nullable=False)
    origin_channel: Mapped[str] = mapped_column(String(24), nullable=False)
    requires_confirmation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    event_at: Mapped[str] = mapped_column(String(32), nullable=False)


class DduCancellationEvent(Base):
    __tablename__ = "ddu_cancellation_events"
    __table_args__ = (
        CheckConstraint("cancellation_status IN ('solicitada', 'confirmada demo', 'rechazada demo')", name="ck_ddu_cancellation_status"),
        CheckConstraint("reason_code IN ('usuario', 'error_datos', 'prueba_demo')", name="ck_ddu_cancellation_reason"),
        CheckConstraint("restored_previous_state IN (0, 1)", name="ck_ddu_cancellation_restored_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    cancellation_status: Mapped[str] = mapped_column(String(24), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(24), nullable=False)
    restored_previous_state: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    event_at: Mapped[str] = mapped_column(String(32), nullable=False)


class NotificationRecipient(Base):
    __tablename__ = "notification_recipients"
    __table_args__ = (
        CheckConstraint("recipient_status IN ('pendiente', 'entregado demo', 'omitido')", name="ck_notification_recipients_status"),
        CheckConstraint("recipient_type IN ('titular', 'delegado_demo')", name="ck_notification_recipients_type"),
        CheckConstraint("delivery_required IN (0, 1)", name="ck_notification_recipients_required_bool"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notification_id: Mapped[str] = mapped_column(ForeignKey("notifications.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    recipient_status: Mapped[str] = mapped_column(String(24), nullable=False)
    recipient_type: Mapped[str] = mapped_column(String(24), nullable=False)
    delivery_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class NotificationReadEvent(Base):
    __tablename__ = "notification_read_events"
    __table_args__ = (
        CheckConstraint("read_channel IN ('portal', 'casilla_demo')", name="ck_notification_read_channel"),
        CheckConstraint("acknowledged IN (0, 1)", name="ck_notification_read_ack_bool"),
        CheckConstraint("read_duration_seconds >= 0", name="ck_notification_read_duration_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notification_id: Mapped[str] = mapped_column(ForeignKey("notifications.id"), nullable=False)
    read_channel: Mapped[str] = mapped_column(String(24), nullable=False)
    acknowledged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    read_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    read_at: Mapped[str] = mapped_column(String(32), nullable=False)


class NotificationCategory(Base):
    __tablename__ = "notification_categories"
    __table_args__ = (
        CheckConstraint("category_code IN ('informativa', 'recordatorio', 'alerta', 'tramite')", name="ck_notification_categories_code"),
        CheckConstraint("enabled IN (0, 1)", name="ck_notification_categories_enabled_bool"),
        CheckConstraint("retention_days >= 0", name="ck_notification_categories_retention_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    retention_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class NotificationPriority(Base):
    __tablename__ = "notification_priorities"
    __table_args__ = (
        CheckConstraint("priority_code IN ('baja', 'media', 'alta', 'urgente_demo')", name="ck_notification_priorities_code"),
        CheckConstraint("sort_order >= 0", name="ck_notification_priorities_sort_nonnegative"),
        CheckConstraint("requires_banner IN (0, 1)", name="ck_notification_priorities_banner_bool"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    priority_code: Mapped[str] = mapped_column(String(24), nullable=False, unique=True)
    label: Mapped[str] = mapped_column(String(80), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    requires_banner: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class NotificationDeliveryAttempt(Base):
    __tablename__ = "notification_delivery_attempts"
    __table_args__ = (
        CheckConstraint("delivery_status IN ('pendiente', 'enviado demo', 'fallido demo', 'reintentando')", name="ck_notification_delivery_status"),
        CheckConstraint("channel IN ('portal', 'email_demo', 'casilla_demo')", name="ck_notification_delivery_channel"),
        CheckConstraint("attempt_number >= 1", name="ck_notification_delivery_attempt_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notification_id: Mapped[str] = mapped_column(ForeignKey("notifications.id"), nullable=False)
    delivery_status: Mapped[str] = mapped_column(String(24), nullable=False)
    channel: Mapped[str] = mapped_column(String(24), nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    attempted_at: Mapped[str] = mapped_column(String(32), nullable=False)


class AuthorizationDecision(Base):
    __tablename__ = "authorization_decisions"
    __table_args__ = (
        CheckConstraint("decision IN ('aprobar', 'rechazar', 'revocar')", name="ck_authorization_decisions_decision"),
        CheckConstraint("factor_verified IN (0, 1)", name="ck_authorization_decisions_factor_bool"),
        CheckConstraint("decision_source IN ('portal', 'api_mock', 'soporte_demo')", name="ck_authorization_decisions_source"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    authorization_id: Mapped[str] = mapped_column(ForeignKey("authorization_requests.id"), nullable=False)
    decision: Mapped[str] = mapped_column(String(24), nullable=False)
    factor_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    decision_source: Mapped[str] = mapped_column(String(24), nullable=False)
    decided_at: Mapped[str] = mapped_column(String(32), nullable=False)


class AuthorizationHistory(Base):
    __tablename__ = "authorization_history"
    __table_args__ = (
        CheckConstraint("history_event IN ('creada', 'actualizada', 'decidida', 'revocada')", name="ck_authorization_history_event"),
        CheckConstraint("visible_to_user IN (0, 1)", name="ck_authorization_history_visible_bool"),
        CheckConstraint("length(summary) >= 8", name="ck_authorization_history_summary_min"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    authorization_id: Mapped[str] = mapped_column(ForeignKey("authorization_requests.id"), nullable=False)
    history_event: Mapped[str] = mapped_column(String(24), nullable=False)
    summary: Mapped[str] = mapped_column(String(220), nullable=False)
    visible_to_user: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    event_at: Mapped[str] = mapped_column(String(32), nullable=False)


class SensitiveDataCategory(Base):
    __tablename__ = "sensitive_data_categories"
    __table_args__ = (
        CheckConstraint("category_type IN ('salud_generica', 'social_generica', 'biometrica_demo', 'otra_generica')", name="ck_sensitive_data_type"),
        CheckConstraint("requires_explicit_consent IN (0, 1)", name="ck_sensitive_data_consent_bool"),
        CheckConstraint("retention_days >= 0", name="ck_sensitive_data_retention_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_type: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    requires_explicit_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    retention_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class Institution(Base):
    __tablename__ = "institutions"
    __table_args__ = (
        CheckConstraint("institution_type IN ('servicio_publico_demo', 'municipio_demo', 'programa_demo')", name="ck_institutions_type"),
        CheckConstraint("active IN (0, 1)", name="ck_institutions_active_bool"),
        CheckConstraint("length(display_name) >= 5", name="ck_institutions_name_min"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    institution_type: Mapped[str] = mapped_column(String(40), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    support_label: Mapped[str] = mapped_column(String(120), nullable=False)


class InstitutionIntegration(Base):
    __tablename__ = "institution_integrations"
    __table_args__ = (
        CheckConstraint("integration_type IN ('api_mock', 'archivo_demo', 'manual_demo')", name="ck_institution_integrations_type"),
        CheckConstraint("sync_enabled IN (0, 1)", name="ck_institution_integrations_sync_bool"),
        CheckConstraint("timeout_seconds BETWEEN 1 AND 120", name="ck_institution_integrations_timeout_range"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    institution_id: Mapped[str] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    integration_type: Mapped[str] = mapped_column(String(24), nullable=False)
    sync_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    timeout_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    endpoint_label: Mapped[str] = mapped_column(String(120), nullable=False)


class IntegrationStatusEvent(Base):
    __tablename__ = "integration_status_events"
    __table_args__ = (
        CheckConstraint("status IN ('ok', 'degradado demo', 'fallido demo')", name="ck_integration_status_events_status"),
        CheckConstraint("severity IN ('info', 'warning', 'critical_demo')", name="ck_integration_status_events_severity"),
        CheckConstraint("retry_count >= 0", name="ck_integration_status_events_retry_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    integration_id: Mapped[str] = mapped_column(ForeignKey("institution_integrations.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False)
    severity: Mapped[str] = mapped_column(String(24), nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    event_at: Mapped[str] = mapped_column(String(32), nullable=False)


class HelpArticle(Base):
    __tablename__ = "help_articles"
    __table_args__ = (
        CheckConstraint("article_status IN ('borrador', 'publicado demo', 'archivado')", name="ck_help_articles_status"),
        CheckConstraint("audience IN ('publico', 'autenticado', 'operador_demo')", name="ck_help_articles_audience"),
        CheckConstraint("view_count >= 0", name="ck_help_articles_views_nonnegative"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("help_categories.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    article_status: Mapped[str] = mapped_column(String(24), nullable=False)
    audience: Mapped[str] = mapped_column(String(24), nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class HelpCategory(Base):
    __tablename__ = "help_categories"
    __table_args__ = (
        CheckConstraint("category_status IN ('activa', 'oculta demo')", name="ck_help_categories_status"),
        CheckConstraint("sort_order >= 0", name="ck_help_categories_sort_nonnegative"),
        CheckConstraint("public_visible IN (0, 1)", name="ck_help_categories_visible_bool"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    category_status: Mapped[str] = mapped_column(String(24), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    public_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class PublicNews(Base):
    __tablename__ = "public_news"
    __table_args__ = (
        CheckConstraint("news_status IN ('borrador', 'publicada demo', 'archivada')", name="ck_public_news_status"),
        CheckConstraint("importance IN ('baja', 'media', 'alta')", name="ck_public_news_importance"),
        CheckConstraint("pinned IN (0, 1)", name="ck_public_news_pinned_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    news_status: Mapped[str] = mapped_column(String(24), nullable=False)
    importance: Mapped[str] = mapped_column(String(16), nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    published_at: Mapped[str] = mapped_column(String(32), nullable=False)


class PublicServiceCard(Base):
    __tablename__ = "public_service_cards"
    __table_args__ = (
        CheckConstraint("card_status IN ('activa', 'oculta demo', 'archivada')", name="ck_public_service_cards_status"),
        CheckConstraint("service_type IN ('login', 'ddu', 'notificaciones', 'ayuda')", name="ck_public_service_cards_type"),
        CheckConstraint("sort_order >= 0", name="ck_public_service_cards_sort_nonnegative"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    card_status: Mapped[str] = mapped_column(String(24), nullable=False)
    service_type: Mapped[str] = mapped_column(String(24), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    action_label: Mapped[str] = mapped_column(String(80), nullable=False)


class AccessibilityCheck(Base):
    __tablename__ = "accessibility_checks"
    __table_args__ = (
        CheckConstraint("wcag_level IN ('A', 'AA', 'AAA', 'no_aplica')", name="ck_accessibility_checks_wcag"),
        CheckConstraint("result IN ('pasa', 'falla', 'pendiente')", name="ck_accessibility_checks_result"),
        CheckConstraint("issue_count >= 0", name="ck_accessibility_checks_issues_nonnegative"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    screen_id: Mapped[str] = mapped_column(String(32), nullable=False)
    wcag_level: Mapped[str] = mapped_column(String(16), nullable=False)
    result: Mapped[str] = mapped_column(String(16), nullable=False)
    issue_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    checked_at: Mapped[str] = mapped_column(String(32), nullable=False)


class PrototypeScreen(Base):
    __tablename__ = "prototype_screens"
    __table_args__ = (
        CheckConstraint("screen_area IN ('publica', 'privada', 'modal', 'admin_demo')", name="ck_prototype_screens_area"),
        CheckConstraint("screen_status IN ('implementada', 'pendiente', 'descartada')", name="ck_prototype_screens_status"),
        CheckConstraint("requires_auth IN (0, 1)", name="ck_prototype_screens_auth_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    screen_area: Mapped[str] = mapped_column(String(24), nullable=False)
    screen_status: Mapped[str] = mapped_column(String(24), nullable=False)
    requires_auth: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    route_hint: Mapped[str] = mapped_column(String(120), nullable=False)


class BusinessRule(Base):
    __tablename__ = "business_rules"
    __table_args__ = (
        CheckConstraint("rule_status IN ('vigente', 'pendiente', 'retirada')", name="ck_business_rules_status"),
        CheckConstraint("rule_domain IN ('auth', 'ddu', 'notificaciones', 'autorizaciones', 'seguridad')", name="ck_business_rules_domain"),
        CheckConstraint("priority IN ('baja', 'media', 'alta')", name="ck_business_rules_priority"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    rule_status: Mapped[str] = mapped_column(String(24), nullable=False)
    rule_domain: Mapped[str] = mapped_column(String(32), nullable=False)
    priority: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(80), nullable=False)


class ValidationRule(Base):
    __tablename__ = "validation_rules"
    __table_args__ = (
        CheckConstraint("validation_type IN ('check_sql', 'pydantic', 'frontend', 'manual')", name="ck_validation_rules_type"),
        CheckConstraint("severity IN ('info', 'warning', 'error')", name="ck_validation_rules_severity"),
        CheckConstraint("automated IN (0, 1)", name="ck_validation_rules_automated_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    target: Mapped[str] = mapped_column(String(120), nullable=False)
    validation_type: Mapped[str] = mapped_column(String(24), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    automated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str] = mapped_column(String(240), nullable=False)


class ProductChecklistItem(Base):
    __tablename__ = "product_checklist_items"
    __table_args__ = (
        CheckConstraint("item_status IN ('cumplido', 'pendiente', 'bloqueado')", name="ck_product_checklist_status"),
        CheckConstraint("criterion_type IN ('funcional', 'tecnico', 'seguridad', 'deploy')", name="ck_product_checklist_criterion"),
        CheckConstraint("evidence_required IN (0, 1)", name="ck_product_checklist_evidence_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    item_status: Mapped[str] = mapped_column(String(24), nullable=False)
    criterion_type: Mapped[str] = mapped_column(String(24), nullable=False)
    evidence_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    owner_agent: Mapped[str] = mapped_column(String(80), nullable=False)


class TestEvidenceRecord(Base):
    __tablename__ = "test_evidence_records"
    __table_args__ = (
        CheckConstraint("evidence_type IN ('pytest', 'node_check', 'manual', 'screenshot')", name="ck_test_evidence_type"),
        CheckConstraint("result IN ('passed', 'failed', 'pending')", name="ck_test_evidence_result"),
        CheckConstraint("duration_seconds >= 0", name="ck_test_evidence_duration_nonnegative"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    evidence_type: Mapped[str] = mapped_column(String(24), nullable=False)
    result: Mapped[str] = mapped_column(String(16), nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    command: Mapped[str] = mapped_column(String(180), nullable=False)
    recorded_at: Mapped[str] = mapped_column(String(32), nullable=False)


class DeploymentTarget(Base):
    __tablename__ = "deployment_targets"
    __table_args__ = (
        CheckConstraint("environment IN ('local', 'sandbox', 'ec2_pendiente')", name="ck_deployment_targets_environment"),
        CheckConstraint("target_status IN ('pendiente', 'preparado_demo', 'bloqueado')", name="ck_deployment_targets_status"),
        CheckConstraint("external_network_enabled IN (0, 1)", name="ck_deployment_targets_external_bool"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    environment: Mapped[str] = mapped_column(String(24), nullable=False)
    target_status: Mapped[str] = mapped_column(String(24), nullable=False)
    external_network_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deployment_note: Mapped[str] = mapped_column(String(220), nullable=False)
    owner_agent: Mapped[str] = mapped_column(String(80), nullable=False)
