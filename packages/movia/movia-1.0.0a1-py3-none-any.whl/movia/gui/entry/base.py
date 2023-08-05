#!/usr/bin/env python3

"""
** Defines the global style and behavior of the tabs of the entries table. **
-----------------------------------------------------------------------------
"""

import importlib.machinery
import importlib.util
import inspect
import logging
import re
import typing

from PyQt6 import QtCore, QtGui, QtWidgets
import numpy as np

from movia.core.classes.node import Node
from movia.core.compilation.tree_to_graph import new_node
from movia.gui.base import MoviaWidget
from movia.utils import get_project_root



class Entry(MoviaWidget, QtWidgets.QListWidget):
    """
    ** Allows to visualize the entries and to unify some functionalities. **
    """

    def __init__(self,
        parent,
        sub_dirs: list[str],
        excluded_clsn: set[str],
        classnames: typing.Union[type, tuple[type]]
    ):
        """
        Parameters
        ----------
        sub_dirs : list[str]
            The name of the folders to explore from the ``movia/core/`` directory.
        excluded_clsn : set[str]
            All classes to be excluded from the widget.
        classnames : typing.Union[type, tuple[type]]
            Valid classes for object selection.
        """
        super().__init__(parent)
        self._parent = parent

        assert isinstance(sub_dirs, list), sub_dirs.__class__.__name__
        assert all(isinstance(e, str) for e in sub_dirs), sub_dirs
        assert isinstance(excluded_clsn, set), excluded_clsn.__class__.__name__
        assert all(isinstance(e, str) for e in excluded_clsn), excluded_clsn
        self.sub_dirs = sub_dirs
        self.excluded_clsn = excluded_clsn
        self.classnames = classnames

        self.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.setResizeMode(QtWidgets.QListView.ResizeMode.Adjust)
        self.setUniformItemSizes(True)
        self.setIconSize(QtCore.QSize(128, 128))

    def dragLeaveEvent(self, event):
        """
        ** Prepares for drop in other widgets.
        """
        if len(self.selectedItems()) != 1:
            logging.error("can drag and drop only one item, not %d", len(self.selectedItems()))
            self.app.global_vars["drag_an_drop"] = None
            event.ignore()
            return

        classname, path = [i.data(3) for i in self.selectedItems()].pop()
        mod_name = ".".join(("movia" / path.relative_to(get_project_root()).with_suffix("")).parts)
        spec = importlib.util.spec_from_loader(
            mod_name, importlib.machinery.SourceFileLoader(mod_name, str(path))
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        generator_cls = dict(inspect.getmembers(mod))[classname]
        node_name, attrs = new_node(self.app.graph, generator_cls.default())
        self.app.global_vars["drag_an_drop"] = (node_name, attrs)
        event.accept()

    def refresh(self):
        """
        ** Updates the display of the list. **
        """
        self.clear()

        # complete the elements
        elements = {}
        for filepath in (
            file for sub_dir in self.sub_dirs
            for file in (get_project_root()/"core"/sub_dir).rglob("*.py")
        ):
            spec = importlib.util.spec_from_file_location("foo", filepath)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for classname, node_cls in inspect.getmembers(mod):
                if (
                    inspect.isclass(node_cls)
                    and issubclass(node_cls, Node)
                    and issubclass(node_cls, self.classnames)
                    and classname not in self.excluded_clsn
                ):
                    widget_name = re.sub(r"(?!^)([A-Z]+)", r"_\1",classname).lower()
                    elements[widget_name] = (classname, filepath)

        # deletion of common name parts
        if len(elements) != 1:
            while len({n[0] for n in elements}) == 1:
                elements = {n[1:]: e for n, e in elements.items()}
            while len({n[-1] for n in elements}) == 1:
                elements = {n[:-1]: e for n, e in elements.items()}

        # append generator to the view
        for widget_name in sorted(elements):
            img = np.zeros((128, 128, 3), dtype=np.uint8)
            icon = QtGui.QIcon(QtGui.QPixmap(QtGui.QImage(
                img.data, img.shape[1], img.shape[0], 3*img.shape[1],
                QtGui.QImage.Format.Format_BGR888
            )))
            item = QtWidgets.QListWidgetItem(icon, widget_name, parent=self)
            item.setData(3, elements[widget_name]) # 0 for text, 1 for icon, 2 for text, 3 is free!
            self.addItem(item)
