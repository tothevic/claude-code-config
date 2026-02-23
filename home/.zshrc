# Starship.rs
eval "$(starship init zsh)"
export PATH="$PATH:/opt/nvim-linux-x86_64/bin"

. "$HOME/.local/bin/env"

# Airis MCP Gateway 상태 확인
_airis_status() {
    local health
    health=$("/mnt/c/Program Files/Docker/Docker/resources/bin/docker" inspect --format='{{.State.Health.Status}}' airis-mcp-gateway 2>/dev/null)
    if [ "$health" = "healthy" ]; then
        echo "✓ Airis MCP Gateway ready"
    elif [ -n "$health" ]; then
        echo "⏳ Airis MCP Gateway starting... ($health)"
    fi
}
_airis_status
