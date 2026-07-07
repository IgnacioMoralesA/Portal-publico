"""CLI de la fábrica."""

from __future__ import annotations

import argparse
from pathlib import Path

from .orchestrator import initialize_project, run_project


def main() -> None:
    parser = argparse.ArgumentParser(prog="factory", description="Fábrica ClaveÚnica ARNES SDD")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--project", default="project")

    p_run = sub.add_parser("run")
    p_run.add_argument("--project", default="project")
    p_run.add_argument("--objective", required=True)
    p_run.add_argument("--economy", action="store_true", default=True)
    p_run.add_argument("--max-context-tokens", type=int, default=3500)

    args = parser.parse_args()
    project = Path(args.project)

    if args.cmd == "init":
        initialize_project(project)
        print(f"Proyecto inicializado en {project}")
    elif args.cmd == "run":
        run_dir = run_project(project, args.objective, economy_mode=args.economy, max_context_tokens=args.max_context_tokens)
        print(f"Run creado: {run_dir}")


if __name__ == "__main__":
    main()
