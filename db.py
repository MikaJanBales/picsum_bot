import psycopg2
from psycopg2 import Error


def create_table():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            host="localhost",
            database="telegram",
            user="telegram",
            password="telegram"
        )
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_create_database = "CREATE TABLE IF NOT EXISTS photo (id SERIAL PRIMARY KEY, num_id INT, author VARCHAR(50), width INT, height INT, url VARCHAR(70), download_url VARCHAR(70), UNIQUE(num_id, author));"
        cursor.execute(sql_create_database)
        connection.commit()
        cursor.close()
        connection.close()
        print("Таблица успешно создана в PostgreSQL")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def get_info_photo(num_id):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            host="localhost",
            database="telegram",
            user="telegram",
            password="telegram"
        )
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        select_query = "SELECT * FROM photo WHERE num_id = '%s'" % num_id
        cursor.execute(select_query)
        record = cursor.fetchall()
        print("Результат", record)
        connection.commit()
        cursor.close()
        connection.close()

        return record
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def add_photo(info_photo):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            host="localhost",
            database="telegram",
            user="telegram",
            password="telegram"
        )
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        insert_query = "INSERT INTO photo (num_id, author, width, height, url, download_url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
            info_photo['id'], info_photo['author'], info_photo['width'], info_photo['height'],
            info_photo['url'],
            info_photo['download_url'])
        cursor.execute(insert_query)
        connection.commit()
        print("Запись успешно вставлена")
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def get_list_photo():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            host="localhost",
            database="telegram",
            user="telegram",
            password="telegram"
        )
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM photo")
        record = cursor.fetchall()
        print("Результат", record)
        connection.commit()
        cursor.close()
        connection.close()

        return record
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def get_id_and_author_photo():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            host="localhost",
            database="telegram",
            user="telegram",
            password="telegram"
        )
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute("SELECT num_id, author FROM photo")
        record = cursor.fetchall()
        print("Результат", record)
        connection.commit()
        cursor.close()
        connection.close()
        return record
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def delete_photo(num_id):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            host="localhost",
            database="telegram",
            user="telegram",
            password="telegram"
        )
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        delete_query = "DELETE FROM photo WHERE num_id = '%s'" % num_id
        cursor.execute(delete_query)
        connection.commit()
        cursor.close()
        connection.close()
        print("Запись успешно удалена из таблицы")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
