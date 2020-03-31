import ctypes
import sys
import os
from OpenGL.GL import *


class Shader(object):

    def __int__(self, vertexPath, fragmentPath, geometryPath):
        try:
            self.vShaderFile = open(vertexPath)
            self.fShaderFile = open(fragmentPath)
            self.vertexCode = self.vShaderFile.read()
            self.fragmentCode = self.fShaderFile.read()
            self.vShaderFile.close()
            self.fShaderFile.close()
            if geometryPath is not None:
                self.gShaderFile = open(geometryPath)
                self.geometryCode = self.gShaderFile.read()
                self.gShaderFile.close()
        except OSError:
            print("read file error")

        self.vertex = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertex, 1, self.vertexCode, None)
        glCompileShader(self.vertex)

    def __checkComileErrors(self, shader, _type):
        success = GLint()
        infoLog = GLchar(1024)
        if _type != "PROGRAM":
            glGetShaderiv(shader, GL_COMPILE_STATUS, success)
            if not success:
                glGetShaderInfoLog(shader, 1024, None, infoLog)
                print("ERROR::SHADER_COMPILATION_ERROR of type:%s\n%s\n", _type, infoLog)
        else:
            glGetProgramiv(shader, GL_LINK_STATUS, success)
            if not success:
                glGetProgramInfoLog(shader, 1024, None, infoLog)
                print("ERROR::PROGRAM_LINKING_ERROR of type:%s\n%s\n", _type, infoLog)
