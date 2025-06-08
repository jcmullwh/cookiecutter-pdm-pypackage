"""{{cookiecutter.project_short_description}}"""

from importlib.metadata import version

__version__ = version(__package__ or __name__)


def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a:
            The first operand.
        b:
            The second operand.

    Examples:
        Add two integers

            r = add(2, 3)
            print(r)  # 5
    """
    return a + b
