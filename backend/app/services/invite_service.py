import secrets
import string
import datetime
from sqlalchemy.orm import Session
from app.models import InviteCode, UserResult


def generate_code() -> str:
    """生成12位区分大小写的邀请码"""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(12))


def create_invite_codes(db: Session, count: int) -> list[str]:
    codes = []
    for _ in range(count):
        code = generate_code()
        while db.query(InviteCode).filter(InviteCode.code == code).first():
            code = generate_code()
        invite = InviteCode(code=code)
        db.add(invite)
        codes.append(code)
    db.commit()
    return codes


def verify_and_use_code(db: Session, code: str) -> tuple[bool, str, int | None, str | None]:
    """
    验证邀请码（区分大小写）。
    返回: (valid, message, invite_id, share_id_or_none)
    - 未使用的码：标记为已用，返回 valid=True, share_id=None
    - 已使用的码：返回 valid=True, share_id=对应的结果share_id（用于查看报告）
    - 不存在的码：返回 valid=False
    """
    invite = db.query(InviteCode).filter(InviteCode.code == code).first()
    if not invite:
        return False, "邀请码不存在", None, None

    if invite.is_used:
        # 已使用的邀请码 -> 查找对应的测试结果
        result = db.query(UserResult).filter(UserResult.invite_code_id == invite.id).first()
        if result:
            return True, "该邀请码已完成测试，正在跳转到报告页面", invite.id, result.share_id
        return True, "继续未完成的测试", invite.id, None

    invite.is_used = True
    invite.used_at = datetime.datetime.utcnow()
    invite.used_by = f"user_{invite.id}"
    db.commit()
    return True, "验证成功", invite.id, None
