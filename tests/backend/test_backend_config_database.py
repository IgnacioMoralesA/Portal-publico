import runpy

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.backend.config import BASE_DIR, Settings, settings
from app.backend.database import Base, get_db
from app.backend.main import create_app


def test_settings_are_local_mock_only():
    local_settings = Settings()

    assert settings.environment == "local_mock"
    assert local_settings.database_url.startswith("sqlite:///")
    assert str(BASE_DIR) in local_settings.database_url
    assert local_settings.external_services_enabled is False
    assert "demo" in local_settings.demo_token


def test_get_db_yields_and_closes_session():
    generator = get_db()
    db = next(generator)

    assert db.is_active
    try:
        next(generator)
    except StopIteration:
        pass


def test_create_app_registers_expected_metadata():
    app = create_app()

    assert app.title == settings.app_name
    assert app.version == settings.version
    assert any(route.path == "/health" for route in app.routes)


def test_backend_main_module_prints_import_message(capsys):
    runpy.run_module("app.backend.main", run_name="__main__")

    assert "import OK" in capsys.readouterr().out


def test_temporary_sqlite_database_can_be_created():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        table_names = set(db.bind.dialect.get_table_names(db.bind.connect()))

    assert "users" in table_names
    assert "deployment_targets" in table_names
