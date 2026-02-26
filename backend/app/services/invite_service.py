import secrets
import string
import datetime
from sqlalchemy.orm import Session
from app.models import InviteCode


def generate_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(8))


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


def verify_and_use_code(db: Session, code: str) -> tuple[bool, str, int | None]:
    invite = db.query(InviteCode).filter(InviteCode.code == code).first()
    if not invite:
        return False, "邀请码不存在", None
    if invite.is_used:
        return False, "该邀请码已被使用", None
    invite.is_used = True
    invite.used_at = datetime.datetime.utcnow()
    invite.used_by = f"user_{invite.id}"
    db.commit()
    return True, "验证成功", invite.id
