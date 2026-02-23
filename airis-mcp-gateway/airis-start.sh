#!/bin/bash
DOCKER="/mnt/c/Program Files/Docker/Docker/resources/bin/docker"
COMPOSE_DIR="/home/tovic/.superclaude/airis-mcp-gateway"

# Docker Desktop이 준비될 때까지 대기 (최대 60초)
timeout=60
until "$DOCKER" info > /dev/null 2>&1; do
    if [ $timeout -le 0 ]; then
        exit 1
    fi
    sleep 2
    ((timeout -= 2))
done

cd "$COMPOSE_DIR"
"$DOCKER" compose down
"$DOCKER" compose up -d

# 게이트웨이가 healthy 될 때까지 대기 (최대 120초)
timeout=120
until [ "$("$DOCKER" inspect --format='{{.State.Health.Status}}' airis-mcp-gateway 2>/dev/null)" = "healthy" ]; do
    if [ $timeout -le 0 ]; then
        exit 1
    fi
    sleep 2
    ((timeout -= 2))
done
