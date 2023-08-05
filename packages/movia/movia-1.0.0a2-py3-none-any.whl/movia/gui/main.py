#!/usr/bin/env python3

"""
** Entry point of the graphic interface. **
-------------------------------------------
"""


import pathlib
import pickle
import typing

from PyQt6 import QtCore, QtWidgets

from movia.gui.actions import create_actions
from movia.gui.app.app import App
from movia.gui.base import MoviaWidget
from movia.gui.edition_tabs import EditionTabs
from movia.gui.entry_tabs import EntryTabs
from movia.gui.export.settings import WindowsExportSettings
from movia.gui.menu import fill_menu
from movia.gui.toolbar import MainToolBar
from movia.gui.video_viewer import VideoViewer



class MainWindow(MoviaWidget, QtWidgets.QMainWindow):
    """
    ** The main window for video editing interface. **
    """

    def __init__(self):
        super().__init__()
        self._parent = None

        self._app = App()

        self.actions = create_actions(self)

        # declaration
        self.setWindowTitle("Movia")
        self.sub_windows = {
            "toolbar": MainToolBar(self, self.actions),
            "entry_tabs": EntryTabs(self),
            "video_viewer": VideoViewer(self),
            "edition_tabs": EditionTabs(self),
        }
        fill_menu(self.menuBar(), self.actions)

        # location
        self.addToolBar(self.sub_windows["toolbar"])
        h_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal, self)
        h_splitter.addWidget(self.sub_windows["entry_tabs"])
        h_splitter.addWidget(self.sub_windows["video_viewer"])
        v_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical, self)
        v_splitter.addWidget(h_splitter)
        v_splitter.addWidget(self.sub_windows["edition_tabs"])
        self.setCentralWidget(v_splitter)

    @property
    def app(self):
        """
        ** Allows to rewrite this method of the parent class. **
        """
        return self._app

    def closeEvent(self, event):
        """
        ** Takes precautions before properly releasing resources. **
        """
        print("save")
        event.accept()

    def crash(self, msg):
        """
        ** Displays a critical error message. **
        """
        QtWidgets.QMessageBox.critical(None, "Application crashed", msg)

    def export(self):
        """
        ** Brings up the export window. **
        """
        WindowsExportSettings(self).exec()

    def load_project(self, project_file: typing.Union[str, pathlib.Path]):
        """
        ** Allows to open and load a file representing a project. **

        Parameters
        ----------
        project_file : pathlike
            The name or path of the file.
        """
        assert isinstance(project_file, (str, pathlib.Path)), project_file.__class__.__name__
        project_file = pathlib.Path(project_file)
        with project_file.open("rb") as file:
            app_state = pickle.load(file)
        self.app.__setstate__(app_state)
        self.refresh()

    def refresh(self):
        """
        ** Updates the elements of this widget and child widgets. **
        """
        self.sub_windows["entry_tabs"].refresh()
        self.sub_windows["video_viewer"].refresh()
        self.sub_windows["edition_tabs"].refresh()
