import bcrypt
import pymysql
import sqlite3

from typing import Union, List, Tuple, Dict


class OpenPySQL:
    """
    This code defines a Python class called OpenPySQL that can be used to interact with both SQLite and MySQL databases. 

    The class has the following methods:

    __init__(self, connection: object, engine: str)
    - Initializes the OpenPySQL class by setting the connection and engine type passed as arguments.

    sqlite(cls, filepath: str) -> 'OpenPySQL'
    - A class method that creates a connection to a SQLite database at a specified filepath.

    mysql(cls, user: str, password: str, database: str, host: str = 'localhost', port: int = 3306)
    - A class method that creates a connection to a MySQL database using the provided credentials.

    hashpw(password: str) -> str
    - A static method that returns a bcrypt hash of a plaintext password.

    checkpw(password: str, hashed: str) -> bool
    - A static method that checks whether a plaintext password matches a stored hashed password.

    query(self, query: str) -> None
    - A property method that sets the query string to be executed next.

    value(self, value: Union[int, str, List, Tuple, None]) -> None
    - A property method that sets the parameters for the next query.

    fetch(self, size: int = 1) -> Union[List[Dict], Dict, None]
    - Executes a query and returns the specified number of rows.
    - Set size=0 to fetch all rows while size=1 to fetch one row.

    execute(self) -> None
    - Executes the current query with the current parameters.

    close(self) -> None
    - Closes the database connection.
    """

    def __init__(self, connection: object, engine: str):
        self.con = connection
        self.eng = engine
        if self.eng == 'sqlite':
            self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    @classmethod
    def sqlite(cls, filepath: str) -> 'OpenPySQL':
        connection = sqlite3.connect(filepath)
        return cls(connection, 'sqlite')

    @classmethod
    def mysql(cls, user: str, password: str, database: str, host: str = 'localhost', port: int = 3306) -> 'OpenPySQL':
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return cls(connection, 'mysql')

    @staticmethod
    def hashpw(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=13)).decode()

    @staticmethod
    def checkpw(password: str, hashed: str) -> bool:
        if bcrypt.checkpw(password.encode(), hashed.encode()):
            return True
        return False

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, query: str) -> None:
        if self.eng == 'mysql':
            query = query.replace('?', '%s')
        self._query = query

    @property
    def value(self) -> Tuple[Union[int, str], ...]:
        return self._value

    @value.setter
    def value(self, value: Union[int, str, List, Tuple, None]) -> None:
        if value:
            if any(isinstance(value, t) for t in [int, str]):
                value = (value,)
            if isinstance(value, List):
                value = tuple(value)
        self._value = value or ()

    def fetch(self, size: int = 1) -> Union[List[Dict], Dict, None]:
        if self.eng == 'mysql':
            self.cur.execute(self.query, self.value)
            if size == 0:
                return self.cur.fetchall()
            elif size == 1:
                return self.cur.fetchone()
        elif self.eng == 'sqlite':
            exec = self.cur.execute(self.query, self.value)
            if size == 0:
                if res := exec.fetchall():
                    return [{k: r[k] for k in r.keys()} for r in res]
            elif size == 1:
                if res := exec.fetchone():
                    return {k: res[k] for k in res.keys()}
        return

    def execute(self) -> None:
        if self.value:
            if any(isinstance(self.value[0], t) for t in [str, int]):
                self.cur.execute(self.query, self.value)
            else:
                self.cur.executemany(self.query, self.value)
        else:
            self.cur.execute(self.query)
        self.con.commit()

    def close(self) -> None:
        self.con.close()
