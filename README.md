# Service Manager - Система управління сервісним центром

Це комплексна система управління сервісним центром, побудована на **Django** та **Django REST Framework (DRF)** з підтримкою Docker.

## Функціональність

### 🔧 Управління сервісними замовленнями
- Створення та відстеження ремонтних замовлень
- Управління клієнтами та їх пристроями
- Каталог запчастин та послуг
- Система статусів замовлень

### 👥 Аутентифікація та авторизація
- Реєстрація та вхід користувачів
- JWT токени для API
- Різні рівні доступу

### 📊 Логування та моніторинг
- Детальне логування всіх дій
- Система звітності
- Аудит змін

### 🌐 REST API
- Повноцінний REST API з Swagger документацією
- CRUD операції для всіх сутностей
- JWT аутентифікація

## Технологічний стек

### Backend
- **Python 3.11**
- **Django 5.2** - веб-фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - база даних
- **JWT** - аутентифікація

### Frontend
- **HTML/CSS/JavaScript**
- **Bootstrap** - UI фреймворк
- **Django Templates**

### DevOps
- **Docker** - контейнеризація
- **Docker Compose** - оркестрація
- **Nginx** - веб-сервер
- **Gunicorn** - WSGI сервер

## Швидкий старт

### З Docker (рекомендовано)

1. **Клонування репозиторію:**
   ```bash
   git clone <repo-url>
   cd service_manager
   ```

2. **Запуск з Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Створення суперкористувача:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Відкрити в браузері:**
   - Основна сторінка: http://localhost
   - API документація: http://localhost/swagger/
   - Admin панель: http://localhost/admin/

### Локальна розробка

1. **Клонування репозиторію:**
   ```bash
   git clone <repo-url>
   cd service_manager
   ```

2. **Створення віртуального середовища:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # або
   venv\Scripts\activate     # Windows
   ```

3. **Встановлення залежностей:**
   ```bash
   pip install -r requirments.txt
   ```

4. **Налаштування бази даних:**
   - Встановіть PostgreSQL
   - Створіть базу даних `computer_service`
   - Налаштуйте змінні середовища в `.env` файлі

5. **Застосування міграцій:**
   ```bash
   python manage.py migrate
   ```

6. **Створення суперкористувача:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Запуск сервера розробки:**
   ```bash
   python manage.py runserver
   ```

## Структура проекту

```
service_manager/
├── service_manager/          # Основний проект Django
│   ├── settings.py          # Налаштування проекту
│   ├── urls.py              # Головні URL маршрути
│   └── management/          # Management команди
├── authenticate/            # Додаток аутентифікації
│   ├── models/             # Моделі користувачів
│   ├── views.py            # Представлення
│   └── templates/          # Шаблони
├── service/                # Основний додаток сервісу
│   ├── models/             # Моделі даних
│   ├── views.py            # Представлення
│   ├── api_views.py        # API представлення
│   └── templates/          # Шаблони
├── logs/                   # Додаток логування
│   ├── models.py           # Моделі логів
│   └── views.py            # Представлення логів
├── Dockerfile              # Docker образ
├── docker-compose.yml      # Docker Compose конфігурація
└── nginx.conf              # Nginx конфігурація
```

## API Endpoints

### Аутентифікація
- `POST /api/token/` - Отримання JWT токена
- `POST /api/token/refresh/` - Оновлення токена
- `POST /api/token/verify/` - Верифікація токена

### Клієнти
- `GET /service/clients/` - Список клієнтів
- `POST /service/clients/` - Створення клієнта
- `GET /service/clients/{id}/` - Деталі клієнта
- `PUT /service/clients/{id}/` - Оновлення клієнта
- `DELETE /service/clients/{id}/` - Видалення клієнта

### Пристрої
- `GET /service/devices/` - Список пристроїв
- `POST /service/devices/` - Створення пристрою
- `GET /service/devices/{id}/` - Деталі пристрою
- `PUT /service/devices/{id}/` - Оновлення пристрою
- `DELETE /service/devices/{id}/` - Видалення пристрою

### Замовлення
- `GET /service/repair-orders/` - Список замовлень
- `POST /service/repair-orders/` - Створення замовлення
- `GET /service/repair-orders/{id}/` - Деталі замовлення
- `PUT /service/repair-orders/{id}/` - Оновлення замовлення
- `DELETE /service/repair-orders/{id}/` - Видалення замовлення

## Змінні середовища

Створіть файл `.env` в корені проекту:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=computer_service
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Static Files
STATIC_URL=static/
STATIC_ROOT=staticfiles

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=debug.log
```

## Розробка

### Запуск тестів
```bash
python manage.py test
```

### Створення міграцій
```bash
python manage.py makemigrations
```

### Застосування міграцій
```bash
python manage.py migrate
```

### Збірка статичних файлів
```bash
python manage.py collectstatic
```

## Docker команди

### Розробка
```bash
# Запуск тільки бази даних
docker-compose up db

# Запуск всіх сервісів
docker-compose up --build

# Запуск у фоновому режимі
docker-compose up -d
```

### Управління
```bash
# Перегляд логів
docker-compose logs

# Зупинка сервісів
docker-compose down

# Перезапуск
docker-compose restart
```

## Ліцензія

Цей проект створений для навчальних цілей.

## Автор

Розроблено як pet project для вивчення Django, DRF та Docker.