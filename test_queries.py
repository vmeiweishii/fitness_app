"""
test_queries.py - Примеры запросов для отчета
"""

from app import app, db
from models import Клиент, Абонемент, Тренер, Групповое_занятие, Бронь
from sqlalchemy import func
import sys

class Colors:
    """Класс для цветного вывода в терминал"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓{Colors.END} {Colors.BOLD}{message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def print_header(title):
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{title:^60}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

def demonstrate_queries():
    print_header("ДЕМОНСТРАЦИЯ ЗАПРОСОВ К БАЗЕ ДАННЫХ")
    
    with app.app_context():
        # 1. SELECT - выборка данных
        print_header("1. SELECT - ВЫБОРКА ДАННЫХ")
        print_info("Запрос: SELECT * FROM Клиент LIMIT 5")
        
        clients = Клиент.query.limit(5).all()
        if clients:
            print_success("Запрос выполнен успешно!")
            print(f"\n{'Фамилия':<15} {'Имя':<15} {'Телефон':<15} {'Email':<20}")
            print("-" * 65)
            for client in clients:
                print(f"{client.Фамилия:<15} {client.Имя:<15} {client.Телефон or '-':<15} {client.email or '-':<20}")
        else:
            print(f"{Colors.RED}✗ Нет данных{Colors.END}")
        
        # 2. INSERT - вставка данных
        print_header("2. INSERT - ВСТАВКА ДАННЫХ")
        print_info("Запрос: INSERT INTO Клиент (Фамилия, Имя, Телефон, email, Дата_рождения) VALUES (...)")
        
        try:
            new_client = Клиент(
                Фамилия="Тестовый",
                Имя="Клиент",
                Телефон="+79990000000",
                email="test_client@example.com",
                Дата_рождения="1995-05-15"
            )
            db.session.add(new_client)
            db.session.commit()
            print_success(f"Клиент создан успешно! ID: {new_client.Код_клиента}")
            print(f"   Имя: {new_client.Фамилия} {new_client.Имя}")
            print(f"   Контакты: {new_client.Телефон}, {new_client.email}")
        except Exception as e:
            db.session.rollback()
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        # 3. UPDATE - обновление данных
        print_header("3. UPDATE - ОБНОВЛЕНИЕ ДАННЫХ")
        print_info("Запрос: UPDATE Клиент SET Телефон = '+79991112233' WHERE Фамилия = 'Тестовый'")
        
        try:
            client = Клиент.query.filter_by(Фамилия="Тестовый").first()
            if client:
                old_phone = client.Телефон
                client.Телефон = "+79991112233"
                db.session.commit()
                print_success("Данные обновлены успешно!")
                print(f"   Старый телефон: {old_phone}")
                print(f"   Новый телефон: {client.Телефон}")
            else:
                print(f"{Colors.YELLOW}⚠ Клиент не найден{Colors.END}")
        except Exception as e:
            db.session.rollback()
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        # 4. DELETE - удаление данных
        print_header("4. DELETE - УДАЛЕНИЕ ДАННЫХ")
        print_info("Запрос: DELETE FROM Клиент WHERE Фамилия = 'Тестовый'")
        
        try:
            test_client = Клиент.query.filter_by(Фамилия="Тестовый").first()
            if test_client:
                client_name = f"{test_client.Фамилия} {test_client.Имя}"
                db.session.delete(test_client)
                db.session.commit()
                print_success(f"Клиент удален успешно!")
                print(f"   Удален: {client_name}")
            else:
                print(f"{Colors.YELLOW}⚠ Клиент не найден{Colors.END}")
        except Exception as e:
            db.session.rollback()
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        # 5. JOIN - сложные запросы
        print_header("5. JOIN - СЛОЖНЫЕ ЗАПРОСЫ")
        print_info("Запрос: SELECT * FROM Клиент JOIN Абонемент ON Клиент.Код_клиента = Абонемент.Код_клиента WHERE Абонемент.Статус = 'Активен'")
        
        try:
            clients_with_abonement = db.session.query(Клиент).join(Абонемент).filter(
                Абонемент.Статус == 'Активен'
            ).limit(3).all()
            
            if clients_with_abonement:
                print_success("Запрос выполнен успешно!")
                print(f"\n{'Фамилия':<15} {'Имя':<15} {'Тип абонемента':<20}")
                print("-" * 50)
                for client in clients_with_abonement:
                    # Находим абонемент клиента
                    abonement = Абонемент.query.filter_by(
                        Код_клиента=client.Код_клиента,
                        Статус='Активен'
                    ).first()
                    abonement_type = abonement.Тип_абонемента if abonement else "Неизвестно"
                    print(f"{client.Фамилия:<15} {client.Имя:<15} {abonement_type:<20}")
            else:
                print(f"{Colors.YELLOW}⚠ Нет клиентов с активными абонементами{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        # 6. Агрегатные функции
        print_header("6. АГРЕГАТНЫЕ ФУНКЦИИ - СТАТИСТИКА")
        print_info("Запросы: COUNT, GROUP BY")
        
        try:
            total_clients = Клиент.query.count()
            active_abonements = Абонемент.query.filter_by(Статус='Активен').count()
            trainers_count = Тренер.query.count()
            group_classes = Групповое_занятие.query.count()
            
            print_success("Статистика получена успешно!")
            print(f"\n{'Метрика':<25} {'Значение':<10}")
            print("-" * 35)
            print(f"{'Всего клиентов':<25} {total_clients:<10}")
            print(f"{'Активных абонементов':<25} {active_abonements:<10}")
            print(f"{'Тренеров':<25} {trainers_count:<10}")
            print(f"{'Групповых занятий':<25} {group_classes:<10}")
            
            # Дополнительная статистика
            print(f"\n{Colors.BOLD}Дополнительная статистика:{Colors.END}")
            
            # Типы абонементов
            from sqlalchemy import func
            abonement_types = db.session.query(
                Абонемент.Тип_абонемента,
                func.count(Абонемент.Код_абонемента).label('count')
            ).group_by(Абонемент.Тип_абонемента).all()
            
            print(f"\n{'Тип абонемента':<20} {'Количество':<10}")
            print("-" * 30)
            for type_name, count in abonement_types:
                print(f"{type_name:<20} {count:<10}")
                
        except Exception as e:
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        print_header("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")

if __name__ == "__main__":
    # Включаем цветной вывод для Windows
    if sys.platform == "win32":
        import os
        os.system("color")
    
    demonstrate_queries()