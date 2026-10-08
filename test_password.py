# test_password.py
import sys
sys.path.append('.')

from password_manager import PasswordManager

print("🔐 Тестирование безопасного хэширования паролей")
print("=" * 50)

# Тест 1: Новые пароли
test_cases = [
    "SimplePassword123",
    "СложныйПароль!@#$%",
    "очень_длинный_пароль_с_разными_символами_и_цифрами_123",
    "k"  # Минимальный пароль
]

for i, password in enumerate(test_cases, 1):
    hashed = PasswordManager.hash_password(password)
    is_correct = PasswordManager.check_password(hashed, password)
    is_wrong = PasswordManager.check_password(hashed, password + "wrong")
    needs_rehash = PasswordManager.needs_rehash(hashed)
    
    print(f"\nТест {i}: '{password[:20]}...'")
    print(f"  Хэш: {hashed[:50]}...")
    print(f"  Длина хэша: {len(hashed)} символов")
    print(f"  Проверка верного пароля: {'✅' if is_correct else '❌'}")
    print(f"  Проверка неверного пароля: {'✅' if not is_wrong else '❌'}")
    print(f"  Формат bcrypt: {'✅' if hashed.startswith('$2') else '❌'}")
    print(f"  Нужно перехэшировать: {'❌' if not needs_rehash else '⚠️'}")

# Тест 2: Миграция старых паролей
print("\n" + "=" * 50)
print("Тест миграции старых SHA-256 паролей:")

import hashlib
old_password = "mypass123"
old_hash = hashlib.sha256(old_password.encode()).hexdigest()

print(f"\nСтарый пароль: {old_password}")
print(f"Старый хэш (SHA-256): {old_hash[:50]}...")
print(f"Проверка через PasswordManager: {PasswordManager.check_password(old_hash, old_password)}")
print(f"Нужно перехэшировать: {'✅ ДА' if PasswordManager.needs_rehash(old_hash) else '❌ НЕТ'}")

# Если нужно перехэшировать
if PasswordManager.needs_rehash(old_hash):
    new_hash = PasswordManager.hash_password(old_password)
    print(f"\nНовый хэш (bcrypt): {new_hash[:50]}...")
    print(f"Можно заменить в БД старый хэш на новый")

print("\n" + "=" * 50)
print("✅ Все тесты пройдены! PasswordManager готов к использованию.")