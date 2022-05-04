# -*- coding: utf-8 -*-

# --- App modules ---
from .base_table_class import Table
from .sql_connection import SqlConnection


class Genres(Table):
    """
    Table representation Genres
    """
    def __init__(self):
        """
        Class constructor
        """
        # Open sql connection
        super().__init__(type(self).__name__)
        self.db = SqlConnection()
