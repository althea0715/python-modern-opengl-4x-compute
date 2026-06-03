from contextlib import contextmanager
from typing import Iterator

from pyassimp import postprocess
from pyassimp.structs import Scene

@contextmanager
def load(filename: str, file_type=None, processing=postprocess.aiProcess_Triangulate) -> Iterator[Scene]: ...
