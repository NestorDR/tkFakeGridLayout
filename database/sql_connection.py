# -*- coding: utf-8 -*-

# os: library that allows access to OperatingSystem-dependent functionalities
import os
# sqlite3: C library that provides a lightweight disk-based sql without a separate server,
#          process and allows accessing the sql using a nonstandard variant of the SQL query language
import sqlite3
# sys: module which provides access to variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter
import sys


class SqlConnection:
    """
    SQL sql connection
    """
    def __init__(self):
        # Identify the application directory, set as db folder
        # Set sql folder
        self.folder = os.path.abspath(os.path.dirname(str(sys.modules['__main__'].__file__)))
        # Define the sql engine - we are working with SQLite for this example
        self.database = os.path.join(self.folder, 'movies.db')
        # Set sql connection, object that represents the sql
        self.connection = sqlite3.connect(self.database, detect_types=sqlite3.PARSE_DECLTYPES)
        # Create a Cursor, object that with its execute() method allows to perform SQL commands
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection = None

    @staticmethod
    def sql_scripts_folder() -> str:
        folder_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql')
        if not os.path.exists(folder_):
            os.makedirs(folder_)
        return folder_

    def connect(self):
        self.connection = sqlite3.connect(self.database)

    def commit(self):
        if self.connection is not None:
            self.connection.commit()

    def close(self):
        if self.connection is not None:
            self.connection.commit()
            self.connection.close()

    def execute(self,
                command_: str,
                commit_: bool = True) -> sqlite3.Cursor:
        """
        Execute command on the DB, returns a cursor.

        :param command_: SQL command to execute
        :param commit_: flag to close or not, the save transaction in the DB.

        :return: cursor with no specific result
        """
        if self.connection is None:
            self.connect()
        cursor = self.connection.cursor()
        cursor.executescript(command_)

        if commit_:
            self.connection.commit()
            self.connection.close()

        return cursor

    def get(self,
            command_: str) -> sqlite3.Cursor:
        """
        SELECT type query against the DB, returns a cursor.
        :param command_: SQL command to execute
        :return: cursor with the result set of the SELECT
        """
        if self.connection is None:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(command_)

        return cursor

    def get_value(self,
                  command_: str,
                  default_value_: object = None):
        """
        SELECT type query against the DB, returns a scalar
        :param command_: SQL command to execute
        :param default_value_: default value to return
        :return: scalar with the result of the SELECT
        :rtype: Any
        """
        if self.connection is None:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(command_)
        row = cursor.fetchone()
        if row:
            value = row[0]
        else:
            value = default_value_
        return value
