import os
import shutil
from typing import Any, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.config import settings
from app.core.auth import get_current_user, get_current_admin_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.track import Track, Genre
from app.db.models.favorite import Favorite
from app.db.models.dislike import Dislike
from app.db.models.review import Review
from app.schemas.track import Track as TrackSchema, TrackCreate, TrackUpdate, TrackWithStats, TrackList

router = APIRouter()

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate file extension"""
    extension = filename.split(".")[-1].lower()
    return extension in allowed_extensions

@router.get("/", response_model=TrackList)
def get_tracks(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
    genre: Optional[str] = None,
    artist: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> Any:
    # Делаем этот эндпоинт общедоступным (не требуя авторизации)
    query = db.query(Track)

    if genre:
        try:
            # Try to convert string to Genre enum
            genre_enum = Genre.from_string(genre)
            query = query.filter(Track.genre == genre_enum)
        except (KeyError, ValueError) as e:
            # Log the error
            print(f"Invalid genre filter: {e}")
            # Return empty result instead of crashing
            return {
                "items": [],
                "total": 0,
                "page": page,
                "size": size,
                "pages": 0
            }

    if artist:
        query = query.filter(Track.artist.ilike(f"%{artist}%"))

    if search:
        query = query.filter(
            (Track.title.ilike(f"%{search}%")) |
            (Track.artist.ilike(f"%{search}%"))
        )

    # Get total count for pagination
    total = query.count()

    # Apply pagination
    tracks = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": tracks,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

@router.get("/{track_id}", response_model=TrackWithStats)
def get_track(
    *,
    db: Session = Depends(get_db),
    track_id: int,
    current_user: Optional[User] = Depends(get_current_user),
) -> Any:
    # Делаем этот эндпоинт общедоступным (не требуя авторизации)
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    favorites_count = db.query(func.count(Favorite.id)).filter(Favorite.track_id == track_id).scalar()
    dislikes_count = db.query(func.count(Dislike.id)).filter(Dislike.track_id == track_id).scalar()
    reviews_count = db.query(func.count(Review.id)).filter(Review.track_id == track_id).scalar()

    is_favorited = None
    is_disliked = None
    if current_user:
        is_favorited = db.query(Favorite).filter(
            Favorite.user_id == current_user.id,
            Favorite.track_id == track_id
        ).first() is not None

        is_disliked = db.query(Dislike).filter(
            Dislike.user_id == current_user.id,
            Dislike.track_id == track_id
        ).first() is not None

    result = TrackWithStats(
        id=track.id,
        title=track.title,
        artist=track.artist,
        genre=track.genre,
        duration=track.duration,
        cover_path=track.cover_path,
        audio_path=track.audio_path,
        favorites_count=favorites_count,
        dislikes_count=dislikes_count,
        reviews_count=reviews_count,
        is_favorited=is_favorited,
        is_disliked=is_disliked
    )

    return result

@router.post("/", response_model=TrackSchema)
def create_track(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    title: str = Form(...),
    artist: str = Form(...),
    genre: str = Form(...),
    duration: float = Form(...),
    cover: UploadFile = File(...),
    audio: UploadFile = File(...),
) -> Any:

    if not validate_file_extension(cover.filename, settings.ALLOWED_COVER_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid cover file format. Allowed formats: {', '.join(settings.ALLOWED_COVER_EXTENSIONS)}"
        )

    if not validate_file_extension(audio.filename, settings.ALLOWED_TRACK_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid audio file format. Allowed formats: {', '.join(settings.ALLOWED_TRACK_EXTENSIONS)}"
        )

    try:
        # Используем новый метод для преобразования строки в жанр
        track_genre = Genre.from_string(genre)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid genre. Allowed genres: {', '.join([g.value for g in Genre])}"
        )

    cover_filename = f"{uuid.uuid4()}.{cover.filename.split('.')[-1].lower()}"
    audio_filename = f"{uuid.uuid4()}.{audio.filename.split('.')[-1].lower()}"

    cover_path = os.path.join(settings.COVERS_DIR, cover_filename)
    audio_path = os.path.join(settings.TRACKS_DIR, audio_filename)

    try:
        cover_full_path = os.path.join(settings.MEDIA_ROOT, cover_path)
        with open(cover_full_path, "wb") as buffer:
            shutil.copyfileobj(cover.file, buffer)

        audio_full_path = os.path.join(settings.MEDIA_ROOT, audio_path)
        with open(audio_full_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
    except Exception as e:
        if os.path.exists(cover_full_path):
            os.remove(cover_full_path)
        if os.path.exists(audio_full_path):
            os.remove(audio_full_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving files: {str(e)}"
        )

    track = Track(
        title=title,
        artist=artist,
        genre=track_genre,
        duration=duration,
        cover_path=f"/media/{cover_path}",
        audio_path=f"/media/{audio_path}"
    )

    db.add(track)
    db.commit()
    db.refresh(track)

    return track