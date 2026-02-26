import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserResult, City
from app.schemas import (
    MatchResultResponse, CityResponse, RunnerUp,
    FullReport, ElementAnalysis, ZodiacAnalysis, TarotReading,
    WuxingAnalysis, EnergyReading, DimensionItem, CareerAdvice,
)
from app.services.matching import generate_full_report

router = APIRouter(prefix="/api/result", tags=["result"])


def _build_report(city: City, score: float, user_vector: list[float] | None) -> FullReport | None:
    """根据城市和用户向量生成完整报告"""
    if user_vector is None:
        return None
    report_data = generate_full_report(city, score, user_vector)
    return FullReport(
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


@router.get("/{share_id}", response_model=MatchResultResponse)
def get_result(share_id: str, db: Session = Depends(get_db)):
    result = db.query(UserResult).filter(UserResult.share_id == share_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="未找到测试结果")

    city = db.query(City).filter(City.id == result.matched_city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="城市数据异常")

    city_resp = CityResponse(
        id=city.id,
        name=city.name,
        country=city.country,
        description=city.description,
        element=city.element,
        zodiac=city.zodiac,
        tarot=city.tarot,
        energy_type=city.energy_type,
        wuxing=city.wuxing,
        vibe=city.vibe,
    )

    # Parse user vector for report generation
    user_vector = None
    if result.user_vector:
        try:
            user_vector = json.loads(result.user_vector)
        except (json.JSONDecodeError, TypeError):
            pass

    report = _build_report(city, result.match_score, user_vector)

    runner_ups_data = json.loads(result.runner_ups)
    runner_up_responses = []
    for ru in runner_ups_data:
        ru_city = db.query(City).filter(City.id == ru["city_id"]).first()
        if ru_city:
            runner_up_responses.append(
                RunnerUp(
                    city=CityResponse(
                        id=ru_city.id, name=ru_city.name,
                        country=ru_city.country, description=ru_city.description,
                        element=ru_city.element, zodiac=ru_city.zodiac,
                        tarot=ru_city.tarot, energy_type=ru_city.energy_type,
                        wuxing=ru_city.wuxing, vibe=ru_city.vibe,
                    ),
                    score=ru["score"],
                )
            )

    return MatchResultResponse(
        city=city_resp,
        score=result.match_score,
        interpretation=result.interpretation,
        report=report,
        runner_ups=runner_up_responses,
        share_id=result.share_id,
    )
