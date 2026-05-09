import logging

import numpy as np

from typing import Final
from ctypes import c_uint32, byref

from PIL import Image

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


def load_texture(path:str) -> c_uint32:
    texture = c_uint32(0)
    glCreateTextures(GL_TEXTURE_2D, 1, texture)

    img = Image.open(path).convert("RGBA")
    glTextureStorage2D(texture, 1, GL_RGBA8, img.width, img.height)
    glTextureSubImage2D(texture, 0, 0, 0, img.width, img.height, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
    
    glTextureParameteri(texture, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTextureParameteri(texture, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTextureParameteri(texture, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTextureParameteri(texture, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glGenerateTextureMipmap(texture)

    return texture


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

    lighting_shader = Shader("./02_light_casters.vs", "./02_light_casters.fs")
    light_cube_shader = Shader("./01_light_cube.vs", "./01_light_cube.fs")

    vertices = np.array(
        [   
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,
            0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  0.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  1.0,
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,

            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,
            0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  1.0,
            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,

            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0,  1.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0,  0.0,
            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,

            0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,
            0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  1.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
            0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0,
            0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,

            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,
            0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0,  1.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0,  0.0,
            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,

            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0,
            0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0,  0.0,
            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0,
        ],
        dtype=np.float32,
    )


    cube_positions = [
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
    cube_vao = c_uint32(0)

    glCreateBuffers(1, byref(vbo))
    glCreateVertexArrays(1, byref(cube_vao))

    glNamedBufferStorage(vbo, vertices.nbytes, vertices, GL_DYNAMIC_STORAGE_BIT)
    glVertexArrayVertexBuffer(cube_vao, 0, vbo, 0, 8 * vertices.itemsize)

    glEnableVertexArrayAttrib(cube_vao, 0)
    glEnableVertexArrayAttrib(cube_vao, 1)
    glEnableVertexArrayAttrib(cube_vao, 2)

    glVertexArrayAttribFormat(cube_vao, 0, 3, GL_FLOAT, GL_FALSE, 0 * vertices.itemsize)
    glVertexArrayAttribFormat(cube_vao, 1, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize)
    glVertexArrayAttribFormat(cube_vao, 2, 2, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize)

    glVertexArrayAttribBinding(cube_vao, 0, 0)
    glVertexArrayAttribBinding(cube_vao, 1, 0)
    glVertexArrayAttribBinding(cube_vao, 2, 0)


    light_cube_vao = c_uint32(0)
    glCreateVertexArrays(1, byref(light_cube_vao))

    glVertexArrayVertexBuffer(light_cube_vao, 0, vbo, 0, 8 * vertices.itemsize)

    glEnableVertexArrayAttrib(light_cube_vao, 0)
    glVertexArrayAttribFormat(light_cube_vao, 0, 3, GL_FLOAT, GL_FALSE, 0 * vertices.itemsize)
    glVertexArrayAttribBinding(light_cube_vao, 0, 0)


    diffuse_map = load_texture("../../img/texture/container2.png")
    specular_map = load_texture("../../img/texture/container2_specular.png")

    lighting_shader.use()
    lighting_shader.set_int("material.diffuse", 0)
    lighting_shader.set_int("material.specular", 1)
    

    global delta_time, last_frame

    while not glfwWindowShouldClose(window):

        current_frame = glfwGetTime()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        process_input(window)

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        lighting_shader.use()
        lighting_shader.set_vec3v("light.position", light_pos)
        lighting_shader.set_vec3v("viewPos", camera.position)

        lighting_shader.set_vec3("light.ambient", 0.2, 0.2, 0.2)
        lighting_shader.set_vec3("light.diffuse", 0.5, 0.5, 0.5)
        lighting_shader.set_vec3("light.specular", 1.0, 1.0, 1.0)        
        lighting_shader.set_float("light.constant", 1.0)
        lighting_shader.set_float("light.linear", 0.09)
        lighting_shader.set_float("light.quadratic", 0.032)

        lighting_shader.set_float("material.shinines", 32.0)

        projection = glm.perspective(glm.radians(camera.zoom), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)
        view = camera.get_view_matrix()
        lighting_shader.set_mat4v("projection", projection)
        lighting_shader.set_mat4v("view", view)

        model = glm.mat4(1.0)
        lighting_shader.set_mat4v("model", model)

        glBindTextureUnit(0, diffuse_map)
        glBindTextureUnit(1, specular_map)

        glBindVertexArray(cube_vao)
        for i, cube_position in enumerate(cube_positions):
            model = glm.mat4(1.0)
            model = glm.translate(model, cube_position)
            angle = 20.0 * i
            model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5))

            lighting_shader.set_mat4v("model", model)
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
