import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from OpenGL.arrays import vbo
import numpy, math, sys 

strVS = """
attribute vec3 aVert;
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform vec4 uColor;
varying vec4 vCol;

void main() {
  // option #1 - fails
  gl_Position = uPMatrix * uMVMatrix * vec4(aVert, 1.0); 
  // option #2 - works
  gl_Position = vec4(aVert, 1.0); 
  // set color
  vCol = vec4(uColor.rgb, 1.0);
}
"""
strFS = """
varying vec4 vCol;

void main() {
  // use vertex color
  gl_FragColor = vCol;
}

"""

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
        self.vertIndex = glGetAttribLocation(self.program, "aVert")
        # color
        self.col0 = [1.0, 1.0, 0.0, 1.0]

        # define quad vertices 
        s = 0.2
        quadV = [
            -s, s, 0.0, 
             -s, -s, 0.0, 
             s, s, 0.0,
             s, s, 0.0,
             -s, -s, 0.0, 
             s, -s, 0.0
             ]

        # vertices
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        vertexData = numpy.array(quadV, numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, GL_STATIC_DRAW)

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