"""
app.py - Основное Flask-приложение для Фитнес-центра
ЛР4: Веб-интерфейс для взаимодействия с БД
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import enum
from sqlalchemy import Enum
import pandas as pd
from datetime import datetime

# ========== НАСТРОЙКА ПРИЛОЖЕНИЯ ==========
app = Flask(__name__)
app.config['SECRET_KEY'] = 'FitnessMasterKey2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:31415@localhost/fitness_center'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ========== МОДЕЛИ ==========
class MyRoles(enum.Enum):
    client_basic = "client_basic"
    trainer_basic = "trainer_basic"
    admin = "admin"

class Users(UserMixin, db.Model):
    __tablename__ = 'web_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(Enum(MyRoles))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Основные таблицы БД
class Клиент(db.Model):
    __tablename__ = 'Клиент'
    Код_клиента = db.Column(db.Integer, primary_key=True)
    Фамилия = db.Column(db.String(50), nullable=False)
    Имя = db.Column(db.String(50), nullable=False)
    Телефон = db.Column(db.String(20))
    email = db.Column(db.String(100))
    Дата_рождения = db.Column(db.Date)
    Дата_регистрации = db.Column(db.Date)

class Тренер(db.Model):
    __tablename__ = 'Тренер'
    Код_тренера = db.Column(db.Integer, primary_key=True)
    Фамилия = db.Column(db.String(50), nullable=False)
    Имя = db.Column(db.String(50), nullable=False)
    Телефон = db.Column(db.String(20))
    Специализация = db.Column(db.String(100))

class Групповое_занятие(db.Model):
    __tablename__ = 'Групповое_занятие'
    Код_занятия = db.Column(db.Integer, primary_key=True)
    Название_занятия = db.Column(db.String(100), nullable=False)
    Описание = db.Column(db.Text)
    Уровень_сложности = db.Column(db.String(30))
    Макс_участников = db.Column(db.Integer)

class Зал(db.Model):
    __tablename__ = 'Зал'
    Код_зала = db.Column(db.Integer, primary_key=True)
    Название_зала = db.Column(db.String(100), nullable=False)
    Вместимость = db.Column(db.Integer)
    Оснащение = db.Column(db.Text)

class Расписание(db.Model):
    __tablename__ = 'Расписание'
    Код_расписания = db.Column(db.Integer, primary_key=True)
    Код_тренера = db.Column(db.Integer, db.ForeignKey('Тренер.Код_тренера'))
    Код_занятия = db.Column(db.Integer, db.ForeignKey('Групповое_занятие.Код_занятия'))
    Код_зала = db.Column(db.Integer, db.ForeignKey('Зал.Код_зала'))
    Дата_занятия = db.Column(db.Date, nullable=False)
    Время_начала = db.Column(db.Time, nullable=False)
    Время_окончания = db.Column(db.Time, nullable=False)

class Бронь(db.Model):
    __tablename__ = 'Бронь'
    Код_брони = db.Column(db.Integer, primary_key=True)
    Код_клиента = db.Column(db.Integer, db.ForeignKey('Клиент.Код_клиента'))
    Код_расписания = db.Column(db.Integer, db.ForeignKey('Расписание.Код_расписания'))
    Дата_брони = db.Column(db.DateTime, default=datetime.utcnow)
    Статус = db.Column(db.String(20), nullable=False)

# Представления
class Доступные_групповые_занятия(db.Model):
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
    __tablename__ = 'Расписание_тренеров'
    Фамилия = db.Column(db.String(50))
    Имя = db.Column(db.String(50))
    Название_занятия = db.Column(db.String(100))
    Дата_занятия = db.Column(db.Date)
    Время_начала = db.Column(db.Time)
    Время_окончания = db.Column(db.Time)
    Название_зала = db.Column(db.String(100))
    Количество_записей = db.Column(db.Integer)

class MainLog(db.Model):
    __tablename__ = 'main_log'
    log_item_id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(1))
    operation_date = db.Column(db.DateTime)
    user_operator = db.Column(db.String(100))
    table_name = db.Column(db.String(50))
    changed_data = db.Column(db.Text)

class SecretData(db.Model):
    __tablename__ = 'secret_data'
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    secret_token = db.Column(db.Text)
    access_level = db.Column(db.Text)

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def sql_to_html(query_result):
    """Преобразование результатов запроса в HTML таблицу"""
    if not query_result:
        return "<div class='alert alert-info'>Нет данных для отображения</div>"
    
    try:
        data = []
        for row in query_result:
            row_dict = {}
            for column in row.__table__.columns:
                value = getattr(row, column.name)
                
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                elif value is None:
                    value = ''
                    
                row_dict[column.name] = str(value)
            data.append(row_dict)
        
        df = pd.DataFrame(data)
        return df.to_html(
            classes='table table-striped table-bordered table-hover',
            index=False,
            escape=False,
            border=0
        )
    except Exception as e:
        return f"<div class='alert alert-danger'>Ошибка при обработке данных: {str(e)}</div>"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Распределение таблиц по ролям (соответствует правам из ЛР3)
roles_distribution = {
    "client_basic": ['Доступные_групповые_занятия'],
    "trainer_basic": ['Расписание_тренеров'],
    "admin": [
        'Клиент', 'Тренер', 'Групповое_занятие', 'Зал', 
        'Расписание', 'Бронь', 'main_log', 'secret_data',
        'Доступные_групповые_занятия', 'Расписание_тренеров'
    ]
}

table_mapping = {
    'Клиент': Клиент,
    'Тренер': Тренер,
    'Групповое_занятие': Групповое_занятие,
    'Зал': Зал,
    'Расписание': Расписание,
    'Бронь': Бронь,
    'main_log': MainLog,
    'secret_data': SecretData,
    'Доступные_групповые_занятия': Доступные_групповые_занятия,
    'Расписание_тренеров': Расписание_тренеров
}

table_names_ru = {
    'Клиент': 'Клиенты',
    'Тренер': 'Тренеры',
    'Групповое_занятие': 'Групповые занятия',
    'Зал': 'Залы',
    'Расписание': 'Расписание',
    'Бронь': 'Бронирования',
    'main_log': 'Логи операций',
    'secret_data': 'Секретные данные',
    'Доступные_групповые_занятия': 'Доступные групповые занятия',
    'Расписание_тренеров': 'Расписание тренеров'
}

# ========== МАРШРУТЫ ==========
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Заполните все поля!')
            return redirect(url_for('register'))
        
        existing = Users.query.filter_by(username=username).first()
        if existing:
            flash('Этот пользователь уже существует!')
            return redirect(url_for('register'))
        
        try:
            # Простое хранение пароля (для демо)
            user = Users(
                username=username,
                password=password,  # В реальном проекте нужно хэшировать!
                role=MyRoles.client_basic
            )
            
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна!')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при регистрации: {str(e)}')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        user = Users.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Простая проверка для демо
            login_user(user)
            flash(f'Добро пожаловать, {username}!')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный логин или пароль')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_role = current_user.role.value
    available_tables = roles_distribution.get(user_role, [])
    
    return render_template('dashboard.html',
                         user_role=user_role,
                         available_tables=available_tables,
                         username=current_user.username,
                         table_names_ru=table_names_ru)

@app.route('/table/<table_name>')
@login_required
def show_table(table_name):
    user_role = current_user.role.value
    available_tables = roles_distribution.get(user_role, [])
    
    if table_name not in available_tables:
        return render_template('error.html', 
                             message='Доступ запрещен',
                             error_code=403), 403
    
    model_class = table_mapping.get(table_name)
    if not model_class:
        return render_template('error.html',
                             message='Таблица не найдена',
                             error_code=404), 404
    
    try:
        data = model_class.query.limit(50).all()
        html_table = sql_to_html(data)
        
        table_name_ru = table_names_ru.get(table_name, table_name)
        
        return render_template('table_view.html',
                             table_name=table_name,
                             table_name_ru=table_name_ru,
                             table_html=html_table,
                             user_role=user_role,
                             username=current_user.username)
    except Exception as e:
        return render_template('error.html',
                             message=f'Ошибка при получении данных: {str(e)}',
                             error_code=500), 500

@app.route('/test_db')
def test_db():
    """Тестовая страница для проверки подключения к БД"""
    try:
        test_result = Клиент.query.first()
        users_count = Users.query.count()
        
        return f"""
        <h1>Тест подключения к БД</h1>
        <p>База данных: fitness_center</p>
        <p>Первый клиент: {test_result.Фамилия if test_result else 'Нет данных'}</p>
        <p>Зарегистрированных пользователей: {users_count}</p>
        <p><a href="/">На главную</a></p>
        """
    except Exception as e:
        return f"Ошибка подключения к БД: {str(e)}"

# ========== ЗАПУСК ПРИЛОЖЕНИЯ ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("=" * 60)
        print("Фитнес-центр: Веб-интерфейс запущен!")
        print("Доступно по адресу: http://localhost:5000")
        print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)