import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import pygame
import cv2
import math
class Mesh0():
    def __init__(self,id,V,F):
        self.color=np.array([
            id&0xff0000,
            id&0x00ff00,
            id&0x0000ff
            ])/255
        # print("f",F)
        self.face=np.array(F).reshape(-1)
        # self.vertex=np.dot(
        #         np.array(V),
        #         np.array([#x2=x1 y2=-z1 z2=y1
        #             [1,0,0],
        #             [0,0,1],
        #             [0,-1,0]
        #         ])
        #     )
        self.vertex=np.array(V)
        self.vertex=self.vertex.reshape(-1)
        self.createVAO()
    def createVAO(this):
        this.vbo = vbo.VBO(np.array(this.vertex,'f'))
        this.ebo = vbo.VBO(np.array(this.face,'H'),target = GL_ELEMENT_ARRAY_BUFFER)
        this.vboLength = len(this.vertex)
        this.eboLength = len(this.face)
        this.bCreate = True
    def draw(this):
        glColor4f(this.color[0], this.color[1], this.color[2], 1.0)  # 设置当前颜色为红色不透明
        this.vbo.bind()
        glInterleavedArrays(GL_V3F,0,None)
        this.ebo.bind()
        glDrawElements(GL_TRIANGLES,this.eboLength,GL_UNSIGNED_SHORT,None)   

class Camera:#摄像机漫游
     origin = [0.0,0.0,0.0]
     length = 1.
     yangle = 0.#俯仰角
     zangle = 0.#偏航角
     __bthree = False
     def __init__(this):
         this.mouselocation = [0.0,0.0]
         this.offest = 0.1#0.01
         this.zangle = 0. if not this.__bthree else math.pi
     def setthree(this,value):
         this.__bthree = value
         this.zangle = this.zangle + math.pi
         this.yangle = -this.yangle          
     def eye(this):#返回视点的位置（即this.origin）
         return this.origin if not this.__bthree else this.direction()
     def target(this):
         return this.origin if this.__bthree else this.direction()
     def direction(this):
         if this.zangle > math.pi * 2.0 :
             this.zangle < - this.zangle - math.pi * 2.0
         elif this.zangle < 0. :
             this.zangle < - this.zangle + math.pi * 2.0
         len = 1. if not this.__bthree else this.length if 0. else 1.
         xy = math.cos(this.yangle) * len
         x = this.origin[0] + xy * math.sin(this.zangle)
         y = this.origin[1] + len * math.sin(this.yangle)
         z = this.origin[2] + xy * math.cos(this.zangle)        
         return [x,y,z]
     def move(this,x,y,z):
         sinz,cosz = math.sin(this.zangle),math.cos(this.zangle)        
         xstep,zstep = x * cosz + z * sinz,z * cosz - x * sinz
         if this.__bthree : 
             xstep = -xstep
             zstep = -zstep
         this.origin = [this.origin[0] + xstep,this.origin[1] + y,this.origin[2] + zstep]        
         print("this.origin",this.origin)
     def positionSet(this,x,y,z):
        this.origin=[x,y,z]
     def rotate(this,z,y):#z偏航角;y俯仰角
         this.zangle,this.yangle = this.zangle - z,this.yangle + y if not this.__bthree else -y
     def rotateSet(this,z,y):
        this.zangle,this.yangle = z,y
     def setLookat(this):
         ve,vt = this.eye(),this.target()
         glLoadIdentity()
         gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2],0.0,1.0,0.0)  #视角朝向的控制
     def keypress(this,key,x,y):#  print("key",key,key in ('e',b'e'))
         if key in ('e', 'E',b'e', b'E'):#  print(key,this.offest)
             this.move(0.,0.,1 * this.offest)
         if key in (b'f', b'F'):
             this.move(1 * this.offest,0.,0.)
         if key in (b's', b'S'):
             this.move(-1 * this.offest,0.,0.)
         if key in (b'd', b'D'):
             this.move(0.,0.,-1 * this.offest)
         if key in (b'w', b'W'):
             this.move(0.,1 * this.offest,0.)
         if key in (b'r', b'R'):
             this.move(0.,-1 * this.offest,0.)
         if key in (b'v', b'V'):#this.__bthree = not this.__bthree
             this.setthree(not this.__bthree)
         if key == GLUT_KEY_UP:
             this.offest = this.offest + 0.1
         if key == GLUT_KEY_DOWN:
             this.offest = this.offest - 0.1
     def mouse(this,x,y):  
         rx = (x - this.mouselocation[0]) * this.offest * 0.1
         ry = (y - this.mouselocation[1]) * this.offest * -0.1
         this.rotate(rx,ry)
         this.mouselocation = [x,y]#记录鼠标此刻的位置

class Rasterization:  
    def __init__(self,renderNodes,v):
        camera = Camera()#common.camera()

        def InitGL(width,height):
            glClearColor(1,1,1,1)#(0.1,0.1,0.5,0.1)#背景颜色
            glClearDepth(1.0)
            glMatrixMode(GL_PROJECTION)#设置投影矩阵
            glLoadIdentity()
            gluPerspective(90,float(width)/float(height),0.1,30000)#初始化视图矩阵     
            camera.positionSet(2213.0870081831645,  23, -1888.057576657758)

        def DrawGLScene():
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)    
            camera.setLookat()
            for m in renderNodes:
                m.draw()
                             
            glutSwapBuffers()
 
        def mouseButton( button, mode, x, y ):    
            if button == GLUT_RIGHT_BUTTON:
                camera.mouselocation = [x,y]
 
        def ReSizeGLScene(Width, Height): 
            glViewport(0, 0, Width, Height)        
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45.0, float(Width)/float(Height), 0.1, 30000)
            glMatrixMode(GL_MODELVIEW)

        width = 800
        height = 800

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width,height)
        glutInitWindowPosition(0,0)
        glutCreateWindow("opengl")

        # pygame.display.set_mode((width,height), DOUBLEBUF | OPENGL)

        InitGL(width, height)
        
        # pygame.display.set_mode((width,height), DOUBLEBUF | OPENGL)

        loop=False#True
        if loop:
            glutDisplayFunc(DrawGLScene)
            glutIdleFunc(DrawGLScene)
            # glutReshapeFunc(ReSizeGLScene)
            glutMouseFunc( mouseButton )
            
            glutMotionFunc(camera.mouse)
            glutKeyboardFunc(camera.keypress)
            glutSpecialFunc(camera.keypress)
            
            glutMainLoop()
        else:
            DrawGLScene()
            # pygame.time.wait(10000)

            image_buffer = glReadPixels(0, 0, width,height, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
            image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(width,height, 3)
            cv2.imwrite(r"image.png", image)
            pygame.quit()


        
        
    @staticmethod
    def getMesh0(mesh,matrix,id):
        # print(mesh.vertex)
        # print(mesh.face)
        
        matrixInstance=np.array(matrix).reshape(4,4).T
        vertex0=np.array(mesh.vertex)
        vertex0=np.c_[vertex0,np.ones(vertex0.shape[0])] #c_是column(列)的缩写，就是按列叠加两个矩阵，就是把两个矩阵左右组合，要求行数相等。
        vertex0=np.dot(vertex0,matrixInstance)[:,0:3]

        vertex0=np.dot(
                np.array(vertex0),
                np.array([
                    [1,0,0],
                    [0,0,-1],
                    [0,1,0]
                ])
            )

        # print(vertex0,np.array(mesh.face)-1)
        # exit(0)
        return Mesh0(id,vertex0,np.array(mesh.face)-1)
