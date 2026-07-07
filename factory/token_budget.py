"""Economía de tokens y compactación de contexto."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .constants import TOKEN_ECONOMY_POLICY


@dataclass
class TokenLedger:
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    max_context_tokens: int = TOKEN_ECONOMY_POLICY["max_context_tokens_per_agent"]
    economy_mode: bool = True

    @property
    def total(self) -> int:
        return self.estimated_input_tokens + self.estimated_output_tokens

    @property
    def within_budget(self) -> bool:
        return self.estimated_input_tokens <= self.max_context_tokens

    def as_dict(self) -> dict:
        return {
            "estimated_input_tokens": self.estimated_input_tokens,
            "estimated_output_tokens": self.estimated_output_tokens,
            "max_context_tokens": self.max_context_tokens,
            "total": self.total,
            "within_budget": self.within_budget,
            "economy_mode": self.economy_mode,
        }


def estimate_tokens(text: str) -> int:
    chars_per_token = int(TOKEN_ECONOMY_POLICY["token_estimation_chars_per_token"])
    return max(1, (len(text) + chars_per_token - 1) // chars_per_token)


def compact_text(text: str, max_tokens: int | None = None) -> str:
    """Compacta texto preservando encabezados, bullets e IDs relevantes."""
    if not text:
        return ""
    max_tokens = max_tokens or TOKEN_ECONOMY_POLICY["max_context_tokens_per_agent"]
    max_chars = max_tokens * TOKEN_ECONOMY_POLICY["token_estimation_chars_per_token"]

    lines = [ln.rstrip() for ln in text.splitlines()]
    keep: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#") or s.startswith("- ") or re.search(r"\b(CU|FUN|RN|CH|EX|ACT|E)\_\d+", s):
            keep.append(s)
        elif len(keep) < 30 and len(s) < 180:
            keep.append(s)

    compact = "\n".join(keep)
    if len(compact) > max_chars:
        compact = compact[:max_chars].rsplit("\n", 1)[0] + "\n...[compactado por presupuesto de tokens]"
    return compact


def select_relevant_sections(text: str, keywords: list[str], max_tokens: int | None = None) -> str:
    """Selecciona bloques que contienen keywords y compacta el resultado."""
    if not text:
        return ""
    chunks = re.split(r"\n(?=##+ )", text)
    selected: list[str] = []
    kws = [k.lower() for k in keywords]
    for chunk in chunks:
        low = chunk.lower()
        if any(k in low for k in kws):
            selected.append(chunk)
    if not selected:
        selected = chunks[:3]
    return compact_text("\n\n".join(selected), max_tokens=max_tokens)
