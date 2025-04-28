from sqlalchemy import Column, String, Float, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base, BaseModel
import enum

class Genre(str, enum.Enum):
    # Имена enum должны соответствовать значениям в базе данных
    POP = "Pop"
    HIPHOP = "Hip-Hop"
    AMBIENT = "Ambient"
    INDIE = "Indie"
    LOFI = "Lo-Fi"
    
    @classmethod
    def from_string(cls, string_value):
        """Convert string to Genre enum"""
        if string_value is None:
            return None
        
        # Попытка прямого совпадения
        for genre in cls:
            if genre.value == string_value:
                return genre
        
        # Попытка совпадения без учета регистра
        lower_value = string_value.lower()
        for genre in cls:
            if genre.value.lower() == lower_value:
                return genre
                
        # Попытка совпадения части строки
        for genre in cls:
            if lower_value in genre.value.lower() or genre.value.lower() in lower_value:
                return genre
                
        # Если не найдено совпадений, вывести информацию о допустимых значениях
        valid_values = [g.value for g in cls]
        raise ValueError(f"Неизвестный жанр: {string_value}. Допустимые значения: {', '.join(valid_values)}")

class Track(Base, BaseModel):
    __tablename__ = "tracks"

    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    genre = Column(Enum(Genre), nullable=False)
    duration = Column(Float, nullable=False)
    cover_path = Column(String, nullable=False)
    audio_path = Column(String, nullable=False)

    playlists = relationship("PlaylistTrack", back_populates="track")
    favorites = relationship("Favorite", back_populates="track", cascade="all, delete-orphan")
    dislikes = relationship("Dislike", back_populates="track", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="track", cascade="all, delete-orphan")