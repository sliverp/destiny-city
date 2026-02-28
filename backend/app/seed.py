import json
import os
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import City, Question, ShareVisitor, ShareReward, TestProgress


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(City).count() == 0:
            seed_cities(db)
        if db.query(Question).count() == 0:
            seed_questions(db)
    finally:
        db.close()


def seed_cities(db: Session):
    seed_path = os.path.join(os.path.dirname(__file__), "seed_data", "cities.json")
    with open(seed_path, "r", encoding="utf-8") as f:
        cities_data = json.load(f)

    for city_data in cities_data:
        city = City(
            name=city_data["name"],
            country=city_data["country"],
            description=city_data["description"],
            element=city_data["element"],
            zodiac=city_data["zodiac"],
            tarot=city_data["tarot"],
            energy_type=city_data["energy_type"],
            wuxing=city_data["wuxing"],
            vibe=city_data["vibe"],
            attributes=json.dumps(city_data["attributes"]),
        )
        db.add(city)
    db.commit()


def seed_questions(db: Session):
    seed_path = os.path.join(os.path.dirname(__file__), "seed_data", "questions.json")
    with open(seed_path, "r", encoding="utf-8") as f:
        questions_data = json.load(f)

    for q_data in questions_data:
        question = Question(
            order_num=q_data["order_num"],
            category=q_data["category"],
            content=q_data["content"],
            options=json.dumps(q_data["options"], ensure_ascii=False),
            belief_systems=q_data.get("belief_systems", "all"),
        )
        db.add(question)
    db.commit()
