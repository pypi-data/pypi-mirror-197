"""Plugin to interactively visualize atoti sessions in JupyterLab.

This package is required to use :meth:`atoti.Session.visualize` and :meth:`atoti_query.QuerySession.visualize`.
"""

from typing import Dict, List


def _jupyter_labextension_paths() -> List[  # pyright: ignore[reportUnusedFunction]
    Dict[str, str]
]:
    """Return the paths used by JupyterLab to load the extension assets."""
    return [{"src": "labextension", "dest": "atoti-jupyterlab"}]
