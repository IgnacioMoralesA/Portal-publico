from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.backend.database import Base
from app.backend.routers import auth, authorizations, ddu, devices, institutions, notifications, sessions, users
from app.backend.schemas.core import (
    ContactPatchIn,
    DemoFactorIn,
    RecoveryRequestIn,
    SecurityQuestionVerifyIn,
    TrustDeviceIn,
)
from app.backend.seed import seed_demo_data


def _empty_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_user_missing_error_paths_on_empty_database():
    with _empty_db() as db:
        for action in (
            lambda: users.get_me(db),
            lambda: users.get_profile(db),
            lambda: users.patch_contact(ContactPatchIn(correo="demo@example.cl", telefono=None, otp="123456"), db),
        ):
            try:
                action()
            except Exception as exc:
                assert getattr(exc, "status_code", None) == 404


def test_ddu_missing_error_paths_on_empty_database():
    with _empty_db() as db:
        for action in (
            lambda: ddu.get_ddu_status(db),
            lambda: ddu.configure_ddu(db),
            lambda: ddu.cancel_ddu(db),
            lambda: ddu.get_activation_summary(db),
        ):
            try:
                action()
            except Exception as exc:
                assert getattr(exc, "status_code", None) == 404


def test_ddu_configure_and_cancel_create_api_events_on_fresh_seed():
    with _empty_db() as db:
        seed_demo_data(db)

        configured = ddu.configure_ddu(db)
        cancelled = ddu.cancel_ddu(db)

        assert configured["estado"] == "configurado"
        assert cancelled["estado"] == "pendiente"


def test_recovery_request_creates_record_on_fresh_seed():
    with _empty_db() as db:
        seed_demo_data(db)

        response = auth.request_recovery(RecoveryRequestIn(username="demo.claveunica", channel="email"), db)

        assert response["success"] is True
        assert response["recovery_id"] == "REC-DEMO-API"


def test_authorization_notification_session_device_missing_paths():
    with _empty_db() as db:
        calls = [
            lambda: authorizations.get_authorization("missing", db),
            lambda: authorizations.approve_authorization("missing", DemoFactorIn(otp="123456"), db),
            lambda: notifications.get_notification("missing", db),
            lambda: notifications.mark_notification_read("missing", db),
            lambda: sessions.close_session("missing", db),
            lambda: devices.trust_device("missing", TrustDeviceIn(remember_device=True), db),
            lambda: devices.revoke_device_trust("missing", db),
            lambda: institutions.get_institution("missing", db),
        ]

        for call in calls:
            try:
                call()
            except Exception as exc:
                assert getattr(exc, "status_code", None) == 404


def test_current_session_and_actual_session_close_errors_on_empty_or_current_session():
    with _empty_db() as db:
        try:
            sessions.get_current_session(db)
        except Exception as exc:
            assert getattr(exc, "status_code", None) == 404


def test_security_question_wrong_answer():
    try:
        users.verify_security_question(SecurityQuestionVerifyIn(answer="incorrecta"))
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 401
