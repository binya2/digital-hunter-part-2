import os

import mysql.connector


class MySQL:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None or not self._client.is_connected():
            self._client = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'localhost'),
                port=int(os.environ.get('MYSQL_PORT', 3306)),
                user=os.environ.get('MYSQL_USER', 'root'),
                password=os.environ.get('MYSQL_PASSWORD', 'root'),
                database=os.environ.get('MYSQL_DATABASE', 'digital_hunter')
            )
        return self._client

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        conn = self.client
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount
            return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()


mysql_service = MySQL()
