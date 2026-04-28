import numpy as np

from enum import Enum, auto
from typing import Self

from pyglm import glm  # type: ignore


class CameraMovement(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()


YAW = -90.0
PITCH = 0.0
SPEED = 2.5
SENSITIVITY = 0.1
ZOOM = 45.0


class Camera:
    def __init__(
        self,
        position: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        up: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        yaw: float = YAW,
        pitch: float = PITCH,
    ):
        self._position = position
        self._world_up = up
        self._yaw = yaw
        self._pitch = pitch

        self._up = glm.vec3(0.0)
        self._right = glm.vec3(0.0)

        self._front = glm.vec3(0.0, 0.0, -1.0)
        self._movement_speed = SPEED
        self._mouse_sensitivity = SENSITIVITY
        self._zoom = ZOOM

        self.update_camera_vectors()

    @classmethod
    def from_scalar(
        cls,
        xpos: float,
        ypos: float,
        zpos: float,
        xup: float,
        yup: float,
        zup: float,
        yaw: float,
        pitch: float,
    ) -> Self:
        position = glm.vec3(xpos, ypos, zpos)
        up = glm.vec3(xup, yup, zup)
        return cls(position, up, yaw, pitch)

    def get_view_matrix(self) -> glm.mat4:
        return glm.lookAt(self._position, self._position + self._front, self._up)

    def process_keyboard(self, direction: CameraMovement, delta_time: float):
        velocity = self._movement_speed * delta_time

        match direction:
            case CameraMovement.FORWARD:
                self._position += self._front * velocity
            case CameraMovement.BACKWARD:
                self._position -= self._front * velocity
            case CameraMovement.LEFT:
                self._position -= self._right * velocity
            case CameraMovement.RIGHT:
                self._position += self._right * velocity

    def process_mouse_movement(
        self, xoffset: float, yoffset: float, constrain_pitch: bool = True
    ):
        xoffset *= self._mouse_sensitivity
        yoffset *= self._mouse_sensitivity

        self._yaw += xoffset
        self._pitch += yoffset

        if constrain_pitch:
            self._pitch = np.clip(self._pitch, -89.0, 89.0)

        self.update_camera_vectors()

    def process_mouse_scroll(self, yoffset: float):

        self._zoom -= yoffset
        self._zoom = np.clip(self._zoom, 1.0, 45.0)

    def update_camera_vectors(self):

        front = glm.vec3()
        front.x = glm.cos(glm.radians(self._yaw)) * glm.cos(glm.radians(self._pitch))
        front.y = glm.sin(glm.radians(self._pitch))
        front.z = glm.sin(glm.radians(self._yaw)) * glm.cos(glm.radians(self._pitch))
        self._front = glm.normalize(front)

        self._right = glm.normalize(glm.cross(self._front, self._world_up))
        self._up = glm.normalize(glm.cross(self._right, self._front))
