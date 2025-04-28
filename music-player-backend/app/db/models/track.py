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
            
        normalized = string_value.lower().replace(' ', '').replace('-', '')
        
        for genre in cls:
            if genre.name.lower() == normalized or genre.value.lower().replace(' ', '').replace('-', '') == normalized:
                return genre
                
        # If no match found, try to match by name without considering case or separators
        for genre in cls:
            if normalized in genre.name.lower() or normalized in genre.value.lower().replace(' ', '').replace('-', ''):
                return genre
                
        raise ValueError(f"Unknown genre: {string_value}")

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