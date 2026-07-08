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
