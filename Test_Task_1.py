import unittest
from unittest.mock import patch
from io import StringIO
from Task_1 import insert_data_into_database, query_and_save, DatabaseConnection, DataLoader

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        # Создаем объекты, необходимые для тестирования, например, DatabaseConnection
        self.db_connection = DatabaseConnection(host='localhost', dbname='postgres', user='postgres', password='mysecretpassword', port='5432')

    def test_insert_data_into_database(self):
        # Тестируем корректность вставки данных в базу данных
        rooms_path = "test_rooms.json"
        students_path = "test_students.json"
        with patch('builtins.open'), patch.object(DataLoader, 'load_rooms_json_data'), patch.object(DataLoader, 'load_students_json_data'), patch.object(DatabaseConnection, 'commit'):
            insert_data_into_database(self.db_connection, rooms_path, students_path)
            # Добавьте проверки, например, с использованием assertEqual, чтобы убедиться, что данные были успешно вставлены.

    def test_query_and_save_json(self):
        # Тестируем корректность выполнения запроса и сохранения результатов в JSON
        sql_query = "SELECT * FROM rooms;"
        file_format = "json"
        output_file_path = "test_output.json"
        with patch('sys.stdout', new_callable=StringIO):
            query_and_save(self.db_connection, sql_query, file_format, output_file_path)
            # Добавьте проверки, например, с использованием assertEqual, чтобы убедиться, что JSON-файл был создан и содержит ожидаемые данные.

    def test_query_and_save_xml(self):
        # Тестируем корректность выполнения запроса и сохранения результатов в XML
        sql_query = "SELECT * FROM rooms;"
        file_format = "xml"
        output_file_path = "test_output.xml"
        with patch('sys.stdout', new_callable=StringIO):
            query_and_save(self.db_connection, sql_query, file_format, output_file_path)
            # Добавьте проверки, например, с использованием assertEqual, чтобы убедиться, что XML-файл был создан и содержит ожидаемые данные.

if __name__ == '__main__':
    unittest.main()

