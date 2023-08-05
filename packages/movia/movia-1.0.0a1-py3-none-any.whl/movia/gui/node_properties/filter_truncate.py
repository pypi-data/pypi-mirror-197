#!/usr/bin/env python3

"""
** Properties of a ``movia.core.filter.basic.truncate.FilterTruncate``. **
--------------------------------------------------------------------------
"""

import fractions
import math

from PyQt6 import QtWidgets

from movia.gui.base import MoviaWidget



class FilterTruncateWidget(MoviaWidget, QtWidgets.QWidget):
    """
    ** Allows to view and modify the properties of a filter of type ``FilterTruncate``.
    """

    def __init__(self, parent, node_name):
        super().__init__(parent)
        self._parent = parent
        self.node_name = node_name
        self._duration_max_textbox = None

        grid_layout = QtWidgets.QGridLayout()
        self.init_duration_max(grid_layout)
        self.setLayout(grid_layout)

    def _validate_duration_max(self, text):
        """
        ** Check that the av kwargs are correct and update the color. **
        """
        duration_max = {"inf": math.inf, "oo": math.inf}.get(text, text)
        try:
            duration_max = fractions.Fraction(duration_max)
        except OverflowError:
            pass
        except ValueError:
            self._duration_max_textbox.setStyleSheet("background:red;")
            return
        else:
            duration_max = str(duration_max)

        backup_duration_max = self.app.graph.nodes[self.node_name]["state"]["duration_max"]
        self.app.graph.nodes[self.node_name]["state"]["duration_max"] = duration_max
        try:
            self.app.tree_node(self.node_name)
        except AssertionError as err:
            self.app.graph.nodes[self.node_name]["state"]["duration_max"] = backup_duration_max
            self._duration_max_textbox.setStyleSheet("background:red;")
            QtWidgets.QMessageBox.warning(
                None, "Invalid duration", f"Unable to change the duration {duration_max} : {err}"
            )
            return
        self._duration_max_textbox.setStyleSheet("background:none;")
        print(f"update duration_max of {self.node_name}: {duration_max}")
        self.main_window.refresh()

    def init_duration_max(self, grid_layout, ref_span=0):
        """
        ** Displays and allows to modify the av kwargs. **
        """
        state = self.app.graph.nodes[self.node_name]["state"]

        grid_layout.addWidget(QtWidgets.QLabel("Duration Max (second):"))
        self._duration_max_textbox = QtWidgets.QLineEdit()
        self._duration_max_textbox.setText(state["duration_max"])
        self._duration_max_textbox.textChanged.connect(self._validate_duration_max)
        grid_layout.addWidget(self._duration_max_textbox, ref_span, 1)
        ref_span += 1

        return ref_span
