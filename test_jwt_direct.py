import sys
sys.path.append('.')

from app import app, db
from models import Users
from auth_tokens import AuthTokenManager
from password_manager import PasswordManager

with app.app_context():
    print("🔐 Тестирование JWT-логики")
    print("=" * 50)

    # 1. Найдите тестового пользователя
    test_user = Users.query.filter_by(username='test_bcrypt').first()
    if not test_user:
        print("❌ Пользователь 'test_bcrypt' не найден.")
        # Создадим временного для теста
        from models import MyRoles
        test_user = Users(
            username='jwt_test_user',
            password=PasswordManager.hash_password('test123'),
            role=MyRoles.client_basic
        )
        db.session.add(test_user)
        db.session.commit()
        print("✅ Создан временный пользователь для теста")
    
    print(f"Тестируем с пользователем: {test_user.username} (ID: {test_user.id})")

    # 2. Создайте токен
    token = AuthTokenManager.create_token(
        user_id=test_user.id,
        username=test_user.username,
        role=test_user.role.value
    )
    print(f"\n1. Токен создан: {token[:50]}...")
    
    # Проверка структуры
    parts = token.split('.')
    print(f"   Структура JWT: {len(parts)} части (ожидается 3): {'✅' if len(parts) == 3 else '❌'}")
    print(f"   Заголовок (header): {parts[0][:30]}...")
    print(f"   Данные (payload): {parts[1][:30]}...")
    print(f"   Подпись (signature): {parts[2][:10]}...")

    # 3. Проверьте токен
    print("\n2. Проверка токена:")
    payload = AuthTokenManager.verify_token(token)
    
    if payload:
        print("   ✅ Токен валиден!")
        print(f"   Данные в payload:")
        print(f"   - sub (subject): '{payload.get('sub')}' (тип: {type(payload.get('sub')).__name__})")
        print(f"   - username: {payload.get('username')}")
        print(f"   - role: {payload.get('role')}")
        print(f"   - exp (expires): {payload.get('exp')}")
        print(f"   - jti (JWT ID): {payload.get('jti')[:8]}...")
    else:
        print("   ❌ Токен невалиден")

    # 4. Проверьте извлечение ID
    print("\n3. Извлечение ID из токена:")
    user_id_from_token = AuthTokenManager.get_user_id_from_token(token)
    print(f"   Полученный ID: {user_id_from_token} (тип: {type(user_id_from_token).__name__})")
    print(f"   Ожидаемый ID: {test_user.id} (тип: {type(test_user.id).__name__})")
    print(f"   Совпадение: {'✅' if user_id_from_token == test_user.id else '❌'}")

    # 5. Тест обновления токена
    print("\n4. Обновление токена:")
    new_token = AuthTokenManager.refresh_token(token)
    if new_token:
        print(f"   ✅ Новый токен создан: {new_token[:50]}...")
        print(f"   Токены разные: {'✅' if token != new_token else '❌'}")
        
        # Проверка нового токена
        new_payload = AuthTokenManager.verify_token(new_token)
        print(f"   Новый токен валиден: {'✅' if new_payload else '❌'}")
        if new_payload:
            print(f"   JTI нового токена: {new_payload.get('jti')[:8]}...")
            print(f"   JTI старого токена: {payload.get('jti')[:8] if payload else 'N/A'}...")
            print(f"   JTI разные: {'✅' if new_payload.get('jti') != payload.get('jti') else '❌'}")
    else:
        print("   ❌ Не удалось обновить токен")

    print("\n" + "=" * 50)
    print("✅ Тестирование JWT завершено!")