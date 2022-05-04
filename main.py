# -*- coding: utf-8 -*-

__author__ = "Nestor D R"
__version__ = "0.0.1"
__license__ = "No license"

# --- Python modules ---
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
import sys
# tkinter: package (“Tk interface”) which is the standard Python interface to the Tcl/Tk GUI toolkit.
import tkinter as tk

# view: package with user interface elements
from view import gui


def main():
    # Create an instance of the Tk class, which is a top level window known as the root window
    root_ = tk.Tk()

    # Set window title, icon
    root_.title('Movie Catalog')
    root_.iconbitmap('assets/catalog_32.ico')

    # Set window width x height, in pixels
    # root_.geometry(f'{layout.DEFAULT_CONTAINER_WIDTH}x{layout.DEFAULT_CONTAINER_HEIGHT}')

    root_.resizable(False, False)

    # Create element container frame widget inside the root window
    main_app_ = gui.Application(root_)

    # Show everything on the display, and responds to user input until the program terminates.
    main_app_.mainloop()


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a file my_module.py, when executed as the main program, the __name__ attribute will be '__main__',
# however if it is used importing it from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    main()

    # Terminate normally
    sys.exit(0)
