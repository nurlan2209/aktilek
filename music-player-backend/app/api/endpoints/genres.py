from fastapi import APIRouter
from typing import List, Dict

from app.db.models.track import Genre

router = APIRouter()

@router.get("/", response_model=List[Dict[str, str]])
def get_all_genres():
    """
    Get all available music genres
    """
    return [{"value": genre.value, "name": genre.value} for genre in Genre]