# 사용자에게 알람 메세지 전송 및 로깅

import subprocess
import logging

def send_tmux_message(session_name, message):
    """
    지정한 tmux 세션에 메시지를 전송한다.
    """
    try:
        subprocess.run(
            ["tmux", "-S", "/tmp/tmux-shared/default", "display-message", "-t", session_name, message],
            check=True
        )
        logging.info(f"[알림 전송] 세션 '{session_name}': {message}")
    except subprocess.CalledProcessError as e:
        logging.error(f"[알림 실패] 세션 '{session_name}': {e}")
    except Exception as e:
        logging.exception(f"[예외 발생] 알림 전송 중 오류: {e}")

def log_event(session_name, message):
    """
    로그 파일에 알림 전송 기록을 남긴다.
    """
    logging.info(f"[로그 기록] 세션 '{session_name}'에 메시지 기록됨: {message}")

def kill_tmux_session(session_name):
    """
    지정한 세션을 종료한다.
    """
    try:
        subprocess.run(
            ["tmux", "-S", "/tmp/tmux-shared/default", "kill-session", "-t", session_name],
            check=True
        )
        logging.info(f"[세션 종료] '{session_name}' 세션이 자동 종료되었습니다.")
    except subprocess.CalledProcessError as e:
        logging.error(f"[세션 종료 실패] '{session_name}': {e}")