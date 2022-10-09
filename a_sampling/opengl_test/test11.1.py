import glfw
from OpenGL.GL import *
import numpy as np
 
import shader as shader
 
glfw.init()
window = glfw.create_window(800, 600, "shader", None, None)
glfw.make_context_current(window)
 
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)
 
vertices = np.array([   # 位置             颜色
                     0.5, -0.5, 0.0,  1.0, 0.0, 0.0,   # 右下
                    -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,   # 左下
                     0.0,  0.5, 0.0,  0.0, 0.0, 1.0    # 顶部
                    ])
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, 8 * vertices.size, vertices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), None)
glEnableVertexArrayAttrib(VAO, 0)
glVertexAttribPointer(1, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), ctypes.c_void_p(8 * 3))
glEnableVertexArrayAttrib(VAO, 1)
 
shaderProgram = shader.Shader("./glsl/test.vs.glsl", "./glsl/test.fs.glsl")

 
while not glfw.window_should_close(window):
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
 
    shaderProgram.use()
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)
 
    glfw.swap_buffers(window)
    glfw.poll_events()
 
shaderProgram.delete()