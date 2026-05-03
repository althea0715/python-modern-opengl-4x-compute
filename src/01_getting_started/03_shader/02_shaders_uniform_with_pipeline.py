import logging

import numpy as np

from typing import Final
from ctypes import c_uint32, POINTER, c_char_p, c_char, cast

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
    void main(){
       gl_Position = vec4(aPos, 1.0);
    }
    """

fragment_shader_source = """
    #version 460 core
    out vec4 FragColor;
    uniform vec4 ourColor;
    void main(){
       FragColor = ourColor;
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


    # VERTEX PIPELINE
    vertex_shader_source_encoded = vertex_shader_source.encode()
    vertex_shader_source_c_char_p = c_char_p(vertex_shader_source_encoded)
    vertex_shader_source_LP_c_char_p = (c_char_p * 1)()
    vertex_shader_source_LP_c_char_p[0] = vertex_shader_source_c_char_p
    vertex_shader_source_LP_LP_char_p = cast(vertex_shader_source_LP_c_char_p, POINTER(POINTER(c_char)))

    vertex_program = glCreateShaderProgramv(GL_VERTEX_SHADER, 1, vertex_shader_source_LP_LP_char_p)
    
    if glGetProgramiv(vertex_program, GL_LINK_STATUS) == GL_FALSE:
        info_log = glGetProgramInfoLog(vertex_program)
        logging.error(f"ERROR::SHADER::VERTEX::COMPILATION_FAILED {info_log}")


    # FRAGMENT PIPELINE
    fragment_shader_source_encoded = fragment_shader_source.encode()
    fragment_shader_source_c_char_p = c_char_p(fragment_shader_source_encoded)
    fragment_shader_source_LP_c_char_p = (c_char_p * 1)()
    fragment_shader_source_LP_c_char_p[0] = fragment_shader_source_c_char_p
    fragment_shader_source_LP_LP_char_p = cast(fragment_shader_source_LP_c_char_p, POINTER(POINTER(c_char)))

    fragment_program = glCreateShaderProgramv(GL_FRAGMENT_SHADER, 1, fragment_shader_source_LP_LP_char_p)
    
    if glGetProgramiv(fragment_program, GL_LINK_STATUS) == GL_FALSE:
        info_log = glGetProgramInfoLog(fragment_program)
        logging.error(f"ERROR::SHADER::FRAGMENT::COMPILATION_FAILED {info_log}")


    # PROGRAM PIPELINE
    glProgramParameteri(vertex_program, GL_PROGRAM_SEPARABLE, GL_TRUE)
    glProgramParameteri(fragment_program, GL_PROGRAM_SEPARABLE, GL_TRUE)

    program_pipeline = c_uint32(0)
    glCreateProgramPipelines(1, program_pipeline)
    glUseProgramStages(program_pipeline, GL_VERTEX_SHADER_BIT, vertex_program)
    glUseProgramStages(program_pipeline, GL_FRAGMENT_SHADER_BIT, fragment_program)

    vertices = np.array(
        [
            0.5, -0.5, 0.0,
            -0.5, -0.5, 0.0,
            0.0,  0.5, 0.0
        ],
        dtype=np.float32,
    )

    vbo = c_uint32(0)
    vao = c_uint32(0)    

    glCreateBuffers(1, vbo)
    glCreateVertexArrays(1, vao)

    glNamedBufferStorage(vbo, vertices.nbytes, vertices, GL_DYNAMIC_STORAGE_BIT)
    glVertexArrayVertexBuffer(vao, 0, vbo, 0, 3 * vertices.itemsize)

    glEnableVertexArrayAttrib(vao, 0)
    glVertexArrayAttribFormat(vao, 0, 3, GL_FLOAT, GL_FALSE, 0)
    glVertexArrayAttribBinding(vao, 0, 0)


    while not glfwWindowShouldClose(window):
        process_input(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        time_value = glfwGetTime()
        green_value = np.sin(time_value) / 2.0 + 0.5
        vertex_color_location = glGetUniformLocation(fragment_program, "ourColor")
        glProgramUniform4f(fragment_program, vertex_color_location, 0.0, green_value, 0.0, 1.0)

        glBindProgramPipeline(program_pipeline)

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteProgram(program_pipeline)
    glDeleteProgramPipelines(program_pipeline)

    glfwDestroyWindow(window)
    glfwTerminate()


if __name__ == "__main__":
    main()
