from pydantic import BaseModel
from typing import Optional


class InviteVerifyRequest(BaseModel):
    code: str


class InviteVerifyResponse(BaseModel):
    valid: bool
    token: str = ""
    message: str = ""
    share_id: str = ""  # 已用邀请码时返回对应的报告share_id


class SubmitAnswersRequest(BaseModel):
    answers: dict[int, str]


class GenerateCodesRequest(BaseModel):
    count: int = 10


class QuestionOption(BaseModel):
    id: str
    content: str
    weights: list[float]


class QuestionResponse(BaseModel):
    id: int
    order_num: int
    category: str
    content: str
    options: list[QuestionOption]


class CityResponse(BaseModel):
    id: int
    name: str
    country: str
    description: str
    element: str
    zodiac: str
    tarot: str
    energy_type: str
    wuxing: str
    vibe: str


class RunnerUp(BaseModel):
    city: CityResponse
    score: float


# ---- 结构化报告模型 ----

class ElementAnalysis(BaseModel):
    element: str
    title: str
    core: str
    strengths: str
    shadow: str
    city_connection: str


class ZodiacAnalysis(BaseModel):
    zodiac: str
    ruling_planet: str
    quality: str
    keyword: str
    analysis: str


class TarotReading(BaseModel):
    card: str
    number: str
    keyword: str
    upright: str
    analysis: str


class WuxingAnalysis(BaseModel):
    wuxing: str
    nature: str
    season: str
    direction: str
    personality: str
    city_match: str


class EnergyReading(BaseModel):
    type: str
    analysis: str


class DimensionItem(BaseModel):
    dimension: str
    label: str
    icon: str
    value: int
    desc: str


class CareerAdvice(BaseModel):
    summary: str
    tags: list[str]


class FullReport(BaseModel):
    destiny_summary: str
    element_analysis: ElementAnalysis
    zodiac_analysis: ZodiacAnalysis
    tarot_reading: TarotReading
    wuxing_analysis: WuxingAnalysis
    energy_reading: EnergyReading
    energy_profile: list[DimensionItem]
    top_dimensions: list[DimensionItem]
    career_advice: CareerAdvice
    city_description: str


class MatchResultResponse(BaseModel):
    city: CityResponse
    score: float
    interpretation: str
    report: Optional[FullReport] = None
    runner_ups: list[RunnerUp]
    share_id: str


class InviteCodeResponse(BaseModel):
    id: int
    code: str
    is_used: bool
    used_by: Optional[str]
    created_at: str
    used_at: Optional[str]
