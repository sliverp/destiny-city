#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cleanup() {
    echo -e "\n${YELLOW}正在停止服务...${NC}"
    if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        kill "$BACKEND_PID" 2>/dev/null
        echo -e "${GREEN}后端已停止${NC}"
    fi
    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        kill "$FRONTEND_PID" 2>/dev/null
        echo -e "${GREEN}前端已停止${NC}"
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

# ========== 后端 ==========
echo -e "${GREEN}[1/4] 检查 Python 环境...${NC}"
if command -v uv &>/dev/null; then
    UV_CMD="uv"
elif command -v python3 &>/dev/null; then
    UV_CMD=""
else
    echo -e "${RED}未找到 uv 或 python3，请先安装${NC}"
    exit 1
fi

echo -e "${GREEN}[2/4] 安装后端依赖并启动...${NC}"
cd "$BACKEND_DIR"
if [ -n "$UV_CMD" ]; then
    uv sync
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
else
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -q fastapi "uvicorn[standard]" sqlalchemy pydantic
    uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
fi

# 等待后端就绪
echo -e "${YELLOW}等待后端启动...${NC}"
for i in $(seq 1 30); do
    if curl -s http://localhost:8000/api/health >/dev/null 2>&1; then
        echo -e "${GREEN}后端已启动 (PID: $BACKEND_PID)${NC}"
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo -e "${RED}后端启动超时${NC}"
        cleanup
    fi
    sleep 1
done

# ========== 前端 ==========
echo -e "${GREEN}[3/4] 安装前端依赖...${NC}"
cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
    npm install
fi

echo -e "${GREEN}[4/4] 启动前端开发服务器...${NC}"
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  所有服务已启动！${NC}"
echo -e "${GREEN}  前端: http://localhost:5173${NC}"
echo -e "${GREEN}  后端: http://localhost:8000${NC}"
echo -e "${GREEN}  按 Ctrl+C 停止所有服务${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

wait
