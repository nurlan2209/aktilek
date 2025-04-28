from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


revision = 'aff5848d0586'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Создаем маппинг существующих значений к правильным значениям enum
    mappings = [
        ("pop", "Pop"),
        ("hip-hop", "Hip-Hop"),
        ("hiphop", "Hip-Hop"),
        ("ambient", "Ambient"),
        ("indie", "Indie"),
        ("lofi", "Lo-Fi"),
        ("lo-fi", "Lo-Fi"),
        # Добавь больше маппингов при необходимости
    ]
    
    # Выполняем SQL для обновления каждого значения
    conn = op.get_bind()
    for old_value, new_value in mappings:
        conn.execute(
            text(f"UPDATE tracks SET genre = :new_value WHERE LOWER(genre) = :old_value"),
            {"new_value": new_value, "old_value": old_value}
        )


def downgrade():
    # Нет пути отката для миграции данных
    pass