import logging

from pathlib import Path
from typing import Literal, cast

from OpenGL.GL import *  # type: ignore


class Shader:

    def __init__(self, vertex_path: Path | str, fragment_path: Path | str):

        self.id: int = 0

        if isinstance(vertex_path, str):
            vertex_path = Path(vertex_path)

        if isinstance(fragment_path, str):
            fragment_path = Path(fragment_path)

        try:
            vertex_code = vertex_path.read_text()
            fragment_code = fragment_path.read_text()
        except FileExistsError as e:
            logging.error(f"ERROR::SHADER::FILE_NOT_SUCCESSFULLY_READ: {e}")
            return

        vertex = cast(int, glCreateShader(GL_VERTEX_SHADER))
        glShaderSource(vertex, vertex_code)
        glCompileShader(vertex)
        self._check_compile_errors(vertex, "VERTEX")

        fragment = cast(int, glCreateShader(GL_FRAGMENT_SHADER))
        glShaderSource(fragment, fragment_code)
        glCompileShader(fragment)
        self._check_compile_errors(fragment, "FRAGMENT")

        self.id = cast(int, glCreateProgram())
        glAttachShader(self.id, vertex)
        glAttachShader(self.id, fragment)
        glLinkProgram(self.id)
        self._check_compile_errors(self.id, "PROGRAM")

        glDeleteShader(vertex)
        glDeleteShader(fragment)

    def _check_compile_errors(
        self, shader: int, shader_t: Literal["PROGRAM", "VERTEX", "FRAGMENT"]
    ):

        match shader_t:
            case "PROGRAM":
                if glGetProgramiv(shader, GL_LINK_STATUS) == GL_FALSE:
                    info_log = glGetProgramInfoLog(shader)
                    logging.error(f"ERROR::SHADER::PROGRAM::LINKING_FAILED {info_log}")

            case "VERTEX" | "FRAGMENT":
                if glGetShaderiv(shader, GL_COMPILE_STATUS) == GL_FALSE:
                    info_log = glGetShaderInfoLog(shader)
                    logging.error(
                        f"ERROR::SHADER::VERTEX::COMPILATION_FAILED {info_log}"
                    )

            case _:
                raise ValueError(f"ERROR::SHADER_TYPE_ERROR: {shader_t}")

    def use(self):
        glUseProgram(self.id)

    def destroy(self):
        glDeleteProgram(self.id)

    def set_bool(self, name: str, value: bool):
        glUniform1i(glGetUniformLocation(self.id, name), value)

    def set_int(self, name: str, value: int):
        glUniform1i(glGetUniformLocation(self.id, name), value)

    def set_float(self, name: str, value: float):
        glUniform1f(glGetUniformLocation(self.id, name), value)
