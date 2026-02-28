import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Question
from app.schemas import QuestionResponse, QuestionOption

router = APIRouter(prefix="/api", tags=["questions"])


@router.get("/questions", response_model=list[QuestionResponse])
def get_questions(
    belief_system: str = Query(default="all", description="bazi / tarot / none / all"),
    db: Session = Depends(get_db),
):
    questions = db.query(Question).order_by(Question.order_num).all()

    # 过滤题目：belief_system 为 "all" 时返回全部，否则返回匹配任意一个所选体系的题目
    if belief_system != "all":
        selected_systems = set(belief_system.split(","))
        questions = [
            q for q in questions
            if q.belief_systems == "all" or selected_systems & set(q.belief_systems.split(","))
        ]

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
