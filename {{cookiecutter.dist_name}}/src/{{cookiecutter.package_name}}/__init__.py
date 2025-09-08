"""{{cookiecutter.project_short_description}}"""

from importlib.metadata import version

__version__ = version(__package__ or __name__)

{% if cookiecutter.brave_browser_support == "Y" -%}
# Brave browser integration
try:
    from .brave_integration import BraveSession, check_brave_rewards_api, get_brave_user_agent
    __all__ = ["add", "BraveSession", "check_brave_rewards_api", "get_brave_user_agent"]
except ImportError:
    # Brave dependencies not installed
    __all__ = ["add"]
{%- else -%}
__all__ = ["add"]
{%- endif %}


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
