# -*- coding: utf-8 -*-

BACKGROUND_COLOR = '#D6EAF8'        # Visit: https://htmlcolorcodes.com
DEFAULT_CONTAINER_WIDTH = 640
DEFAULT_CONTAINER_HEIGHT = 480
DEFAULT_FONT = ('Segoe UI', 9)      # Default font for widgets
DEFAULT_LEFT_MARGIN = 10
DEFAULT_TOP_MARGIN = 5

DEFAULT_ROW_HEIGHT = 20             # Default height for widgets
DEFAULT_LABEL_WIDTH = 80
DEFAULT_INPUT_WIDGET_WIDTH = 213    # Default width for input widgets, like (entry, combobox, ...)
DEFAULT_BUTTON_HEIGHT = DEFAULT_ROW_HEIGHT + int(DEFAULT_ROW_HEIGHT / 2)
DEFAULT_BUTTON_WIDTH = 120
DEFAULT_BUTTON_LEFT_MARGIN = DEFAULT_TOP_MARGIN - 3

DEFAULT_TREEVIEW_GRID_ROWS_COUNT = 10
DEFAULT_TREEVIEW_DATAGRID_WIDTH = 0     # Interpreted as the full width of the container
DEFAULT_TREEVIEW_DATAGRID_HEIGHT = int((DEFAULT_TOP_MARGIN + DEFAULT_ROW_HEIGHT) * DEFAULT_TREEVIEW_GRID_ROWS_COUNT)

DEFAULT_GRID_ROWS_HEIGHT = (DEFAULT_ROW_HEIGHT,                 # 1º row
                            DEFAULT_ROW_HEIGHT,                 # 2º row
                            int(DEFAULT_ROW_HEIGHT / 2),        # 3º row
                            DEFAULT_BUTTON_HEIGHT,              # 4º row
                            int(DEFAULT_ROW_HEIGHT / 2),        # 5º row
                            DEFAULT_TREEVIEW_DATAGRID_HEIGHT)   # 6º row

DEFAULT_GRID_COLUMNS_WIDTH = (DEFAULT_LABEL_WIDTH,              # 1º column
                              DEFAULT_INPUT_WIDGET_WIDTH,       # 2º column
                              DEFAULT_LABEL_WIDTH,              # 3º column
                              DEFAULT_INPUT_WIDGET_WIDTH)       # 4º column

DEFAULT_V_SCROLLBAR_WIDTH = 15
DEFAULT_H_SCROLLBAR_HEIGHT = 15


class FakeGridLayout:
    """
    Class to simulate a Grid (rows x columns) inside the Container based on the Place layout manager,
      thus calculating for each widget absolute coordinates (x, y).
    """
    def __init__(self,
                 rows_height_: () = DEFAULT_GRID_ROWS_HEIGHT,
                 columns_width_: () = DEFAULT_GRID_COLUMNS_WIDTH):
        self.__rows_height = rows_height_
        self.__columns_width = columns_width_

    def get_place(self,
                  row_number_: int,
                  col_number_: int) -> ():
        """
        Calculates the exact coordinates (x, y) to place the widget inside the parent container, obtained from a
          fake-grid mimicked by GRID_ROWS_HEIGHT and GRID_COLUMNS_WIDTH
        :param row_number_: where the widget will be placed inside the container
        :param col_number_: where the widget will be placed inside the container
        :return: coordinates (x, y) to Place the widget inside the container
        """
        x_ = sum(self.__columns_width[:col_number_ - 1]) + DEFAULT_LEFT_MARGIN * col_number_
        y_ = sum(self.__rows_height[:row_number_ - 1]) + DEFAULT_TOP_MARGIN * row_number_
        return x_, y_
