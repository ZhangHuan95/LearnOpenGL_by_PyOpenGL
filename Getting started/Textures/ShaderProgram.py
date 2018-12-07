import os
import sys
import numpy as np
from OpenGL.GL import *


class ShaderProgram(object):
    def __int__(self, vert_path="", frag_path=""):
        self.vert_path = vert_path
        self.frag_path = frag_path
        v_flag = os.path.exists(self.vert_path)
        f_flag = os.path.exists(self.frag_path)
        if not v_flag:
            print("Vertex shader file (--> %s <--) doesn't exist!" % self.vert_path)
        if not f_flag:
            print("Fragment shader file (--> %s <--) doesn't exist!" % self.frag_path)
        if not (f_flag and v_flag):
            sys.exit(1)
        self.initProgram()

    def initProgram(self):
        self.program_id = glCreateProgram()
        vertexSource = self.loadShader(self.vert_path)
        fragmentSource = self.loadShader(self.frag_path)
        vert_id = self.getShader(vertexSource, GL_VERTEX_SHADER)
        frag_id = self.getShader(fragmentSource, GL_FRAGMENT_SHADER)
        glAttachShader(self.program_id, vert_id)
        glAttachShader(self.program_id, frag_id)
        glLinkProgram(self.program_id)
        if glGetProgramiv(self.program_id, GL_LINK_STATUS) != GL_TRUE:
            info = glGetShaderInfoLog(self.program_id)
            glDeleteProgram(self.program_id)
            glDeleteShader(vert_id)
            glDeleteShader(frag_id)
            raise RuntimeError("Error in program linking:%s" % info)
        glDeleteShader(vert_id)
        glDeleteShader(frag_id)

    def loadShader(self, path):
        source_file = open(path)
        shader_source = source_file.read()
        source_file.close()
        return shader_source

    def getShader(self, shader_source, shader_type):
        try:
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, shader_source)
            glCompileShader(shader_id)
            if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
                info = glGetShaderInfoLog(shader_id)
                raise RuntimeError('Shader compilation failed:\n %s' % info)
            return shader_id
        except:
            glDeleteShader(shader_id)
            raise

    def attribLocation(self, name):
        return glGetAttribLocation(self.program_id, name)

    def uniformLocation(self, name):
        return glGetUniformLocation(self.program_id, name)
