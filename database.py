"""
database.py - Подключение к PostgreSQL с разными ролями
"""

import psycopg

class DatabaseManager:
    def __init__(self):
        self.roles_distribution = {
            "client_basic": [
                'Доступные_групповые_занятия', 
                'Групповое_занятие',
                'Зал'
            ],
            "client_advanced": [
                'Мои_брони_и_абонемент',
                'Абонемент',
                'Бронь',
                'Доступные_групповые_занятия'
            ],
            "trainer_basic": [
                'Расписание_тренеров',
                'Групповое_занятие',
                'Зал'
            ],
            "trainer_advanced": [
                'Персональные_тренировки_обзор',
                'Клиент',
                'Расписание_тренеров'
            ],
            "admin": [
                'Клиент', 'Абонемент', 'Тренер', 'Групповое_занятие',
                'Зал', 'Расписание', 'Бронь', 'Персональная_тренировка',
                'main_log', 'secret_data', 'Мои_брони_и_абонемент',
                'Доступные_групповые_занятия'
            ]
        }
        
        self.role_to_db_user = {
            "client_basic": {
                "username": os.getenv("DB_USER_CLIENT_BASIC"),
                "password": os.getenv("DB_PASS_CLIENT_BASIC")
            },
            "client_advanced": {
                "username": os.getenv("DB_USER_CLIENT_ADVANCED"),
                "password": os.getenv("DB_PASS_CLIENT_ADVANCED")
            },
            "trainer_basic": {
                "username": os.getenv("DB_USER_TRAINER_BASIC"),
                "password": os.getenv("DB_PASS_TRAINER_BASIC")
            },
            "trainer_advanced": {
                "username": os.getenv("DB_USER_TRAINER_ADVANCED"),
                "password": os.getenv("DB_PASS_TRAINER_ADVANCED")
            },
            "admin": {
                "username": os.getenv("DB_USER_ADMIN"),
                "password": os.getenv("DB_PASS_ADMIN")
            }
        }

    def get_connection(self, role_name):
        if role_name not in self.role_to_db_user:
            return None
            
        user_info = self.role_to_db_user[role_name]
        
        try:
            return psycopg.connect(
                host='localhost',
                dbname='fitness_center',
                user=user_info['username'],
                password=user_info['password'],
                port=5432
            )
        except Exception as e:
            print(f"Ошибка подключения {role_name}: {e}")
            return None

    def execute_query(self, role_name, query, params=None):
        conn = self.get_connection(role_name)
        if not conn:
            return None, None, f"Не удалось подключиться как {role_name}"

        try:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc.name for desc in cursor.description] if cursor.description else []
                    data = cursor.fetchall()
                    return columns, data, None
                else:
                    conn.commit()
                    return None, cursor.rowcount, None
        except Exception as e:
            return None, None, str(e)
        finally:
            conn.close()

    def get_available_tables(self, role_name):
        return self.roles_distribution.get(role_name, [])

db_manager = DatabaseManager()