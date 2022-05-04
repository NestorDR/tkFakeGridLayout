# -*- coding: utf-8 -*-

class Movie:
    """
    Movie entity
    """
    def __init__(self,
                 id_: int,
                 name_: str,
                 director_: str,
                 gender_: str,
                 duration_: str,
                 available_: bool):
        """
        Class constructor
        """
        self.id = id_
        self.name = name_
        self.director = director_
        self.gender = gender_
        self.duration = duration_
        self.available = available_

    def __str__(self):
        return f'Movie [{self.id}, {self.name}, {self.director}, {self.gender}, {self.duration}, {self.available}]'
