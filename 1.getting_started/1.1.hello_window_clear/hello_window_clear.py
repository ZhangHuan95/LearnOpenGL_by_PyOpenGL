import OpenGL.GL as gl
import glfw

SCR_WIDTH = 800
SCR_HEIGHT = 600


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
        SCR_WIDTH, SCR_HEIGHT, "Learning PyOpenGL", None, None)
    if window == 0:
        print("Failed to create GLFW window")
        glfw.terminate()
        return -1
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    while not glfw.window_should_close(window):
        processInput(window)
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()
    return 0


if __name__ == '__main__':
    main()
