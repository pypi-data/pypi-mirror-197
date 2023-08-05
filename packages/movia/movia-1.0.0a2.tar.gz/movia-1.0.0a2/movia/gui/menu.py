#!/usr/bin/env python3

"""
** Used to configure the main menu. **
--------------------------------------
"""



def fill_menu(menu, actions):
    """
    ** Adds fields to the empty menu. **
    """

    file_menu = menu.addMenu("File")
    file_menu.addAction(actions["import"])
    file_menu.addAction(actions["export"])
    file_menu.addSeparator()

    edit_menu = menu.addMenu("Edit")
    edit_menu.addAction(actions["refresh"])
    edit_menu.addAction(actions["undo"])
    edit_menu.addAction(actions["redo"])
