import OpenGL.GL as gl
import glfw
import sys
import numpy as np

SCR_WIDTH = 800
SCR_HEIGHT = 600

vertexShaderSource = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

fragmentShaderSource = """
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

def frame_size_callback(window, width, height):
    gl.glViewport(0, 0, width, height)


def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def framebuffer_size_callback(window, width, height):
    gl.glViewport(0, 0, width, height)


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(
        SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)

    if window == 0:
        print("Failed to create GLFW window")
        glfw.terminate()
        return -1

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, frame_size_callback)

    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertexShader, vertexShaderSource)
    gl.glCompileShader(vertexShader)

    success = gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS)
    if not success:
        infoLog = gl.glGetShaderInfoLog(vertexShader)
        print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n", infoLog)

    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader, fragmentShaderSource)
    gl.glCompileShader(fragmentShader)
    success = gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS)
    if not success:
        infoLog = gl.glGetShaderInfoLog(fragmentShader)
        print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n", infoLog)

    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)
    success = gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS)
    if not success:
        infoLog = gl.glGetProgramInfoLog(shaderProgram)
        print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n", infoLog)

    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)

    vertices = np.array([
        -0.5, -0.5, 0,  # left
        0.5, -0.5, 0,  # right
        0, 0.5, 0  # top
    ], dtype=np.float32)

    VAO = gl.glGenVertexArrays(1)
    VBO = gl.glGenBuffers(1)
    gl.glBindVertexArray(VAO)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sys.getsizeof(
        vertices), vertices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(
        0, 3, gl.GL_FLOAT, gl.GL_FALSE, 12,  None)
    gl.glEnableVertexAttribArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)
    while not glfw.window_should_close(window):
        processInput(window)
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glUseProgram(shaderProgram)
        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # gl.glDeleteVertexArrays(1, VAO) 这里有点问题。暂时不知道怎么解决
    # gl.glDeleteBuffers(1, VBO)
    glfw.terminate()
    return 0


if __name__ == "__main__":
    main()
