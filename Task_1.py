from decimal import Decimal
import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import argparse
import json
import xml.etree.ElementTree as ET

#  Custom JSON encoder that converts Decimal objects to float.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


# Create a class for the database connection
class DatabaseConnection:
    def __init__(self, host, dbname, user, password, port):
        self.connection = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.close()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

# Create a class for loading data into the database
class DataLoader:
    def __init__(self, db_connection: DatabaseConnection):
        self.connection = db_connection
    
    def load_rooms_json_data(self, rooms_path: str):
        with open(rooms_path) as rooms:
            rooms_data = json.load(rooms)

        for room in rooms_data:
            self.connection.execute_query(f'''INSERT INTO rooms ("id", "name") VALUES {room["id"], room["name"]}''')

    def load_students_json_data(self, students_path: str):
        with open(students_path) as students:
            students_data = json.load(students)

        for student in students_data:
            self.connection.execute_query(f'''INSERT INTO students ("id", "name", "birthday", "room", "sex") 
                           VALUES {student["id"], student["name"], student["birthday"], student["room"], student["sex"]}''')

# Function for inserting data into the database
def insert_data_into_database(db_connection: DatabaseConnection, rooms_path: str, students_path: str):
        data_loader = DataLoader(db_connection)
        data_loader.load_rooms_json_data(rooms_path)
        data_loader.load_students_json_data(students_path)
        db_connection.commit()

# Function for running and saving query
def query_and_save(db_connection: DatabaseConnection, sql_query: str, file_format: str, output_file_path=None):
    
    # Use default path based on the script location
    if output_file_path is None:
            output_file_path = sql_query.split('\n')[0][3:]

    cursor = db_connection.connection.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Save results in JSON format
    if file_format == 'json':
        
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            # query_description = sql_query.split('\n')[0]
            # json_file.write(f"-- SQL Query: {query_description}\n")
            json.dump(results, json_file, indent=2, cls=DecimalEncoder)

    # Save results in XML format
    elif file_format == 'xml':
        root = ET.Element("results")

        for result in results:
            result_element = ET.SubElement(root, "result")
            for i, column_name in enumerate(cursor.description):
                column_value = str(result[i])
                ET.SubElement(result_element, column_name[0]).text = column_value

        paragraph_element = ET.Element("paragraph")
        root.append(paragraph_element)

        tree = ET.ElementTree(root)
        tree.write(output_file_path, encoding='utf-8', xml_declaration=True)
    
    else:
        print("Unsupported file format. Please choose 'json' or 'xml'.")

if __name__ == '__main__':
    # Load environment variables
    load_dotenv()
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    # Create a parser to get variables from the console
    parser = argparse.ArgumentParser(description='Process of load of data about students and rooms into database.')
    parser.add_argument('-rp', dest='room_path', action='store', nargs='?', const='path_default', 
                        help='path for student file')
    parser.add_argument('-sp', dest='students_path', action='store', nargs='?', const='path_default',
                        help='path for room file') 
    parser.add_argument('-ff', dest='file_format', action='store', nargs='?', const='path_default', default='json',
                        help='file format')

    args = parser.parse_args()

    # Variables from the console
    rooms_path = args.room_path
    students_path = args.students_path
    file_format = args.file_format

    # Path to SQL queries
    script_directory = os.path.dirname(os.path.realpath(__file__))
    sql_file_path = os.path.join(script_directory, 'queries.sql')

    # Create a database connection
    db_connection = DatabaseConnection(host=host, dbname=dbname, user=user, password=password, port=port)

    # Insert data into the database
    insert_data_into_database(db_connection=db_connection, rooms_path=rooms_path, students_path=students_path)

    # Run obligate SQL queries
    with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
        sql_queries = sql_file.read()

    queries = [query.strip() for query in sql_queries.split('-- #QUERY') if query.strip()] 

    for query in queries:
        query_and_save(db_connection=db_connection, sql_query=query, file_format=file_format, output_file_path=None)

    db_connection.close()

