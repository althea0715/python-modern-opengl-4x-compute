import logging
import os
from typing import Final

from glfw.GLFW import *  # type: ignore # noqa: F403
from glfw import _GLFWwindow as GLFWwindow  # type: ignore
from OpenGL.GL import *  # type: ignore  # noqa: F403
from pyglm import glm  # type: ignore

from shader import Shader
from camera import Camera, CameraMovement
from model import Model


SCR_WIDTH: Final[int] = 800
SCR_HEIGHT: Final[int] = 600

camera = Camera(glm.vec3(0.0, 0.0, 3.0))
last_x = SCR_WIDTH / 2.0
last_y = SCR_HEIGHT / 2.0
first_mouse = True

delta_time = 0.0
last_frame = 0.0


def main():
    # Change working directory to the script's directory to find shaders
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

    our_shader = Shader("./model_loading.vs", "./model_loading.fs")
    
    # Path to the backpack object
    model_path = os.path.abspath("../resources/objects/backpack/backpack.obj")
    our_model = Model(model_path)

    global delta_time, last_frame

    while not glfwWindowShouldClose(window):
        current_frame = glfwGetTime()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        process_input(window)

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        our_shader.use()

        projection = glm.perspective(glm.radians(camera.zoom), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)
        view: glm.mat4 = camera.get_view_matrix()
        our_shader.set_mat4v("projection", projection)
        our_shader.set_mat4v("view", view)

        # render the loaded model
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.0))
        model = glm.scale(model, glm.vec3(1.0, 1.0, 1.0))
        our_shader.set_mat4v("model", model)
        our_model.draw(our_shader)

        glfwSwapBuffers(window)
        glfwPollEvents()

    our_shader.destroy()

    glfwDestroyWindow(window)
    glfwTerminate()


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
    global first_mouse, last_x, last_y

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


if __name__ == "__main__":
    main()
