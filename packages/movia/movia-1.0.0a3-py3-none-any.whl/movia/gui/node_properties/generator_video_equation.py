#!/usr/bin/env python3

"""
** Properties of a ``movia.core.generation.video.equation.GeneratorVideoEquation``. **
--------------------------------------------------------------------------------------
"""

from PyQt6 import QtWidgets

from movia.core.generation.video.equation import SYMBOLS, parse_color
from movia.gui.base import MoviaWidget



class GeneratorVideoEquationWidget(MoviaWidget, QtWidgets.QWidget):
    """
    ** Allows to view and modify the properties of a node of type ``GeneratorVideoEquation``.
    """

    def __init__(self, parent, node_name):
        super().__init__(parent)
        self._parent = parent
        self.node_name = node_name

        self.textboxs = [None, None, None]

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_shape(grid_layout)
        self.init_expr(grid_layout, ref_span=ref_span)
        self.setLayout(grid_layout)

    def _update_h(self, height):
        shape = self.app.graph.nodes[self.node_name]["state"]["shape"]
        new_shape = (height, shape[1])
        print(f"update height of {self.node_name}: {shape} -> {new_shape}")
        self.update_shape(new_shape)

    def _update_w(self, width):
        shape = self.app.graph.nodes[self.node_name]["state"]["shape"]
        new_shape = (shape[0], width)
        print(f"update width of {self.node_name}: {shape} -> {new_shape}")
        self.update_shape(new_shape)

    def _validate_b(self, text):
        return self.update_color(text, 0)

    def _validate_g(self, text):
        return self.update_color(text, 1)

    def _validate_r(self, text):
        return self.update_color(text, 2)

    def init_expr(self, grid_layout, ref_span=0):
        """
        ** Displays and allows to modify the equations. **
        """
        colors = ("Blue", "Green", "Red")
        state = self.app.graph.nodes[self.node_name]["state"]
        exprs = (str(state["b_expr"]), str(state["g_expr"]), str(state["r_expr"]))
        vals = (self._validate_b, self._validate_g, self._validate_r)
        for i, (color, expr, val) in enumerate(zip(colors, exprs, vals)):
            grid_layout.addWidget(QtWidgets.QLabel(f"{color} Expression:"), ref_span, 0)
            self.textboxs[i] = QtWidgets.QLineEdit()
            self.textboxs[i].setText(expr)
            self.textboxs[i].textChanged.connect(val)
            grid_layout.addWidget(self.textboxs[i], ref_span, 1)
            ref_span += 1
        return ref_span

    def init_shape(self, grid_layout, ref_span=0):
        """
        ** Allows to change the size of the images. **
        """
        shape = self.app.graph.nodes[self.node_name]["state"]["shape"]
        for val, label, action in zip(shape, ("Height", "Width"), (self._update_h, self._update_w)):
            grid_layout.addWidget(QtWidgets.QLabel(f"{label} Resolution:"), ref_span, 0)
            spinbox = QtWidgets.QSpinBox()
            spinbox.setMinimum(1)
            spinbox.setMaximum(2147483647) # maximum admissible limit
            spinbox.setSuffix(" pxl")
            spinbox.setValue(val)
            spinbox.valueChanged.connect(action)
            grid_layout.addWidget(spinbox, ref_span, 1)
            ref_span += 1

        return ref_span

    def update_color(self, text, color_index):
        """
        ** Check that the formula is correct and update the color. **
        """
        try:
            color = parse_color(text)
        except (SyntaxError, ZeroDivisionError):
            self.textboxs[color_index].setStyleSheet("background:red;")
            return
        if color.free_symbols - set(SYMBOLS.values()):
            self.textboxs[color_index].setStyleSheet("background:red;")
            return
        self.textboxs[color_index].setStyleSheet("background:none;")

        print(f"update color of {self.node_name}: {color}")
        color_key = ("b_expr", "g_expr", "r_expr")[color_index]
        self.app.graph.nodes[self.node_name]["state"][color_key] = str(color)
        self.main_window.refresh()

    def update_shape(self, new_shape: tuple[int, int]):
        """
        ** Propagates the shape change of this node. **
        """
        assert isinstance(new_shape, tuple), new_shape.__class__.__name__
        assert isinstance(new_shape[0], int), new_shape[0].__class__.__name__
        assert isinstance(new_shape[1], int), new_shape[1].__class__.__name__
        assert new_shape[0] >= 1, new_shape[0]
        assert new_shape[1] >= 1, new_shape[1]

        self.app.graph.nodes[self.node_name]["state"]["shape"] = new_shape
        self.main_window.refresh()
