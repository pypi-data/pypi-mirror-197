#!/usr/bin/env python3

"""
** Compile an assembly graph into an evaluable source code of tree **
---------------------------------------------------------------------
"""

import ast
import inspect
import pathlib
import re
import unidecode

import networkx

from movia.core.classes.node import Node
from movia.utils import get_project_root



def _node_to_ast(
    node_name: str, graph: networkx.MultiDiGraph
) -> tuple[ast.FunctionDef, list[ast.ImportFrom]]:
    """
    ** Creates the ast Function of this node. **

    Parameters
    ----------
    node_name : str
        The node name to compile.
    graph : networkx.MultiDiGraph
        The assembly graph.

    Returns
    -------
    func : ast.FunctionDef
        The ast fonction corresponding to the part of this branch,
        including the fourch node or the input node.
    modules : list[ast.ImportFrom]
        The movia modules requiers for this branch.

    Notes
    -----
    * No check for performances reasons.
    * Input / Ouput pickalisable, no modification inplace for alow parralelisation.

    Examples
    --------
    >>> import ast
    >>> from movia.core.classes.container import ContainerOutput
    >>> from movia.core.compilation.graph_to_ast import _node_to_ast
    >>> from movia.core.compilation.tree_to_graph import tree_to_graph
    >>> from movia.core.filters.basic.truncate import FilterTruncate
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>>
    >>> gen = GeneratorAudioNoise.default()
    >>> filter_2 = FilterTruncate(gen.out_streams, 10)
    >>> filter_1 = FilterTruncate(filter_2.out_streams, 1)
    >>> graph = tree_to_graph(ContainerOutput(filter_1.out_streams))
    >>>
    >>> func, modules = _node_to_ast("container_output_1", graph)
    >>> print(ast.unparse(func))
    def get_container_output_1(filter_truncate_1: Node) -> ContainerOutput:
        container_output_1 = ContainerOutput.__new__(ContainerOutput)
        container_output_1.setstate([filter_truncate_1.out_streams[0]], state={})
        return container_output_1
    >>> func, modules = _node_to_ast("filter_truncate_1", graph)
    >>> print(ast.unparse(func))
    def get_filter_truncate_1(filter_truncate_2: Node) -> FilterTruncate:
        filter_truncate_1 = FilterTruncate.__new__(FilterTruncate)
        filter_truncate_1.setstate([filter_truncate_2.out_streams[0]], state={'duration_max': '1'})
        return filter_truncate_1
    >>> func, modules = _node_to_ast("generator_audio_noise_1", graph)
    >>> print(ast.unparse(func))
    def get_generator_audio_noise_1() -> GeneratorAudioNoise:
        generator_audio_noise_1 = GeneratorAudioNoise.__new__(GeneratorAudioNoise)
        generator_audio_noise_1.setstate([], state={'seed': 0.0})
        return generator_audio_noise_1
    >>>
    """
    modules = []
    body = []
    name = _node_name_to_var_name(node_name)

    # typing annotaion returns type
    returns = ast.Name(id=graph.nodes[node_name]["class"].__name__, ctx=ast.Load())
    modules.append(_class_to_ast(graph.nodes[node_name]["class"]))

    # node creation statement
    in_var_index = [
        (_node_name_to_var_name(src), int(key.split("->")[0]))
        for src, _, key in graph.in_edges(node_name, keys=True)
    ]
    state = ast.parse(repr(graph.nodes[node_name]["state"]), mode="eval").body
    body.append(
        ast.Assign(
            targets=[ast.Name(id=node_name, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=graph.nodes[node_name]["class"].__name__, ctx=ast.Load()),
                    attr="__new__",
                    ctx=ast.Load(),
                ),
                args=[ast.Name(id=graph.nodes[node_name]["class"].__name__, ctx=ast.Load())],
                keywords=[],
            ),
            lineno=0, # fix AttributeError: 'Assign' object has no attribute 'lineno'
        )
    )
    body.append(
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=node_name, ctx=ast.Load()),
                    attr="setstate",
                    ctx=ast.Load(),
                ),
                args=[
                    ast.List(
                        elts=[
                            ast.Subscript(
                                value=ast.Attribute(
                                    value=ast.Name(id=var, ctx=ast.Load()),
                                    attr="out_streams",
                                    ctx=ast.Load()
                                ),
                                slice=ast.Constant(value=ind),
                                ctx=ast.Load()
                            )
                            for var, ind in in_var_index
                        ],
                        ctx=ast.Load(),
                    )
                ],
                keywords=[ast.keyword(arg="state", value=state)],
            ),
            type_ignores=[],
        )
    )

    # return statement
    body.append(
        ast.Return(value=ast.Name(id=name, ctx=ast.Load()))
    )

    # input args
    args = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg=node, annotation=ast.Name(id="Node", ctx=ast.Load()))
            for node in sorted({n for n, _ in in_var_index})
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )
    modules.append(_class_to_ast(Node))
    func = ast.FunctionDef(
        name=f"get_{name}",
        args=args,
        body=body,
        decorator_list=[],
        returns=returns,
        lineno=0, # fix AttributeError: 'FunctionDef' object has no attribute 'lineno'
    )
    return func, modules


def _class_to_ast(cls: type) -> ast.ImportFrom:
    """
    ** Localise the position of the class and parse the location. **

    Parameters
    ----------
    cls : type
        The class to import.

    Returns
    -------
    imp : ast.ImportFrom
        The parsed location of this class in the movia module.

    Raises
    ------
    TypeError
        If the class is not a movia accessible class.

    Examples
    --------
    >>> import ast
    >>> from movia.core.compilation.graph_to_ast import _class_to_ast
    >>> from movia.core.classes.node import Node
    >>> print(ast.unparse(_class_to_ast(Node)))
    from movia.core.classes.node import Node
    >>>
    """
    if (source := inspect.getsourcefile(cls)) is None:
        raise TypeError(f"impossible to locate {cls}")
    source = pathlib.Path(source).resolve()
    root = get_project_root()
    if not source.is_relative_to(root):
        raise TypeError(f"class {cls} ({source}) is not a movia class ({root})")
    rel_source = "movia" / source.relative_to(root)
    rel_source = rel_source.with_suffix("")
    imp = ast.ImportFrom(
        module=".".join(rel_source.parts), names=[ast.alias(cls.__name__)], level=0
    )
    return imp


def _mod_sort_factor(mods: list[ast.ImportFrom]) -> list[ast.ImportFrom]:
    """
    ** Sorting and factoring an import group. **

    Parameters
    ----------
    mods : list[ast.ImportFrom]
        All modules to be processed, there may be redundancy.

    Returns
    -------
    list[ast.ImportFrom]
        An equivalent sorted and compacted version. The order can be changed.

    Notes
    -----
    This algorithm is in o(n*log(n)).

    Examples
    --------
    >>> import ast
    >>> from pprint import pprint
    >>> from movia.core.compilation.graph_to_ast import _mod_sort_factor
    >>> mods = [
    ...     ast.ImportFrom(module="a.b", names=[ast.alias("f_1")], level=0),
    ...     ast.ImportFrom(module="b", names=[ast.alias("f_2")], level=0),
    ...     ast.ImportFrom(module="b", names=[ast.alias("f_1")], level=0),
    ...     ast.ImportFrom(module="a", names=[ast.alias("f_1")], level=0),
    ...     ast.ImportFrom(module="a", names=[ast.alias("f_2")], level=0),
    ...     ast.ImportFrom(module="a", names=[ast.alias("f_2")], level=0),
    ...     ast.ImportFrom(module="a", names=[ast.alias("f_3"), ast.alias("f_4")], level=0),
    ... ]
    >>> pprint([ast.dump(mod) for mod in _mod_sort_factor(mods)])
    ["ImportFrom(module='a', names=[alias(name='f_1'), alias(name='f_2'), "
     "alias(name='f_3'), alias(name='f_4')], level=0)",
     "ImportFrom(module='a.b', names=[alias(name='f_1')], level=0)",
     "ImportFrom(module='b', names=[alias(name='f_1'), alias(name='f_2')], "
     'level=0)']
    >>>
    """
    assert all(isinstance(mod, ast.ImportFrom) for mod in mods), mods
    assert all(mod.level == 0 for mod in mods), [mod.level for mod in mods]

    mods_as_dict = {}
    for mod in mods:
        mods_as_dict[mod.module] = mods_as_dict.get(mod.module, set())
        mods_as_dict[mod.module].update(
            {
                (alias.name, alias.asname) if alias.asname is not None else (alias.name,)
                for alias in mod.names
            }
        )
    compact_mods = [
        ast.ImportFrom(
            module=module,
            names=[ast.alias(*al) for al in sorted(mods_as_dict[module])],
            level=0, # fix python3.9 ast.unparse: TypeError
        )
        for module in sorted(mods_as_dict)
    ]
    return compact_mods


def _node_name_to_var_name(name: str) -> str:
    """
    ** Converts any string in correct snake case func name style. **

    Parameters
    ----------
    name : str
        The generical non empty name.

    Returns
    -------
    func_name
        The normalized name in chamel case.

    Examples
    --------
    >>> from movia.core.compilation.graph_to_ast import _node_name_to_var_name
    >>> _node_name_to_var_name("Éléphant  2spaceCamelCase_snake__To")
    'elephant_2space_camel_case_snake_to'
    >>> _node_name_to_var_name("0")
    '_0'
    >>>
    """
    assert isinstance(name, str), name.__class__.__name__
    assert not re.fullmatch(r"\s", name), f"name have to contains printable caracters {repr(name)}"

    name = unidecode.unidecode(name) # remove accents
    name = re.sub(r"(?!^)([A-Z]+)", r"_\1", name).lower() # snake case
    name = name.replace(" ", "_")
    while "__" in name:
        name = name.replace("__", "_")
    if name[0].isdigit():
        name = "_" + name
    return name


def graph_to_ast(graph: networkx.MultiDiGraph) -> ast.Module:
    """
    ** Creates the complete source code module from the assembly graph. **

    Parameters
    ----------
    graph : networkx.MultiDiGraph
        The assembly graph.

    Returns
    -------
    module : ast.Module
        The syntaxical graph of an equivalent code.
        The function ``get_complete_tree`` returns the graph.

    Examples
    --------
    >>> import ast
    >>> from movia.core.classes.container import ContainerOutput
    >>> from movia.core.compilation.graph_to_ast import graph_to_ast
    >>> from movia.core.compilation.tree_to_graph import tree_to_graph
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>> graph = tree_to_graph(ContainerOutput(GeneratorAudioNoise.default().out_streams))
    >>> graph_to_ast(graph) # doctest: +ELLIPSIS
    <ast.Module object at ...>
    >>> print(ast.unparse(_))
    from movia.core.classes.container import ContainerOutput
    from movia.core.classes.node import Node
    from movia.core.generation.audio.noise import GeneratorAudioNoise
    <BLANKLINE>
    def get_container_output_1(generator_audio_noise_1: Node) -> ContainerOutput:
        container_output_1 = ContainerOutput.__new__(ContainerOutput)
        container_output_1.setstate([generator_audio_noise_1.out_streams[0]], state={})
        return container_output_1
    <BLANKLINE>
    def get_generator_audio_noise_1() -> GeneratorAudioNoise:
        generator_audio_noise_1 = GeneratorAudioNoise.__new__(GeneratorAudioNoise)
        generator_audio_noise_1.setstate([], state={'seed': 0.0})
        return generator_audio_noise_1
    <BLANKLINE>
    def get_complete_tree() -> ContainerOutput:
        generator_audio_noise_1 = get_generator_audio_noise_1()
        container_output_1 = get_container_output_1(generator_audio_noise_1)
        return container_output_1
    if __name__ == '__main__':
        get_complete_tree().write()
    >>>
    """
    assert isinstance(graph, networkx.MultiDiGraph), graph.__class__.__name__

    body = []
    imps = []

    sequence = [] # index 0 -> bottom, output, index final -> top
    for node in sorted(graph): # sorted for repetability
        func, imp = _node_to_ast(node, graph)
        body.append(func)
        imps.extend(imp)

        # locate func call position in an executable sequence order o(n**2)
        out_var = _node_name_to_var_name(node)
        ref = 0
        for i, (_, args, _) in enumerate(sequence):
            if out_var in args: # if func[i] input need curent node func output
                ref = i + 1
        sequence.insert(ref, (func, {ast_arg.arg for ast_arg in func.args.args}, out_var))

    # import management and simplification
    imps = _mod_sort_factor(imps)
    body = imps + body

    # main func management
    tree_body = []
    for func, args, out_var in sequence:
        tree_body.insert(
            0,
            ast.Assign(
                targets=[ast.Name(id=out_var, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id=func.name, ctx=ast.Load()),
                    args=[ast.Name(id=arg, ctx=ast.Load()) for arg in sorted(args)],
                    keywords=[],
                ),
            ),
        )
    tree_body.append(ast.Return(value=ast.Name(id=sequence[0][2], ctx=ast.Load())))
    body.append(
        ast.FunctionDef(
            name="get_complete_tree",
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=tree_body,
            decorator_list=[],
            returns=sequence[0][0].returns,
        )
    )

    # main script execution
    body.append(
        ast.If(
            test=ast.Compare(
                left=ast.Name(id="__name__", ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value="__main__")],
            ),
            body=[
                ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Name(id="get_complete_tree", ctx=ast.Load()),
                                args=[],
                                keywords=[]
                            ),
                            attr="write",
                            ctx=ast.Load()
                        ),
                        args=[],
                        keywords=[]
                    )
                )
            ],
            orelse=[],
        )
    )

    module = ast.Module(body=body, type_ignores=[])
    module = ast.fix_missing_locations(module) # fix "required field 'lineno' missing"
    return module
