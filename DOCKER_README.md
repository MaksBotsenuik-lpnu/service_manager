# Service Manager - Docker Setup

Цей проект налаштований для роботи з Docker та Docker Compose.

## Структура Docker файлів

- `Dockerfile` - Docker образ для Django додатку
- `docker-compose.yml` - Оркестрація сервісів (Django, PostgreSQL, Nginx)
- `nginx.conf` - Конфігурація Nginx
- `.dockerignore` - Файли, які ігноруються при Docker build
- `init.sql` - Ініціалізація бази даних

## Запуск проекту

### 1. Збірка та запуск всіх сервісів
```bash
docker-compose up --build
```

### 2. Запуск у фоновому режимі
```bash
docker-compose up -d --build
```

### 3. Зупинка сервісів
```bash
docker-compose down
```

### 4. Перегляд логів
```bash
# Всі сервіси
docker-compose logs

# Конкретний сервіс
docker-compose logs web
docker-compose logs db
docker-compose logs nginx
```

## Доступні сервіси

- **Django додаток**: http://localhost:8000
- **Nginx (основний доступ)**: http://localhost:80
- **PostgreSQL**: localhost:5432
- **Django Admin**: http://localhost/admin/
- **Swagger API**: http://localhost/swagger/

## База даних

PostgreSQL база даних автоматично створюється з наступними параметрами:
- **База даних**: computer_service
- **Користувач**: postgres
- **Пароль**: qweasdzxc123
- **Хост**: db (внутрішній Docker мережі)
- **Порт**: 5432

## Створення суперкористувача

Після запуску контейнерів, створіть суперкористувача:

```bash
docker-compose exec web python manage.py createsuperuser
```

## Міграції

Міграції виконуються автоматично при запуску контейнера. Якщо потрібно виконати міграції вручну:

```bash
docker-compose exec web python manage.py migrate
```

## Збірка статичних файлів

Статичні файли збираються автоматично. Для ручного збору:

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## Розробка

Для розробки можна використовувати тільки базу даних:

```bash
# Запустити тільки PostgreSQL
docker-compose up db

# Запустити Django локально з підключенням до Docker бази
python manage.py runserver
```

## Перемінні середовища

Основні змінні середовища налаштовані в `docker-compose.yml`:

- `DEBUG=False` - Режим продакшн
- `DB_HOST=db` - Хост бази даних (Docker контейнер)
- `SECRET_KEY` - Секретний ключ Django
- `ALLOWED_HOSTS` - Дозволені хости

## Troubleshooting

### Проблеми з підключенням до бази даних
```bash
# Перевірка статусу бази даних
docker-compose exec db pg_isready -U postgres

# Підключення до бази даних
docker-compose exec db psql -U postgres -d computer_service
```

### Перезапуск сервісів
```bash
# Перезапуск конкретного сервісу
docker-compose restart web

# Перезапуск всіх сервісів
docker-compose restart
```

### Очищення Docker
```bash
# Видалення контейнерів та мереж
docker-compose down

# Видалення контейнерів, мереж та volumes
docker-compose down -v

# Видалення всіх невикористовуваних ресурсів
docker system prune -a
``` 