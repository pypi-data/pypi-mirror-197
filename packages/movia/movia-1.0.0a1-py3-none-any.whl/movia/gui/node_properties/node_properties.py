#!/usr/bin/env python3

"""
** Interactive window for a specific node properties. **
--------------------------------------------------------
"""

import inspect
import logging

from pdoc.html_helpers import to_html
from PyQt6 import QtCore, QtGui, QtWidgets

from movia.core.classes.container import ContainerInput, ContainerOutput
from movia.core.classes.filter import Filter
from movia.gui.base import MoviaWidget
from movia.gui.node_properties.container_input_ffmpeg import ContainerInputFFMPEGWidget
from movia.gui.node_properties.filter_truncate import FilterTruncateWidget
from movia.gui.node_properties.generator_video_equation import GeneratorVideoEquationWidget



SPECIFIC_PROPERTIES_WIDGET = {
    "ContainerInputFFMPEG": ContainerInputFFMPEGWidget,
    "FilterTruncate": FilterTruncateWidget,
    "GeneratorVideoEquation": GeneratorVideoEquationWidget,
}



class NodeDocumentation(MoviaWidget, QtWidgets.QWidget):
    """
    ** Extracts and formats the documentation for a node. **
    """

    def __init__(self, parent, node_name):
        super().__init__(parent)
        self._parent = parent
        self.node_name = node_name

        layout = QtWidgets.QVBoxLayout()
        self.init_documentation(layout)
        self.setLayout(layout)

    def init_documentation(self, layout):
        """
        ** Extracts the documentation and formats it for display. **
        """
        node = self.app.tree_node(self.node_name)
        font = QtGui.QFont("", -1)
        font.setFixedPitch(True)
        if not QtGui.QFontInfo(font).fixedPitch():
            logging.warning("no fixed pitch font found")

        main_doc = inspect.getdoc(node.__init__)
        main_doc = to_html(main_doc, latex_math=True)
        label_main = QtWidgets.QLabel(main_doc)
        label_main.setWordWrap(True)
        label_main.setFont(font)
        layout.addWidget(label_main)

        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)

        ex_doc = inspect.getdoc(node)
        ex_doc = to_html(ex_doc, latex_math=True)
        label_ex = QtWidgets.QLabel(ex_doc)
        label_ex.setWordWrap(True)
        label_ex.setFont(font)
        layout.addWidget(label_ex)


class GenericProperties(MoviaWidget, QtWidgets.QWidget):
    """
    ** General properties defined in all nodes. **
    """

    def __init__(self, parent, node_name):
        super().__init__(parent)
        self._parent = parent
        self.node_name = node_name

        grid_layout = QtWidgets.QGridLayout()
        self.init_properties(grid_layout)
        self.setLayout(grid_layout)

    def init_properties(self, grid_layout, ref_span=0):
        """
        ** Add the informations about the node properties. **
        """
        node = self.app.tree_node(self.node_name)

        # the title of the section
        title = QtWidgets.QLabel("General Node Properties")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        grid_layout.addWidget(title, ref_span, 0, 1, 2)
        ref_span += 1

        # the general type
        if issubclass(node.__class__, ContainerInput):
            grid_layout.addWidget(QtWidgets.QLabel("Type:"), ref_span, 0)
            grid_layout.addWidget(QtWidgets.QLabel("Input"), ref_span, 1)
            ref_span += 1
        elif issubclass(node.__class__, ContainerOutput):
            grid_layout.addWidget(QtWidgets.QLabel("Type:"), ref_span, 0)
            grid_layout.addWidget(QtWidgets.QLabel("Output"), ref_span, 1)
            ref_span += 1
        elif issubclass(node.__class__, Filter):
            grid_layout.addWidget(QtWidgets.QLabel("Type:"), ref_span, 0)
            grid_layout.addWidget(QtWidgets.QLabel("Filter"), ref_span, 1)
            ref_span += 1

        # all ancestors
        ancestors = " <-- ".join(c.__name__ for c in node.__class__.__mro__[-2::-1])
        grid_layout.addWidget(QtWidgets.QLabel("Ancestors:"), ref_span, 0)
        grid_layout.addWidget(QtWidgets.QLabel(ancestors), ref_span, 1)
        ref_span += 1

        # streams
        in_streams = sorted(
            self.app.graph.in_edges(self.node_name, data=False, keys=True),
            key=lambda src_dst_key: int(src_dst_key[2].split("->")[1])
        )
        out_streams = sorted(
            self.app.graph.out_edges(self.node_name, data=False, keys=True),
            key=lambda src_dst_key: int(src_dst_key[2].split("->")[0])
        )
        for streams, label in zip((in_streams, out_streams), ("Incoming", "Output")):
            if streams:
                grid_layout.addWidget(QtWidgets.QLabel(f"{label} Streams:"), ref_span, 0)
                for i, (src, dst, key) in enumerate(streams):
                    key = key.split('->')
                    grid_layout.addWidget(
                        QtWidgets.QLabel(
                            f"{src} (stream {key[0]}) -> {dst} (stream {key[1]})"
                        ),
                        ref_span+i,
                        1,
                    )
                ref_span += len(in_streams)

        return ref_span


class WindowNodeProperties(MoviaWidget, QtWidgets.QDialog):
    """
    ** Show the node properties. **
    """

    def __init__(self, parent, node_name):
        super().__init__(parent)
        self._parent = parent
        self.node_name = node_name

        layout = QtWidgets.QVBoxLayout()
        self.setWindowTitle(f"Node Properties ({node_name})")

        self.generic_properties = GenericProperties(self, node_name)
        layout.addWidget(self.generic_properties)

        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)

        self.specific_prop = self.init_specific(layout)

        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)

        title = QtWidgets.QLabel("Documentation")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        layout.addWidget(title)
        self.generic_properties = NodeDocumentation(self, node_name)
        scrollable_layout = QtWidgets.QScrollArea(self)
        scrollable_layout.setWidget(self.generic_properties)
        layout.addWidget(scrollable_layout)

        self.setLayout(layout)

    def init_specific(self, layout):
        """
        ** Choose and instantiate the right widget for this node's class. **
        """
        node = self.app.tree_node(self.node_name)
        title = QtWidgets.QLabel("Specific Node Properties")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        layout.addWidget(title)
        if (widget_class := SPECIFIC_PROPERTIES_WIDGET.get(node.__class__.__name__, None)) is None:
            for key, prop in node.getstate().items():
                layout.addWidget(QtWidgets.QLabel(f"{key} = {prop}"))
            return None
        specific_prop = widget_class(self, self.node_name)
        layout.addWidget(specific_prop)
        return specific_prop
