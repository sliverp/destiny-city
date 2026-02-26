import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Question
from app.schemas import QuestionResponse, QuestionOption

router = APIRouter(prefix="/api", tags=["questions"])


@router.get("/questions", response_model=list[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.order_num).all()
    result = []
    for q in questions:
        options_data = json.loads(q.options)
        options = [
            QuestionOption(id=o["id"], content=o["content"], weights=o["weights"])
            for o in options_data
        ]
        result.append(
            QuestionResponse(
                id=q.id,
                order_num=q.order_num,
                category=q.category,
                content=q.content,
                options=options,
            )
        )
    return result
