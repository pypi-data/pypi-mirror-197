#!/usr/bin/env python3

"""
** Definition of the toolbar. **
--------------------------------
"""

from PyQt6 import QtWidgets

from movia.gui.base import MoviaWidget



class MainToolBar(MoviaWidget, QtWidgets.QToolBar):
    """
    ** Main window menu bar. **
    """

    def __init__(self, parent, actions):
        super().__init__(parent)
        self._parent = parent

        # location
        self.addAction(actions["refresh"])
        self.addAction(actions["undo"])
        self.addAction(actions["redo"])

        self.addSeparator()

        self.addAction(actions["export"])
