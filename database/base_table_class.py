# -*- coding: utf-8 -*-

# --- Python modules ---
# inspect: module which provides several useful functions to help get information about live objects such as modules,
#          classes, methods, functions, tracebacks, frame objects, and code objects
import inspect
# os: module which allows access to OperatingSystem-dependent functionalities.
import os
# sqlite3: C library that provides a lightweight disk-based sql without a separate server,
#          process and allows accessing the sql using a nonstandard variant of the SQL query language
import sqlite3
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
import sys

# --- App modules ---
from .sql_connection import SqlConnection
from helper import string_helper


class Table:
    def __init__(self,
                 table_name_: str):
        """
        Class constructor
        """
        # Open sql connection
        self.db = SqlConnection()
        self.table_name = table_name_.lower()

    def create_table(self,
                     sql_script_file_: str = '',
                     drop_if_exists_: bool = False) -> bool:
        """
        Creates a table in database since external SQL script
        :param sql_script_file_: filename with SQL script, if ii is empty will be use default script
        :param drop_if_exists_: drop the old table if it exists
        :return: True if table was created successfully, otherwise False
        """
        if drop_if_exists_:
            self.drop_table()
        elif self.table_exists():
            # Existing table should not be dropped
            return False

        # Identify the SQL script file to run to create a table
        if string_helper.is_none_empty_space(sql_script_file_):
            # If script parameter to create the is empty, set default value
            sql_script_file_ = f'create_{self.table_name}.sql'
        sql_script_file_ = os.path.join(self.db.sql_scripts_folder(), sql_script_file_)

        # Evaluate if SQL script file exists
        if os.path.exists(sql_script_file_):
            # Read SQL script file
            with open(sql_script_file_, 'r') as file_:
                sql_script_ = file_.read()

            # Execute CREATE TABLE command
            self.db.execute(sql_script_)

            return True

        raise ValueError('There is no SQL script to create table.')

    def drop_table(self) -> bool:
        """
        Drops a table in database
        :return: True if table was dropped successfully, otherwise False
        """
        # Set command
        if self.table_exists():
            sql_command_ = f'DROP TABLE IF EXISTS {self.table_name}'

            # Execute command DROP TABLE
            self.db.execute(sql_command_)

            return True

        return False

    def execute(self,
                sql_command_) -> sqlite3.Cursor:
        """
        Executes a command on the sql
        """
        try:
            # Execute SQL command
            return self.db.execute(sql_command_)
        except Exception as e:
            print(f'SQL execution error over {self.table_name} table.\nMethod: {inspect.stack()[0][0].f_code.co_name}.',
                  {sys.exc_info()[0]}, e)
            raise e

    def fechtall(self,
                 order_by_: str = 'id ASC') -> []:
        """
        Fetches all the rows of the table
        :param order_by_: orders the result set of a query by the specified column list
        :return: list with all table rows
        """
        command_ = f'SELECT * FROM \'{self.table_name}\''
        if not string_helper.is_none_empty_space(order_by_):
            command_ += f' ORDER BY {order_by_}'
        return self.db.get(command_).fetchall()

    def delete(self,
               id_: int):
        """
        Delete a record from the database
        """
        command_ = f'DELETE FROM \'{self.table_name}\' WHERE id = {id_}'
        return self.db.execute(command_)

    def table_exists(self) -> bool:
        """
        Identifies if the table exists in the database.
        """
        if string_helper.is_none_empty_space(self.table_name):
            raise ValueError('Table name is required.')

        command_ = f'SELECT COUNT(*) FROM sqlite_master WHERE type = \'table\' AND name = \'{self.table_name}\''
        counter_ = self.db.get_value(command_, 0)
        return counter_ > 0
