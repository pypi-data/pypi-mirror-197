#!/usr/bin/env python3

"""
** Executes all the tests via the ``pytest`` module. **
-------------------------------------------------------
"""

try:
    from pylint.lint import Run as PylintRun
except ImportError as err:
    raise ImportError("pylint paquage required (pip install movia[dev])") from err
try:
    import pytest
except ImportError as err:
    raise ImportError("pytest paquage required (pip install movia[dev])") from err

from movia.utils import get_project_root


def test() -> int:
    """
    ** Performs all unit tests. **
    """
    root = get_project_root()
    if (code := (
        PylintRun(["--rcfile", str(root.parent / ".pylintrc"), str(root)], exit=False)
        .linter.msg_status
    )):
        return code
    paths = (
        [str(root / "utils.py")]
        + [str(root / "core")]
        + sorted(str(p) for p in (root / "testing" / "tests").rglob("*.py"))
    )
    if (code := pytest.main(["-m", "not slow", "--full-trace", "--doctest-modules"] + paths)):
        return int(code)
    if (code := pytest.main(["-m", "slow", "--full-trace", "--verbose"] + paths)):
        return int(code)
    return 0


if __name__ == '__main__':
    test()
