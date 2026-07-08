from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models import HelpArticle, HelpCategory


router = APIRouter()


@router.get("/categories")
def list_help_categories(db: Session = Depends(get_db)):
    rows = db.scalars(select(HelpCategory).order_by(HelpCategory.sort_order)).all()
    return [
        {
            "id": item.id,
            "slug": item.slug,
            "label": item.label,
            "category_status": item.category_status,
            "public_visible": item.public_visible,
        }
        for item in rows
    ]


@router.get("/articles")
def list_help_articles(db: Session = Depends(get_db)):
    rows = db.scalars(select(HelpArticle).order_by(HelpArticle.id)).all()
    return [
        {
            "id": item.id,
            "category_id": item.category_id,
            "title": item.title,
            "article_status": item.article_status,
            "audience": item.audience,
            "view_count": item.view_count,
        }
        for item in rows
    ]
