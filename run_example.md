## tmux_monitor 프로젝트 시연 환경 구성

### 1. 루트 계정에서 초기 환경 설정
```bash
# 1-1. 작업 디렉토리로 이동 및 압축 해제
cd ~
mkdir -p /task && cd /task
tar -xzvf tmux_monitor.tar.gz
cd tmux_monitor

# 1-2. 실행 권한 부여
chmod +x tmux_monitor.py

# 1-3. 공유 tmux 소켓 디렉토리 생성
sudo mkdir -p /tmp/tmux-shared
sudo chmod 777 /tmp/tmux-shared
```
---
### 2. 일반 사용자(user1)에서 테스트 세션 생성
```bash
# 공유 소켓을 사용하는 tmux 세션을 bg 생성
# 이 소켓은 루트 계정이 관리하는 감시대상 소켓
tmux -S /tmp/tmux-shared/default new-session -d -s test1
```
---
### 3. 루트 계정에서 모니터링 실행
```bash
# IDLE_THRESHOLD는 tmux_monitor.py 내부에 설정됨 (임시값: 10초)
# 실 운영 환경에서는 3600(1시간) 등으로 조정 가능

# 3-1. 작업 디렉토리 이동
cd /task/tmux_monitor

# 3-2. 모니터링 스크립트 실행
sudo python3 tmux_monitor.py
```
---
### 4. 루트 계정에서 로그 목록 확인
```bash
sudo tail -f logs/tmux_monitor.log
```
---
### 5. 테스트 세션 idle 상태로 만들기
```bash
# 테스트 세션 만든 후 아무 키도 입력하지 않고 10초 이상 놔두면 idle 시간 누적(감지)
tmux -S /tmp/tmux-shared/default attach -t test1
# 바로 ctrl + B D 누르고 대기 (세션에서 빠져나오고 bg 수행)

```