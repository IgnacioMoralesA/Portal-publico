import pytest
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.backend.database import Base, engine
from app.backend.models import DeploymentTarget, OtpChallenge, ValidationRule
from app.backend.seed import DEMO_USER_ID, init_db


def _check_names() -> set[str]:
    return {
        constraint.name
        for table in Base.metadata.tables.values()
        for constraint in table.constraints
        if isinstance(constraint, CheckConstraint)
    }


def test_principal_check_constraints_exist():
    names = _check_names()

    expected = {
        "ck_users_username_min",
        "ck_auth_factor_type",
        "ck_ddu_estado",
        "ck_notifications_prioridad",
        "ck_authorizations_estado",
        "ck_otp_challenges_attempt_range",
        "ck_trusted_devices_score_range",
        "ck_notification_delivery_attempt_positive",
        "ck_validation_rules_type",
        "ck_deployment_targets_environment",
    }
    assert expected.issubset(names)


@pytest.mark.parametrize(
    "row",
    [
        OtpChallenge(id="OTP-BAD", user_id=DEMO_USER_ID, challenge_status="aprobado", channel="fax", attempt_count=1, created_at="2026-07-05"),
        ValidationRule(id="VAL-BAD", target="otp", validation_type="otro", severity="error", automated=True, description="Regla invalida demo"),
        DeploymentTarget(id="DEP-BAD", environment="produccion", target_status="pendiente", external_network_enabled=False, deployment_note="No debe aceptar produccion real.", owner_agent="agent.test"),
    ],
)
def test_representative_check_constraints_reject_invalid_values(row):
    init_db()

    with Session(engine) as db:
        db.add(row)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
