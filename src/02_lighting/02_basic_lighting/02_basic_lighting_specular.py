import logging

import numpy as np

from typing import Final
from ctypes import c_uint32

from glfw.GLFW import *  # type: ignore
from glfw import _GLFWwindow as GLFWwindow  # type: ignore
from OpenGL.GL import *  # type: ignore
from pyglm import glm  # type: ignore

from shader import Shader
from camera import Camera, CameraMovement


SCR_WIDTH: Final[int] = 800
SCR_HEIGHT: Final[int] = 600

camera = Camera(glm.vec3(0.0, 0.0, 3.0))
last_x = SCR_WIDTH / 2.0
last_y = SCR_HEIGHT / 2.0
first_mouse = True

delta_time = 0.0
last_frame = 0.0

light_pos = glm.vec3(1.2, 1.0, 2.0)


def framebuffer_size_callback(window: GLFWwindow, width: int, height: int):
    glViewport(0, 0, width, height)


def process_input(window: GLFWwindow):
    if glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
        glfwSetWindowShouldClose(window, True)

    global delta_time
    
    if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
        camera.process_keyboard(CameraMovement.FORWARD, delta_time)

    if glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
        camera.process_keyboard(CameraMovement.BACKWARD, delta_time)

    if glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS:
        camera.process_keyboard(CameraMovement.LEFT, delta_time)

    if glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS:
        camera.process_keyboard(CameraMovement.RIGHT, delta_time)


def mouse_callback(window: GLFWwindow, xpos: float, ypos: float):

    global first_mouse, last_x, last_y, yaw, pitch, camera_front

    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos
    last_x = xpos
    last_y = ypos

    camera.process_mouse_movement(xoffset, yoffset)


def scroll_callback(window: GLFWwindow, xoffset: float, yoffset: float):
    camera.process_mouse_scroll(yoffset)


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
    glfwSetCursorPosCallback(window, mouse_callback)
    glfwSetScrollCallback(window, scroll_callback)

    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)

    lighting_shader = Shader("./02_basic_lighting.vs", "./02_basic_lighting.fs")
    light_cube_shader = Shader("./01_light_cube.vs", "./01_light_cube.fs")

    vertices = np.array(
        [   
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
            0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,

            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
            0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,

            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,
            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,

            0.5,  0.5,  0.5,  1.0,  0.0,  0.0,
            0.5,  0.5, -0.5,  1.0,  0.0,  0.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
            0.5, -0.5,  0.5,  1.0,  0.0,  0.0,
            0.5,  0.5,  0.5,  1.0,  0.0,  0.0,

            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
            0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,

            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
            0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
        ],
        dtype=np.float32,
    )

    vbo = c_uint32(0)
    cube_vao = c_uint32(0)

    glCreateBuffers(1, vbo)
    glCreateVertexArrays(1, cube_vao)

    glNamedBufferStorage(vbo, vertices.nbytes, vertices, GL_DYNAMIC_STORAGE_BIT)
    glVertexArrayVertexBuffer(cube_vao, 0, vbo, 0, 6 * vertices.itemsize)

    glEnableVertexArrayAttrib(cube_vao, 0)
    glEnableVertexArrayAttrib(cube_vao, 1)

    glVertexArrayAttribFormat(cube_vao, 0, 3, GL_FLOAT, GL_FALSE, 0 * vertices.itemsize)
    glVertexArrayAttribFormat(cube_vao, 1, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize)

    glVertexArrayAttribBinding(cube_vao, 0, 0)
    glVertexArrayAttribBinding(cube_vao, 1, 0)


    light_cube_vao = c_uint32(0)
    glCreateVertexArrays(1, light_cube_vao)

    glVertexArrayVertexBuffer(light_cube_vao, 0, vbo, 0, 6 * vertices.itemsize)

    glEnableVertexArrayAttrib(light_cube_vao, 0)
    glVertexArrayAttribFormat(light_cube_vao, 0, 3, GL_FLOAT, GL_FALSE, 0 * vertices.itemsize)
    glVertexArrayAttribBinding(light_cube_vao, 0, 0)
    

    global delta_time, last_frame

    while not glfwWindowShouldClose(window):

        current_frame = glfwGetTime()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        process_input(window)

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        lighting_shader.use()
        lighting_shader.set_vec3("objectColor", 1.0, 0.5, 0.31)
        lighting_shader.set_vec3("lightColor", 1.0, 1.0, 1.0)
        lighting_shader.set_vec3v("lightPos", light_pos)
        lighting_shader.set_vec3v("viewPos", camera._position)

        projection = glm.perspective(glm.radians(camera._zoom), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)
        view = camera.get_view_matrix()
        lighting_shader.set_mat4v("projection", projection)
        lighting_shader.set_mat4v("view", view)

        model = glm.mat4(1.0)
        model = glm.scale(model, glm.vec3(1.0))
        lighting_shader.set_mat4v("model", model)

        glBindVertexArray(cube_vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)
    
        light_cube_shader.use()
        light_cube_shader.set_mat4v("projection", projection)
        light_cube_shader.set_mat4v("view", view)        
        model = glm.mat4(1.0)
        model = glm.translate(model, light_pos)
        model = glm.scale(model, glm.vec3(0.2))
        light_cube_shader.set_mat4v("model", model)

        glBindVertexArray(light_cube_vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glDeleteVertexArrays(1, cube_vao)
    glDeleteVertexArrays(1, light_cube_vao)
    glDeleteBuffers(1, vbo)
    lighting_shader.destroy()
    light_cube_shader.destroy()

    glfwDestroyWindow(window)
    glfwTerminate()


if __name__ == "__main__":
    main()
