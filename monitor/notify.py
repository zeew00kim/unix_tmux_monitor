# 사용자에게 알람 메세지 전송 및 로깅

import subprocess
import logging

def send_tmux_message(session_name, message):
    """
    지정한 tmux 세션에 메시지를 전송한다.

    Args:
        session_name (str): 메시지를 보낼 tmux 세션 이름
        message (str): 표시할 메시지 내용
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
    지정한 세션에 대해 로그 파일에 이벤트 기록을 남긴다.

    Args:
        session_name (str): 대상 세션 이름
        message (str): 전송한 메시지 내용
    """
    logging.info(f"[로그 기록] 세션 '{session_name}'에 메시지 기록됨: {message}")
