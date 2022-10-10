from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy, math, sys 
class Renderer:
    def __init__(self,w,h,V,F):
        self.width = w
        self.height = h
        self.elemSize=4# uint32 以及 float32 占用空间的大小
        self.aspect = self.width/float(self.height)

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)# 显示模式:GLUT_SINGLE无缓冲直接显示|GLUT_RGBA采用RGB(A非alpha)#glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("test")
        glutHideWindow()

        # create shader
        strVS = open(r"./a_sampling/renderLib/glsl/vert.glsl","r",encoding="utf-8").read()
        strFS = open(r"./a_sampling/renderLib/glsl/frag.glsl","r",encoding="utf-8").read()
        self.program = compileProgram(
            compileShader(strVS,GL_VERTEX_SHADER),
            compileShader(strFS,GL_FRAGMENT_SHADER)
            )
        glUseProgram(self.program)

        self.pMatrixUniform = glGetUniformLocation(self.program, 'uPMatrix')
        self.mvMatrixUniform = glGetUniformLocation(self.program, "uMVMatrix")

        # attributes
        self.vertIndex = glGetAttribLocation(self.program, "aVert")#aVert是着色器读取数据时的变量名

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        
        # vertices
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        # print("v",V)
        vertexData = numpy.array(V, numpy.float32)  # 32位即4B
        glBufferData(GL_ARRAY_BUFFER, self.elemSize * len(vertexData), vertexData, GL_STATIC_DRAW)

        self.EBO=glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.EBO)
        indexData = numpy.array(F, dtype='uint32')
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.elemSize * len(indexData), indexData, GL_STATIC_DRAW)
        self.EBO_Len=len(indexData)#索引个数

    # render 
    def render(self, pMatrix, mvMatrix):  
        glClearColor(1,1,1,1)#(0.1,0.1,0.5,0.1)#背景颜色
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#清空颜色缓存区和深度缓存区

        # use shader
        glUseProgram(self.program)

        # set proj matrix
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, pMatrix)

        # set modelview matrix
        glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)

        #enable arrays
        glEnableVertexAttribArray(self.vertIndex)

        # set buffers 
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, int(self.elemSize * 6), None)
        glEnableVertexArrayAttrib(self.VAO, 0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, int(self.elemSize * 6), ctypes.c_void_p(self.elemSize * 3))
        glEnableVertexArrayAttrib(self.VAO, 1)

        # draw
        glDrawElements(GL_TRIANGLES,self.EBO_Len , GL_UNSIGNED_INT, None)

        # disable arrays
        glDisableVertexAttribArray(self.vertIndex)  
    
    def getVP(self):
        # build projection matrix
        fov = math.radians(45.0)
        f = 1.0/math.tan(fov/2.0)
        zN, zF = (0.1, 100.0)
        a = self.aspect
        pMatrix = numpy.array([f/a, 0.0, 0.0,               0.0, 
                               0.0, f,   0.0,               0.0, 
                               0.0, 0.0, (zF+zN)/(zN-zF),  -1.0, 
                               0.0, 0.0, 2.0*zF*zN/(zN-zF), 0.0], numpy.float32)

        # modelview matrix
        mvMatrix = numpy.array([1.0, 0.0, 0.0, 0.0, 
                                0.0, 1.0, 0.0, 0.0, 
                                0.0, 0.0, 1.0, 0.0, 
                                0.5, 0.0, -5.0, 1.0], numpy.float32)
        return pMatrix, mvMatrix
    @staticmethod
    def getVP2(direction,pos):
        V_All_Inverse=[
            [
                1, 0, 0, 0, 
                0, 1, 0, 0, 
                0, 0, 1, 0, 
                2207, 27, -1880, 1
            ],
            [
                1, 0, 0, 0, 
                0, 2.220446049250313e-16, 1, 0, 
                0, -1, 2.220446049250313e-16, 0, 
                2207, 27, -1880, 1
            ],
            [
                1, 0, 0, 0, 
                0, -1, 1.2246467991473532e-16, 0, 
                0, -1.2246467991473532e-16, -1, 0, 
                2207, 27, -1880, 1
            ],

            [
                1, 0, 0, 0, 
                0, -2.220446049250313e-16, -1, 0, 
                0, 1, -2.220446049250313e-16, 0, 
                2207, 27, -1880, 1
            ],
            [
                2.220446049250313e-16, 0, -1, 0, 
                0, 1, 0, 0, 
                1, 0, 2.220446049250313e-16, 0, 
                2207, 27, -1880, 1
            ],
            [
                2.220446049250313e-16, 0, 1, 0, 
                0, 1, 0, 0, 
                -1, 0, 2.220446049250313e-16, 0, 
                2207, 27, -1880, 1
            ]
        ]
        v_inverse=V_All_Inverse[direction]
        for i in range(3):
            v_inverse[12+i]=pos[i]
        v_inverse=numpy.array(v_inverse, numpy.float32).reshape(4,4)
        v=numpy.linalg.inv(v_inverse).reshape(-1)
        p=numpy.array([
            1.0000000000000002, 0, 0, 0, 
            0, 1.0000000000000002, 0, 0, 
            0, 0, -1.000006666688889, -1, 
            0, 0, -0.20000066666888888, 0
        ], numpy.float32)
        return p,v


    def getImag(self):
        image_buffer = glReadPixels(0, 0, self.width,self.height, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
        image = numpy.frombuffer(image_buffer, dtype=numpy.uint8).reshape(self.width,self.height, 3)
        return image
if __name__ == "__main__":#用于测试
    prog = Renderer(
        400,400,
        [
            -0.2,    0.2,   0,   1.0, 0.0, 0.0,
            -0.2,  -0.2,   0,  1.0, 0.0, 0.0,
            0.2,    0.2,   0,  1.0, 0.0, 0.0,
            0,  -0.2,   0,    1.0, 0.0, 0.0, #s,    s,   0, 
            -1,  -1,   0,      1.0, 0.0, 0.0, 
            1,   1,   0,       0.0, 1.0, 0.0, 
        ],
        [
            0,1,3,
            3,4,5
        ]
    )
    pMatrix, mvMatrix=prog.getVP()
    prog.render(pMatrix, mvMatrix)
    print(prog.getImag())

