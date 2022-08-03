# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# pynput.keyboard: contains classes for controlling and monitoring the keyboard.
from pynput.keyboard import Key, Controller

# --- Python modules ---
# sys: module which provides access to variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
import sys
# tkinter: this package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit.
import tkinter as tk
from tkinter import messagebox, ttk

# --- App modules ---
from database.movies_table import Movies
from database.genres_table import Genres
from model.movie_model import Movie
from helper import layout


class Application(tk.Frame):
    """
    Class of a specialized frame for the app. Inherits from tk.Frame.
    """
    def __init__(self,
                 master_: tk.Tk):
        """
        Class constructor
        :param master_: window that will contain this frame
        """
        # Save parent widget (probably the top level window )
        self.master = master_
        self.container_width = layout.DEFAULT_CONTAINER_WIDTH
        self.container_height = layout.DEFAULT_CONTAINER_HEIGHT

        # Call constructor of Frame superclass, setting master frame or window and other configs
        super().__init__(self.master, width=self.container_width, height=self.container_height)

        # Set Pack as layout manager, thus allowing to show the frame
        self.pack()

        # Config display (ie alternative to resize)
        self.config(background=layout.BACKGROUND_COLOR)

        # Create fake grid layout fake-grid mimicked by GRID_ROWS_HEIGHT and GRID_COLUMNS_WIDTH, in order to place
        #   each widget based on Place layout manager
        self.fake_grid = layout.FakeGridLayout(layout.DEFAULT_GRID_ROWS_HEIGHT,
                                               layout.DEFAULT_GRID_COLUMNS_WIDTH)
        # Create controls/widgets in the GUI
        self.__create_widgets()

        # Create main menu
        self.menu_bar = MenuBar(self)
        master_.config(menu=self.menu_bar)

    def __create_widgets(self):
        """
        Create and add the widgets to the container thought as a grid, but positioning them after translation to Place
          positioning.
        """
        # Get fake grid to var to made easier its referenced
        fk = self.fake_grid

        # Create data fields and associated items
        self.id = None

        # Row Nº 1
        x_, y_ = fk.get_place(1, 1)             # get absolute (x, y) Place for widget in fake row 1 and fake col 1
        self.label_name = self.__create_label('Movie name', x_, y_)
        x_, y_ = fk.get_place(1, 2)             # get absolute (x, y) Place for widget in fake row 1 and fake col 2
        self.name = tk.StringVar()
        self.entry_name = self.__create_entry(self.name, False, x_, y_)
        x_, y_ = fk.get_place(1, 3)             # get absolute (x, y) Place for widget in fake row 1 and fake col 3
        self.label_name = self.__create_label('Director', x_, y_)
        x_, y_ = fk.get_place(1, 4)             # get absolute (x, y) Place for widget in fake row 1 and fake col 4
        self.director = tk.StringVar()
        self.entry_director = self.__create_entry(self.director, False, x_, y_)

        # Row Nº 2
        x_, y_ = fk.get_place(2, 1)             # get absolute (x, y) Place for widget in fake row 2 and fake col 1
        self.label_genre = self.__create_label('Main genre', x_, y_)
        x_, y_ = fk.get_place(2, 2)             # get absolute (x, y) Place for widget in fake row 2 and fake col 2
        # Dropdown genre menu options
        genre_values = Genres().fechtall('name ASC')        # get list of values for movie genre combo box from database
        genre_values = [tuple_[1] for tuple_ in genre_values]   # with list comprehension extract name (2º column)
        self.genre = tk.StringVar(self)
        self.combobox_genre = self.__create_combobox(self.genre, genre_values, False, x_, y_,
                                                     width_=layout.DEFAULT_INPUT_WIDGET_WIDTH)
        x_, y_ = fk.get_place(2, 3)             # get absolute (x, y) Place for widget in fake row 2 and fake col 3
        self.label_duration = self.__create_label('Duration', x_, y_)
        x_, y_ = fk.get_place(2, 4)             # get absolute (x, y) Place for widget in fake row 2 and fake col 4
        self.duration = tk.StringVar(self)      # Alternately DoubleVar()
        width_ = int(layout.DEFAULT_INPUT_WIDGET_WIDTH / 2)
        self.entry_duration = self.__create_entry(self.duration, False, x_, y_, width_=width_)
        x_ += width_ + layout.DEFAULT_LEFT_MARGIN * 3
        width_ = self.container_width - x_ - layout.DEFAULT_LEFT_MARGIN
        self.available = tk.BooleanVar()
        self.checkbox_available = self.__create_checkbox(self.available, 'Available', enabled_=False,
                                                         x_=x_, y_=y_, width_=width_)

        # Create five (5) buttons
        _, y_ = fk.get_place(4, 1)             # get absolute x Place for 1º button in fake row 4
        buttons_count = 5
        total_width = (layout.DEFAULT_BUTTON_LEFT_MARGIN + layout.DEFAULT_BUTTON_WIDTH)
        x_ = self.container_width - total_width * buttons_count - layout.DEFAULT_LEFT_MARGIN
        self.button_new = self.__create_button('New', self.__new, True, x_, y_)
        self.button_new.focus()                     # Set focus on button New
        x_ += total_width
        self.button_edit = self.__create_button('Edit', self.__edit, False, x_, y_)
        x_ += total_width
        self.button_cancel = self.__create_button('Cancel', self.__cancel, False, x_, y_)
        x_ += total_width
        self.button_save = self.__create_button('Save', self.__save, False, x_, y_)
        x_ += total_width
        self.button_delete = self.__create_button('Delete', self.__delete, False, x_, y_)

        # Fetch data to load datagrid
        movies_ = self.__fetch_movies()

        # Create data grid
        x_, y_ = fk.get_place(6, 1)             # get absolute (x, y) Place for widget in fake row 6 and fake col 1
        datagrid_height_ = self.container_height - y_ - layout.DEFAULT_TOP_MARGIN * 2
        self.datagrid = self.__create_treeview_datagrid(
            items_=movies_,
            columns_=('Name', 'Director', 'Genre', 'Duration', 'Available'),
            col_headings_=('Movie name', 'Director', 'Main Genre', 'Duration', 'Available'),
            col_widths_=(200, 200, 150, 100, 70),
            col_anchors_=(tk.W, tk.W, tk.W, tk.W, tk.CENTER),
            x_=x_, y_=y_, height_=datagrid_height_)

        # Bind event with its event handler
        self.datagrid.bind('<<TreeviewSelect>>', self.__enable_edit)

    def __create_label(self,
                       text_: str = 'New Label',
                       x_: int = 0, y_: int = 0,
                       font_: tuple = layout.DEFAULT_FONT) -> tk.Label:
        """
        Add a new label to the GUI using Place layout manager
        :param text_: string of text to show in the widget
        :param x_: horizontal offset in pixels for displaying widget
        :param y_:  vertical offset in pixels for displaying widget
        :param font_: font style for displaying widget

        :return: a new label
        """
        # Create new label
        # anchor parameter specifies how the image is aligned within the final displaying,
        #   aligning options: E is Right, W is Left, N is Top, S is bottom
        new_label_ = tk.Label(self, text=text_, font=font_, anchor=tk.W, background=layout.BACKGROUND_COLOR)
        # Place label
        new_label_.place(x=x_, y=y_, width=layout.DEFAULT_LABEL_WIDTH)

        return new_label_

    def __create_entry(self,
                       text_variable_: tk.Variable,
                       enabled_: bool = True,
                       x_: int = 0, y_: int = 0,
                       width_: int = layout.DEFAULT_INPUT_WIDGET_WIDTH, height_: int = layout.DEFAULT_ROW_HEIGHT,
                       font_: tuple = layout.DEFAULT_FONT) -> tk.Entry:
        """
        Add a new entry to the GUI using Place layout manager
        :param text_variable_: variable whose value is linked to the widget value
        :param enabled_: flag to indicate whether the widget is displayed enabled or disabled
        :param x_: horizontal offset in pixels for displaying widget
        :param y_:  vertical offset in pixels for displaying widget
        :param width_: width of the widget in pixels
        :param height_: height of the widget in pixels
        :param font_: font style for displaying widget

        :return: a new entry
        """
        # Create new entry
        new_entry_ = tk.Entry(self, textvariable=text_variable_, font=font_,
                              state=tk.NORMAL if enabled_ else tk.DISABLED)
        # Place entry
        new_entry_.place(x=x_, y=y_, width=width_, height=height_)

        return new_entry_

    def __create_combobox(self,
                          text_variable_: tk.Variable,
                          values_: [],
                          enabled_: bool = True,
                          x_: int = 0, y_: int = 0,
                          width_: int = layout.DEFAULT_INPUT_WIDGET_WIDTH, height_: int = layout.DEFAULT_ROW_HEIGHT,
                          font_: tuple = layout.DEFAULT_FONT) -> ttk.Combobox:
        """
        Add a new combobox to the GUI using Place layout manager
        :param text_variable_: variable whose value is linked to the widget value
        :param values_: list with all the options to show
        :param enabled_: flag to indicate whether the widget is displayed enabled or disabled
        :param x_: horizontal offset in pixels for displaying widget
        :param y_:  vertical offset in pixels for displaying widget
        :param width_: width of the widget in pixels
        :param height_: height of the widget in pixels
        :param font_: font style for displaying widget

        :return: a new dropdown
        """
        # Create new combobox
        new_dropdown_ = ttk.Combobox(self, textvariable=text_variable_, values=values_, font=font_,
                                     state=tk.NORMAL if enabled_ else tk.DISABLED)
        # Place dropdown
        new_dropdown_.place(x=x_, y=y_, width=width_, height=height_)

        return new_dropdown_

    def __create_checkbox(self,
                          variable_: tk.Variable,
                          text_: str = 'New checkbox',
                          command_=None,
                          on_value_: any = True, off_value_: any = False,
                          enabled_: bool = True,
                          x_: int = 0, y_: int = 0,
                          width_: int = layout.DEFAULT_INPUT_WIDGET_WIDTH, height_: int = layout.DEFAULT_ROW_HEIGHT,
                          font_: tuple = layout.DEFAULT_FONT) -> tk.Checkbutton:
        """
        Add a new checkbox to the GUI using Place layout manager
        :param variable_: variable whose value is linked to the widget value
        :param text_: string of text to show in the widget
        :param command_: a callback to be invoked when the checkbox/checkbutton is pressed
        :param on_value_: if the checkbox is checked, the value of the variable will be on_value_
        :param off_value_: if the checkbox is unchecked, the value of the variable will be off_value_
        :param enabled_: flag to indicate whether the widget is displayed enabled or disabled
        :param x_: horizontal offset in pixels for displaying widget
        :param y_:  vertical offset in pixels for displaying widget
        :param width_: width of the widget in pixels
        :param height_: height of the widget in pixels
        :param font_: font style for displaying widget

        :return: a new checkbox
        """
        # Create new checkbox
        new_checkbox_ = tk.Checkbutton(self, variable=variable_, text=text_, command=command_,
                                       onvalue=on_value_, offvalue=off_value_,
                                       font=font_, background=layout.BACKGROUND_COLOR,
                                       state=tk.NORMAL if enabled_ else tk.DISABLED)
        # Place checkbox
        new_checkbox_.place(x=x_, y=y_, width=width_, height=height_)

        return new_checkbox_

    def __create_button(self,
                        text_: str = 'New button',
                        command_=None,
                        enabled_: bool = True,
                        x_: int = 0, y_: int = 0,
                        width_: int = layout.DEFAULT_BUTTON_WIDTH, height_: int = layout.DEFAULT_BUTTON_HEIGHT,
                        font_: tuple = None) -> tk.Button:
        """
        Add a new button to the GUI using Place layout manager
        :param text_: string of text to show in the widget
        :param command_: a callback to be invoked when the button is pressed
        :param enabled_: flag to indicate whether the widget is displayed enabled or disabled
        :param x_: horizontal offset in pixels for displaying widget
        :param y_:  vertical offset in pixels for displaying widget
        :param width_: width for displaying widget
        :param height_: height of the widget in pixels
        :param font_: font style for displaying widget

        :return: a new button
        """
        # Create font style for the new button
        style_ = None
        if font_ is not None:
            # Config font style
            style_ = ttk.Style()
            style_.configure('app.TButton', font=font_)

        # Create new button
        new_button_ = ttk.Button(self, text=text_, command=command_,
                                 state=tk.NORMAL if enabled_ else tk.DISABLED,
                                 style='' if style_ is None else 'app.TButton')
        # Place button
        new_button_.place(x=x_, y=y_, width=width_, height=height_)

        return new_button_

    def __create_treeview_datagrid(self,
                                   items_: list,
                                   columns_: tuple,
                                   col_headings_: tuple,
                                   col_widths_: tuple,
                                   col_anchors_: tuple,
                                   x_: int = 0, y_: int = 0,
                                   width_: int = layout.DEFAULT_TREEVIEW_DATAGRID_WIDTH,
                                   height_: int = layout.DEFAULT_TREEVIEW_DATAGRID_HEIGHT) -> ttk.Treeview:
        """
        Add a new datagrid as a ttk.TreeView instance, to the GUI using Place layout manager
        :param items_: item list to load the datagrid
        :param columns_: list of column identifiers
        :param col_headings_: list of texts to display in the column headings
        :param col_widths_: list of column widths
        :param col_anchors_: list of column anchors (the anchor specifies where to position the content of the column)
        :param x_: horizontal offset in pixels for displaying widget
        :param y_:  vertical offset in pixels for displaying widget
        :param width_: width for displaying widget
        :param height_: height of the widget in pixels

        :return: a new datagrid as a ttk.TreeView instance
        """

        # Create new data grid as a ttk.TreeView instance
        new_datagrid_ = ttk.Treeview(self, columns=columns_)

        # Place datagrid in layout
        if width_ == layout.DEFAULT_TREEVIEW_DATAGRID_WIDTH:
            width_ = self.container_width - layout.DEFAULT_LEFT_MARGIN * 2  # Alternatively width_ = self.winfo_width()
        width_ = width_ - layout.DEFAULT_V_SCROLLBAR_WIDTH
        height_ = height_ - layout.DEFAULT_H_SCROLLBAR_HEIGHT
        new_datagrid_.place(x=x_, y=y_, width=width_, height=height_)

        # Add vertical and horizontal scrollbars
        v_scrollbar_ = ttk.Scrollbar(self, orient=tk.VERTICAL, command=new_datagrid_.yview)
        v_scrollbar_.place(x=width_ + layout.DEFAULT_LEFT_MARGIN, y=y_,
                           width=layout.DEFAULT_V_SCROLLBAR_WIDTH, height=height_)

        h_scrollbar_ = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=new_datagrid_.xview)
        h_scrollbar_.place(x=x_, y=y_ + height_,
                           width=width_, height=layout.DEFAULT_H_SCROLLBAR_HEIGHT)

        # Link datatable (TreeView widget) with scrollbars
        new_datagrid_.configure(yscrollcommand=v_scrollbar_.set, xscrollcommand=h_scrollbar_.set)

        # Create columns
        new_datagrid_.heading('#0', text='Identifier')
        new_datagrid_.column('#0', width=80, stretch=tk.NO)
        for i in range(0, len(columns_)):
            new_datagrid_.heading(columns_[i], text=col_headings_[i])       # Define headings.
            # stretch: If this option is True, the column's width will be adjusted when the widget is resized
            new_datagrid_.column(columns_[i], anchor=col_anchors_[i], stretch=tk.NO, width=col_widths_[i])

        if len(items_) > 0:
            self.__load_datagrid_(new_datagrid_, items_)

        return new_datagrid_

    def __load_datagrid_(self,
                         datagrid_: ttk.Treeview = None,
                         items_: list = None):
        """
        Load data rows in data grid
        :param items_: item list fetched from database
        """
        if datagrid_ is None:
            datagrid_ = self.datagrid

        # Clear old items
        for item in datagrid_.get_children():
            datagrid_.delete(item)

        if items_ is None:
            items_ = []
        else:
            items_.reverse()

        for row in items_:
            datagrid_.insert('', 0, text=row[0],
                             values=(row[1], row[2], row[3], row[4], 'Yes' if row[5] else 'No'))

    @staticmethod
    def __fetch_movies() -> []:
        """
        Fetch data from the database for the datagrid (a ttk.TreeView instance), ordered by column name
        :return: data row list
        """
        list_ = []
        try:
            list_ = Movies().fechtall('name ASC')
        except Exception as e:
            messagebox.showerror('Error', f'{sys.exc_info()[0]}\n{str(e)}')

        return list_

    def __new(self):
        """
        Clean and prepare widgets to create a new record
        """
        self.__clean()                              # Clean entry widgets
        self.__toggle_widgets_state(tk.NORMAL)      # Enable widgets to allow edit a new item
        self.entry_name.focus()                     # Set focus on 1º entry widget

    def __enable_edit(self,
                      _):
        """
        Enable the edit button to be able to edit the selected item/record in the data grid
        """
        if len(self.datagrid.selection()) > 0:
            # Enable button widgets
            self.button_edit.config(state=tk.NORMAL)

    def __edit(self):
        """
        Edit the selected item in the datagrid, also enabling its deletion
        """
        selection_ = self.datagrid.selection()
        if len(selection_) > 0:
            selected_item_ = self.datagrid.item(selection_[0])

            self.id = selected_item_['text']
            self.name.set(selected_item_['values'][0])
            self.director.set(selected_item_['values'][1])
            self.genre.set(selected_item_['values'][2])
            self.duration.set(selected_item_['values'][3])
            self.available.set(True if selected_item_['values'][4] == 'Yes' else False)

            self.__toggle_widgets_state(tk.NORMAL)      # Enable widgets to allow edit
            self.button_delete.config(state=tk.NORMAL)  # Also enable Delete button

    def __save(self):
        """
        Save a new or existing movie in the database
        """
        try:
            self.__toggle_widgets_state(tk.DISABLED)    # Disable widgets to cancel editing

            movie_ = Movie(                             # Instantiate a new movie to save in database
                self.id,
                self.name.get(),
                self.director.get(),
                self.genre.get(),
                self.duration.get(),
                self.available.get()
            )

            Movies().save(movie_)                       # Save it in database
            movies_ = self.__fetch_movies()             # Fetch updated data from the database
            self.__load_datagrid_(items_=movies_)       # Refresh datagrid

            # Prepare view for next action
            self.__clean()                              # Clean entry widgets
            self.__toggle_widgets_state(tk.DISABLED)    # Disable widgets waiting for new edition
            self.button_new.focus()                     # Set focus on button New

        except Exception as e:
            messagebox.showerror('Error', f'{sys.exc_info()[0]}\n{str(e)}')

    def __cancel(self):
        """
        Clean and disable widgets to cancel record editing
        """
        self.__clean()                              # Clean entry widgets
        self.__toggle_widgets_state(tk.DISABLED)    # Disable widgets to cancel editing
        self.button_new.focus()                     # Set focus on button New

    def __delete(self):
        """
        Deletes the selected item/record of the database
        """

        # Confirm drop
        response_ = tk.messagebox.askquestion('Delete item',
                                              f'Are you sure you want to delete movie {self.name.get()}?',
                                              icon='warning')
        if response_ == 'yes':
            Movies().delete(self.id)                    # Delete from database the record identified with ID
            movies_ = self.__fetch_movies()             # Fetch data from the database
            self.__load_datagrid_(items_=movies_)       # Refresh datagrid

            # Prepare view for next action
            self.__clean()                              # Clean entry widgets
            self.__toggle_widgets_state(tk.DISABLED)    # Disable widgets waiting for new edition
            self.button_new.focus()                     # Set focus on button New

        else:
            messagebox.showinfo('Information', 'Deletion canceled by user.')

    def __clean(self):
        """
        Clean entry widgets
        """
        self.id = None
        self.name.set('')
        self.director.set('')
        self.duration.set('')
        self.genre.set('')
        self.available.set(False)

    def __toggle_widgets_state(self,
                               state_: []):
        """
        Enable or disable widgets in the GUI
        :param state_: state to set on widgets
        """
        # Enable/Disable entry widgets
        self.entry_name.config(state=state_)
        self.entry_director.config(state=state_)
        self.combobox_genre.config(state=state_)
        self.entry_duration.config(state=state_)
        self.checkbox_available.config(state=state_)

        # Enable/Disable button widgets
        self.button_save.config(state=state_)
        self.button_cancel.config(state=state_)
        if state_ == tk.DISABLED:
            self.button_edit.config(state=state_)
            self.button_delete.config(state=state_)

    @staticmethod
    def create():
        """
        Create tables in the database
        """
        try:
            # Initialize the counter of created tables
            counter_ = 0

            # Create genres table
            if Genres().create_table():
                counter_ += 1

            # Create movies table
            if Movies().create_table():
                counter_ += 1

            messagebox.showinfo('Information', f'{counter_} tables created successfully.')

        except Exception as e:
            messagebox.showerror('Error', f'{sys.exc_info()[0]}\n{str(e)}')

    @staticmethod
    def drop():
        """
        Drop tables from the database
        """
        try:
            # Confirm drop
            response_ = tk.messagebox.askquestion('Drop tables',
                                                  'Are you sure you want to drop the tables in Database?',
                                                  icon='warning')
            if response_ == 'yes':
                # Dropping confirmed, initialize counter of tables dropped
                counter_ = 0

                # Drop movies if exists
                if Movies().drop_table():
                    counter_ += 1

                # Drop genres if exists
                if Genres().drop_table():
                    counter_ += 1

                messagebox.showinfo('Information', f'{counter_} table(s) dropped.')

            else:
                messagebox.showinfo('Information', 'Dropping of tables canceled by user.')

        except Exception as e:
            messagebox.showerror('Error', f'{sys.exc_info()[0]}\n{str(e)}')


class MenuBar(tk.Menu):
    """
    Class of menu bar for the app. Inherits from tk.Menu.
    Visit: https://pythonguides.com/python-tkinter-menu-bar/
    """
    def __init__(self,
                 master_: Application):
        """
        Class constructor
        :param master_: top level window that will contain this menu bar
        """

        # Create menu bar associated to the app parent widget
        self.application = master_
        self.master = self.application.master
        tk.Menu.__init__(self, self.master)

        # Create a drop-down Home menu
        home_menu_ = tk.Menu(self, tearoff=False)
        home_menu_.add_command(label="Create tables", command=self.application.create)
        home_menu_.add_command(label="Drop tables", command=self.application.drop)
        home_menu_.add_separator()
        home_menu_.add_command(label="Exit", underline=1, command=self.quit)
        # Associate drop-down Home menu to the menu bar
        self.add_cascade(label="Home", underline=0, menu=home_menu_)

        # Create a drop-down Edit menu
        edit_menu_ = tk.Menu(self, tearoff=False)
        edit_menu_.add_command(label="Undo", command=lambda: __press_ctrl_plus('z'))
        edit_menu_.add_separator()
        edit_menu_.add_command(label="Cut", command=lambda: __press_ctrl_plus('x'))
        edit_menu_.add_command(label="Copy", command=lambda: __press_ctrl_plus('c'))
        edit_menu_.add_command(label="Paste", command=lambda: __press_ctrl_plus('v'))
        # Associate drop-down Edit menu to the menu bar
        self.add_cascade(label="Edit", menu=edit_menu_)

        # Create a drop-down Help menu
        help_menu_ = tk.Menu(self, tearoff=False)
        help_menu_.add_command(label="About", command=self.__about)
        # Associate drop-down Help menu to the menu bar
        self.add_cascade(label="Help", menu=help_menu_)

    @staticmethod
    def __about():
        messagebox.showinfo('About Movie Catalog',
                            f'Movie Catalog\n\nDeveloped to test a Fake Grid layout method '
                            f'based on a Real Place layout manager')


def __press_ctrl_plus(key_):
    """
    Simulates to press a key while holding <ctrl> key
    :param key_: key to press with the <ctrl> key
    """
    # Create keyboard controller to send hot-key programmatically (virtual keyboard events)
    keyboard = Controller()

    key_ = key_.lower()
    keyboard.press(Key.ctrl)
    keyboard.press(key_)
    keyboard.release(key_)
    keyboard.release(Key.ctrl)
