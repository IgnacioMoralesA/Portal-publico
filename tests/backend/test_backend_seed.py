from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.backend.database import Base
from app.backend.models import (
    AuthorizationRequest,
    DeploymentTarget,
    ProductChecklistItem,
    User,
    UserSession,
)
from app.backend.seed import DEMO_USER_ID, seed_demo_data


def test_seed_populates_empty_database_and_is_idempotent():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        seed_demo_data(db)
        seed_demo_data(db)

        assert db.get(User, DEMO_USER_ID)
        assert len(db.scalars(select(UserSession)).all()) == 3
        assert len(db.scalars(select(AuthorizationRequest)).all()) == 5
        assert db.get(ProductChecklistItem, "CHK-DEMO-001")
        assert db.get(DeploymentTarget, "DEP-DEMO-001")
