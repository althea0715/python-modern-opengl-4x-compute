import logging

import numpy as np

from typing import Final
from ctypes import c_uint32, byref

from glfw.GLFW import *  # type: ignore
from glfw import _GLFWwindow as GLFWwindow  # type: ignore
from OpenGL.GL import *  # type: ignore


SCR_WIDTH: Final[int] = 800
SCR_HEIGHT: Final[int] = 600


def framebuffer_size_callback(window: GLFWwindow, width: int, height: int):
    glViewport(0, 0, width, height)


def process_input(window: GLFWwindow):
    if glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
        glfwSetWindowShouldClose(window, True)


vertex_shader_source = """
    #version 460 core
    layout (location = 0) in vec3 aPos;
    layout (location = 1) in vec3 aColor;
    out vec3 ourColor;
    void main(){
       gl_Position = vec4(aPos, 1.0);
       ourColor = aColor;
    }
    """

fragment_shader_source = """
    #version 460 core
    out vec4 FragColor;
    in vec3 ourColor;
    void main(){
       FragColor = vec4(ourColor, 1.0);
    }
    """


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

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)

    if glGetShaderiv(vertex_shader, GL_COMPILE_STATUS) == GL_FALSE:
        info_log = glGetShaderInfoLog(vertex_shader)
        logging.error(f"ERROR::SHADER::VERTEX::COMPILATION_FAILED {info_log}")

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)

    if glGetShaderiv(fragment_shader, GL_COMPILE_STATUS) == GL_FALSE:
        info_log = glGetShaderInfoLog(fragment_shader)
        logging.error(f"ERROR::SHADER::FRAGMENT::COMPILATION_FAILED {info_log}")

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) == GL_FALSE:
        info_log = glGetProgramInfoLog(shader_program)
        logging.error(f"ERROR::SHADER::PROGRAM::LINKING_FAILED {info_log}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

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

    glCreateBuffers(1, byref(vbo))
    glCreateVertexArrays(1, byref(vao))

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

        glUseProgram(shader_program)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteProgram(shader_program)

    glfwDestroyWindow(window)
    glfwTerminate()


if __name__ == "__main__":
    main()
