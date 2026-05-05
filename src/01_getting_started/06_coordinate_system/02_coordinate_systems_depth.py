import logging

import numpy as np

from typing import Final
from ctypes import c_uint32, byref

from PIL import Image

from glfw.GLFW import *  # type: ignore
from glfw import _GLFWwindow as GLFWwindow  # type: ignore
from OpenGL.GL import *  # type: ignore
from pyglm import glm  

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

    glEnable(GL_DEPTH_TEST)

    our_shader = Shader("./02_coordinate_systems_depth.vs", "./02_coordinate_systems_depth.fs")

    vertices = np.array(
        [   
            -0.5, -0.5, -0.5,  0.0, 0.0,
            0.5, -0.5, -0.5,  1.0, 0.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 0.0,

            -0.5, -0.5,  0.5,  0.0, 0.0,
            0.5, -0.5,  0.5,  1.0, 0.0,
            0.5,  0.5,  0.5,  1.0, 1.0,
            0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,

            -0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 0.0,

            0.5,  0.5,  0.5,  1.0, 0.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            0.5, -0.5, -0.5,  0.0, 1.0,
            0.5, -0.5, -0.5,  0.0, 1.0,
            0.5, -0.5,  0.5,  0.0, 0.0,
            0.5,  0.5,  0.5,  1.0, 0.0,

            -0.5, -0.5, -0.5,  0.0, 1.0,
            0.5, -0.5, -0.5,  1.0, 1.0,
            0.5, -0.5,  0.5,  1.0, 0.0,
            0.5, -0.5,  0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,

            -0.5,  0.5, -0.5,  0.0, 1.0,
            0.5,  0.5, -0.5,  1.0, 1.0,
            0.5,  0.5,  0.5,  1.0, 0.0,
            0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,
        ],
        dtype=np.float32,
    )

    vbo = c_uint32(0)
    vao = c_uint32(0)

    glCreateBuffers(1, byref(vbo))
    glCreateVertexArrays(1, byref(vao))
    
    glNamedBufferStorage(vbo, vertices.nbytes, vertices, GL_DYNAMIC_STORAGE_BIT)
    glVertexArrayVertexBuffer(vao, 0, vbo, 0, 5 * vertices.itemsize)

    glEnableVertexArrayAttrib(vao, 0)
    glEnableVertexArrayAttrib(vao, 1)

    glVertexArrayAttribFormat(vao, 0, 3, GL_FLOAT, GL_FALSE, 0 * vertices.itemsize)
    glVertexArrayAttribFormat(vao, 1, 2, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize)

    glVertexArrayAttribBinding(vao, 0, 0)
    glVertexArrayAttribBinding(vao, 1, 0)

    texture1 = c_uint32(0)
    glCreateTextures(GL_TEXTURE_2D, 1, texture1)
    glTextureParameteri(texture1, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTextureParameteri(texture1, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTextureParameteri(texture1, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTextureParameteri(texture1, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open("../../img/texture/container.jpg").convert("RGBA").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    glTextureStorage2D(texture1, 1, GL_RGBA8, img.width, img.height)
    glTextureSubImage2D(texture1, 0, 0, 0, img.width, img.height, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
    glGenerateTextureMipmap(texture1)


    texture2 = c_uint32(0)
    glCreateTextures(GL_TEXTURE_2D, 1, texture2)
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBindTextureUnit(0, texture1)
        glBindTextureUnit(1, texture2)

        our_shader.use()

        model           = glm.mat4(1.0)
        view            = glm.mat4(1.0)
        projection      = glm.mat4(1.0)
        model = glm.rotate(model, glfwGetTime(), glm.vec3(0.5, 1.0, 0.0))
        view = glm.translate(view, glm.vec3(0.0, 0.0, -3.0))
        projection = glm.perspective(glm.radians(45.0), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)

        model_loc = glGetUniformLocation(our_shader.id, "model")
        view_loc = glGetUniformLocation(our_shader.id, "view")

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        our_shader.set_mat4v("projection", projection)
        
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteTextures(1, texture1)
    glDeleteTextures(1, texture2)
    our_shader.destroy()

    glfwDestroyWindow(window)
    glfwTerminate()


if __name__ == "__main__":
    main()