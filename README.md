Задание:
Написать небольшой сервис в виде телеграмм чат-бота на Python,
который получает на вход ссылку на picsum.photos , обрабатывает ее и
сохраняет изображения за пользователем.
Пользователь может просматривать свои изображения, удалять их и
выгружать в виде таблицы.

1) Download all the libraries and packages with the required versions required for the project using the command:

```
pip install -r requirements.txt
```

2) We start docker, thereby creating a local database using the command:

```
docker-compose up -d
```

3) Bot launch:

```
python main.py
```