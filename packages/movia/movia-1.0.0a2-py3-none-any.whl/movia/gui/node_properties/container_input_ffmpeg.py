#!/usr/bin/env python3

"""
** Properties of a ``movia.core.io.read.ContainerInputFFMPEG``. **
------------------------------------------------------------------
"""

import json
import pathlib

from PyQt6 import QtWidgets

from movia.core.analysis.streams import get_streams_type
from movia.gui.base import MoviaWidget



class ContainerInputFFMPEGWidget(MoviaWidget, QtWidgets.QWidget):
    """
    ** Allows to view and modify the properties of a node of type ``ContainerInputFFMPEG``.
    """

    def __init__(self, parent, node_name):
        super().__init__(parent)
        self._parent = parent
        self.node_name = node_name
        self._filename_av_kwargs = None
        self._filename_textbox = None

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_path(grid_layout)
        self.init_av_kwargs(grid_layout, ref_span=ref_span)
        self.setLayout(grid_layout)

    def _validate_av_kwargs(self, text):
        """
        ** Check that the av kwargs are correct and update the color. **
        """
        try:
            av_kwargs = json.loads(text)
        except json.JSONDecodeError:
            self._av_kwargs_textbox.setStyleSheet("background:red;")
            return
        if not all(isinstance(k, str) for k in av_kwargs):
            self._av_kwargs_textbox.setStyleSheet("background:red;")
            return

        backup_av_kwargs = self.app.graph.nodes[self.node_name]["state"]["av_kwargs"]
        self.app.graph.nodes[self.node_name]["state"]["av_kwargs"] = av_kwargs
        try:
            for stream in self.app.tree_node(self.node_name).out_streams:
                stream.snapshot(0) # forced to decode a frame to check for possible errors
        except (AssertionError, TypeError) as err:
            self.app.graph.nodes[self.node_name]["state"]["av_kwargs"] = backup_av_kwargs
            self._av_kwargs_textbox.setStyleSheet("background:red;")
            QtWidgets.QMessageBox.warning(
                None, "Invalid arguments", f"Unable to change the arguments {av_kwargs} : {err}"
            )
            return

        self._av_kwargs_textbox.setStyleSheet("background:none;")
        print(f"update av kwargs of {self.node_name}: {av_kwargs}")
        self.main_window.refresh()

    def _validate_filename(self, text):
        """
        ** Check that the filename is correct and update the color. **
        """
        path = pathlib.Path(text)
        if not path.is_file():
            self._filename_textbox.setStyleSheet("background:red;")
            return
        if not get_streams_type(path, ignore_errors=True):
            self._filename_textbox.setStyleSheet("background:red;")
            return

        backup_filename = self.app.graph.nodes[self.node_name]["state"]["filename"]
        self.app.graph.nodes[self.node_name]["state"]["filename"] = str(path)
        try:
            self.app.tree()
        except AssertionError as err:
            self.app.graph.nodes[self.node_name]["state"]["filename"] = backup_filename
            self._filename_textbox.setStyleSheet("background:red;")
            QtWidgets.QMessageBox.warning(
                None, "Renaming not permitted", f"Unable to change the filename {path} : {err}"
            )
            return

        self._filename_textbox.setStyleSheet("background:none;")
        print(f"update filename of {self.node_name}: {path}")
        self.main_window.refresh()

    def init_av_kwargs(self, grid_layout, ref_span=0):
        """
        ** Displays and allows to modify the av kwargs. **
        """
        state = self.app.graph.nodes[self.node_name]["state"]

        grid_layout.addWidget(QtWidgets.QLabel("PyAv parameters (json):"))
        self._av_kwargs_textbox = QtWidgets.QLineEdit()
        self._av_kwargs_textbox.setText(json.dumps(state["av_kwargs"], sort_keys=True))
        self._av_kwargs_textbox.textChanged.connect(self._validate_av_kwargs)
        grid_layout.addWidget(self._av_kwargs_textbox, ref_span, 1)
        ref_span += 1

        return ref_span

    def init_path(self, grid_layout, ref_span=0):
        """
        ** Displays and allows to modify the filename. **
        """
        state = self.app.graph.nodes[self.node_name]["state"]

        grid_layout.addWidget(QtWidgets.QLabel("File Path:"), ref_span, 0)
        self._filename_textbox = QtWidgets.QLineEdit()
        self._filename_textbox.setText(state["filename"])
        self._filename_textbox.textChanged.connect(self._validate_filename)
        grid_layout.addWidget(self._filename_textbox, ref_span, 1)
        ref_span += 1

        return ref_span
