#!/usr/bin/env python3

"""
** Interactive window for help to choose the export settings. **
----------------------------------------------------------------
"""


import ast
import logging
import multiprocessing.pool
import pathlib
import stat

import black
from PyQt6 import QtCore, QtGui, QtWidgets

from movia.core.compilation.export.compatibility import (CodecInfos, EncoderInfos, MuxerInfos,
    WriteInfos)
from movia.core.compilation.export.default import suggest_export_params
from movia.core.compilation.graph_to_ast import graph_to_ast
from movia.core.compilation.tree_to_graph import tree_to_graph
from movia.core.io.write import ContainerOutputFFMPEG
from movia.gui.base import MoviaWidget



class CodecComboBox(MoviaWidget, QtWidgets.QComboBox):
    """
    ** Lists the availables codecs. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.currentTextChanged.connect(self.text_changed)

        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)

    def text_changed(self, codec):
        """
        ** The action when a new codec is selected. **
        """
        if not codec: # for avoid catching self.clear()
            return

        index = self.parent.index
        if self.app.export_settings["codecs"][index] != codec:
            self.app.export_settings["codecs"][index] = codec
            print(f"update export codec ({index}): {self.app.export_settings['codecs'][index]}")
            if (
                codec == "default"
                or self.app.export_settings["encoders"][index] not in CodecInfos(codec).encoders
            ):
                self.parent.encoder_combo_box.text_changed("default")
            self.parent.parent.refresh()

    def refresh(self):
        """
        ** Updates the list with the available codecs. **
        """
        self.clear()
        index = self.parent.index
        self.addItem(self.app.export_settings["codecs"][index])
        if self.app.export_settings["codecs"][index] != "default":
            self.addItem("default")
        for codec in sorted(self.parent.available_codecs):
            if codec == self.app.export_settings["codecs"][index]:
                continue
            self.addItem(codec)


class ContainerSettings(MoviaWidget, QtWidgets.QWidget):
    """
    ** Settings of the container file. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._muxer_combo_box = None
        self._muxer_doc_set = None
        self._textbox = None
        self._muxers_cache = None

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_title(grid_layout)
        ref_span = self.init_filename(grid_layout, ref_span)
        ref_span = self.init_muxer_combo_box(grid_layout, ref_span)
        self.init_muxer_doc_set(grid_layout, ref_span)
        self.setLayout(grid_layout)

    def _validate_path(self, new_path):
        """
        ** Try to validate the new path if it is valid. **
        """
        try:
            self.update_path(new_path)
        except AssertionError:
            self._textbox.setStyleSheet("background:red;")
        else:
            self._textbox.setStyleSheet("background:none;")

    @property
    def available_muxers(self):
        """
        ** Set of muxers supporting the different types of streams, for a given codecs set. **
        """
        codecs_types = (
            {codec for codec in self.app.export_settings["codecs"] if codec != "default"},
            {stream.type for stream in self.app.tree().in_streams},
        )
        if self._muxers_cache is None or self._muxers_cache[0] != codecs_types:
            muxers = list(WriteInfos().muxers) # frozen the iteration order
            with multiprocessing.pool.ThreadPool() as pool:
                self._muxers_cache = (
                codecs_types,
                    {
                        muxer for muxer, ok in zip(
                            muxers,
                            pool.imap(
                                (lambda muxer: (
                                    codecs_types[1].issubset(set(MuxerInfos(muxer).default_codecs))
                                    and MuxerInfos(muxer).contains_codecs(codecs_types[0]))
                                ),
                                muxers
                            )
                        ) if ok
                    },
                )
        return self._muxers_cache[1]

    def filename_dialog(self):
        """
        ** Opens a window to choose a new file name. **
        """
        new_path, _ = QtWidgets.QFileDialog.getSaveFileName(self)
        if new_path:
            try:
                self.update_path(new_path)
            except AssertionError as err:
                QtWidgets.QMessageBox.warning(
                    None, "Invalid filename", f"Unable to change the filename {new_path} : {err}"
                )

    def init_filename(self, grid_layout, ref_span=0):
        """
        ** The field containing the file name. **
        """
        grid_layout.addWidget(QtWidgets.QLabel("Path:"), ref_span, 0)
        self._textbox = QtWidgets.QLineEdit(self)
        self._textbox.textChanged.connect(self._validate_path)
        grid_layout.addWidget(self._textbox, ref_span, 1)
        filename_button = QtWidgets.QPushButton(self)
        filename_button.setText("Select")
        filename_button.clicked.connect(self.filename_dialog)
        grid_layout.addWidget(filename_button, ref_span, 2)
        return ref_span + 1

    def init_muxer_combo_box(self, grid_layout, ref_span=0):
        """
        ** The name of the muxer container format. **
        """
        grid_layout.addWidget(QtWidgets.QLabel("Muxer:"), ref_span, 0)
        self._muxer_combo_box = MuxersComboBox(self)
        grid_layout.addWidget(self._muxer_combo_box, ref_span, 1, 1, 2)
        return ref_span + 1

    def init_muxer_doc_set(self, grid_layout, ref_span=0):
        """
        ** The name of the muxer container format. **
        """
        grid_layout.addWidget(QtWidgets.QLabel("Muxer Config:"), ref_span, 0)
        self._muxer_doc_set = MuxersDocSet(self)
        grid_layout.addWidget(self._muxer_doc_set, ref_span, 1, 1, 3)
        return ref_span + 1

    def init_title(self, grid_layout, ref_span=0):
        """
        ** The section title. **
        """
        title = QtWidgets.QLabel("Muxer Settings")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        grid_layout.addWidget(title, ref_span, 0, 1, 3)
        return ref_span + 1

    def refresh(self):
        """
        ** Updates the displayed informations. **
        """
        new_text = (
            f"{self.app.export_settings['parent']}/{self.app.export_settings['stem']}"
            f"{self.app.export_settings['suffix']}"
        )
        self._textbox.setStyleSheet("background:none;")
        self._textbox.setText(new_text)
        self._muxer_combo_box.refresh()
        self._muxer_doc_set.refresh()

    def update_path(self, new_path):
        """
        ** Check that the new path is correct and set the new path in the settings. **
        """
        assert isinstance(new_path, str), new_path.__class__.__name__
        new_path = pathlib.Path(new_path)
        assert not new_path.is_dir(), new_path
        assert new_path.parent.is_dir(), new_path
        assert new_path.suffix == "" or any(
            new_path.suffix == suf
            for mux in self.available_muxers
            for suf in MuxerInfos(mux).extensions
        ), f"suffix {new_path.suffix} not allow"

        modif = False

        if self.app.export_settings["parent"] != str(new_path.parent):
            modif = True
            self.app.export_settings["parent"] = str(new_path.parent)
            print(f"update export directory: {self.app.export_settings['parent']}")
        if self.app.export_settings["stem"] != new_path.stem:
            modif = True
            self.app.export_settings["stem"] = new_path.stem
            print(f"update export file stem: {self.app.export_settings['stem']}")
        if new_path.suffix != self.app.export_settings["suffix"]:
            modif = True
            self.app.export_settings["suffix"] = new_path.suffix
            print(f"update export suffix: {self.app.export_settings['suffix']}")
            if new_path.suffix:
                self.app.export_settings["muxer"] = MuxerInfos.from_suffix(new_path.suffix).name
                print(f"update export muxer: {self.app.export_settings['muxer']}")

        if modif:
            self.parent.refresh()


class EncoderComboBox(MoviaWidget, QtWidgets.QComboBox):
    """
    ** Lists the availables codecs. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.currentTextChanged.connect(self.text_changed)

        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)

    def text_changed(self, encoder):
        """
        ** The action when a new encoder is selected. **
        """
        if not encoder: # for avoid catching self.clear()
            return

        index = self.parent.index
        if self.app.export_settings["encoders"][index] != encoder:
            self.app.export_settings["encoders"][index] = encoder
            print(f"update export encoder ({index}): {self.app.export_settings['encoders'][index]}")
            if encoder != "default":
                self.parent.codec_combo_box.text_changed(EncoderInfos(encoder).codec)
            self.parent.parent.refresh()

    def refresh(self):
        """
        ** Updates the list with the available encoders. **
        """
        self.clear()
        index = self.parent.index
        self.addItem(self.app.export_settings["encoders"][index])
        if self.app.export_settings["encoders"][index] != "default":
            self.addItem("default")
        for encoder in sorted(self.parent.available_encoders):
            if encoder == self.app.export_settings["encoders"][index]:
                continue
            self.addItem(encoder)


class EncoderConfig(MoviaWidget, QtWidgets.QWidget):
    """
    ** Able to choose and edit the encoder for a given stream. **
    """

    def __init__(self, parent, stream):
        super().__init__(parent)
        self._parent = parent
        self.stream = stream

        self._codecs_cache = None
        self._encoders_cache = None
        self._encoder_doc_set = None
        self.codec_combo_box = None
        self.encoder_combo_box = None

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_title(grid_layout)
        ref_span = self.init_codec_combo_box(grid_layout, ref_span)
        ref_span = self.init_encoder_combo_box(grid_layout, ref_span)
        self.init_encoder_doc_set(grid_layout, ref_span)
        self.setLayout(grid_layout)

    @property
    def available_codecs(self):
        """
        ** Set of codecs supporting for this streams, for a given muxer and encoder. **
        """
        mux_enc = (
            self.app.export_settings["muxer"],
            self.app.export_settings["encoders"][self.index],
        )
        if self._codecs_cache is None or self._codecs_cache[0] != mux_enc:
            codecs = WriteInfos().codecs
            if mux_enc[1] != "default":
                codecs &= {EncoderInfos(mux_enc[1]).codec}
            if mux_enc[0] != "default":
                codecs &= MuxerInfos(mux_enc[0]).codecs
            codecs = {codec for codec in codecs if CodecInfos(codec).type == self.stream.type}
            self._codecs_cache = (mux_enc, codecs)
        return self._codecs_cache[1]

    @property
    def available_encoders(self):
        """
        ** Set of encoders supporting for this streams, for a given muxer and codec. **
        """
        mux_cod = (
            self.app.export_settings["muxer"],
            self.app.export_settings["codecs"][self.index],
        )
        if self._encoders_cache is None or self._encoders_cache[0] != mux_cod:
            encoders = WriteInfos().encoders
            if mux_cod[1] != "default":
                encoders &= CodecInfos(mux_cod[1]).encoders
            if mux_cod[0] != "default":
                encoders &= MuxerInfos(mux_cod[0]).encoders
            encoders = {
                encoder for encoder in encoders if EncoderInfos(encoder).type == self.stream.type
            }
            self._encoders_cache = (mux_cod, encoders)
        return self._encoders_cache[1]

    @property
    def index(self):
        """
        ** The input stream index of the container output. **
        """
        for index, stream in enumerate(self.app.tree().in_streams):
            if stream is self.stream:
                return index
        raise KeyError(f"the stream {self.stream} is missing in the container output")

    def init_codec_combo_box(self, grid_layout, ref_span=0):
        """
        ** The name of the codec. **
        """
        grid_layout.addWidget(QtWidgets.QLabel("Codec:"), ref_span, 0)
        self.codec_combo_box = CodecComboBox(self)
        grid_layout.addWidget(self.codec_combo_box, ref_span, 1, 1, 2)
        return ref_span + 1

    def init_encoder_combo_box(self, grid_layout, ref_span=0):
        """
        ** The name of the encoder. **
        """
        grid_layout.addWidget(QtWidgets.QLabel("Encoder:"), ref_span, 0)
        self.encoder_combo_box = EncoderComboBox(self)
        grid_layout.addWidget(self.encoder_combo_box, ref_span, 1, 1, 2)
        return ref_span + 1

    def init_encoder_doc_set(self, grid_layout, ref_span=0):
        """
        ** The name of the encoder container format. **
        """
        grid_layout.addWidget(QtWidgets.QLabel("Encoder Config:"), ref_span, 0)
        self._encoder_doc_set = EncoderDocSet(self)
        grid_layout.addWidget(self._encoder_doc_set, ref_span, 1, 1, 3)
        return ref_span + 1

    def init_title(self, grid_layout, ref_span=0):
        """
        ** The section title. **
        """
        title = QtWidgets.QLabel(f"Stream {self.index} Encoder Settings ({self.stream.type})")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        grid_layout.addWidget(title, ref_span, 0, 1, 3)
        return ref_span + 1

    def refresh(self):
        """
        ** Updates the displayed informations. **
        """
        self.codec_combo_box.refresh()
        self.encoder_combo_box.refresh()
        self._encoder_doc_set.refresh()


class EncoderDocSet(MoviaWidget, QtWidgets.QWidget):
    """
    ** Allows append special params for the selected encoder. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self._doc_label = None
        self._settings_label = None
        self._settings_textbox = None

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_doc(grid_layout)
        self.init_settings(grid_layout, ref_span)
        self.setLayout(grid_layout)

    def _validate_settings(self, settings):
        """
        ** Set the new settings. **
        """
        groups = settings.split(",")
        sub_groups = [g.split("=") for g in groups]
        if any(len(sg) != 2 for sg in sub_groups):
            self._settings_textbox.setStyleSheet("background:red;")
            return
        index = self.parent.index
        doc = EncoderInfos(self.app.export_settings["encoders"][index]).doc
        settings = dict(sub_groups)
        if any(k not in doc for k in settings):
            self._settings_textbox.setStyleSheet("background:red;")
            return

        self._settings_textbox.setStyleSheet("background:none;")
        self.app.export_settings["encoders_settings"][index] = settings
        print(
            f"update export encoders settings ({index}): "
            f"{self.app.export_settings['encoders_settings'][index]}"
        )

    def init_doc(self, grid_layout, ref_span=0):
        """
        ** The field containing the documentation of the encoder. **
        """
        self._doc_label = QtWidgets.QLabel()
        scrollable_layout = QtWidgets.QScrollArea(self)
        scrollable_layout.setWidgetResizable(True)
        scrollable_layout.setWidget(self._doc_label)
        grid_layout.addWidget(scrollable_layout, ref_span, 0, 1, 2)
        return ref_span + 1

    def init_settings(self, grid_layout, ref_span=0):
        """
        ** The custom parameters. **
        """
        self._settings_label = QtWidgets.QLabel("Custom Settings:")
        self._settings_label.hide()
        grid_layout.addWidget(self._settings_label, ref_span, 0)
        self._settings_textbox = QtWidgets.QLineEdit(self)
        self._settings_textbox.textChanged.connect(self._validate_settings)
        self._settings_textbox.hide()
        grid_layout.addWidget(self._settings_textbox, ref_span, 1)
        return ref_span + 1

    def refresh(self):
        # refresh documentation
        index = self.parent.index
        if self.app.export_settings["encoders"][index] == "default":
            doc = "To configure more parameters, you have to select a specific encoder."
            font = QtGui.QFont()
        else:
            doc = EncoderInfos(self.app.export_settings["encoders"][index]).doc
            font = QtGui.QFont("", -1)
            font.setFixedPitch(True)
            if not QtGui.QFontInfo(font).fixedPitch():
                logging.warning("no fixed pitch font found")
        self._doc_label.setFont(font)
        self._doc_label.setText(doc)

        # refresh setting entry
        if self.app.export_settings["encoders"][index] == "default":
            self._settings_label.hide()
            self._settings_textbox.hide()
        else:
            self._settings_label.show()
            self._settings_textbox.show()


class MuxersComboBox(MoviaWidget, QtWidgets.QComboBox):
    """
    ** Lists the availables muxers. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.currentTextChanged.connect(self.text_changed)

        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)

    def text_changed(self, muxer):
        """
        ** The action when a new muxer is selected. **
        """
        if not muxer: # for avoid catching self.clear()
            return

        if self.app.export_settings["muxer"] != muxer:
            self.app.export_settings["muxer"] = muxer
            print(f"update export muxer: {self.app.export_settings['muxer']}")
            if muxer != "default":
                suffix = sorted(MuxerInfos(muxer).extensions)
                suffix = suffix.pop(0) if len(suffix) >= 1 else ""
            else:
                suffix = ""
            if self.app.export_settings["suffix"] != suffix:
                self.app.export_settings["suffix"] = suffix
                print(f"update export suffix: {self.app.export_settings['suffix']}")
            self.parent.parent.refresh()

    def refresh(self):
        """
        ** Updates the list with the available muxers. **
        """
        self.clear()
        self.addItem(self.app.export_settings["muxer"])
        if self.app.export_settings["muxer"] != "default":
            self.addItem("default")
        for muxer in sorted(self.parent.available_muxers):
            if muxer == self.app.export_settings["muxer"]:
                continue
            self.addItem(muxer) # audio-x-generic, QtGui.QIcon.fromTheme("video-x-generic")


class MuxersDocSet(MoviaWidget, QtWidgets.QWidget):
    """
    ** Allows append special params for the selected muxer. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self._doc_label = None
        self._settings_label = None
        self._settings_textbox = None

        grid_layout = QtWidgets.QGridLayout()
        ref_span = self.init_doc(grid_layout)
        self.init_settings(grid_layout, ref_span)
        self.setLayout(grid_layout)

    def _validate_settings(self, settings):
        """
        ** Set the new settings. **
        """
        groups = settings.split(",")
        sub_groups = [g.split("=") for g in groups]
        if any(len(sg) != 2 for sg in sub_groups):
            self._settings_textbox.setStyleSheet("background:red;")
            return
        doc = MuxerInfos(self.app.export_settings["muxer"]).doc
        settings = dict(sub_groups)
        if any(k not in doc for k in settings):
            self._settings_textbox.setStyleSheet("background:red;")
            return

        self._settings_textbox.setStyleSheet("background:none;")
        self.app.export_settings["muxer_settings"] = settings
        print(f"update export muxer settings: {self.app.export_settings['muxer_settings']}")

    def init_doc(self, grid_layout, ref_span=0):
        """
        ** The field containing the documentation of the muxer. **
        """
        self._doc_label = QtWidgets.QLabel()
        scrollable_layout = QtWidgets.QScrollArea(self)
        scrollable_layout.setWidgetResizable(True)
        scrollable_layout.setWidget(self._doc_label)
        grid_layout.addWidget(scrollable_layout, ref_span, 0, 1, 2)
        return ref_span + 1

    def init_settings(self, grid_layout, ref_span=0):
        """
        ** The custom parameters. **
        """
        self._settings_label = QtWidgets.QLabel("Custom Settings:")
        self._settings_label.hide()
        grid_layout.addWidget(self._settings_label, ref_span, 0)
        self._settings_textbox = QtWidgets.QLineEdit(self)
        self._settings_textbox.textChanged.connect(self._validate_settings)
        self._settings_textbox.hide()
        grid_layout.addWidget(self._settings_textbox, ref_span, 1)
        return ref_span + 1

    def refresh(self):
        # refresh documentation
        if self.app.export_settings["muxer"] == "default":
            doc = "To configure more parameters, you have to select a specific muxer."
            font = QtGui.QFont()
        else:
            doc = MuxerInfos(self.app.export_settings["muxer"]).doc
            font = QtGui.QFont("", -1)
            font.setFixedPitch(True)
            if not QtGui.QFontInfo(font).fixedPitch():
                logging.warning("no fixed pitch font found")
        self._doc_label.setFont(font)
        self._doc_label.setText(doc)

        # refresh setting entry
        if self.app.export_settings["muxer"] == "default":
            self._settings_label.hide()
            self._settings_textbox.hide()
        else:
            self._settings_label.show()
            self._settings_textbox.show()


class WindowsExportSettings(MoviaWidget, QtWidgets.QDialog):
    """
    ** Show the exportation settings. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._container_settings = None
        self._encoders = []

        self.setWindowTitle("Export settings")

        layout = QtWidgets.QVBoxLayout()
        self.init_container(layout)
        self.init_encoders(layout)
        self.init_next(layout)
        self.setLayout(layout)

        self.refresh()

    def export(self):
        """
        ** Compile to python, close main windows and excecute the new file. **
        """
        self.accept()
        streams = self.app.tree().in_streams
        filename, streams_settings, container_settings = suggest_export_params(
            streams,
            filename=(
                pathlib.Path(self.app.export_settings["parent"]) / self.app.export_settings["stem"]
            ),
            muxer=self.app.export_settings["muxer"],
            encodecs=[
                c if e == "default" else e
                for c, e in zip(
                    self.app.export_settings["codecs"], self.app.export_settings["encoders"]
                )
            ],
        )
        tree = ContainerOutputFFMPEG(
            streams,
            filename=filename,
            streams_settings=streams_settings,
            container_settings=container_settings,
        )
        code = ast.unparse(graph_to_ast(tree_to_graph(tree)))
        code = "#!/usr/bin/env python3\n" + code
        code = black.format_str(code, mode=black.Mode())

        # write file and give execution permission
        filename = filename.with_suffix(".py")
        with open(filename, "w", encoding="utf-8") as code_file:
            code_file.write(code)
        filename.chmod(filename.stat().st_mode | stat.S_IEXEC)

        # close
        self.main_window.close()

    def init_container(self, layout):
        """
        ** General configuration of the container. **
        """
        self._container_settings = ContainerSettings(self)
        layout.addWidget(self._container_settings)

    def init_encoder(self, layout, stream):
        """
        ** Initialisation for a given stream. **
        """
        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)
        encoder = EncoderConfig(self, stream)
        layout.addWidget(encoder)
        self._encoders.append(encoder)

    def init_encoders(self, layout):
        """
        ** Specific encoding for each streams. **
        """
        for stream in self.app.tree().in_streams:
            self.init_encoder(layout, stream)

    def init_next(self, layout):
        """
        ** The button for the next stape. **
        """
        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)
        button = QtWidgets.QPushButton("Let's Go!")
        button.clicked.connect(self.export)
        layout.addWidget(button)

    def refresh(self):
        self._container_settings.refresh()
        for enc in self._encoders:
            enc.refresh()
