"""{{cookiecutter.project_short_description}}"""

from importlib import metadata

try:
    __version__ = metadata.version(__package__ or __name__)
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"


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
