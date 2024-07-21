# Прогноз погоды

Использовались Django и Django Rest Framework.

* Вывод прогноза погоды в удобном виде
* Написаны тесты
* Всё помещено в Docker контейнер
* Сделано API, показывающее сколько раз вводили город

#### Вывод погоды на ближайший час:

![img.png](media/images/img.png)

#### Введён неверный город:

![img_1.png](media/images/img_1.png)

#### API, показывающее сколько раз вводили город:

![img_2.png](media/images/img_2.png)

### Установка с помощью Docker

Создайте файл ```.env``` и скопируйте туда содержимое из ```.env.example```.

```bash
SECRET_KEY=secret
DEBUG_MODE=True
DATABASE_URL=postgres://username:password@localhost:5432/db_name
DATABASE_URL_DOCKER=postgres://postgres:postgres@db:5432/postgres
```

Выполните команду:

```bash
docker-compose up -d --build
```

Запустите миграции:

```bash
docker-compose exec web python manage.py migrate
```

Создайте суперюзера:

```bash
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: `http://localhost:8000/`<br>
API, показывающее сколько раз вводили город: `http://localhost:8000/api/statistics/`

Чтобы посмотреть вывод логов:

```bash
 docker-compose logs -f 'web'
```

Чтобы запустить тесты:

```bash
docker-compose exec web python manage.py test
```

Чтобы остановить все контейнеры:

```bash
docker-compose down
```

### Установка

Сначала установите Postgres и запустите его.

Создайте файл ```.env``` и скопируйте туда содержимое из ```.env.example```. Измените username, password и dbname для
DATABASE_URl на те, которые используются в вашем локальном Postgres.

```bash
SECRET_KEY=secret
DEBUG_MODE=True
DATABASE_URL=postgres://username:password@localhost:5432/dbname
DATABASE_URL_DOCKER=postgres://postgres:postgres@db:5432/postgres
```

Установите зависимости проекта с помощью pip и активируйте виртуальную среду:

```bash
python -m venv .venv 
```
```bash
.venv\Scripts\Activate.ps1 
```
```bash
pip install -r requirements.txt
```

После этого примените миграции, создайте суперюзера и запустите сервер:

```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver  
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000/`<br>
API, показывающее сколько раз вводили город: `http://127.0.0.1:8000/api/statistics/`








