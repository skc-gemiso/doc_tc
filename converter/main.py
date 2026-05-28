#!/usr/bin/env python3
"""CLI entry point: python main.py task.json"""
import json
import sys

from converter import run
from converter.models.task import ConvertTask


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <task.json>", file=sys.stderr)
        sys.exit(1)

    task_file = sys.argv[1]
    try:
        with open(task_file, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to read task file: {e}", file=sys.stderr)
        sys.exit(1)

    task = ConvertTask.from_dict(data)
    run(task)


if __name__ == "__main__":
    main()
