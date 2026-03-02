"""
csprotocol — Command Service Protocol
Reference implementation of CSS-1.0

Author:     Petro Nazarenko
Repository: github.com/petro-nazarenko/command-service-protocol
PyPI:       csprotocol
License:    MIT
"""

__version__ = "1.0.0-draft"
__author__ = "Petro Nazarenko"
__spec_version__ = "CSS-1.0"

from csprotocol.parser import parse_command, Command
from csprotocol.generator import generate_one_liner
from csprotocol.main import handle

__all__ = [
    "parse_command",
    "generate_one_liner",
    "handle",
    "Command",
    "__version__",
    "__spec_version__",
]
