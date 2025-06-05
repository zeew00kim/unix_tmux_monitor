# 메인 실행 스크립트

import logging
from monitor.session import get_tmux_sessions
from monitor.users import get_logged_in_users
from monitor.filter import filter_idle_sessions
from monitor.notify import send_tmux_message, log_event, kill_tmux_session

IDLE_THRESHOLD = 10  # 테스트용: 10초 이상 idle 시 처리
LOG_FILE = "logs/tmux_monitor.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    logging.info("===== tmux 세션 감시 시작 =====")

    # 1. 세션 정보 수집
    sessions = get_tmux_sessions()
    logging.info(f"세션 수집 완료: {len(sessions)}개")

    # 2. 로그인 사용자 수집
    users = get_logged_in_users()
    logging.info(f"현재 로그인 사용자: {users}")

    # 3. 비활성 세션 필터링
    targets = filter_idle_sessions(sessions, users, IDLE_THRESHOLD)
    logging.info(f"비활성 세션 필터링 결과: {len(targets)}개")

    # 4. 알림 및 자동 종료
    for session in targets:
        msg = "[경고] 세션이 1시간 이상 비활성 상태입니다. 자동 종료 대상이 될 수 있습니다."
        send_tmux_message(session["name"], msg)
        log_event(session["name"], msg)
        kill_tmux_session(session["name"]) # 해당 세션 tmux 강제 종료

    logging.info("===== 감시 완료 =====\n")

if __name__ == "__main__":
    main()