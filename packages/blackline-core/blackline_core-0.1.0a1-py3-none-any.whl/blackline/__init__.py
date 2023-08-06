from pkgutil import extend_path
from typing import List

__path__: List[str] = extend_path(__path__, __name__)

__version__ = "0.1.0a1"
