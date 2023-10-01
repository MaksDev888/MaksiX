# MaksiX - Социальная сеть

MaksiX - это урезанная версия социальной сети, которая предоставляет базовый функционал, такой как добавление друзей, подписчиков, просмотр страниц как других пользователй, так и своей.

>Технологии, используемые на проекте:

>>1. Python ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
>>2. Django ![Django](https://img.shields.io/badge/-Django-0aad48?style=flat-square&logo=Django)
>>3. DjangoRestFramework ![Django Rest Framework](https://img.shields.io/badge/DRF-red?style=flat-square&logo=Django)
>>4. PostgresSQL ![Postgresql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
>>5. pgAdmin ![pgAdmin](https://img.shields.io/badge/PG-pgAdmin-blue?style=flat-square&logo=pgAdmin)
# Как запустить проект:

В папку Проекта расположить .env файл со следующими параметрами:

1. DB_NAME=**Имя БД**
2. DB_USER=**Имя пользователя БД**
3. DB_PASSWORD=**Пароль БД**
4. DB_HOST=**Хост или адресс БД**
5. DB_PORT=**Порт БД**

Скачать docker: 
1. Для [windows](https://docs.docker.com/desktop/windows/install/)
2. Для [macOS](https://docs.docker.com/desktop/mac/install/)
3. Для дистрибутивов [Linux](https://docs.docker.com/desktop/linux/#uninstall)

После установки проверьте конфигурацию переменных окружений 
командой:
```
docker-compose config
```
Если всё успешно, все переменные на местах, запустить командой:
```
docker-compose -f docker-compose.dev.yml up --build -d
```

Что бы создать суперпользователя, 
необходимо войти в контейнер командой:
```
docker exec -it Social_Network_MaksiX bash
```
Применить миграции:
```
python manage.py migrate
```
Собрать статику:
```
python manage.py collectstatic
```
После ввести команду:
```
python manage.py createsuperuser
```
и следовать дальнейшим инструкциям.

Для выхода введите:
```
exit
```
