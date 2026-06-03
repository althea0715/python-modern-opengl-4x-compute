from __future__ import annotations
import numpy as np

from typing import Final, Any
from ctypes import Structure

class Node(Structure):
    name: str
    transformation: np.ndarray
    parent: Node | None
    children: list[Node]
    meshes: list[Mesh]
    metadata: dict[str, Any]

class Scene(Structure):
    AI_SCENE_FLAGS_INCOMPLETE: Final[int] = 0x1
    AI_SCENE_FLAGS_VALIDATED: Final[int] = 0x2
    AI_SCENE_FLAGS_VALIDATION_WARNING: Final[int] = 0x4
    AI_SCENE_FLAGS_NON_VERBOSE_FORMAT: Final[int] = 0x8
    AI_SCENE_FLAGS_TERRAIN: Final[int] = 0x10
    AI_SCENE_FLAGS_ALLOW_SHARED: Final[int] = 0x20

    rootnode: Node
    flags: int
    meshes: list[Mesh]
    materials: list[Material]
    animations: list[Any]
    cameras: list[Any]
    lights: list[Any]

class Mesh(Structure):
    name: str
    vertices: np.ndarray
    normals: np.ndarray
    tangents: np.ndarray
    bitangents: np.ndarray
    colors: list[np.ndarray]
    texturecoords: list[np.ndarray]
    faces: np.ndarray
    materialindex: int

class Material(Structure):
    properties: dict[tuple[str, int], Any]
