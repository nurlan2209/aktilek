1. Установить 11 вервию пайтона

## Cоздать базу данных в бд tuneviewer



https://www.python.org/downloads/release/python-3110/

## Запуск бэкенда

# Перейти в директорию бэкенда
```bash
cd music-player-backend
```

# Создать виртуальное окружение ( !!! НЕ 13 версия пайтона )
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

# Установить зависимости
```bash
pip install -r requirements.txt
```

# Настроить базу данных и выполнить миграции

# 1
```bash
alembic stamp head
```

# 2
```bash
alembic revision --autogenerate -m "Initial migration"
```

# 3
```bash
alembic upgrade head
```

# Запустить FastAPI сервер
```bash
uvicorn app.main:app --reload
```


## для получения роли администратора можно запустить файл python setrole.py
```bash
python setrole.py
```
## Он автоматически изменить роль на адмиситратора пользователя под id = 1

## Запуск фронтенда:
# Перейти в директорию фронтенда
```bash
cd music-player
```

# Установить зависимости
```bash
npm install
```

# Запустить сервер разработки
```bash
npm run dev
```