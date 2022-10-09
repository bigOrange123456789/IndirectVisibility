#需要： 顶点颜色  #可以输入视图矩阵和投影矩阵

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
import numpy, math, sys 

strVS = open(r"./glsl/test12.vs.glsl","r",encoding="utf-8").read()
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
        # self.vertColor = glGetAttribLocation(self.program, "cVert")
        # color
        self.col0 = [1.0, 1.0, 0.0, 1.0]

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)
        
        # vertices
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        vertexData = numpy.array([
           -0.2,    0.2,   0,  1.0, 0.0, 0.0,
             -0.2,  -0.2,   0,  1.0, 0.0, 0.0,
             0.2,    0.2,   0, 1.0, 0.0, 0.0,
              0,  -0.2,   0, 1.0, 0.0, 0.0,#s,    s,   0, 
             -1,  -1,   0, 1.0, 0.0, 0.0, 
             1,   1,   0, 1.0, 0.0, 0.0, 
             ], numpy.float32)  # 32位即4B
        glBufferData(GL_ARRAY_BUFFER, elemSize * len(vertexData), vertexData, GL_STATIC_DRAW)

        self.EBO=glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.EBO)
        indexData = numpy.array([
            0,1,3,
            3,4,5
             ], dtype='uint32')
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elemSize * len(indexData), indexData, GL_STATIC_DRAW)
        self.index_len=len(indexData)#索引个数

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
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, int(elemSize * 6), None)
        '''
        index:第几个属性,从0开始取，0，1，2，顺序自己定义，例如顶点位置，纹理，法线 这里只有顶点位置，也只能讨论顶点位置，所以为0
        size:一个顶点所有数据的个数，这里每个顶点又两个浮点数属性值，所以是2
        type:顶点描述数据的类型，这里position数组中的数据全部为float，所以是GL_FLOAT
        normalized:是否需要显卡帮忙把数据归一化到-1到+1区间，这里不需要，所以设置GL_FALSE
        stride:一个顶点占有的总的字节数，这里为两个float，所以是sizeof(float)*2
        pointer:当前指针指向的vertex内部的偏离字节数，可以唯一的标识顶点某个属性的偏移量 这里是指向第一个属性,顶点坐标,偏移量为0
        '''

        # draw
        # glDrawArrays(GL_TRIANGLES, 0, 6)
        glDrawElements(GL_TRIANGLES,self.index_len , GL_UNSIGNED_INT, None)
        '''
        mode:接受的值和在glBegin()中接受的值一样，可以是GL_POLYGON、GL_TRIANGLES、GL_TRIANGLE_STRIP、GL_LINE_STRIP等。
        count:组合几何图形的元素的个数，一般是点的个数。
        type:indeices数组的数据类型，既然是索引，一般是整型的。
        indices:索引数组
        '''

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