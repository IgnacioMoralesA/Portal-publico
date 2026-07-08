from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def read_doc(name: str) -> str:
    path = DOCS / name
    assert path.exists(), f"missing {path}"
    return path.read_text(encoding="utf-8")


def count_ids(text: str, prefix: str) -> int:
    return len(set(re.findall(rf"\b{re.escape(prefix)}\d{{3}}\b", text)))


def test_scope_catalog_documents_exist_and_have_required_counts():
    read_doc("SYSTEM_SPECIFICATION.md")

    use_cases = read_doc("USE_CASE_CATALOG.md")
    assert count_ids(use_cases, "CU-") >= 10

    flows = read_doc("FUNCTIONAL_FLOW_CATALOG.md")
    flow_ids = set(re.findall(r"\b(?:FUN|FLUJO)-\d{3}\b", flows))
    assert len(flow_ids) >= 30

    screens = read_doc("SCREEN_INVENTORY.md")
    screen_ids = set(re.findall(r"\b(?:UI|SCREEN)-\d{3}\b", screens))
    assert len(screen_ids) >= 30

    rules = read_doc("BUSINESS_RULES_CATALOG.md")
    assert count_ids(rules, "RN-") >= 60

    read_doc("PRODUCT_COMPLETENESS_CHECKLIST.md")


def test_scope_matrix_mentions_minimum_backend_criteria():
    matrix = read_doc("SCOPE_COMPLIANCE_MATRIX.md").lower()
    assert "40 tablas" in matrix
    assert "40 endpoints" in matrix
    assert "100" in matrix and "check" in matrix


def test_docs_do_not_claim_real_production_operation():
    checked_docs = [
        "SYSTEM_SPECIFICATION.md",
        "USE_CASE_CATALOG.md",
        "FUNCTIONAL_FLOW_CATALOG.md",
        "SCREEN_INVENTORY.md",
        "BUSINESS_RULES_CATALOG.md",
        "PRODUCT_COMPLETENESS_CHECKLIST.md",
        "SCOPE_COMPLIANCE_MATRIX.md",
        "README.md",
    ]
    forbidden_patterns = [
        r"\best[aá] desplegado en producci[oó]n\b",
        r"\bsistema productivo real\b",
        r"\boperaci[oó]n productiva real habilitada\b",
        r"\bdeploy ec2 cumplido\b",
        r"\bec2 aws cumple\b",
    ]

    for relative in checked_docs:
        path = ROOT / relative if relative == "README.md" else DOCS / relative
        text = path.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert not re.search(pattern, text), f"{relative} claims real production: {pattern}"
        assert "sandbox" in text or "no produccion" in text or "no producción" in text
