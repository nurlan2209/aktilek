# fix_genres.py
from app.db.session import engine
from sqlalchemy.sql import text

def fix_genres():
    # Соединение с базой данных
    with engine.connect() as conn:
        # Создаем транзакцию
        with conn.begin():
            # Создаем маппинг существующих значений к правильным значениям enum
            mappings = [
                ("pop", "Pop"),
                ("hip-hop", "Hip-Hop"),
                ("hiphop", "Hip-Hop"),
                ("ambient", "Ambient"),
                ("indie", "Indie"),
                ("lofi", "Lo-Fi"),
                ("lo-fi", "Lo-Fi"),
            ]
            
            # Выполняем SQL для обновления каждого значения
            for old_value, new_value in mappings:
                print(f"Обновляем: {old_value} -> {new_value}")
                conn.execute(
                    text("UPDATE tracks SET genre = :new_value WHERE LOWER(genre) = :old_value"),
                    {"new_value": new_value, "old_value": old_value}
                )
        
    print("Обновление завершено!")

if __name__ == "__main__":
    fix_genres()