## 유닉스기초 3차 팀 프로젝트 (TMUX monitor)

### session.py -> get_tmux_sessions()

tmux list-sessions -F "#{session_name}"<br>
명령어를 통해 모든 세션 이름을 가져옵니다.

각 세션에 대해 tmux display-message -p "#{session_idle}"<br>
명령어를 실행하여 idle 시간을 초 단위로 조회합니다.

{ "name": 세션명, "idle": idle시간(초) }<br>
형식의 딕셔너리를 리스트로 구성해 반환합니다.

---
### users.py -> get_logged_in_users()

**작동 방식 :**
1. who 명령어를 사용하여 현재 로그인된 사용자 세션을 조회합니다.
2. 각 출력 라인에서 **첫 번째 필드(사용자명)**만 추출합니다.
3. 중복 제거(set) 후 리스트로 변환하여 반환합니다.

**예외 처리 :**
1. who 명령 실행 실패 시 로그에 에러 기록 후 빈 리스트 반환
2. 명령 실행 중 예외 발생 시 로그 기록 후 빈 리스트 반환
---
### filter.py -> filter_idle_sessions()

**작동 방식 :**
1. sessions 리스트의 각 항목(세션 딕셔너리)을 순회하면서 아래 조건을 확인:
    - session["idle"] >= idle_threshold
    - session["name"] not in logged_in_users
2. 조건을 만족하는 세션만 리스트에 담아 반환합니다.
3. 통과한 세션에 대해서는 로그에 기록합니다.
---
### notify.py -> send_tmux_message()

**작동 방식 :**
1. tmux display-message -t `<session_name>` `<message>` 명령을 subprocess로 실행
2. 명령 실행이 실패할 경우 로그에 에러 메시지를 기록
---
### tmux_monitor.py (메인 실행 스크립트)

**주요 실행 흐름 :**
1. tmux 세션 목록 수집 -> get_tmux_sessions()
2. 로그인 사용자 목록 수집 -> get_logged_in_users()
3. 비활성 세션 필터링 -> filter_idle_sessions()
4. 메시지 전송 + 로그기록 -> send_tmux_message() + log_event()

**로그 출력 :**
1. 실행 결과는 logs/tmux_monitor.log에 자동 저장됩니다.
2. 로그 항목에는 실행 시간, 필터링 결과, 메시지 전송 내역 등이 포함됩니다.