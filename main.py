#!/usr/bin/env python3
"""
CLI entry point

파일 지정:  python main.py task.json
stdin 입력: echo '{"taskId":1,...}' | python main.py
"""
import json
import sys

from converter import run
from converter.models.task import ConvertTask


def main() -> None:
    try:
        if len(sys.argv) == 2:
            with open(sys.argv[1], encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to read task: {e}", file=sys.stderr)
        sys.exit(1)

    task = ConvertTask.from_dict(data)
    run(task)


if __name__ == "__main__":
    main()
