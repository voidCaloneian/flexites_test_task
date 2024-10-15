Структура README:
- [Начало работы с проектом (установка, зависмости, миграции, фикстуры и тесты)](#Начало)
- [API документация](#API)
- [Описание тестового задания](#Тестовое)

## Начало
### Клонирование
```bash
git clone https://github.com/voidCaloneian/flexites_test_task.git
cd flexites_test_task
```
### Создание виртуального окружения
```
python3 -m venv venv
```

### Активация виртуального окружения (для разных систем команды разные):
-  Для macOS/Linux:
```
source venv/bin/activate
```
- Для Windows:
```
venv\Scripts\activate
```

### Установка зависимостей из requirements.txt
```
pip install -r requirements.txt
```

### Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Генерация объектов моделей для ручного тестирования (curl, Postman)
```
python manage.py create_random_data
```

### Запуск автоматических тестов
```
python manage.py test --parallel -v 2
```

### Запуск сервера
```
python manage.py runserver
```

## API

Базовый URL: http://localhost:8000/api/
Аутентификация: JSON Web Tokens (JWT)
Формат данных: JSON
Контент Тип: application/json

### Создание Нового Пользователя (Регистрация)
- URL: /api/users/
- Метод: POST
- Описание: Позволяет зарегистрировать нового пользователя, создавая учетную запись с предоставленными данными.
- Разрешения: AllowAny (доступно всем, без аутентификации)
Параметры Запроса:
- email (строка, уникальное поле) - почта
- password (строка, минимум 8 символов) - пароль
- first_name (строка, максимум 30 символов) - имя
- last_name (строка, максимум 30 символов) - фамилия
- phone (строка, опционально, от 9 до 15 символов, в формате +9999999999) - номер телефона
- avatar (файл, опционально, Разрешены JPEG, PNG, GIF и WEBP, автоматическое кадрирование до 200 пикселей в ширину)
- organization_ids (список чисел, опционально) - ID организаций

Пример Body:
```json
{
    "email": "petr@gmail.com",
    "password": "SecurePassword123!",
    "first_name": "Петр",
    "last_name": "Петров",
    "phone": "+79876543210",
    "avatar": "<file (multipart/form-data)>",
    "organization_ids": [1, 2]
}
```

Пример Ответа:

```json
{
    "id": 1,
    "email": "petr@gmail.com",
    "first_name": "Петр",
    "last_name": "Петров",
    "phone": "+79876543210",
    "avatar": "http://localhost:8000/media/avatars/abcd1234.jpg",
    "organizations": [
        {
            "id": 5,
            "name": "Emex",
            "description": "Потянуться сохранять тюрьма изменение научить. Товар уронить ведь материя покинуть. Забирать дружно один вздрогнуть поймать увеличиваться рот налево."
        },
        {
            "id": 11,
            "name": "Копылова Инк",
            "description": "Банк заявление расстройство парень. Теория сынок провал холодно факультет. Освобождение деловой коммунизм ведь желание дружно привлекать сынок."
        }
    ]
}
```

Статус коды:
- 201 Created: Объект был успешно создан.
- 400 Bad Request: Неправильный запрос. Возвращается, если данные, переданные для создания пользователя, не прошли валидацию.
- 500 Internal Server Error: Внутренняя ошибка сервера. Возвращается, если возникла непредвиденная ошибка на стороне сервера при обработке запроса

### Авторизация Пользователя (Получение JWT Токенов)
- URL: /api/token/
- Метод: POST
- Описание: Позволяет аутентифицировать пользователя по email и паролю, возвращая JWT токены для дальнейшего использования.
- Разрешения: AllowAny (доступно всем, без аутентификации)
Параметры запроса:
- email (строка) - почта 
- password (строка) - пароль в незашифрованном виде

Пример Body:
```json
{
    "email": "user@example.com",
    "password": "SecurePassword123!"
}
```

Пример Ответа:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Статус коды:
- 200 OK: Успешный запрос. Возвращается, если учётные данные пользователя корректны, и в ответе содержатся два токена: access-токен и refresh-токен.
- 400 Bad Request: Неправильный запрос. Возвращается, если данные запроса некорректны, например, если не указаны обязательные поля (почта пользователя или пароль).
- 401 Unauthorized: Не указан JWT токен в заголовках.
- 500 Internal Server Error: Внутренняя ошибка сервера. Возвращается, если возникла непредвиденная ошибка на стороне сервера.

### Редактирование Своего Профиля (Изменение Данных в Профиле)
- URL: /api/users/{id}/
- Метод: PATCH или PUT
- Описание: Позволяет аутентифицированному пользователю обновить свои данные в профиле. Пользователь может изменять свои личные данные, а также связывать/разрывать связи с организациями.
- Разрешения: IsAuthenticated и IsStaffOrUserBySelf (пользователь может редактировать только свой профиль или нужно иметь токен администратора, чтобы редактировать любой профиль)
Заголовки запроса:
- Authorization: Bearer <JWT_TOKEN>
Параметры запроса (что хотим изменить, всё опционально):
- email (строка) - почта
- password (строка) - пароль
- first_name (строка, максимум 30 символов) - имя
- last_name (строка, максимум 30 символов) - фамилия
- phone (строка, от 9 до 15 символов, в формате +9999999999) - номер телефона
- avatar (файл, Разрешены JPEG, PNG, GIF и WEBP, автоматическое кадрирование до 200 пикселей в ширину)
- organization_ids (список чисел, опционально) - ID организаций

Тело Запроса:
```json
{
    "email": "newemail@example.com",         
    "password": "NewSecurePassword123!",    
    "first_name": "Петр",                    
    "last_name": "Петров",                   
    "phone": "+79876543210",                 
    "avatar": "<file (multipart/form-data)>",             
    "organization_ids": [2, 3]               
}
```

Пример Ответа:
```json
{
    "id": 1,
    "email": "newemail@example.com",
    "first_name": "Петр",
    "last_name": "Петров",
    "phone": "+79876543210",
    "avatar": "http://localhost:8000/media/avatars/efgh5678.jpg",
    "organizations": [
        {
            "id": 2,
            "name": "Emex",
            "description": "Потянуться сохранять тюрьма изменение научить. Товар уронить ведь материя покинуть. Забирать дружно один вздрогнуть поймать увеличиваться рот налево."
        },
        {
            "id": 3,
            "name": "Компания Адамас",
            "description": "Житель кидать указанный белье волк обида о. Спалить выкинуть вскинуть неправда. Смертельный ремень бетонный. Житель расстегнуть беспомощный процесс."
        }
    ]
}
```

Статус коды:
- 200 OK: Успешное обновление. Возвращается, если данные пользователя успешно обновлены.
- 400 Bad Request: Неправильный запрос. Возвращается, если данные не прошли валидацию, например, если были переданы некорректные поля.
- 401 Unauthorized: Не указан JWT токен в заголовках.
- 403 Forbidden: Доступ запрещён. Возвращается, если пользователь не имеет права изменять данные другого пользователя или недостаточно прав для выполнения запроса.
- 404 Not Found: Пользователь не найден. Возвращается, если объект пользователя с указанным ID не существует.
- 500 Internal Server Error: Внутренняя ошибка сервера. Возвращается, если возникла непредвиденная ошибка на стороне сервера.

### Вывод Списка Всех Пользователей и Связанных с Ними Организаций
- URL: /api/users/
- Метод: GET
- Описание: Позволяет администраторам получить список всех пользователей вместе с их организациями.
- Разрешения: IsAdminUser (доступно только администраторам)

Пример ответа:
```json
[
    {
        "id": 116,
        "email": "nikifstzxvaaagasqqgassdqwegd@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "",
        "avatar": null,
        "organizations": [
            {
                "id": 5,
                "name": "Emex",
                "description": "Потянуться сохранять тюрьма изменение научить. Товар уронить ведь материя покинуть. Забирать дружно один вздрогнуть поймать увеличиваться рот налево."
            },
            {
                "id": 11,
                "name": "Копылова Инк",
                "description": "Банк заявление расстройство парень. Теория сынок провал холодно факультет. Освобождение деловой коммунизм ведь желание дружно привлекать сынок."
            }
        ],
        "is_active": true,
        "is_staff": false,
        "date_joined": "2024-10-15T08:21:27.061233Z"
    },
    {
        "id": 115,
        "email": "artem1996@example.net",
        "first_name": "Евдокия",
        "last_name": "Федосеев",
        "phone": "81710839741",
        "avatar": null,
        "organizations": [],
        "is_active": true,
        "is_staff": false,
        "date_joined": "2024-10-15T08:19:00.000926Z"
    },
  {
    "id": 114,
    "email": "izmail_1982@example.net",
    "first_name": "Павел",
    "last_name": "Гущина",
    "phone": "+75928758206",
    "avatar": null,
    "organizations": [
      {
        "id": 14,
        "name": "Горбачев Групп",
        "description": "Возникновение остановить прошептать материя рабочий крутой. Господь одиннадцать висеть нервно боец. Спорт инструкция освобождение тусклый опасность."
      },
      {
        "id": 19,
        "name": "НПО «Кудрявцева Сазонов»",
        "description": "Карман означать чувство функция идея.\nМотоцикл песня рис вздрогнуть тревога запустить сверкающий. Пища поколение разнообразный академик обида белье нажать. Изменение число прежде указанный."
      },
      {
        "id": 21,
        "name": "ЗАО «Логинов, Баранов и Киселев»",
        "description": "Войти полюбить пастух изучить помолчать сверкать пол. Грудь дошлый результат пробовать при. Собеседник тяжелый единый смертельный некоторый похороны."
      }
    ],
    "is_active": true,
    "is_staff": false,
    "date_joined": "2024-10-15T08:18:59.836836Z"
    // ... И так далее
  }
}
```
Статус коды:
- 200 OK: Успешное выполнение. Возвращается, если список пользователей был успешно получен, и пользователь имеет необходимые права доступа (в нашем случае - является администратором).
- 401 Unauthorized: Не указан JWT токен в заголовках.
- 403 Forbidden: Доступ запрещён. Возвращается, если пользователь не имеет прав для просмотра списка пользователей (в нашем случае - действие доступно только администраторам, а текущий пользователь — обычный пользователь).
- 500 Internal Server Error: Внутренняя ошибка сервера. Возвращается, если произошла ошибка на стороне сервера при обработке запроса.

### Вывод Одного Пользователя по Его ID со Списком Связанных с Ним Организаций
- URL: /api/users/{id}/
- Метод: GET
- Описание: Позволяет получить подробную информацию о конкретном пользователе, включая связанные с ним организации.
- Разрешения: IsAuthenticated и IsStaffOrUserBySelf (пользователь может просматривать только свой профиль или быть администратором)

Пример Ответа:
```json
{
  "id": 116,
  "email": "nikifstzxvaaagasqqgassdqwegd@gmail.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "",
  "avatar": null,
  "organizations": [
    {
      "id": 5,
      "name": "Emex",
      "description": "Потянуться сохранять тюрьма изменение научить. Товар уронить ведь материя покинуть. Забирать дружно один вздрогнуть поймать увеличиваться рот налево."
    },
    {
      "id": 11,
      "name": "Копылова Инк",
      "description": "Банк заявление расстройство парень. Теория сынок провал холодно факультет. Освобождение деловой коммунизм ведь желание дружно привлекать сынок."
    }
  ],
  "is_active": true,
  "is_staff": false,
  "date_joined": "2024-10-15T08:21:27.061233Z"
}
```

### Создание Новой Организации
- URL: /api/organizations/
- Метод: POST
- Описание: Позволяет администраторам создавать новые организации, предоставляя необходимые данные.
- Разрешения: IsAdminUser (доступно только администраторам)
Заголовки запроса:
- Authorization: Bearer <JWT_TOKEN>
Параметры запроса:
- name (строка, максимум 100 символов) - Название организации
- description (строка, опционально) - Описание организации

Пример Body:
```json
{
  "name": "Флексайтс",
  "description": "Веб-студия"
}
```
Статус коды:
- 201 Created: Успешное создание. Возвращается, если организация была успешно создана. В ответе возвращается созданный объект.
- 400 Bad Request: Неправильный запрос. Возвращается, если переданные данные для создания организации не прошли валидацию.
- 401 Unauthorized: Не указан JWT токен в заголовках.
- 403 Forbidden: Доступ запрещён. Пользлователь - не администратор.
- 500 Internal Server Error: Внутренняя ошибка сервера. Возвращается, если на стороне сервера произошла непредвиденная ошибка при обработке запроса.

### Вывод Списка Всех Организаций
- URL: /api/organizations/
- Метод: GET
- Описание: Позволяет получить список всех организаций вместе с пользователями, связанными с каждой организацией.
Разрешения: Доступно всем, даже не авторизованным.

Пример ответа:
```json
[
    {
        "id": 1,
        "name": "Caloneians",
        "description": "Завоёвываем земли",
        "users": []
    },
    {
        "id": 2,
        "name": "ОАО «Якушев, Русаков и Сорокин»",
        "description": "Кидать порог мотоцикл пропасть степь. Поколение четыре зима правый помимо.",
        "users": [
            {
                "id": 55,
                "email": "nesterovleon@example.org",
                "first_name": "Мстислав",
                "last_name": "Мамонтов"
            }
        ]
    },
    {
        "id": 3,
        "name": "Аргос",
        "description": "Мучительно рабочий темнеть ребятишки выражение.\nИнтернет мимо пастух. Даль поставить приятель военный. Костер трубка вывести соответствие палка.",
        "users": [
            {
                "id": 27,
                "email": "trofimovladimir@example.org",
                "first_name": "Капитон",
                "last_name": "Одинцов"
            },
            {
                "id": 24,
                "email": "harlampi_66@example.net",
                "first_name": "Ратибор",
                "last_name": "Князева"
            },
            {
                "id": 15,
                "email": "boleslav1994@example.com",
                "first_name": "Викентий",
                "last_name": "Гурьев"
            }
        ]
    }
  ]
```
Статус коды:
- 200 OK: Успешное выполнение. Возвращается, если список организаций был успешно получен.
- 500 Internal Server Error: Внутренняя ошибка сервера. Возвращается, если произошла непредвиденная ошибка на стороне сервера при обработке запроса.

## Тестовое

Создать Django REST framework приложение, с переопределённым пользователем и списком организаций в которых он состоит.
Две модели
+ Пользователь:
- Емайл
- Пароль
- Фамилия
- Имя
- Телефон
- Аватар(фотография).
- Связь на список организаций(может быть больше одной)
- *Базовые (технические) поля django, кроме логина, он не должен использоваться

+ Организация:
- Название
- Краткое описание

Функционал:
// все запросы делаются через через curl/postman/вебинтерфейс DRF, по RestAPI. Формат данных передаётся в json.

1) Создание нового пользователя(регистрация) ✅
2) Авторизация пользователя только по емайлу и паролю ✅
3) Редактирование своего профиля (изменение данных в профиле) ✅
4) Вывод списка всех пользователей и связанные с ними организации ✅
5) Вывод одного пользователя по его ID, со списком связанных с ним организаций ✅
5) Добавление новой организации ✅ 
6) Вывод списка всех организаций ✅

Дополнительный функционал, по желанию:
1) Вывод списка всех организаций(п.6 выше), со списком пользователей, которые связаны с каждой из них. ✅
2) Аватар/фотография пользователя, картинка должна при загрузке переименовываться [a-zA-Z0-9]. А так же resize(уменьшить) до размеров не больше 200х200 px. ✅
3) Авторизация пользователя должна происходить через JWT, передача приватных данных(изменения профиля), происходят через этот токен. Можно использовать отдельную библиотеку. ✅
4) Добавить unit-test ✅

Требования:
1) Python 3.8+ ✅
2) Проект должен быть залит на Github/Bitbucket и быть публичным. ✅
3) Проект должен быть в виртуальном окружении venv. Должен присутствовать файл со списком используемых в проекте пакетов и их версий. ✅
4) База данных по умолчанию от django: sqlite3 ✅
5) Описание какие методы есть, какие параметры они принимают, какие отдают. ✅
