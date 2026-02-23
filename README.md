
# 다른 컴퓨터에서도 동일 Claude Code 사용하기 위한 설정 방법 가이드

# 1. Claude Status Line 변경
## 1. 파일 복사

- ~/.clade/statusline-command.sh
- ~/.clade/statusline.py 복사
- settings.json 수정

# 2. Warp 터미널에서 새 탭을 열 때 Airis MCP Gateway 연결 상태 표시
## 1. 전체 과정
- 복사 필요한 파일은 /airis-mcp-gateway 디렉토리에 있고, Claude Code가 생성한 가이드는 /docs/ airis-mcp-gateway/airis-setup-guide.md에 있음
- `airis-mcp-gateway.service` 수정(User=YOUR_USERNAME, ExecStart 경로) 후 systemd 서비스 등록
## 2. 파일 복사
- /etc/wsl.conf 복사
- /etc/systemd/system/airis-mcp-gateway.service 복사
- /home/tovic/.local/bin/airis-start.sh 복사
- user 레벨 MCP 설정 파일 ~/.claude.json에 MCP 서버 추가

## 3. Airis MCP Gateway 상태 확인 systemd 서비스 등록

```
sudo systemctl daemon-reload
sudo systemctl enable airis-mcp-gateway
sudo systemctl start airis-mcp-gateway
```