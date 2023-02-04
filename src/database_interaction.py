import pymysql
from pymysql import cursors
pymysql.connections.Connection

class DatabaseInteractor:
    """ Responsible for interacting with the database cloud service
    
    Attributes:
        connection (pymysql.connections.Connection)
    
    """

    def __init__(self, drop_table: bool):
        timeout = 10
        self.connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=cursors.DictCursor,
            db="defaultdb",
            # Put your mysql service api and password obtained from the aiven cloud:
            host="",
            passwd="",
            read_timeout=timeout,
            write_timeout=timeout,
            port=11265,
            user="avnadmin",
        )
        cursor = self.connection.cursor()
        if drop_table:
            cursor.execute("DROP TABLE IF EXISTS posts")
            cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, description VARCHAR(1024), email VARCHAR(1024), state VARCHAR(1024), category VARCHAR(1024))")
            self.connection.commit()
        print("Connected to database...")

    async def deposit_to_database(self, id: int, description: str, email: str):
        """ Inserts a new record to the database
        
        Args:
            id (str): The new record's id
            description (str): The description of the post
            email (str): The email address of the post's owner
        
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO posts VALUES('{id}', '{description}', '{email}', 'pending', '')")
            self.connection.commit()
        finally:
            pass
    
    def update_record(self, id: int, state: str, category: str):
        """ Updates an existing record in the database
        
        Args:
            id (str): The new record's id
            state (str): State of the post
            category (str): Category of the post's image
        
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE posts SET state = '{state}' WHERE id = {id}")
            cursor.execute(f"UPDATE posts SET category = '{category}' WHERE id = {id}")
            self.connection.commit()
        finally:
            pass
    
    def get_record(self, id: int):
        """ Returns an existing record to the database
        
        Args:
            id (str): The record's id
        
        """
        
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
        record = cursor.fetchone()
        return record
    
