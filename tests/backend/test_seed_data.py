from sqlalchemy import Text, func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import String

from app.backend.database import Base, engine
from app.backend.models import (
    AuthorizationRequest,
    DeploymentTarget,
    Notification,
    ProductChecklistItem,
    User,
    UserSession,
)
from app.backend.seed import DEMO_USER_ID, init_db


def test_seed_runs_and_main_tables_have_demo_data():
    init_db()

    with Session(engine) as db:
        assert db.get(User, DEMO_USER_ID)
        assert db.scalar(select(func.count()).select_from(UserSession)) >= 3
        assert db.scalar(select(func.count()).select_from(Notification)) >= 2
        assert db.scalar(select(func.count()).select_from(AuthorizationRequest)) >= 5
        assert db.get(ProductChecklistItem, "CHK-DEMO-001")
        assert db.get(DeploymentTarget, "DEP-DEMO-001")


def test_seed_is_idempotent():
    init_db()
    init_db()

    with Session(engine) as db:
        assert db.scalar(select(func.count()).select_from(User).where(User.id == DEMO_USER_ID)) == 1
        assert db.scalar(select(func.count()).select_from(ProductChecklistItem).where(ProductChecklistItem.id == "CHK-DEMO-001")) == 1


def test_seed_has_no_real_personal_data_urls_or_secrets():
    init_db()

    forbidden = [
        "accounts.claveunica",
        "api.claveunica",
        "claveunica.gob.cl",
        "casillaunica.gob.cl",
        "notificaciones.gob.cl",
        "client_secret",
        "refresh_token",
        "private_key",
        "-----begin",
        "sk-",
    ]
    allowed_markers = ["demo", "ficticio", "generico", "example.cl", "***"]
    values: list[str] = []

    with Session(engine) as db:
        for table in Base.metadata.sorted_tables:
            text_columns = [column for column in table.columns if isinstance(column.type, (String, Text))]
            if not text_columns:
                continue
            for row in db.execute(select(*text_columns)).all():
                values.extend(str(value).lower() for value in row if value)

    joined = "\n".join(values)
    for marker in forbidden:
        assert marker not in joined
    assert any(marker in joined for marker in allowed_markers)
