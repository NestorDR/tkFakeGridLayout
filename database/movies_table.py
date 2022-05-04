# -*- coding: utf-8 -*-

# --- App modules ---
from .base_table_class import Table
from helper import string_helper
from model import movie_model
from .sql_connection import SqlConnection


class Movies(Table):
    """
    Table representation Movies
    """
    def __init__(self):
        """
        Class constructor
        """
        # Open sql connection
        super().__init__(type(self).__name__)
        self.db = SqlConnection()

    def save(self,
             movie: movie_model.Movie):
        """
        Save a record in the database
        """

        # Validate data
        if string_helper.is_none_empty_space(movie.name):
            raise ValueError('The movie name cannot be empty.')
        if string_helper.is_none_empty_space(movie.director):
            raise ValueError('The movie director cannot be empty.')
        if string_helper.is_none_empty_space(movie.gender):
            raise ValueError('The movie gender cannot be empty.')
        if string_helper.is_none_empty_space(movie.duration):
            raise ValueError('The movie duration cannot be empty.')

        if movie.id is None or movie.id == 0:
            self.__insert(movie)
        else:
            self.__update(movie)

    def __insert(self,
                 movie: movie_model.Movie):
        sql_command_ = f"""
            INSERT INTO {self.table_name}
            (
                name,
                director,
                gender,
                duration,
                available
            )
            VALUES
            (
                '{movie.name.strip()}',
                '{movie.director.strip()}',
                '{movie.gender.strip()}',
                '{movie.duration.strip()}',
                {movie.available}
            )"""

        # Execute command in sql
        self.execute(sql_command_)

    def __update(self,
                 movie: movie_model.Movie):
        sql_command_ = f"""
            UPDATE  {self.table_name}
               SET  name      = '{movie.name.strip()}',
                    director  = '{movie.director.strip()}',
                    gender    = '{movie.gender.strip()}',
                    duration  = '{movie.duration.strip()}',
                    available = {movie.available}
             WHERE  id = {movie.id}"""

        # Execute command in sql
        self.execute(sql_command_)
