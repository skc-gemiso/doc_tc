#!/usr/bin/env python3
"""
CLI entry point - 즉시 리턴 후 백그라운드에서 변환 실행

파일 지정:  python doc_tc.py task.json
stdin 입력: echo '{"taskId":1,...}' | python doc_tc.py
"""
import json
import subprocess
import sys

_BG_FLAG = '--background'


def main() -> None:
    if _BG_FLAG in sys.argv:
        _run_background()
    else:
        _spawn_background()


def _spawn_background() -> None:
    """JSON을 읽고 백그라운드 프로세스를 띄운 뒤 즉시 리턴."""
    try:
        if len(sys.argv) == 2:
            with open(sys.argv[1], encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to read task: {e}", file=sys.stderr)
        sys.exit(1)

    json_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")

    proc = subprocess.Popen(
        [sys.executable, __file__, _BG_FLAG],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,  # 부모 프로세스 종료 시 영향 없음
    )
    proc.stdin.write(json_bytes)
    proc.stdin.close()
    sys.exit(0)  # 즉시 리턴


def _run_background() -> None:
    """실제 변환 작업 수행 (백그라운드 프로세스에서 실행)."""
    from converter import run
    from converter.models.task import ConvertTask

    try:
        data = json.load(sys.stdin)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to read task: {e}", file=sys.stderr)
        sys.exit(1)

    task = ConvertTask.from_dict(data)
    run(task)


if __name__ == "__main__":
    main()
