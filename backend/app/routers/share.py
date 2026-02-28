import secrets
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import ShareVisitor, ShareReward, InviteCode, UserResult
from app.services.invite_service import generate_code

router = APIRouter(prefix="/api/share", tags=["share"])

REQUIRED_VISITORS = 3


@router.post("/{share_id}/visit")
def record_visit(
    share_id: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """记录分享页访客，返回进度和奖励码"""
    # 验证 share_id 存在
    result = db.query(UserResult).filter(UserResult.share_id == share_id).first()
    if not result:
        return {"error": "分享链接无效"}

    # 获取或设置 visitor_id cookie（永不过期）
    visitor_id = request.cookies.get("visitor_id", "")
    if not visitor_id:
        visitor_id = secrets.token_hex(16)
        response.set_cookie(
            key="visitor_id",
            value=visitor_id,
            max_age=10 * 365 * 24 * 3600,  # 10年
            httponly=True,
            samesite="lax",
        )

    # 检查是否是分享者自己（同一邀请码对应的用户）
    # 通过 cookie 判断：如果 visitor_id 和 token 对应同一个 invite_code_id 就不算
    # 简化处理：直接根据 visitor_id 去重

    # 检查是否已经记录过
    existing = db.query(ShareVisitor).filter(
        ShareVisitor.share_id == share_id,
        ShareVisitor.visitor_id == visitor_id,
    ).first()

    if not existing:
        db.add(ShareVisitor(share_id=share_id, visitor_id=visitor_id))
        db.commit()

    # 统计独立访客数
    unique_count = db.query(func.count(ShareVisitor.id)).filter(
        ShareVisitor.share_id == share_id
    ).scalar() or 0

    # 检查是否已有奖励
    reward = db.query(ShareReward).filter(ShareReward.share_id == share_id).first()
    reward_code = None

    if unique_count >= REQUIRED_VISITORS and not reward:
        # 生成奖励邀请码
        code = generate_code()
        while db.query(InviteCode).filter(InviteCode.code == code).first():
            code = generate_code()
        new_invite = InviteCode(code=code)
        db.add(new_invite)
        db.flush()

        reward = ShareReward(share_id=share_id, reward_code_id=new_invite.id)
        db.add(reward)
        db.commit()
        reward_code = code
    elif reward and reward.reward_code_id:
        invite = db.query(InviteCode).filter(InviteCode.id == reward.reward_code_id).first()
        if invite:
            reward_code = invite.code

    # 检查奖励码是否已被使用
    reward_code_used = False
    if reward and reward.reward_code_id:
        invite = db.query(InviteCode).filter(InviteCode.id == reward.reward_code_id).first()
        if invite and invite.is_used:
            reward_code_used = True

    return {
        "visitor_count": min(unique_count, REQUIRED_VISITORS),
        "required": REQUIRED_VISITORS,
        "completed": unique_count >= REQUIRED_VISITORS,
        "reward_code": reward_code,
        "reward_code_used": reward_code_used,
    }


@router.get("/{share_id}/progress")
def get_progress(
    share_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """获取分享进度（不记录访问）"""
    result = db.query(UserResult).filter(UserResult.share_id == share_id).first()
    if not result:
        return {"error": "分享链接无效"}

    unique_count = db.query(func.count(ShareVisitor.id)).filter(
        ShareVisitor.share_id == share_id
    ).scalar() or 0

    reward = db.query(ShareReward).filter(ShareReward.share_id == share_id).first()
    reward_code = None
    reward_code_used = False
    if reward and reward.reward_code_id:
        invite = db.query(InviteCode).filter(InviteCode.id == reward.reward_code_id).first()
        if invite:
            reward_code = invite.code
            reward_code_used = invite.is_used

    return {
        "visitor_count": min(unique_count, REQUIRED_VISITORS),
        "required": REQUIRED_VISITORS,
        "completed": unique_count >= REQUIRED_VISITORS,
        "reward_code": reward_code,
        "reward_code_used": reward_code_used,
    }
