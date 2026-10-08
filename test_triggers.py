"""
test_triggers.py - Проверка системы логирования из ЛР3
"""

from app import app, db
from models import MainLog, Клиент, Абонемент
import sys

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓{Colors.END} {Colors.BOLD}{message}{Colors.END}")

def print_header(title):
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{title:^60}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

def test_logging():
    print_header("ПРОВЕРКА СИСТЕМЫ ЛОГИРОВАНИЯ (из ЛР3)")
    
    with app.app_context():
        # Проверяем существование таблицы логов
        initial_log_count = MainLog.query.count()
        print(f"Начальное количество записей в логе: {initial_log_count}")
        
        if initial_log_count > 0:
            print_success("Таблица логов существует и содержит данные")
            # Показываем последние записи
            recent_logs = MainLog.query.order_by(
                MainLog.operation_date.desc()
            ).limit(3).all()
            
            print(f"\n{Colors.BOLD}Последние 3 записи в логе:{Colors.END}")
            print(f"{'Дата':<25} {'Тип':<5} {'Таблица':<20} {'Пользователь':<15}")
            print("-" * 70)
            for log in recent_logs:
                date_str = log.operation_date.strftime('%Y-%m-%d %H:%M:%S') if log.operation_date else "N/A"
                print(f"{date_str:<25} {log.operation_type:<5} {log.table_name:<20} {log.user_operator:<15}")
        else:
            print(f"{Colors.YELLOW}⚠ Таблица логов пуста{Colors.END}")
        
        # Тест 1: INSERT - должен создать запись в логе
        print_header("ТЕСТ 1: INSERT ОПЕРАЦИЯ")
        print("Создаем тестового клиента...")
        
        try:
            # Запоминаем количество записей до операции
            logs_before = MainLog.query.count()
            
            # Создаем тестового клиента
            test_client = Клиент(
                Фамилия="ЛогТест",
                Имя="Иван",
                Телефон="+79001112233",
                email="logtest@example.com",
                Дата_рождения="1985-03-15"
            )
            
            db.session.add(test_client)
            db.session.commit()
            client_id = test_client.Код_клиента
            
            # Проверяем лог после операции
            logs_after = MainLog.query.count()
            
            if logs_after > logs_before:
                print_success("INSERT операция залогирована!")
                print(f"   Записей до: {logs_before}")
                print(f"   Записей после: {logs_after}")
                print(f"   Добавлено: {logs_after - logs_before} записей")
                
                # Показываем новую запись в логе
                new_log = MainLog.query.order_by(
                    MainLog.operation_date.desc()
                ).first()
                
                if new_log and new_log.operation_type == 'I':
                    print_success(f"   Тип операции: INSERT (ожидаемо)")
                    print_success(f"   Таблица: {new_log.table_name} (ожидаемо: Клиент)")
                    print(f"   Время: {new_log.operation_date}")
                else:
                    print(f"{Colors.RED}✗ Неправильный тип операции в логе{Colors.END}")
            else:
                print(f"{Colors.RED}✗ Операция не попала в лог!{Colors.END}")
            
        except Exception as e:
            db.session.rollback()
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        # Тест 2: UPDATE - должен создать запись в логе
        print_header("ТЕСТ 2: UPDATE ОПЕРАЦИЯ")
        print("Обновляем телефон тестового клиента...")
        
        try:
            if 'test_client' in locals():
                logs_before = MainLog.query.count()
                
                # Обновляем данные
                test_client.Телефон = "+79009998877"
                db.session.commit()
                
                logs_after = MainLog.query.count()
                
                if logs_after > logs_before:
                    print_success("UPDATE операция залогирована!")
                    print(f"   Добавлено: {logs_after - logs_before} записей")
                    
                    # Проверяем последнюю запись
                    last_log = MainLog.query.order_by(
                        MainLog.operation_date.desc()
                    ).first()
                    
                    if last_log and last_log.operation_type == 'U':
                        print_success(f"   Тип операции: UPDATE (ожидаемо)")
                    else:
                        print(f"{Colors.YELLOW}⚠ Неправильный тип операции{Colors.END}")
                else:
                    print(f"{Colors.RED}✗ UPDATE не залогирован!{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠ Тестовый клиент не создан, пропускаем UPDATE тест{Colors.END}")
                
        except Exception as e:
            db.session.rollback()
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        # Тест 3: DELETE - должен создать запись в логе
        print_header("ТЕСТ 3: DELETE ОПЕРАЦИЯ")
        print("Удаляем тестового клиента...")
        
        try:
            if 'test_client' in locals() and test_client:
                logs_before = MainLog.query.count()
                
                # Удаляем клиента
                db.session.delete(test_client)
                db.session.commit()
                
                logs_after = MainLog.query.count()
                
                if logs_after > logs_before:
                    print_success("DELETE операция залогирована!")
                    print(f"   Добавлено: {logs_after - logs_before} записей")
                    
                    last_log = MainLog.query.order_by(
                        MainLog.operation_date.desc()
                    ).first()
                    
                    if last_log and last_log.operation_type == 'D':
                        print_success(f"   Тип операции: DELETE (ожидаемо)")
                    else:
                        print(f"{Colors.YELLOW}⚠ Неправильный тип операции{Colors.END}")
                else:
                    print(f"{Colors.RED}✗ DELETE не залогирован!{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠ Тестовый клиент не существует, пропускаем DELETE тест{Colors.END}")
                
        except Exception as e:
            db.session.rollback()
            print(f"{Colors.RED}✗ Ошибка: {e}{Colors.END}")
        
        # Итоговая статистика
        print_header("ИТОГОВАЯ СТАТИСТИКА")
        
        final_log_count = MainLog.query.count()
        print(f"Всего записей в логе: {final_log_count}")
        
        if final_log_count > initial_log_count:
            added = final_log_count - initial_log_count
            print_success(f"Добавлено за тест: {added} записей")
            
            # Статистика по типам операций
            from sqlalchemy import func
            operation_stats = db.session.query(
                MainLog.operation_type,
                func.count(MainLog.log_item_id).label('count')
            ).group_by(MainLog.operation_type).all()
            
            print(f"\n{Colors.BOLD}Статистика по типам операций:{Colors.END}")
            print(f"{'Тип':<10} {'Количество':<10}")
            print("-" * 20)
            for op_type, count in operation_stats:
                op_name = {
                    'I': 'INSERT',
                    'U': 'UPDATE', 
                    'D': 'DELETE'
                }.get(op_type, op_type)
                print(f"{op_name:<10} {count:<10}")
        else:
            print(f"{Colors.RED}✗ За время теста не добавлено ни одной записи в лог!{Colors.END}")
        
        print_success("Тестирование системы логирования завершено!")

if __name__ == "__main__":
    # Включаем цветной вывод для Windows
    if sys.platform == "win32":
        import os
        os.system("color")
    
    test_logging()