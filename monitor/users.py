# 현재 로그인한 사용자의 정보를 수집

import subprocess
import logging

def get_logged_in_users():
    """
    현재 로그인한 사용자 계정 목록을 반환한다.

    Returns:
        list[str]: 로그인 중인 사용자 이름 목록 (중복 제거)
        예: ['ce22f067', 'ubuntu']
    """
    try:
        result = subprocess.run(
            ["who"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            logging.error(f"'who' 명령 실행 실패 : {result.stderr.strip()}")
            return []

        users = set()
        for line in result.stdout.strip().split('\n'):
            if line:
                username = line.split()[0]
                users.add(username)

        return list(users)

    except Exception as e:
        logging.exception(f"로그인 사용자 정보 수집 중 오류 발생 : {e}")
        return []