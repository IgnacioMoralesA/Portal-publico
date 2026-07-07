"""Carga de fuentes y construcción de context-pack."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .constants import SOURCE_DOCUMENTS, TOKEN_ECONOMY_POLICY
from .token_budget import estimate_tokens, select_relevant_sections


def sha256_short(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def load_source_manifest(input_dir: Path) -> list[dict[str, Any]]:
    path = input_dir / "source-manifest.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    manifest = []
    for p in sorted(input_dir.glob("*")):
        if p.is_file():
            manifest.append({
                "source_id": f"S{len(manifest)+1:02d}",
                "filename": p.name,
                "sha256": sha256_short(p.read_bytes()),
                "bytes": p.stat().st_size,
            })
    return manifest


def load_markdown_sources(input_dir: Path) -> dict[str, str]:
    sources: dict[str, str] = {}
    for name in SOURCE_DOCUMENTS:
        p = input_dir / name
        if p.exists() and p.suffix.lower() in {".md", ".json", ".txt"}:
            sources[name] = p.read_text(encoding="utf-8", errors="replace")
    for p in sorted(input_dir.glob("*.md")):
        sources.setdefault(p.name, p.read_text(encoding="utf-8", errors="replace"))
    return sources


def build_context_pack(project_dir: Path, objective: str, keywords: list[str] | None = None, max_tokens: int | None = None) -> dict[str, Any]:
    input_dir = project_dir / "input"
    keywords = keywords or [
        "claveúnica", "claveunica", "portal", "ddu", "notificaciones", "casillaúnica",
        "autorizaciones", "2fa", "sesiones", "casos de uso", "calidad", "garantía"
    ]
    max_tokens = max_tokens or TOKEN_ECONOMY_POLICY["max_context_tokens_per_agent"]

    manifest = load_source_manifest(input_dir)
    sources = load_markdown_sources(input_dir)

    excerpts = []
    budget_per_doc = max(500, max_tokens // max(1, len(sources)))
    for filename, text in sources.items():
        excerpt = select_relevant_sections(text, keywords, max_tokens=budget_per_doc)
        excerpts.append({
            "filename": filename,
            "excerpt": excerpt,
            "estimated_tokens": estimate_tokens(excerpt),
        })

    total = sum(e["estimated_tokens"] for e in excerpts)
    pack = {
        "objective": objective,
        "economy_mode": True,
        "max_context_tokens": max_tokens,
        "estimated_tokens": total,
        "within_budget": total <= max_tokens,
        "source_manifest": manifest,
        "excerpts": excerpts,
        "token_rules": [
            "Usar IDs de evidencia antes que citas largas.",
            "No reenviar documentos completos a agentes.",
            "Pedir sólo chunks específicos si falta información.",
            "Producir delta de archivos y salidas acotadas.",
        ],
    }
    return pack


def write_context_pack(project_dir: Path, run_dir: Path, objective: str, max_tokens: int | None = None) -> Path:
    pack = build_context_pack(project_dir, objective, max_tokens=max_tokens)
    out = run_dir / "context-pack.json"
    out.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
