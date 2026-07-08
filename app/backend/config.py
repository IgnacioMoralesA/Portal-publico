from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Settings:
    app_name = "ClaveUnica Demo Backend Local"
    environment = "local_mock"
    version = "0.1.0"
    database_url = f"sqlite:///{BASE_DIR / 'local.db'}"
    demo_username = "demo.claveunica"
    demo_password = "DemoLocal2026"
    demo_otp = "123456"
    demo_token = "demo-local-token"
    external_services_enabled = False


settings = Settings()
