if __name__ == "__main__":  # 用于测试
 __author__ = "WSX"

 import numpy as np

 from OpenGL.GLUT import *

 from OpenGL.GL import *

 import ctypes

 #顶点着色器部分

 VERTEX_SHADER = """

 #version 330

 layout (location = 0) in vec3 Position;

 void main()

 {

     gl_Position = vec4(0.5 * Position.x, 0.5 * Position.y, Position.z, 1.0);

     }

 """

 #片段着色器部分,字符串类型

 FRAGMENT_SHADER = """

 #version 330

 out vec4 FragColor;

 void main()

 {

     FragColor = vec4(1.0, 0.0, 0.0, 1.0);

     }

 """

 def Create_Shader( ShaderProgram, Shader_Type , Source):  #创建并且添加着色器（相当于AddShader）Shader_Type为类型

     ShaderObj = glCreateShader( Shader_Type )  #创建Shader对象

     glShaderSource(ShaderObj , Source)

     glCompileShader(ShaderObj)  #进行编译

     glAttachShader(ShaderProgram, ShaderObj)  #将着色器对象关联到程序上

 def Compile_Shader():  #编译着色器

     Shader_Program = glCreateProgram()  #创建空的着色器程序

     Create_Shader(Shader_Program , GL_VERTEX_SHADER , VERTEX_SHADER)

     Create_Shader(Shader_Program , GL_FRAGMENT_SHADER , FRAGMENT_SHADER)

     glLinkProgram(Shader_Program)

     glUseProgram(Shader_Program)

 def Draw():

     glClear(GL_COLOR_BUFFER_BIT)

     glEnableVertexAttribArray(0)

     glBindBuffer(GL_ARRAY_BUFFER, VBO)

     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None) #这里的None不能写为0

     glDrawArrays(GL_TRIANGLES, 0, 3)

     glDisableVertexAttribArray(0)  #解析数据 例如一个矩阵里含有 位置 、颜色、多种信息

     glutSwapBuffers()

 def CreateBuffer():  #创建顶点缓存器

     global VBO   #设置为全局变量

     vertex = np.array([[-1.0,-1.0,0.0],

                        [1.0,-1.0,0.0],

                        [0.0,1.0,0.0]],dtype="float32")   #创建顶点数组

     VBO = glGenBuffers(1)  #创建缓存

     glBindBuffer(GL_ARRAY_BUFFER , VBO)   #绑定

     glBufferData(GL_ARRAY_BUFFER , vertex.nbytes , vertex , GL_STATIC_DRAW)   #输入数据

 def main():

     glutInit([])

     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  # 显示模式 双缓存

     glutInitWindowPosition(100, 100)  # 窗口位置

     glutInitWindowSize(500, 500)  # 窗口大小

     glutCreateWindow("sanjiao")  # 创建窗口

     glutInitContextVersion(4,3)   #为了兼容

     glutInitContextProfile(GLUT_CORE_PROFILE)   #为了兼容

     glutDisplayFunc(Draw)  # 回调函数

     glClearColor(0.0, 0.0, 0.0, 0.0)

     CreateBuffer()

     Compile_Shader()

     glutMainLoop()

 main()