# Airis MCP Gateway 설정 가이드

## 개요
WSL2 환경에서 Docker 기반 Airis MCP Gateway를 systemd 서비스로 자동 시작하는 설정.

---

## 핵심 파일 목록

| 파일 | 설명 |
|------|------|
| `/etc/wsl.conf` | WSL systemd 활성화 |
| `/etc/systemd/system/airis-mcp-gateway.service` | systemd 서비스 정의 |
| `/home/tovic/.local/bin/airis-start.sh` | 실제 시작 스크립트 |
| `/home/tovic/.superclaude/airis-mcp-gateway/docker-compose.yml` | Docker Compose 설정 |
| `/home/tovic/.superclaude/airis-mcp-gateway/mcp-config.json` | MCP 서버 목록 및 API 키 |
| `/home/tovic/.claude/settings.json` | Claude Code 설정 |
| `/home/tovic/.claude/statusline-command.sh` | 상태바 스크립트 |

---

## 파일 내용

### /etc/wsl.conf
```ini
[boot]
systemd=true

[user]
default=tovic
```

### /etc/systemd/system/airis-mcp-gateway.service
```ini
[Unit]
Description=Airis MCP Gateway
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
User=tovic
ExecStart=/home/tovic/.local/bin/airis-start.sh

[Install]
WantedBy=multi-user.target
```
- `Type=oneshot` + `RemainAfterExit=yes`: 스크립트 실행 후 종료해도 "active" 상태 유지
- `active (exited)` 상태가 정상

### /home/tovic/.local/bin/airis-start.sh
```bash
#!/bin/bash
DOCKER="/mnt/c/Program Files/Docker/Docker/resources/bin/docker"
COMPOSE_DIR="/home/tovic/.superclaude/airis-mcp-gateway"

# Docker Desktop이 준비될 때까지 대기 (최대 60초)
timeout=60
until "$DOCKER" info > /dev/null 2>&1; do
    if [ $timeout -le 0 ]; then exit 1; fi
    sleep 2
    ((timeout -= 2))
done

cd "$COMPOSE_DIR"
"$DOCKER" compose down
"$DOCKER" compose up -d

# airis-mcp-gateway 컨테이너가 healthy 될 때까지 대기 (최대 120초)
timeout=120
until [ "$("$DOCKER" inspect --format='{{.State.Health.Status}}' airis-mcp-gateway 2>/dev/null)" = "healthy" ]; do
    if [ $timeout -le 0 ]; then exit 1; fi
    sleep 2
    ((timeout -= 2))
done
```
- **주의**: `tovic` 사용자명과 Docker 경로가 하드코딩되어 있음. 다른 PC 적용 시 변경 필요.

### Docker 컨테이너 3개
| 컨테이너 | 포트 | 역할 |
|----------|------|------|
| `airis-serena` | 8000 | Semantic code retrieval |
| `airis-mcp-gateway-core` | 9390 | Docker MCP Gateway |
| `airis-mcp-gateway` | 9400 | Airis FastAPI 프록시 (메인) |

### MCP 서버 목록 (mcp-config.json)
airis-agent, context7, fetch, memory, sequential-thinking, serena, tavily, supabase, playwright, magic, morphllm, chrome-devtools, github, postgres, stripe, twilio, cloudflare

---

## 다른 PC에 동일 환경 구성하는 단계별 가이드

### Step 1: WSL systemd 활성화
```bash
sudo nano /etc/wsl.conf
```
```ini
[boot]
systemd=true

[user]
default=YOUR_USERNAME
```
WSL 재시작: Windows에서 `wsl --shutdown` 후 재시작

### Step 2: 필요 디렉토리 및 파일 복사
```bash
mkdir -p ~/.superclaude/airis-mcp-gateway
mkdir -p ~/.local/bin
mkdir -p ~/.claude
```
복사할 파일:
- `docker-compose.yml` → `~/.superclaude/airis-mcp-gateway/`
- `mcp-config.json` → `~/.superclaude/airis-mcp-gateway/`
- `airis-start.sh` → `~/.local/bin/`
- `statusline-command.sh`, `statusline.py` → `~/.claude/`

### Step 3: airis-start.sh 수정
```bash
nano ~/.local/bin/airis-start.sh
```
변경사항:
- `DOCKER` 경로: Docker Desktop 설치 위치에 맞게 수정
- `COMPOSE_DIR`: `/home/YOUR_USERNAME/.superclaude/airis-mcp-gateway`
- 실행 권한 부여: `chmod +x ~/.local/bin/airis-start.sh`

### Step 4: systemd 서비스 등록
```bash
sudo nano /etc/systemd/system/airis-mcp-gateway.service
```
위의 서비스 파일 내용 붙여넣기 (User=YOUR_USERNAME, ExecStart 경로 수정)

```bash
sudo systemctl daemon-reload
sudo systemctl enable airis-mcp-gateway
sudo systemctl start airis-mcp-gateway
```

### Step 5: Claude Code settings.json 설정
`~/.claude/settings.json`:
```json
{
  "model": "opusplan",
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  },
  "syntaxHighlightingDisabled": false,
  "skipDangerousModePermissionPrompt": true
}
```

### Step 6: 검증
```bash
# 서비스 상태 확인
systemctl status airis-mcp-gateway

# 컨테이너 확인
docker ps

# MCP Gateway 응답 확인
curl http://localhost:9400/health
```

---

## 동작 원리
1. WSL 부팅 시 systemd가 `airis-mcp-gateway.service` 자동 실행
2. 서비스가 `airis-start.sh` 호출
3. 스크립트가 Docker Desktop 준비를 기다린 후 컨테이너 시작
4. `airis-mcp-gateway` 컨테이너가 healthy 상태가 되면 스크립트 종료
5. Claude Code 시작 시 MCP 서버 연결 가능

## 참고사항
- Claude Code는 Airis가 ready 상태가 된 **후**에 시작해야 MCP 연결이 됨
- 터미널 새 창에서 Airis 상태는 **한 번만** 표시됨 (세션당 1회)
- `active (exited)` systemd 상태는 정상 (oneshot 타입)
