from sqlalchemy.orm import Session
from sqlalchemy import func, Float
from app.entities.book_entity import Book
from fastapi import HTTPException
from typing import List, Dict


def get_overview_stats(db: Session) -> Dict:
    try:
        total_books = db.query(func.count(Book.id)).scalar()
        avg_price = db.query(func.avg(func.cast(Book.price, Float))).scalar()
        rating_distribution = db.query(Book.rating, func.count(Book.id)).group_by(Book.rating).all()

        return {
            "total_books": total_books,
            "average_price": round(avg_price, 2) if avg_price else 0.0,
            "rating_distribution": {r[0]: r[1] for r in rating_distribution}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating general statistics: {str(e)}")


def get_category_stats(db: Session) -> List[Dict]:
    try:
        results = db.query(
            Book.category,
            func.count(Book.id),
            func.avg(func.cast(Book.price, Float))
        ).group_by(Book.category).all()

        return [
            {
                "category": row[0],
                "total_books": row[1],
                "average_price": round(row[2], 2) if row[2] else 0.0
            }
            for row in results
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics by category: {str(e)}")
