import json
import uuid
import base64
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Question, UserResult
from app.schemas import (
    SubmitAnswersRequest, MatchResultResponse, CityResponse, RunnerUp,
    FullReport, ElementAnalysis, ZodiacAnalysis, TarotReading,
    WuxingAnalysis, EnergyReading, DimensionItem, CareerAdvice,
)
from app.services.matching import (
    calculate_user_vector, match_cities,
    generate_interpretation, generate_full_report,
)

router = APIRouter(prefix="/api/test", tags=["test"])


def decode_token(authorization: str = Header(...)) -> int:
    try:
        token = authorization.replace("Bearer ", "")
        data = json.loads(base64.urlsafe_b64decode(token))
        return data["invite_id"]
    except Exception:
        raise HTTPException(status_code=401, detail="无效的认证令牌")


@router.post("/submit", response_model=MatchResultResponse)
def submit_test(
    req: SubmitAnswersRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(...),
):
    invite_id = decode_token(authorization)

    # Check if already submitted
    existing = db.query(UserResult).filter(UserResult.invite_code_id == invite_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="该邀请码已完成测试")

    # Build questions map
    questions = db.query(Question).all()
    questions_map: dict[int, list] = {}
    for q in questions:
        options = json.loads(q.options)
        questions_map[q.id] = options

    # Calculate user vector and match
    user_vector = calculate_user_vector(req.answers, questions_map)
    ranked = match_cities(user_vector, db)

    if not ranked:
        raise HTTPException(status_code=500, detail="匹配失败")

    best_city, best_score = ranked[0]
    interpretation = generate_interpretation(best_city, best_score)

    # Generate full report
    report_data = generate_full_report(best_city, best_score, user_vector)

    runner_ups_data = [
        {"city_id": c.id, "score": s} for c, s in ranked[1:4]
    ]

    share_id = str(uuid.uuid4())[:8]

    result = UserResult(
        share_id=share_id,
        invite_code_id=invite_id,
        answers=json.dumps(req.answers),
        matched_city_id=best_city.id,
        match_score=best_score,
        interpretation=interpretation,
        user_vector=json.dumps(user_vector),
        runner_ups=json.dumps(runner_ups_data),
    )
    db.add(result)
    db.commit()

    city_resp = CityResponse(
        id=best_city.id,
        name=best_city.name,
        country=best_city.country,
        description=best_city.description,
        element=best_city.element,
        zodiac=best_city.zodiac,
        tarot=best_city.tarot,
        energy_type=best_city.energy_type,
        wuxing=best_city.wuxing,
        vibe=best_city.vibe,
    )

    runner_up_responses = []
    for c, s in ranked[1:4]:
        runner_up_responses.append(
            RunnerUp(
                city=CityResponse(
                    id=c.id, name=c.name, country=c.country,
                    description=c.description, element=c.element,
                    zodiac=c.zodiac, tarot=c.tarot,
                    energy_type=c.energy_type, wuxing=c.wuxing,
                    vibe=c.vibe,
                ),
                score=s,
            )
        )

    # Build report response
    report = FullReport(
        destiny_summary=report_data["destiny_summary"],
        element_analysis=ElementAnalysis(**report_data["element_analysis"]),
        zodiac_analysis=ZodiacAnalysis(**report_data["zodiac_analysis"]),
        tarot_reading=TarotReading(**report_data["tarot_reading"]),
        wuxing_analysis=WuxingAnalysis(**report_data["wuxing_analysis"]),
        energy_reading=EnergyReading(**report_data["energy_reading"]),
        energy_profile=[DimensionItem(**d) for d in report_data["energy_profile"]],
        top_dimensions=[DimensionItem(**d) for d in report_data["top_dimensions"]],
        career_advice=CareerAdvice(**report_data["career_advice"]),
        city_description=report_data["city_description"],
    )

    return MatchResultResponse(
        city=city_resp,
        score=best_score,
        interpretation=interpretation,
        report=report,
        runner_ups=runner_up_responses,
        share_id=share_id,
    )
