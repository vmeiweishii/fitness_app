from app import app, db
from models import Users, RoleRequest, MyRoles

with app.app_context():
    user = Users.query.first()
    if user:
        print(f"Тестируем с пользователем: {user.username}")
        
        # Пробуем создать запрос с Enum
        request = RoleRequest(
            user_id=user.id,
            requested_role=MyRoles.trainer_basic,  # Используем Enum!
            reason='Тест Enum'
        )
        
        try:
            db.session.add(request)
            db.session.commit()
            print(f"✅ Запрос создан с Enum!")
            print(f"   ID: {request.id}")
            print(f"   Роль (значение): {request.requested_role.value}")
            print(f"   Роль (Enum): {request.requested_role}")
            
            # Удалим тестовую запись
            db.session.delete(request)
            db.session.commit()
            print("✅ Тестовая запись удалена")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка с Enum: {e}")