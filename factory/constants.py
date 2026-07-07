"""Constantes centrales de la fábrica."""

FACTORY_NAME = "Fabrica_ClaveUnica_ARNES_SDD"
FACTORY_VERSION = "1.1.0-token-economy"
SCHEMA_VERSION = "1.0.0"
POLICY_VERSION = "1.1.0"
TOOL_REGISTRY_VERSION = "1.0.0"
MEMORY_VERSION = "1.0.0"
WORKFLOW_VERSION = "1.1.0"
INDEX_VERSION = "1.0.0"
MODEL_SNAPSHOT = "deterministic-local-harness"
MODEL_SEED = 12345

FINAL_STATUSES = ["complete", "needs_user_input", "not_answerable", "error"]

SDD_PHASES = [
    "intake",
    "specify",
    "clarify",
    "checklist",
    "context",
    "plan",
    "plan_validation",
    "tasks",
    "analyze",
    "implement",
    "validate",
    "observe",
    "close",
]

ROUTE = [
    ("specify", ["agent.spec_detallada"]),
    ("clarify", ["agent.spec_detallada"]),
    ("checklist", ["agent.qa_checklist"]),
    ("context", ["agent.context_rag", "agent.ocr_ui_analyst", "agent.token_economizer"]),
    ("plan", ["agent.architect_plan", "agent.ui_web_modern", "agent.api_security_docs"]),
    ("plan_validation", ["agent.security_policy", "agent.qa_checklist", "agent.token_economizer"]),
    ("tasks", ["agent.architect_plan", "agent.tests_coverage", "agent.doc_tecnica_detalle"]),
    ("analyze", ["agent.qa_checklist", "agent.security_policy"]),
    ("implement", ["agent.implementacion_doc_code"]),
    ("validate", ["agent.tests_coverage", "agent.security_policy", "agent.qa_checklist"]),
    ("observe", ["agent.token_billing", "agent.observability_sre", "agent.token_economizer"]),
    ("close", ["agent.doc_tecnica_detalle", "agent.token_billing", "agent.qa_checklist"]),
]

SOURCE_DOCUMENTS = [
    "source-manifest.json",
    "ESPECIFICACION_REPLICA_FABRICA.md",
    "especificacion_requerimientos_funcionales.md",
]

DESIGN_DOCS = [
    "01_Constitucion_y_Especificacion_Fabrica.md",
    "02_Politicas_y_Gates.md",
    "03_Registros_Agentes_Skills_Tools.md",
    "04_Ruta_SDD.md",
    "05_Economia_de_Tokens.md",
]

TOKEN_ECONOMY_POLICY = {
    "enabled_default": True,
    "max_context_tokens_per_agent": 3500,
    "max_agent_output_tokens": 1200,
    "max_final_report_tokens": 1800,
    "token_estimation_chars_per_token": 4,
    "avoid_full_document_reinjection": True,
    "prefer_source_ids_over_quotes": True,
    "compress_repeated_context": True,
    "require_delta_outputs": True,
    "budget_gate": "hard_fail_if_context_exceeds_limit",
}

APPROVAL_REQUIRED_FOR = [
    "external.write_unapproved",
    "deploy.direct",
    "db.write",
    "secrets.read",
    "memory.write_ungated",
]
