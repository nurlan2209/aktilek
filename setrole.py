import psycopg2

DATABASE_URL = "postgresql://postgres:0000@localhost:5432/tuneviewer"

def update_user_roles():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            # Приводим к типу userrole с учётом регистра
            cur.execute("SELECT id FROM users WHERE role = 'USER'::userrole")
            users = cur.fetchall()
            print(f"Найдено {len(users)} пользователей с ролью 'USER'.")

            if users:
                cur.execute("UPDATE users SET role = 'ADMIN'::userrole WHERE role = 'USER'::userrole")
                print("Роли обновлены на 'ADMIN'.")
            else:
                print("Нет пользователей с ролью 'USER'.")
    finally:
        conn.close()

if __name__ == "__main__":
    update_user_roles()
