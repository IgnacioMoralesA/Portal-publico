from pathlib import Path

from factory.context import build_context_pack
from factory.orchestrator import run_project
from factory.registry import agent_registry, tool_registry
from factory.validators import validate_required_run_artifacts


def test_registry_has_token_economizer():
    assert "agent.token_economizer" in agent_registry()
    assert tool_registry()["shell.free"].allowed is False


def test_context_pack_budget(tmp_path: Path):
    project = tmp_path / "project"
    (project / "input").mkdir(parents=True)
    (project / "input" / "especificacion_requerimientos_funcionales.md").write_text(
        "# Requisitos\n\n## CU_001\nPortal ClaveÚnica DDU notificaciones 2FA sesiones autorizaciones.",
        encoding="utf-8",
    )
    pack = build_context_pack(project, "Construir portal", max_tokens=500)
    assert pack["estimated_tokens"] <= 500
    assert pack["economy_mode"] is True


def test_run_project_creates_artifacts(tmp_path: Path):
    project = tmp_path / "project"
    (project / "input").mkdir(parents=True)
    (project / "input" / "especificacion_requerimientos_funcionales.md").write_text(
        "# Especificación\n\n## CU_001\nPortal público de ClaveÚnica.\n\n## CU_005\nConfigurar DDU.",
        encoding="utf-8",
    )
    run_dir = run_project(project, "Construir portal ClaveÚnica", max_context_tokens=1000)
    assert not validate_required_run_artifacts(run_dir)
    assert (run_dir / "final-report.md").exists()
