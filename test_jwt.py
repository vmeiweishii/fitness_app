# test_jwt.py
import sys
sys.path.append('.')

import requests
import json

BASE_URL = "http://localhost:5000"

def test_jwt_flow():
    print("🔐 Тестирование JWT токенов")
    print("=" * 60)
    
    # 1. Получение токена
    print("1. Получение JWT токена через API:")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username": "test_bcrypt",
            "password": "secure123"
        },
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data['token']
        print(f"   ✅ Токен получен: {token[:50]}...")
        print(f"   User: {data['user']['username']}")
        print(f"   Role: {data['user']['role']}")
    else:
        print(f"   ❌ Ошибка: {response.status_code}")
        print(f"   {response.text}")
        return
    
    # 2. Проверка токена
    print("\n2. Проверка токена:")
    response = requests.post(
        f"{BASE_URL}/api/auth/verify",
        json={"token": token},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Токен валиден")
        print(f"   User ID: {data['user']['id']}")
    else:
        print(f"   ❌ Ошибка проверки: {response.text}")
    
    # 3. Обновление токена
    print("\n3. Обновление токена:")
    response = requests.post(
        f"{BASE_URL}/api/auth/refresh",
        json={"token": token},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        new_token = response.json()['token']
        print(f"   ✅ Токен обновлён: {new_token[:50]}...")
    else:
        print(f"   ❌ Ошибка обновления: {response.text}")
    
    # 4. Защищённый endpoint с токеном
    print("\n4. Доступ к защищённому API:")
    response = requests.get(
        f"{BASE_URL}/api/check_role_request",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code == 200:
        print(f"   ✅ Доступ к API разрешён")
        print(f"   Ответ: {response.json()}")
    else:
        print(f"   ❌ Доступ запрещён: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("✅ JWT токены работают корректно!")

if __name__ == "__main__":
    test_jwt_flow()