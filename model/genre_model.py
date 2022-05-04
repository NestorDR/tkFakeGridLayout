# -*- coding: utf-8 -*-

class Genre:
    """
    Genre entity
    """
    def __init__(self,
                 id_: int,
                 name_: str):
        """
        Class constructor
        """
        self.id = id_
        self.name = name_

    def __str__(self):
        return f'Genre [{self.id}, {self.name}]'
