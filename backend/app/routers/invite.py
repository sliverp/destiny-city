import secrets
import base64
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import InviteVerifyRequest, InviteVerifyResponse
from app.services.invite_service import verify_and_use_code

router = APIRouter(prefix="/api/invite", tags=["invite"])


@router.post("/verify", response_model=InviteVerifyResponse)
def verify_invite(req: InviteVerifyRequest, db: Session = Depends(get_db)):
    code = req.code.strip().upper()
    valid, message, invite_id = verify_and_use_code(db, code)
    if not valid:
        return InviteVerifyResponse(valid=False, message=message)

    # Create a simple token encoding the invite_id
    token_data = json.dumps({"invite_id": invite_id})
    token = base64.urlsafe_b64encode(token_data.encode()).decode()
    return InviteVerifyResponse(valid=True, token=token, message=message)
