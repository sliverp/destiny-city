import time
import json
import base64
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import InviteVerifyRequest, InviteVerifyResponse
from app.services.invite_service import verify_and_use_code

router = APIRouter(prefix="/api/invite", tags=["invite"])

# 防暴力破解：记录错误次数 {key: (error_count, first_error_time)}
_fail_tracker: dict[str, tuple[int, float]] = defaultdict(lambda: (0, 0.0))
FAIL_LIMIT = 3
BAN_SECONDS = 120


def _get_client_key(request: Request) -> str:
    """获取客户端标识：优先用 cookie 中的 visitor_id，其次用 IP"""
    visitor_id = request.cookies.get("visitor_id", "")
    ip = request.client.host if request.client else "unknown"
    return f"{ip}:{visitor_id}" if visitor_id else ip


def _check_rate_limit(key: str) -> tuple[bool, int]:
    """检查是否被限流。返回 (is_blocked, remaining_seconds)"""
    count, first_time = _fail_tracker[key]
    if count >= FAIL_LIMIT:
        elapsed = time.time() - first_time
        if elapsed < BAN_SECONDS:
            return True, int(BAN_SECONDS - elapsed)
        # 封禁时间已过，重置
        _fail_tracker[key] = (0, 0.0)
    return False, 0


def _record_fail(key: str):
    count, first_time = _fail_tracker[key]
    if count == 0:
        _fail_tracker[key] = (1, time.time())
    else:
        _fail_tracker[key] = (count + 1, first_time)


def _clear_fail(key: str):
    _fail_tracker.pop(key, None)


@router.post("/verify", response_model=InviteVerifyResponse)
def verify_invite(req: InviteVerifyRequest, request: Request, db: Session = Depends(get_db)):
    client_key = _get_client_key(request)

    # 检查是否被封禁
    blocked, remaining = _check_rate_limit(client_key)
    if blocked:
        return InviteVerifyResponse(
            valid=False,
            message=f"输入错误次数过多，请在 {remaining} 秒后重试"
        )

    # 区分大小写，不做 upper() 转换
    code = req.code.strip()
    valid, message, invite_id, share_id = verify_and_use_code(db, code)

    if not valid:
        _record_fail(client_key)
        count, _ = _fail_tracker[client_key]
        remaining_tries = max(0, FAIL_LIMIT - count)
        if remaining_tries > 0:
            message = f"{message}，还可尝试 {remaining_tries} 次"
        else:
            message = f"{message}，连续错误过多，请等待 2 分钟后重试"
        return InviteVerifyResponse(valid=False, message=message)

    # 验证成功，清除错误记录
    _clear_fail(client_key)

    if share_id:
        # 已使用的邀请码，返回 share_id 让前端跳转到报告页
        return InviteVerifyResponse(valid=True, token="", message=message, share_id=share_id)

    # 新邀请码，生成 token
    token_data = json.dumps({"invite_id": invite_id})
    token = base64.urlsafe_b64encode(token_data.encode()).decode()
    return InviteVerifyResponse(valid=True, token=token, message=message)
