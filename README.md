# Тестовое задание для стажировки VK по направлению Python

## Friends REST API
### Описание:
API с базовым функционалом друзей в социальной сети. Можно отправлять, принимать и отклонять приглашения дружить, 
просматривать все свои входящие и исходящие приглашения, а также список своих друзей.

### OpenAPI спецификация:  
yml-файл со спецификацией API находится по пути ```./docs/openap-schema.yml```.  

### Запуск:
#### 1. Скопировать проект на компьютер, перейти в папку disturbed_config.

- Создать файл ```.env``` и добавить в него следующие строки:
```
SECRET_KEY='#85r+v$gtn@yt*yzmewwtv)0dz(ohb2gj9ae1e=^ket5p*n6!x'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- Выполнить команду для сборки:\
```docker-compose up -d```

#### 2. После сборки проекта в контейнеры выполнить миграции:

- ```docker-compose exec api python manage.py migrate```

#### 3. Доступные эндпоинты и примеры запросов:
В заголовках необходимо передать JWT токен в виде пары ключ-значение ```Autorization : Bearer <token>```  
- ```http://0.0.0.0:80/api/users/``` - POST, регистрация
    Запрос:  
    ```
    {
        "username": "username",
        "password": "password"
    }
    ```
- ```http://0.0.0.0:80/api/users/me/``` - GET, информация о текущем пользователе
- ```http://0.0.0.0:80/api/auth/jwt/create/``` - POST, получение JWT токена  
    Запрос:  
    ```
    {
        "username": "username",
        "password": "password"
    }
    ```
    Ответ:  
    ```
    {
        "refresh": <token>,
        "access": <token>
    }
    ```
- ```http://0.0.0.0:80/api/jwt/refresh/``` - POST, обновление JWT токена  
- ```http://0.0.0.0:80/api/users/<id>``` - GET, получение информации о пользователе с айди ```<id>```  
    Ответ:  
    ```
    {
        "id": 1,
        "username": "username",
        "friendship_status": "Requested to be your friend"
    }
    ```
- ```http://0.0.0.0:80/api/users/friends/``` - GET, получение списка друзей  
    Ответ:  
    ```
    [
        {
            "id": 1,
            "username": "username",
            "friendship_status": "Not friends"
        },
        {
            "id": 2,
            "username": "username2",
            "friendship_status": "Friend"
        },
    ]
    ```
- ```http://0.0.0.0:80/api/users/<id>/add_friend/``` - POST, добавить друга с айди ```<id>```  
    Ответ:  
    ```
    {
        "id": 1,
        "requested_by": "username2",
        "requested_to": "username"
    }
    ```
- ```http://0.0.0.0:80/api/users/<id>/delete_friend/``` - DELETE, удалить друга с айди ```<id>```  
- ```http://0.0.0.0:80/api/friend_requests/outgoing/``` - GET, получить все исходящие заявки в друзья  
    Ответ:  
    ```
    [
        {
            "requested_to": "username",
        },
        {
            "requested_to": "username2",
        },
    ]
    ```
- ```http://0.0.0.0:80/api/friend_requests/incoming/``` - GET, получить все входящие заявки в друзья  
    Ответ:  
    ```
    [
        {
            "id": 1,
            "requested_by": "username",
        },
        {
            "id": 2,
            "requested_by": "username2",
        },
    ]
- ```http://0.0.0.0:80/api/friend_requests/incoming/<request_id>/accept/``` - POST, принять заявку в друзья  
    Ответ:  
    ```
    {
        "id": 1,
        "username": "username",
        "friendship_status": "Friend"
    }
    ```
- ```http://0.0.0.0:80/api/friend_requests/incoming/<request_id>/decline/``` - POST, отклонить заявку в друзья  