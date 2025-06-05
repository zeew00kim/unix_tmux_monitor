# tmux 세션 정보 수집

import subprocess
import logging
from datetime import datetime

def get_tmux_sessions():
    """
    현재 실행 중인 tmux 세션 목록과 각 세션의 idle 시간(초 단위)을 반환
    ex) [{'name': 'test1', 'idle': 4000}, ...]
    """

    sessions = []

    try:
        # 1. 세션 이름 수집
        result = subprocess.run(
            ["tmux", "-S", "/tmp/tmux-shared/default", "list-sessions", "-F", "#{session_name}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            logging.error(f"tmux list-sessions 실패 : {result.stderr.strip()}")
            return []

        session_names = result.stdout.strip().split('\n')

        # 2. 각 세션의 idle 시간 계산
        for name in session_names:
            idle_result = subprocess.run(
                ["tmux", "-S", "/tmp/tmux-shared/default", "display-message", "-p", "-t", name, "#{session_activity}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if idle_result.returncode != 0:
                logging.warning(f"세션 '{name}'의 idle 시간 조회 실패 : {idle_result.stderr.strip()}")
                continue

            try:
                last_active_ts = int(idle_result.stdout.strip())
                now_ts = int(datetime.now().timestamp())
                idle_seconds = now_ts - last_active_ts
                sessions.append({"name": name, "idle": idle_seconds})
            except ValueError:
                logging.warning(f"세션 '{name}'의 idle 시간 파싱 실패 : {idle_result.stdout.strip()}")

    except Exception as e:
        logging.exception(f"tmux 세션 정보 수집 중 오류 발생 : {e}")

    return sessions