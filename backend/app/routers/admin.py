import os
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import InviteCode
from app.schemas import GenerateCodesRequest, InviteCodeResponse
from app.services.invite_service import create_invite_codes

router = APIRouter(prefix="/api/admin", tags=["admin"])

ADMIN_KEY = os.environ.get("ADMIN_KEY", "destiny-admin-2024")


def verify_admin(x_admin_key: str = Header(...)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="管理员密钥错误")
    return True


@router.post("/invite-codes")
def generate_codes(
    req: GenerateCodesRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    if req.count < 1 or req.count > 100:
        raise HTTPException(status_code=400, detail="数量需在 1-100 之间")
    codes = create_invite_codes(db, req.count)
    return {"codes": codes}


@router.get("/invite-codes", response_model=list[InviteCodeResponse])
def list_codes(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    invites = db.query(InviteCode).order_by(InviteCode.id.desc()).all()
    return [
        InviteCodeResponse(
            id=inv.id,
            code=inv.code,
            is_used=inv.is_used,
            used_by=inv.used_by,
            created_at=inv.created_at.isoformat() if inv.created_at else "",
            used_at=inv.used_at.isoformat() if inv.used_at else None,
        )
        for inv in invites
    ]
