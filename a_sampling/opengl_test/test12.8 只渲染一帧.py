#需要： 将计算结果输出  #可以输入视图矩阵和投影矩阵

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
import numpy, math, sys 

elemSize=4 # uint32 以及 float32 占用空间的大小
# 3D scene
class Scene:
    # initialization
    def __init__(self):
        # create shader
        strVS = open(r"./glsl/test12.6.vs.glsl","r",encoding="utf-8").read()
        strFS = open(r"./glsl/test12.fs.glsl","r",encoding="utf-8").read()
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

        #enable arrays
        glEnableVertexAttribArray(self.vertIndex)

        # set buffers 
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, int(elemSize * 6), None)
        glEnableVertexArrayAttrib(self.VAO, 0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, int(elemSize * 6), ctypes.c_void_p(elemSize * 3))
        glEnableVertexArrayAttrib(self.VAO, 1)

        # draw
        glDrawElements(GL_TRIANGLES,self.EBO_Len , GL_UNSIGNED_INT, None)

        # disable arrays
        glDisableVertexAttribArray(self.vertIndex)             

class Renderer:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.aspect = self.width/float(self.height)


    def draw(self):
        def getImag():
            image_buffer = glReadPixels(0, 0, self.width,self.height, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
            image = numpy.frombuffer(image_buffer, dtype=numpy.uint8).reshape(self.width,self.height, 3)
            return image
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
        print(getImag())
        glutSwapBuffers()

    def run(self):
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.width, self.height)
        self.window = glutCreateWindow("Minimal")

        self.scene = Scene()
        self.draw()

glutInit(sys.argv)
prog = Renderer()
prog.run()