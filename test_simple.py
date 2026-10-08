import sys
sys.path.append('.')

from app import app, db
from models import Users, RoleRequest, MyRoles

with app.app_context():
    # Создаём тестового пользователя если нет
    test_user = Users.query.filter_by(username='test_user_lr6').first()
    if not test_user:
        test_user = Users(
            username='test_user_lr6',
            password='test123',
            role=MyRoles.client_basic
        )
        db.session.add(test_user)
        db.session.commit()
        print('Создан тестовый пользователь')
    
    # Пробуем запрос
    try:
        request = RoleRequest(
            user_id=test_user.id,
            requested_role=MyRoles.trainer_basic,
            reason='Тестовая заявка'
        )
        db.session.add(request)
        db.session.commit()
        print(f'✅ УСПЕХ! Создан запрос ID: {request.id}')
        print(f'   Роль: {request.requested_role}')
        print(f'   Статус: {request.status}')
        
        # Проверяем, что можно прочитать
        saved_request = RoleRequest.query.get(request.id)
        print(f'✅ Прочитано из БД: {saved_request.requested_role}')
        
        # Удаляем тестовые данные
        db.session.delete(request)
        db.session.delete(test_user)
        db.session.commit()
        print('✅ Тестовые данные удалены')
        
    except Exception as e:
        db.session.rollback()
        print(f'❌ Ошибка: {e}')
        import traceback
        traceback.print_exc()