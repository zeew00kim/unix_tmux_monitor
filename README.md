## 루트 계정에서 생성된 tmux 서버에서 사용하는 감시도구

### 루트 계정에서 초기 환경 설정
1. /task/tmux_monitor 디렉토리에 코드와 로그 저장
2. /tmp/tmux-shared/default 경로에 tmux 소켓 생성
3. 루트가 모든 세션 제어 가능하도록 공유 경로 설정

### 일반 사용자(user1)에서 테스트 세션 생성
1. /tmp/tmux-shared/default 소켓을 사용해 test1 세션 생성
2. 이 세션은 루트가 만든 소켓 기반이므로 루트가 감시 가능

### 루트 계정에서 모니터링 실행
1. tmux_monitor.py 실행 시:
2. /tmp/tmux-shared/default의 세션 목록 가져옴
3. #{session_activity}로 idle 시간 계산
4. idle 시간이 기준 이상인 세션을 필터링
5. 세션에 경고 메시지 전송
6. 해당 세션 강제 종료

### 루트 계정에서 로그 확인
1. logs/tmux_monitor.log에 모든 작업 기록됨
2. 어떤 세션이 종료됐는지, 어떤 메시지를 보냈는지 로그에서 확인 가능

### 테스트 세션 idle 상태 유도
1. tmux 세션 접속 → 아무 입력 없이 10초 이상 대기 → 세션 idle 상태
2. tmux_monitor.py 실행 시 해당 세션이 자동 감지, 경고 후 종료