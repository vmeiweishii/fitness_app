"""
models.py - Модели SQLAlchemy для базы данных Фитнес-центра
SQLAlchemy 2.0.43 + Python 3.13.1
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, Date, Time, Boolean, Numeric, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import enum

# Базовый класс для моделей SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# ========== РОЛИ ПОЛЬЗОВАТЕЛЕЙ (из ЛР3) ==========
class MyRoles(enum.Enum):
    client_basic = "client_basic"
    client_advanced = "client_advanced"
    trainer_basic = "trainer_basic"
    trainer_advanced = "trainer_advanced"
    admin = "admin"

# ========== ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ ВЕБ-ИНТЕРФЕЙСА ==========
class Users(UserMixin, db.Model):
    __tablename__ = 'web_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.Enum(MyRoles))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ========== ОСНОВНЫЕ ТАБЛИЦЫ (из ЛР2) ==========
class Клиент(db.Model):
    """Сущность 'Клиент' из ЛР1"""
    __tablename__ = 'Клиент'
    
    Код_клиента = db.Column(db.Integer, primary_key=True)
    Фамилия = db.Column(db.String(50), nullable=False)
    Имя = db.Column(db.String(50), nullable=False)
    Телефон = db.Column(db.String(20))
    email = db.Column(db.String(100))
    Дата_рождения = db.Column(db.Date)
    Дата_регистрации = db.Column(db.Date)

class Абонемент(db.Model):
    """Сущность 'Абонемент' из ЛР1"""
    __tablename__ = 'Абонемент'
    
    Код_абонемента = db.Column(db.Integer, primary_key=True)
    Код_клиента = db.Column(db.Integer, db.ForeignKey('Клиент.Код_клиента'), nullable=False)
    Дата_начала = db.Column(db.Date, nullable=False)
    Дата_окончания = db.Column(db.Date, nullable=False)
    Статус = db.Column(db.String(20), nullable=False)
    Тип_абонемента = db.Column(db.String(50), nullable=False)
    
    # Связи
    клиент = db.relationship('Клиент', backref='абонементы')

class Тренер(db.Model):
    """Сущность 'Тренер' из ЛР1"""
    __tablename__ = 'Тренер'
    
    Код_тренера = db.Column(db.Integer, primary_key=True)
    Фамилия = db.Column(db.String(50), nullable=False)
    Имя = db.Column(db.String(50), nullable=False)
    Телефон = db.Column(db.String(20))
    Специализация = db.Column(db.String(100))

class Групповое_занятие(db.Model):
    """Сущность 'Групповое_занятие' из ЛР1"""
    __tablename__ = 'Групповое_занятие'
    
    Код_занятия = db.Column(db.Integer, primary_key=True)
    Название_занятия = db.Column(db.String(100), nullable=False)
    Описание = db.Column(db.Text)
    Уровень_сложности = db.Column(db.String(30))
    Макс_участников = db.Column(db.Integer)

class Зал(db.Model):
    """Сущность 'Зал' из ЛР1"""
    __tablename__ = 'Зал'
    
    Код_зала = db.Column(db.Integer, primary_key=True)
    Название_зала = db.Column(db.String(100), nullable=False)
    Вместимость = db.Column(db.Integer)
    Оснащение = db.Column(db.Text)

class Расписание(db.Model):
    """Сущность 'Расписание' из ЛР1"""
    __tablename__ = 'Расписание'
    
    Код_расписания = db.Column(db.Integer, primary_key=True)
    Код_тренера = db.Column(db.Integer, db.ForeignKey('Тренер.Код_тренера'), nullable=False)
    Код_занятия = db.Column(db.Integer, db.ForeignKey('Групповое_занятие.Код_занятия'), nullable=False)
    Код_зала = db.Column(db.Integer, db.ForeignKey('Зал.Код_зала'), nullable=False)
    Дата_занятия = db.Column(db.Date, nullable=False)
    Время_начала = db.Column(db.Time, nullable=False)
    Время_окончания = db.Column(db.Time, nullable=False)
    
    # Связи
    тренер = db.relationship('Тренер', backref='расписания')
    занятие = db.relationship('Групповое_занятие', backref='расписания')
    зал = db.relationship('Зал', backref='расписания')

class Бронь(db.Model):
    """Сущность 'Бронь' из ЛР1"""
    __tablename__ = 'Бронь'
    
    Код_брони = db.Column(db.Integer, primary_key=True)
    Код_клиента = db.Column(db.Integer, db.ForeignKey('Клиент.Код_клиента'), nullable=False)
    Код_расписания = db.Column(db.Integer, db.ForeignKey('Расписание.Код_расписания'), nullable=False)
    Дата_брони = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    Статус = db.Column(db.String(20), nullable=False)
    
    # Связи
    клиент = db.relationship('Клиент', backref='брони')
    расписание = db.relationship('Расписание', backref='брони')

class Персональная_тренировка(db.Model):
    """Сущность 'Персональная_тренировка' из ЛР1"""
    __tablename__ = 'Персональная_тренировка'
    
    Код_тренировки = db.Column(db.Integer, primary_key=True)
    Код_клиента = db.Column(db.Integer, db.ForeignKey('Клиент.Код_клиента'), nullable=False)
    Код_тренера = db.Column(db.Integer, db.ForeignKey('Тренер.Код_тренера'), nullable=False)
    Тип_тренировки = db.Column(db.String(100))
    Продолжительность = db.Column(db.Integer)
    
    # Связи
    клиент = db.relationship('Клиент', backref='персональные_тренировки')
    тренер = db.relationship('Тренер', backref='персональные_тренировки')

# ========== ПРЕДСТАВЛЕНИЯ (из ЛР2) ==========
# Для представлений используем простые модели без связей
class Мои_брони_и_абонемент(db.Model):
    """Представление 'Мои_брони_и_абонемент' из ЛР2"""
    __tablename__ = 'Мои_брони_и_абонемент'
    
    Фамилия = db.Column(db.String(50), primary_key=True)
    Имя = db.Column(db.String(50), primary_key=True)
    Тип_абонемента = db.Column(db.String(50))
    Статус_абонемента = db.Column(db.String(20))
    Дата_брони = db.Column(db.TIMESTAMP)
    Статус_брони = db.Column(db.String(20))
    Название_занятия = db.Column(db.String(100))
    Дата_занятия = db.Column(db.Date)
    Время_начала = db.Column(db.Time)

class Доступные_групповые_занятия(db.Model):
    """Представление 'Доступные_групповые_занятия' из ЛР2"""
    __tablename__ = 'Доступные_групповые_занятия'
    
    Название_занятия = db.Column(db.String(100), primary_key=True)
    Уровень_сложности = db.Column(db.String(30))
    Фамилия = db.Column(db.String(50))
    Имя = db.Column(db.String(50))
    Дата_занятия = db.Column(db.Date)
    Время_начала = db.Column(db.Time)
    Время_окончания = db.Column(db.Time)
    Название_зала = db.Column(db.String(100))
    Специализация = db.Column(db.String(100))

class Расписание_тренеров(db.Model):
    """Представление 'Расписание_тренеров' из ЛР2"""
    __tablename__ = 'Расписание_тренеров'
    __table_args__ = {'info': {'is_view': True}}  # Указываем, что это представление
    
    Фамилия = db.Column(db.String(50))
    Имя = db.Column(db.String(50))
    Название_занятия = db.Column(db.String(100))
    Дата_занятия = db.Column(db.Date)
    Время_начала = db.Column(db.Time)
    Время_окончания = db.Column(db.Time)
    Название_зала = db.Column(db.String(100))
    Количество_записей = db.Column(db.Integer)
    
    # Для представлений без явного первичного ключа используем autoload
    # или создаем составной первичный ключ из существующих полей
    __mapper_args__ = {
        'primary_key': [Фамилия, Имя, Дата_занятия, Время_начала]
    }

class Персональные_тренировки_обзор(db.Model):
    """Представление 'Персональные_тренировки_обзор' из ЛР2"""
    __tablename__ = 'Персональные_тренировки_обзор'
    __table_args__ = {'info': {'is_view': True}}
    
    Фамилия_тренера = db.Column(db.String(50))
    Имя_тренера = db.Column(db.String(50))
    Фамилия_клиента = db.Column(db.String(50))
    Имя_клиента = db.Column(db.String(50))
    Тип_тренировки = db.Column(db.String(100))
    Продолжительность = db.Column(db.Integer)
    Телефон = db.Column(db.String(20))
    
    __mapper_args__ = {
        'primary_key': [Фамилия_тренера, Имя_тренера, Фамилия_клиента, Имя_клиента]
    }

class Отчет_по_бронированиям(db.Model):
    """Представление 'Отчет_по_бронированиям' из ЛР2"""
    __tablename__ = 'Отчет_по_бронированиям'
    __table_args__ = {'info': {'is_view': True}}
    
    Фамилия = db.Column(db.String(50))
    Имя = db.Column(db.String(50))
    Название_занятия = db.Column(db.String(100))
    Дата_брони = db.Column(db.TIMESTAMP)
    Статус = db.Column(db.String(20))
    Фамилия_тренера = db.Column(db.String(50))
    Имя_тренера = db.Column(db.String(50))
    Дата_занятия = db.Column(db.Date)
    
    __mapper_args__ = {
        'primary_key': [Фамилия, Имя, Дата_брони, Название_занятия]
    }

class Загрузка_залов(db.Model):
    """Представление 'Загрузка_залов' из ЛР2"""
    __tablename__ = 'Загрузка_залов'
    __table_args__ = {'info': {'is_view': True}}
    
    Название_зала = db.Column(db.String(100))
    Вместимость = db.Column(db.Integer)
    Дата_занятия = db.Column(db.Date)
    Название_занятия = db.Column(db.String(100))
    Количество_участников = db.Column(db.Integer)
    Фамилия = db.Column(db.String(50))
    Имя = db.Column(db.String(50))
    
    __mapper_args__ = {
        'primary_key': [Название_зала, Дата_занятия, Название_занятия]
    }

# ========== СИСТЕМА ЗАПРОСОВ НА РОЛИ ==========
class RoleRequest(db.Model):
    """Запросы пользователей на получение расширенных ролей"""
    __tablename__ = 'role_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('web_users.id'), nullable=False)
    requested_role = db.Column(db.Enum(MyRoles), nullable=False)  # Используем тот же Enum!
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('web_users.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reason = db.Column(db.Text, nullable=True)
    admin_comment = db.Column(db.Text, nullable=True)
    
    # Связи
    user = db.relationship('Users', foreign_keys=[user_id], backref='role_requests')
    reviewer = db.relationship('Users', foreign_keys=[reviewed_by])

# ========== СИСТЕМНЫЕ ТАБЛИЦЫ (из ЛР3) ==========
class MainLog(db.Model):
    """Лог-таблица из ЛР3"""
    __tablename__ = 'main_log'
    
    log_item_id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(1))
    operation_date = db.Column(db.DateTime)
    user_operator = db.Column(db.String(100))
    table_name = db.Column(db.String(50))
    changed_data = db.Column(db.JSON)

class SecretData(db.Model):
    """Таблица с зашифрованными данными из ЛР3"""
    __tablename__ = 'secret_data'
    
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    secret_token = db.Column(db.Text)
    access_level = db.Column(db.Text)