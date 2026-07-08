from sqlalchemy import CheckConstraint, inspect

from app.backend.database import Base, engine
from app.backend.seed import init_db


EXPECTED_TABLES = {
    "users",
    "auth_factors",
    "login_attempts",
    "user_sessions",
    "ddu_profiles",
    "notifications",
    "authorization_requests",
    "audit_events",
    "user_profiles",
    "user_contact_methods",
    "security_questions",
    "password_recovery_requests",
    "otp_challenges",
    "session_events",
    "trusted_devices",
    "device_risk_assessments",
    "ddu_activation_events",
    "ddu_cancellation_events",
    "notification_recipients",
    "notification_read_events",
    "notification_categories",
    "notification_priorities",
    "notification_delivery_attempts",
    "authorization_decisions",
    "authorization_history",
    "sensitive_data_categories",
    "institutions",
    "institution_integrations",
    "integration_status_events",
    "help_articles",
    "help_categories",
    "public_news",
    "public_service_cards",
    "accessibility_checks",
    "prototype_screens",
    "business_rules",
    "validation_rules",
    "product_checklist_items",
    "test_evidence_records",
    "deployment_targets",
}


def test_database_has_at_least_40_sqlalchemy_tables():
    init_db()

    assert len(Base.metadata.tables) >= 40
    assert EXPECTED_TABLES.issubset(set(Base.metadata.tables))


def test_sqlite_database_contains_expected_tables():
    init_db()

    table_names = set(inspect(engine).get_table_names())
    assert len(table_names) >= 40
    assert EXPECTED_TABLES.issubset(table_names)


def test_metadata_has_at_least_100_check_constraints():
    check_count = sum(
        1
        for table in Base.metadata.tables.values()
        for constraint in table.constraints
        if isinstance(constraint, CheckConstraint)
    )

    assert check_count >= 100
