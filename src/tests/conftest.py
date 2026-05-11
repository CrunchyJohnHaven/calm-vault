"""Shared pytest config: put `src/` on sys.path so flat-module imports work
regardless of where pytest is invoked from."""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
