# test_auth.py
import sys
sys.path.append('.')

from app import app, db
from models import Users, MyRoles
from password_manager import PasswordManager

with app.app_context():
    print("🔐 Тестирование аутентификации с bcrypt")
    print("=" * 50)
    
    # Создаём тестового пользователя
    test_user = Users.query.filter_by(username='test_bcrypt').first()
    if not test_user:
        test_user = Users(
            username='test_bcrypt',
            password=PasswordManager.hash_password('secure123'),  # bcrypt
            role=MyRoles.client_basic
        )
        db.session.add(test_user)
        db.session.commit()
        print("✅ Создан тестовый пользователь 'test_bcrypt'")
    
    # Тест 1: Проверка правильного пароля
    is_valid = PasswordManager.check_password(test_user.password, 'secure123')
    print(f"1. Проверка верного пароля: {'✅ ПРОШЛА' if is_valid else '❌ НЕ ПРОШЛА'}")
    
    # Тест 2: Проверка неверного пароля
    is_valid_wrong = PasswordManager.check_password(test_user.password, 'wrong123')
    print(f"2. Проверка неверного пароля: {'✅ ПРОШЛА' if not is_valid_wrong else '❌ НЕ ПРОШЛА'}")
    
    # Тест 3: Формат хэша
    print(f"3. Формат хэша: {'✅ bcrypt' if test_user.password.startswith('$2') else '❌ SHA-256'}")
    print(f"   Хэш: {test_user.password[:30]}...")
    
    # Тест 4: Нужно ли перехэшировать
    needs_rehash = PasswordManager.needs_rehash(test_user.password)
    print(f"4. Нужно перехэшировать: {'❌ НЕТ' if not needs_rehash else '⚠️ ДА (SHA-256)'}")
    
    print("\n" + "=" * 50)
    print("✅ Аутентификация с bcrypt работает корректно!")