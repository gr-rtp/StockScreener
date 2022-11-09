from dotenv import dotenv_values
import psycopg2 as db
import os
from config import ROOT_DIR

config = dotenv_values(os.path.join(ROOT_DIR, 'db.local.env'))

DB_HOST = config['DB_HOST']
DB_NAME = config['DB_NAME']
DB_USER = config['DB_USER']
DB_PASS = config['DB_PASS']

class Database:
    def __init__(self) -> None:
        self.connect()
        pass
    
    def connect(self):
        self.connection = db.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

        print("============= DB Connected =============")

    def disconnect(self) -> None:
        self.connection.close()
        
        print("============= DB Disconnected =============")

db_instance = Database()

class DB_Service:
    def __init__(self) -> None:
        self.database = db_instance
        self.connection = self.database.connection
    
    def open_cursor(self):
        return self.connection.cursor()

    def close_cursor(self, cursor):
        cursor.close()