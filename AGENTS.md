# Repository Guidelines

## Project Structure & Module Organization

This repository is currently documentation-first. Source materials live in `docs/`:

- `especificacion_requerimientos_funcionales-2.md` is the consolidated functional specification.
- `Rex._N°997-2023_aprueba_bases-mp.pdf` and `ANEXO_N°7.pdf`–`ANEXO_N°8.pdf` are source PDFs.
- `ANEXO_N°3.docx`–`ANEXO_N°6.docx` are administrative and technical annexes.

Keep source documents unchanged unless a correction is explicitly required. Add derived diagrams or extracted images under `docs/anexos_imagenes/`, matching the relative path referenced by the specification. If application code is introduced, place it in `src/` and tests in `tests/`, then update this guide.

## Build, Test, and Development Commands

There is no build system or automated test suite yet. Use lightweight document checks from the repository root:

```powershell
rg --files docs
rg -n -g "*.md" "^(#|##|###) " docs
rg -n -g "*.md" "CU_[0-9]{3}|FUN_[0-9]{3}|FT_[0-9]{3}" docs
```

These commands inventory tracked documentation, inspect heading structure, and spot requirement identifiers. Before submitting changes, preview edited Markdown and verify links, tables, accents, and referenced files.

## Coding Style & Naming Conventions

Write Markdown in UTF-8, using concise Spanish for project content and one top-level heading per file. Keep headings hierarchical and tables readable. Preserve the established identifiers: `S##` for sources, `E##` for evidence, and three-digit IDs such as `CU_001`, `FUN_001`, `FT_001`, `RN_001`, `CH_001`, `EX_001`, and `OT_001`. Never renumber existing entries merely for presentation; traceability depends on stable IDs.

Use descriptive lowercase filenames for new Markdown documents, separated with underscores, for example `matriz_trazabilidad.md`.

## Testing Guidelines

Document review is the current test process. Confirm every new or changed requirement has a source/evidence reference, acceptance criteria remain testable, and cross-referenced IDs exist. Check that generated assets open correctly and that binary annexes are not accidentally replaced.

## Commit & Pull Request Guidelines

No Git history is available in the current repository snapshot, so no existing commit convention can be inferred. Use short, imperative commits such as `docs: clarify DDU cancellation flow`.

Pull requests should summarize the change, list affected requirement IDs and source documents, explain traceability updates, and include screenshots only when diagrams or rendered formatting change. Link the relevant issue or decision record when available.

## Security & Configuration

Do not add credentials, personal data, or unredacted working notes. Treat procurement and identity-system documents as controlled project material and preserve their provenance.
