import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    element = Column(String(20), nullable=False)
    zodiac = Column(String(20), nullable=False)
    tarot = Column(String(50), nullable=False)
    energy_type = Column(String(50), nullable=False)
    wuxing = Column(String(10), nullable=False)
    vibe = Column(String(200), nullable=False)
    attributes = Column(Text, nullable=False)  # JSON: list of 10 floats


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    order_num = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    options = Column(Text, nullable=False)  # JSON: list of {id, content, weights}


class InviteCode(Base):
    __tablename__ = "invite_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(8), unique=True, nullable=False, index=True)
    is_used = Column(Boolean, default=False, nullable=False)
    used_by = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    used_at = Column(DateTime, nullable=True)


class UserResult(Base):
    __tablename__ = "user_results"

    id = Column(Integer, primary_key=True, index=True)
    share_id = Column(String(36), unique=True, nullable=False, index=True)
    invite_code_id = Column(Integer, nullable=False)
    answers = Column(Text, nullable=False)  # JSON
    matched_city_id = Column(Integer, nullable=False)
    match_score = Column(Float, nullable=False)
    interpretation = Column(Text, nullable=False)
    user_vector = Column(Text, nullable=True)  # JSON: list of 10 floats
    runner_ups = Column(Text, nullable=False)  # JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
