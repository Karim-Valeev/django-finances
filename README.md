# finances

1. `python3 -m venv env` - инициализация виртуального окружения
2. `source env/bin/activate` - вход в виртуальное окружение
3. `pip install -r requirements.txt` - установка зависимостей
3,5. Если Бд через докер: `docker-compose up`
4. `python src/manage.py migrate` - запуск миграций
5. `python src/manage.py loaddata note_type_fixture.yaml` - загрузка фикстуры
6. `python src/manage.py runserver` - запуск приложения
7. `python src/manage.py createsuperuser` - создание суперпользователя


