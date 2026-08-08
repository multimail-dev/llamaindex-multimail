"""LlamaIndex tools for MultiMail -- email capabilities for LlamaIndex agents."""

import warnings as _warnings

_warnings.warn(
    "The llamaindex-multimail PyPI package is deprecated and unmaintained (retired 2026-08-08). "
    "Use MultiMail's MCP server (https://mcp.multimail.dev) or REST API "
    "(https://multimail.dev/docs) instead.",
    FutureWarning,
    stacklevel=2,
)


from llamaindex_multimail.tools import MultiMailToolSpec

__version__ = "0.1.0"
__all__ = ["MultiMailToolSpec"]
