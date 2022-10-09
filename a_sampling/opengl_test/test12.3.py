#需要： 1.顶点颜色 2.顶点索引 #可以输入视图矩阵和投影矩阵

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

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        
        # vertices
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        s = 0.2
        # vertexData = numpy.array([
        #     -s,    s,   0, 0,
        #      -s,  -s,   0, 0,
        #      s,    s,   0, 0,
        #      s,    s,   0, 0,
        #      -s,  -s,   0, 0,
        #      s,   -s,   0, 0 
        #      ], numpy.float32)  # 32位即4B
        vertexData = numpy.array([
           -s,    s,   0, 
             -s,  -s,   0, 
             s,    s,   0, 
              0,  -s,   0,#s,    s,   0, 
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
        print("sys.getsizeof(vertexData)",sys.getsizeof(vertexData))
        print("4 * len(vertexData)",4 * len(vertexData))

        self.EBO=glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.EBO)
        indexData = numpy.array([
            0,1,3,
            3,4,5
             ], dtype='uint32')
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER,sys.getsizeof(indexData),indexData,GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(indexData), indexData, GL_STATIC_DRAW)
        print("sys.getsizeof(indexData)",sys.getsizeof(indexData))
        print("4 * len(indexData)",4 * len(indexData))
 

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
        elemSize=4
        glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, int(elemSize * 3), None)#glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, int(4 * 6), None)#glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, 0, None)#最后一位应该是偏移量
                        #      缓存区       取前三个  元素格式  ？   ？        
        '''
        index:第几个属性,从0开始取，0，1，2，顺序自己定义，例如顶点位置，纹理，法线 这里只有顶点位置，也只能讨论顶点位置，所以为0
        size:一个顶点所有数据的个数，这里每个顶点又两个浮点数属性值，所以是2
        type:顶点描述数据的类型，这里position数组中的数据全部为float，所以是GL_FLOAT
        normalized:是否需要显卡帮忙把数据归一化到-1到+1区间，这里不需要，所以设置GL_FALSE
        stride:一个顶点占有的总的字节数，这里为两个float，所以是sizeof(float)*2
        pointer:当前指针指向的vertex内部的偏离字节数，可以唯一的标识顶点某个属性的偏移量 这里是指向第一个属性,顶点坐标,偏移量为0
        '''
        # glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), None)
        # glVertexAttribPointer(1, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), ctypes.c_void_p(8 * 3))
        # GL_ELEMENT_ARRAY_BUFFER

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        # glVertexAttribPointer(self.vertIndex, 3, GL_UNSIGNED_INT, GL_FALSE, int(elemSize * 3), None)#glVertexAttribPointer(self.vertIndex, 3, GL_UNSIGNED_INT, GL_FALSE, int(elemSize * 3), None) #GL_BYTE, GL_SHORT,GL_FIXED,GL_FLOAT; 
        # glVertexAttribPointer(0, 3, GL_UNSIGNED_INT, False, 0, None)
        '''
        index:指定要修改的顶点属性的索引值
        size:指定每个顶点属性的组件数量。必须为1、2、3或者4。初始值为4。（如position是由3个（x,y,z）组成，而颜色是4个（r,g,b,a））
        type:指定数组中每个组件的数据类型。可用的符号常量有GL_BYTE, GL_UNSIGNED_BYTE, GL_SHORT,GL_UNSIGNED_SHORT, GL_FIXED, 和 GL_FLOAT，初始值为GL_FLOAT。
        normalized:指定当被访问时，固定点数据值是否应该被归一化（GL_TRUE）或者直接转换为固定点值（GL_FALSE）。   
        stride:指定连续顶点属性之间的偏移量。如果为0，那么顶点属性会被理解为：它们是紧密排列在一起的。初始值为0。
        pointer:指定一个指针，指向数组中第一个顶点属性的第一个组件。初始值为0。
        '''


        # draw
        # glDrawArrays(GL_TRIANGLES, 0, 6)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
        # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        # glDrawElements(GL_TRIANGLES, 2, GL_UNSIGNED_INT, None)
        '''
        mode:接受的值和在glBegin()中接受的值一样，可以是GL_POLYGON、GL_TRIANGLES、GL_TRIANGLE_STRIP、GL_LINE_STRIP等。
        count：组合几何图形的元素的个数，一般是点的个数。
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