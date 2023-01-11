Тестовое задание - https://docviewer.yandex.com/view/0/?page=1&*=0TOrSeE7j%2BCWfLhuXm50Om0ZZL17InVybCI6InlhLWRpc2stcHVibGljOi8vK3RMbjB1c3hKYnZlVVZOVG5kK1JMblhTdERBdUdVaDB0NlRSNXR1QlhuZGNFZlJiKzNYN3JqRU9EaktsMkNNNHEvSjZicG1SeU9Kb25UM1ZvWG5EYWc9PSIsInRpdGxlIjoidGhlX2ZhY3RvcnlfYm90X3Rhc2sucGRmIiwibm9pZnJhbWUiOmZhbHNlLCJ1aWQiOiIwIiwidHMiOjE2NzMzNTkyMDY2MDUsInl1IjoiOTg3ODYzMjkyMTY1MzQyMjkwNiJ9
___

### Помимо основных заданий был добавлен докер и подключен swagger он доступен по /docs

### Логика работы токена: после регистрации можно получить сгенерированный токен ( /echo/get_token/ ), далее нужно его активировать в телеграм боте:  команда /follow , после этого можно отправлять сообщения по апи
___
## Установка с докером

### Необходимо создать .env файл и добавить переменные окружения (админка создаться автоматически, данные будут взяты с переменных окружения)
```
# Django
DJANGO_SECRET_KEY='secret_key'

DJANGO_SUPERUSER_PASSWORD=test_password
DJANGO_SUPERUSER_EMAIL=root@root.com
DJANGO_SUPERUSER_USERNAME=root

# Postgres
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db
POSTGRES_HOST=db

# Telegram KEY
TELEGRAM_KEY=

```
## Запуск
```
docker-compose up --build
```