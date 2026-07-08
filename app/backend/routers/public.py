from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import PublicNews, PublicServiceCard


router = APIRouter()


@router.get("/news")
def list_public_news(db: Session = Depends(get_db)):
    rows = db.scalars(select(PublicNews).order_by(PublicNews.pinned.desc(), PublicNews.published_at.desc())).all()
    return [
        {
            "id": item.id,
            "title": item.title,
            "news_status": item.news_status,
            "importance": item.importance,
            "pinned": item.pinned,
            "published_at": item.published_at,
        }
        for item in rows
    ]


@router.get("/service-cards")
def list_service_cards(db: Session = Depends(get_db)):
    rows = db.scalars(select(PublicServiceCard).order_by(PublicServiceCard.sort_order)).all()
    return [
        {
            "id": item.id,
            "title": item.title,
            "card_status": item.card_status,
            "service_type": item.service_type,
            "action_label": item.action_label,
        }
        for item in rows
    ]
