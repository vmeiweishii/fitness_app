"""
test_roles.py - Тестирование ролевой модели
"""

from app import app, db
from models import Users, MyRoles
from flask_login import login_user
from database import db_manager

def test_all_roles():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ РОЛЕВОЙ МОДЕЛИ")
    print("=" * 60)
    
    with app.app_context():
        # Создаем тестовых пользователей если их нет
        test_users = [
            ('test_client_basic', 'test123', MyRoles.client_basic),
            ('test_client_advanced', 'test123', MyRoles.client_advanced),
            ('test_trainer_basic', 'test123', MyRoles.trainer_basic),
            ('test_trainer_advanced', 'test123', MyRoles.trainer_advanced),
            ('test_admin', 'test123', MyRoles.admin),
        ]
        
        for username, password, role in test_users:
            if not Users.query.filter_by(username=username).first():
                user = Users(
                    username=username,
                    password=password,
                    role=role
                )
                db.session.add(user)
        
        db.session.commit()
        print("✓ Тестовые пользователи созданы")
        
        # Тестируем доступ к таблицам для каждой роли
        print("\n" + "=" * 60)
        print("ДОСТУПНЫЕ ТАБЛИЦЫ ДЛЯ КАЖДОЙ РОЛИ:")
        print("=" * 60)
        
        for role_name in ['client_basic', 'client_advanced', 'trainer_basic', 'trainer_advanced', 'admin']:
            tables = db_manager.get_available_tables(role_name)
            print(f"\n{role_name.upper():20} ({len(tables)} таблиц):")
            for table in tables:
                print(f"  - {table}")

if __name__ == "__main__":
    test_all_roles()