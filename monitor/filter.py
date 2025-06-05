# 세션 필터링 목적 로직

import logging

def filter_idle_sessions(sessions, logged_in_users, idle_threshold):
    """
    세션 목록 중 다음 조건을 모두 만족하는 세션만 반환한다:
    - idle 시간이 기준(threshold) 이상
    - 세션 이름이 현재 로그인된 사용자 목록에 포함되지 않음

    Args:
        sessions (list[dict]): tmux 세션 정보 리스트
            ex) [{'name': 'session1', 'idle': 4000}, ...]
        logged_in_users (list[str]): 현재 로그인 사용자 이름 리스트
        idle_threshold (int): idle 시간 기준 (초 단위)

    Returns:
        list[dict]: 필터링된 세션 목록
    """
    filtered = []

    for session in sessions:
        name = session.get("name")
        idle = session.get("idle", 0)

        if idle >= idle_threshold:
            filtered.append(session)
            logging.info(f"필터링 통과 : {name} (idle {idle}s)")

    return filtered
