#需要： 1.顶点颜色 2.顶点索引

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from OpenGL.arrays import vbo
import numpy, math, sys 

strVS = open(r"./glsl/test12.vs.glsl","r",encoding="utf-8").read()
strFS = open(r"./glsl/test12.fs.glsl","r",encoding="utf-8").read()

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
        # self.vertColor = glGetAttribLocation(self.program, "cVert")
        # color
        self.col0 = [1.0, 1.0, 0.0, 1.0]

        # vertices
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        s = 0.2
        vertexData = numpy.array([
            -s,    s,   0, 
             -s,  -s,   0, 
             s,    s,   0,
             s,    s,   0,
             -s,  -s,   0, 
             s,   -s,   0
             ], numpy.float32)  # 32位即4B
        # vertexData2 = numpy.array([   # 位置    颜色
        #              0.5, -0.5, 0.0,  1.0, 0.0, 0.0,   # 右下
        #             -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,   # 左下
        #              0.0,  0.5, 0.0,  0.0, 0.0, 1.0    # 顶部
        #             ])#每个变量大小默认8B
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertexData), vertexData, GL_STATIC_DRAW)
        # glBufferData(GL_ARRAY_BUFFER, 8 * vertexData2.size, vertexData2, GL_STATIC_DRAW)

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

        # set buffers 
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, 0, None)
        # glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), None)
        # glVertexAttribPointer(1, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), ctypes.c_void_p(8 * 3))

        # draw
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # disable arrays
        glDisableVertexAttribArray(self.vertIndex)            


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

    def keyPressed(self, *args):
        sys.exit()

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
        glutKeyboardFunc(self.keyPressed) # Checks for key strokes
        self.scene = Scene()
        glutMainLoop()

glutInit(sys.argv)
prog = Renderer()
prog.run()