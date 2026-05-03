import logging

import numpy as np

from typing import Final
from ctypes import c_uint32

from glfw.GLFW import *  # type: ignore
from glfw import _GLFWwindow as GLFWwindow  # type: ignore
from OpenGL.GL import *  # type: ignore

from shader import Shader


SCR_WIDTH: Final[int] = 800
SCR_HEIGHT: Final[int] = 600


def framebuffer_size_callback(window: GLFWwindow, width: int, height: int):
    glViewport(0, 0, width, height)


def process_input(window: GLFWwindow):
    if glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
        glfwSetWindowShouldClose(window, True)


def main():

    glfwInit()
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
    if not window:
        logging.error("Failed to create GLFW window")
        glfwTerminate()
        return

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback)

    our_shader = Shader("./03_shader.vs", "./03_shader.fs")

    vertices = np.array(
        [   
            # positions         # colors
            0.5, -0.5, 0.0,     1.0, 0.0, 0.0,
            -0.5, -0.5, 0.0,    0.0, 1.0, 0.0,
            0.0,  0.5, 0.0,     0.0, 0.0, 1.0 
        ],
        dtype=np.float32,
    )

    vbo = c_uint32(0)
    vao = c_uint32(0)    

    glCreateBuffers(1, vbo)
    glCreateVertexArrays(1, vao)

    glNamedBufferStorage(vbo, vertices.nbytes, vertices, GL_DYNAMIC_STORAGE_BIT)
    glVertexArrayVertexBuffer(vao, 0, vbo, 0, 6 * vertices.itemsize)

    glEnableVertexArrayAttrib(vao, 0)
    glEnableVertexArrayAttrib(vao, 1)

    glVertexArrayAttribFormat(vao, 0, 3, GL_FLOAT, GL_FALSE, 0 * vertices.itemsize)
    glVertexArrayAttribFormat(vao, 1, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize)

    glVertexArrayAttribBinding(vao, 0, 0)
    glVertexArrayAttribBinding(vao, 1, 0)


    while not glfwWindowShouldClose(window):
        process_input(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        our_shader.use()
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    our_shader.destroy()

    glfwDestroyWindow(window)
    glfwTerminate()


if __name__ == "__main__":
    main()
