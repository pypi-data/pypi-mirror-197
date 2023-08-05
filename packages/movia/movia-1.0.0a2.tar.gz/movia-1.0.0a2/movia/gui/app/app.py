#!/usr/bin/env python3

"""
** Interface between windows and data. **
-----------------------------------------
"""

import pathlib
import threading
import typing

import networkx

from movia.core.classes.container import ContainerOutput
from movia.core.classes.node import Node
from movia.core.classes.stream import Stream
from movia.core.compilation.graph_to_tree import graph_to_tree, update_tree
from movia.core.compilation.tree_to_graph import tree_to_graph
from movia.core.filters.basic.truncate import FilterTruncate



class App:
    """
    ** Contains the shared data. **

    Attributes
    ----------
    export_settings : dict[str]
        The exportation parameters for ffmpeg.
    graph : networkx.MultiDiGraph
        The assembly graph, the main element that contains all the operations to be performed.
    project_files : list[str]
        All the paths of the imported files.
    """

    def __init__(self):
        self._persistant = {} # all for the state.
        self._compile_lock = threading.Lock()
        self._graph = tree_to_graph(ContainerOutput(FilterTruncate.default().out_streams))
        self.global_vars = {}

    def __getstate__(self) -> dict:
        """
        ** Allows to help serialization. **
        """
        return {
            "graph": self.graph,
            "project_files": self.project_files,
            "export_settings": self.export_settings
        }

    def __setstate__(self, state: dict):
        """
        ** Allows deserialization. **
        """
        assert isinstance(state, dict), state.__class__.__name__

        self.export_settings = state.get("export_settings", {})
        self.graph = state.get("graph", None)
        self.project_files = state.get("project_files", [])

    @property
    def export_settings(self) -> dict[str]:
        """
        ** The exporation parameters. **

        Notes
        -----
        * Modifications are inplace.
        * Need to replace the "default" values.
        """
        export_settings = self._persistant.get("export_settings", {})
        export_settings["parent"] = export_settings.get("parent", str(pathlib.Path.cwd()))
        if "stem" not in export_settings:
            export_settings["stem"] = "movia_project"
            while (pathlib.Path(export_settings["parent"]) / export_settings["stem"]).exists():
                export_settings["stem"] += "_bis"
        export_settings["suffix"] = export_settings.get("suffix", "")
        export_settings["muxer"] = export_settings.get("muxer", "default")
        export_settings["muxer_settings"] = export_settings.get("muxer_settings", {})
        export_settings["codecs"] = ( # list
            export_settings.get("codecs", ["default" for _ in self.tree().in_streams])
            [:len(self.tree().in_streams)]
        )
        export_settings["encoders"] = ( # list
            export_settings.get("encoders", ["default" for _ in self.tree().in_streams])
            [:len(self.tree().in_streams)]
        )
        export_settings["encoders_settings"] = ( # list
            export_settings.get("encoders_settings", [{} for _ in self.tree().in_streams])
            [:len(self.tree().in_streams)]
        )
        self._persistant["export_settings"] = export_settings # for inplace edition, not setter
        return export_settings

    @property
    def graph(self) -> networkx.MultiDiGraph:
        """
        ** The assembly graph. **
        """
        return self._graph

    @graph.setter
    def graph(self, graph: networkx.MultiDiGraph):
        """
        ** Performs verification. **
        """
        assert isinstance(graph, networkx.MultiDiGraph)
        with self._compile_lock:
            self._graph = graph

    @property
    def project_files(self) -> list[str]:
        """
        ** The list of absolute paths of the imported files. **
        """
        return self._persistant.get("project_files", [])

    @project_files.setter
    def project_files(self, values: list[typing.Union[str, pathlib.Path]]):
        """
        ** Performs verification and standardization. **
        """
        assert isinstance(values, list), values.__class__.__name__
        assert all(isinstance(p, (str, pathlib.Path)) for p in values), values

        # normalize paths
        project_files_ = [str(pathlib.Path(p).resolve()) for p in values]

        # removes redundancy by keeping the order
        red = set()
        project_files = []
        for path in project_files_:
            if path in red:
                continue
            red.add(path)
            project_files.append(path)
        self._persistant["project_files"] = project_files

    def tree(self) -> ContainerOutput:
        """
        ** Returns the node associated with the complete graph. **

        Returns
        -------
        container_output : movia.core.classes.container.ContainerOutput
            The terminal node of the assembly graph.
        """
        with self._compile_lock:
            container_output = graph_to_tree(self.graph)
        return container_output

    def tree_edge(self, edge: tuple[str, str, str]) -> Stream:
        """
        ** Returns the updated tree of this edge. **

        Parameters
        ----------
        edge : tuple[str, str, str]
            The name of the edge in the graph (src_node, dst_node, key).

        Returns
        -------
        Stream
            The dynamic tree corresponding to this edge.

        Notes
        -----
        All the ``tree`` attributes are updated to the current state of the assembly graph.
        """
        assert isinstance(edge, tuple), edge.__class__.__name__
        assert len(edge) == 3, edge
        for name in edge:
            assert isinstance(name, str), name.__class__.__name__
        with self._compile_lock:
            assert self.graph.has_edge(*edge)
            update_tree(self.graph)
            src, dst, key = edge
            tree = self.graph.edges[src, dst, key]["tree"]
        return tree

    def tree_node(self, node: str) -> Node:
        """
        ** Returns the updated tree of this node. **

        Parameters
        ----------
        node : str
            The name of the node in the graph.

        Returns
        -------
        movia.core.classes.node.Node
            The dynamic tree corresponding to this node.

        Notes
        -----
        All the ``tree`` attributes are updated to the current state of the assembly graph.
        """
        assert isinstance(node, str), node.__class__.__name__
        with self._compile_lock:
            assert node in self.graph
            update_tree(self.graph)
            tree = self.graph.nodes[node]["tree"]
        return tree

    def undo(self):
        """
        ** Return to the previous step. **
        """
        print("undo")

    def redo(self):
        """
        ** Allows you to move forward in the steps. **
        """
        print("redo")
