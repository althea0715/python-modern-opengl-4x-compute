import logging

import numpy as np

from typing import Final
from ctypes import c_uint32, byref

from PIL import Image

from glfw.GLFW import *  # type: ignore
from glfw import _GLFWwindow as GLFWwindow  # type: ignore
from OpenGL.GL import *  # type: ignore
from pyglm import glm   # pip install pyglm

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

    our_shader = Shader("./01_shader.vs", "./01_shader.fs")

    vertices = np.array(
        [   
            # positions         # texture coords
            0.5,  0.5, 0.0,     1.0, 1.0,
            0.5, -0.5, 0.0,     1.0, 0.0,
            -0.5, -0.5, 0.0,    0.0, 0.0,
            -0.5,  0.5, 0.0,    0.0, 1.0, 
        ],
        dtype=np.float32,
    )

    indices = np.array(
        [   
            0, 1, 3,
            1, 2, 3
        ],
        dtype=np.uint32,
    )

    vbo = c_uint32(0)
    vao = c_uint32(0)
    ebo = c_uint32(0)    

    glCreateBuffers(1, byref(vbo))
    glCreateVertexArrays(1, byref(vao))
    glCreateBuffers(1, byref(ebo))

    glNamedBufferStorage(vbo, vertices.nbytes, vertices, GL_DYNAMIC_STORAGE_BIT)
    glNamedBufferStorage(ebo, indices.nbytes, indices, GL_DYNAMIC_STORAGE_BIT)
    glVertexArrayVertexBuffer(vao, 0, vbo, 0, 5 * vertices.itemsize)

    glVertexArrayElementBuffer(vao, ebo)

    glEnableVertexArrayAttrib(vao, 0)
    glEnableVertexArrayAttrib(vao, 1)

    glVertexArrayAttribFormat(vao, 0, 3, GL_FLOAT, GL_FALSE, 0 * vertices.itemsize)
    glVertexArrayAttribFormat(vao, 1, 2, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize)

    glVertexArrayAttribBinding(vao, 0, 0)
    glVertexArrayAttribBinding(vao, 1, 0)

    texture1 = c_uint32(0)
    glCreateTextures(GL_TEXTURE_2D, 1, byref(texture1))
    glTextureParameteri(texture1, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTextureParameteri(texture1, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTextureParameteri(texture1, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTextureParameteri(texture1, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open("../../img/texture/container.jpg").convert("RGBA").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    glTextureStorage2D(texture1, 1, GL_RGBA8, img.width, img.height)
    glTextureSubImage2D(texture1, 0, 0, 0, img.width, img.height, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
    glGenerateTextureMipmap(texture1)

    texture2 = c_uint32(0)
    glCreateTextures(GL_TEXTURE_2D, 1, byref(texture2))
    glTextureParameteri(texture2, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTextureParameteri(texture2, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTextureParameteri(texture2, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTextureParameteri(texture2, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open("../../img/texture/awesomeface.png").convert("RGBA").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    glTextureStorage2D(texture2, 1, GL_RGBA8, img.width, img.height)
    glTextureSubImage2D(texture2, 0, 0, 0, img.width, img.height, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
    glGenerateTextureMipmap(texture2)

    our_shader.use()
    our_shader.set_int("texture1", 0)
    our_shader.set_int("texture2", 1)

    while not glfwWindowShouldClose(window):
        process_input(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glBindTextureUnit(0, texture1)
        glBindTextureUnit(1, texture2)

        transform = glm.mat4(1.0)
        transform = glm.translate(transform, glm.vec3(0.5, -0.5, 0.0))
        transform = glm.rotate(transform, glfwGetTime(), glm.vec3(0.0, 0.0, 1.0))

        our_shader.use()
        transform_loc = glGetUniformLocation(our_shader.id, "transform")
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(transform))

        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteBuffers(1, ebo)
    glDeleteTextures(1, texture1)
    glDeleteTextures(1, texture2)
    our_shader.destroy()

    glfwDestroyWindow(window)
    glfwTerminate()


if __name__ == "__main__":
    main()