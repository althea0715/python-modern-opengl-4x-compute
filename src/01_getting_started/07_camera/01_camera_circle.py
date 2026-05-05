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

    our_shader = Shader("./01_camera.vs", "./01_camera.fs")

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

    cubePositions = [
        glm.vec3( 0.0,  0.0,  0.0),
        glm.vec3( 2.0,  5.0, -15.0),
        glm.vec3(-1.5, -2.2, -2.5),
        glm.vec3(-3.8, -2.0, -12.3),
        glm.vec3( 2.4, -0.4, -3.5),
        glm.vec3(-1.7,  3.0, -7.5),
        glm.vec3( 1.3, -2.0, -2.5),
        glm.vec3( 1.5,  2.0, -2.5),
        glm.vec3( 1.5,  0.2, -1.5),
        glm.vec3(-1.3,  1.0, -1.5),
    ]

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

    projection = glm.perspective(glm.radians(45.0), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)
    our_shader.set_mat4v("projection", projection)

    while not glfwWindowShouldClose(window):
        process_input(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBindTextureUnit(0, texture1)
        glBindTextureUnit(1, texture2)

        our_shader.use()

        view = glm.mat4(1.0)
        radius = 10.0
        cam_x = np.sin(glfwGetTime()) * radius
        cam_z = np.cos(glfwGetTime()) * radius
        view = glm.lookAt(glm.vec3(cam_x, 0.0, cam_z), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))    
        our_shader.set_mat4v("view", view)

        glBindVertexArray(vao)

        for i, cubePosition in enumerate(cubePositions):
            model = glm.mat4(1.0)
            model = glm.translate(model, cubePosition)
            angle = 20.0 * i
            model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5))
            our_shader.set_mat4v("model", model)
            
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