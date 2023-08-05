#!/usr/bin/env python3

"""
** Defines the actions. **
--------------------------
"""

from PyQt6 import QtGui



def create_actions(parent) -> dict[str, QtGui.QAction]:
    """
    Returns
    -------
    actions : dict
        To each action name, associate the action PyQt ``QtGui.QAction``.
    """

    actions = {}

    actions["import"] = QtGui.QAction("Import Files...", parent)
    actions["import"].setIcon(QtGui.QIcon.fromTheme("list-add"))
    actions["import"].setShortcut("ctrl+f")
    actions["import"].triggered.connect(lambda: print("import"))

    actions["undo"] = QtGui.QAction("Undo", parent)
    actions["undo"].setIcon(QtGui.QIcon.fromTheme("edit-undo"))
    actions["undo"].setShortcut("ctrl+z")
    actions["undo"].triggered.connect(parent.app.undo)

    actions["redo"] = QtGui.QAction("Redo", parent)
    actions["redo"].setIcon(QtGui.QIcon.fromTheme("edit-redo"))
    actions["redo"].setShortcut("ctrl+y")
    actions["redo"].triggered.connect(parent.app.redo)

    actions["refresh"] = QtGui.QAction("Refresh", parent)
    actions["refresh"].setIcon(QtGui.QIcon.fromTheme("view-refresh"))
    actions["refresh"].setShortcut("F5")
    actions["refresh"].triggered.connect(parent.refresh)

    actions["export"] = QtGui.QAction("Export", parent)
    actions["export"].setIcon(QtGui.QIcon.fromTheme("media-record"))
    actions["export"].setShortcut("ctrl+e")
    actions["export"].triggered.connect(parent.export)

    return actions
