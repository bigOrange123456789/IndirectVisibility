from OpenGL.GL import *
 
 
class Shader:
    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path, mode='r', encoding='utf-8') as vertex_stream:
            vertex_code = vertex_stream.readlines()
        with open (fragment_path, mode='r', encoding='utf-8') as fragment_stream:
            fragment_code = fragment_stream.readlines()
 
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_code)
        glCompileShader(vertex_shader)
        status = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not status:
            print("[ERROR]: " + bytes.decode(glGetShaderInfoLog(vertex_shader)))
 
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_code)
        glCompileShader(fragment_shader)
        status = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if not status:
            print("[ERROR]: " + bytes.decode(glGetShaderInfoLog(fragment_shader)))
 
        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)
        status = glGetProgramiv(shader_program, GL_LINK_STATUS )
        if not status:
            print("[ERROR]: " + bytes.decode(glGetProgramInfoLog(shader_program)))
 
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        self.shaderProgram = shader_program
 
    def use(self):
        glUseProgram(self.shaderProgram)
 
    def delete(self):
        glDeleteProgram(self.shaderProgram)