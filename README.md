# Quiz Game Bot

��� ������� ������ ���� ��������� ��� Telegram � Vkontakte.

## ��������

������ �������� ���� ����� - Telegram ���� (bot_tg.py) � Vkontakte ���� (bot_vk.py).

## ����������

- Python 3.8 � ����
- Docker � Docker Compose ��� ������� � �����������

## �������������

### ������ ��������

1. ���������� �����������:

```
   pip install -r requirements.txt
 ```
2. ��������� ���������� ��������� ��� ���� .env � ������� � ����������� ��� VK API, Telegram � Redis. ��������� ����������.

REDIS_HOST=host: ������ Redis

REDIS_PORT=����

REDIS_PASSWORD=������

TELEGRAM_BOT_API=API ����, ������� �� ��������� ��� �������� ���� � Telegram

VK_TOKEN= API ����, ������� �� ��������� ��� �������� ������ � ���������

�������� � ������� ����� questions � ���� �������� ����� � ��������� � ��������.

��������� ���� Telegram:

```
   python bot_tg.py
```
��������� ���� Vkontakte:

```
python bot_vk.py
```

## ������ � Docker

�������� Docker-������:

```
docker-compose build

```

��������� ����������:

```
docker-compose up -d
```

