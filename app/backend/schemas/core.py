from pydantic import BaseModel, ConfigDict


class HealthOut(BaseModel):
    status: str
    version: str


class ApiStatusOut(BaseModel):
    status: str
    environment: str
    app_name: str
    external_services_enabled: bool
    note: str


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    success: bool
    message: str
    requires_otp: bool = True
    session_id: str | None = None


class VerifyOtpIn(BaseModel):
    otp: str


class VerifyOtpOut(BaseModel):
    success: bool
    message: str
    token: str | None = None


class DemoFactorIn(BaseModel):
    otp: str


class ToggleFactorIn(BaseModel):
    factor_type: str
    enabled: bool


class RecoveryRequestIn(BaseModel):
    username: str
    channel: str = "email"


class RecoveryConfirmIn(BaseModel):
    recovery_id: str
    otp: str


class ContactPatchIn(BaseModel):
    correo: str | None = None
    telefono: str | None = None
    otp: str


class SecurityQuestionVerifyIn(BaseModel):
    answer: str


class TrustDeviceIn(BaseModel):
    remember_device: bool = True


class UserMeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    nombre: str
    run_enmascarado: str
    correo: str
    telefono: str
    clave_unica_estado: str
    segundo_factor_activo: bool
    sesiones_activas: int


class DduStatusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    estado: str
    domicilio: str
    alerta_pendiente: bool
    fecha_configuracion: str
    canal: str
    casilla_demo: str


class SessionItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    actual: bool
    dispositivo: str
    navegador: str
    ubicacion: str
    ultimo_acceso: str
    estado: str
    riesgo: str


class NotificationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    institucion: str
    titulo: str
    estado: str
    fecha_recepcion: str
    prioridad: str
    categoria: str
    contenido: str


class AuthorizationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    institucion: str
    finalidad: str
    tipo_dato: str
    fecha_solicitud: str
    estado: str
    fecha_decision: str
    historial: list[str]
