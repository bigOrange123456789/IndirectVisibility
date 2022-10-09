#需要： 将计算结果输出  #可以输入视图矩阵和投影矩阵

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
import numpy, math, sys 

strVS = open(r"./glsl/test12.6.vs.glsl","r",encoding="utf-8").read()
strFS = open(r"./glsl/test12.fs.glsl","r",encoding="utf-8").read()
elemSize=4 # uint32 以及 float32 占用空间的大小
# 3D scene
class Scene:
    # initialization
    def __init__(self):
        # create shader
        self.program = compileProgram(
            compileShader(strVS,GL_VERTEX_SHADER),
            compileShader(strFS,GL_FRAGMENT_SHADER)
            )
        glUseProgram(self.program)

        self.pMatrixUniform = glGetUniformLocation(self.program, 'uPMatrix')
        self.mvMatrixUniform = glGetUniformLocation(self.program, "uMVMatrix")
        self.colorU = glGetUniformLocation(self.program, "uColor")

        # attributes
        self.vertIndex = glGetAttribLocation(self.program, "aVert")#aVert是着色器读取数据时的变量名
        self.vertColor = glGetAttribLocation(self.program, "cVert")
        # color
        self.col0 = [1.0, 1.0, 0.0, 1.0]

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        
        # vertices
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        vertexData = numpy.array([
           -0.2,    0.2,   0,   1.0, 0.0, 0.0,
             -0.2,  -0.2,   0,  1.0, 0.0, 0.0,
             0.2,    0.2,   0,  1.0, 0.0, 0.0,
              0,  -0.2,   0,    1.0, 0.0, 0.0,#s,    s,   0, 
             -1,  -1,   0,      1.0, 0.0, 0.0, 
             1,   1,   0,       0.0, 1.0, 0.0, 
             ], numpy.float32)  # 32位即4B
        glBufferData(GL_ARRAY_BUFFER, elemSize * len(vertexData), vertexData, GL_STATIC_DRAW)

        self.EBO=glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.EBO)
        indexData = numpy.array([
            0,1,3,
            3,4,5
             ], dtype='uint32')
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elemSize * len(indexData), indexData, GL_STATIC_DRAW)
        self.EBO_Len=len(indexData)#索引个数

    # render 
    def render(self, pMatrix, mvMatrix):  
        # use shader
        glUseProgram(self.program)

        # set proj matrix
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, pMatrix)

        # set modelview matrix
        glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)

        # set color
        glUniform4fv(self.colorU, 1, self.col0)

        #enable arrays
        glEnableVertexAttribArray(self.vertIndex)
        # glEnableVertexAttribArray(self.vertColor)

        # set buffers 
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, int(elemSize * 6), None)
        # glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, int(elemSize * 6), elemSize * 3)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, int(elemSize * 6), None)
        glEnableVertexArrayAttrib(self.VAO, 0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, int(elemSize * 6), ctypes.c_void_p(elemSize * 3))
        glEnableVertexArrayAttrib(self.VAO, 1)

        # draw
        glDrawElements(GL_TRIANGLES,self.EBO_Len , GL_UNSIGNED_INT, None)

        # disable arrays
        glDisableVertexAttribArray(self.vertIndex)     
        # glDisableVertexAttribArray(self.vertColor)            

class Renderer:
    def __init__(self):
        pass

    def reshape(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glClearColor(0.8, 0.8, 0.8,1.0)
        glutPostRedisplay()


    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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

        # render
        self.scene.render(pMatrix, mvMatrix)
        # swap buffers
        glutSwapBuffers()

    def run(self):
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(400, 400)
        self.window = glutCreateWindow("Minimal")
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.draw)
        self.scene = Scene()
        glutMainLoop()

glutInit(sys.argv)
prog = Renderer()
prog.run()