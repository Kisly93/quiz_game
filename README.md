# Quiz Game Bot

Это простой проект бота викторины для Telegram и Vkontakte.

## Описание

Проект включает двух ботов - Telegram бота (bot_tg.py) и Vkontakte бота (bot_vk.py).

## Требования

- Python 3.8 и выше
- Docker и Docker Compose для запуска в контейнерах

## Использование

### Запуск локально

1. Установите зависимости:

```
   pip install -r requirements.txt
 ```
2. Настройте переменные окружения или файл .env с ключами и настройками для VK API, Telegram и Redis. Доступные переменные.

REDIS_HOST=host: Сервер Redis

REDIS_PORT=Порт

REDIS_PASSWORD=Пароль

TELEGRAM_BOT_API=API ключ, который вы получаете при создании бота в Telegram

VK_TOKEN= API ключ, который вы получаете при создании группы в ВКонтакте

Создайте в проекте папку questions и туда положите файлы с вопросами и ответами.

Запустите бота Telegram:

```
   python bot_tg.py
```
Запустите бота Vkontakte:

```
python bot_vk.py
```

## Запуск в Docker

Соберите Docker-образы:

```
docker-compose build

```

Запустите контейнеры:

```
docker-compose up -d
```
## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте Devman.
