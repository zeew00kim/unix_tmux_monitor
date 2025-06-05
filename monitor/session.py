# tmux 세션 정보 수집

import subprocess
import logging

def get_tmux_sessions():
    """
    현재 실행 중인 tmux 세션 목록과 각 세션의 idle 시간(초 단위)을 반환
    ex) [{'name': 'session', 'idle' : 4000}, ...]
    """

    sessions = []

    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            logging.error(f"tmux list-sessions 실패 : {result.stderr.strip()}")
            return []

        session_names = result.stdout.strip().split('\n')

        for name in session_names:
            idle_result = subprocess.run(
                ["tmux", "display-message", "-p", "-t", name, "#{session_idle}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if idle_result.returncode != 0:
                logging.warning(f"세션 '{name}'의 idle 시간 조회 실패 : {idle_result.stderr.strip()}")
                continue

            try:
                idle_seconds = int(idle_result.stdout.strip())
                sessions.append({"name": name, "idle": idle_seconds})
            except ValueError:
                logging.warning(f"세션 '{name}'의 idle 시간 파싱 실패 : {idle_result.stdout.strip()}")

    except Exception as e:
        logging.exception(f"tmux 세션 정보 수집 중 오류 발생 : {e}")

    return sessions