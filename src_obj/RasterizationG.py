import numpy as np
import cv2
import math
import pygame
from renderLib.Mesh0 import Mesh0
from renderLib.Camara import Camera
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

class Rasterization:  
    def loop(self):
        camera=self.camera
        def mouseButton( button, mode, x, y ):    
            if button == GLUT_RIGHT_BUTTON:
                camera.mouselocation = [x,y]
        def ReSizeGLScene(Width, Height): 
            glViewport(0, 0, Width, Height)        
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45.0, float(Width)/float(Height), 0.1, 30000)
            glMatrixMode(GL_MODELVIEW)
        glutDisplayFunc(self.DrawGLScene)
        glutIdleFunc(self.DrawGLScene)
        # glutReshapeFunc(ReSizeGLScene)
        glutMouseFunc( mouseButton )
        glutMotionFunc(camera.mouse)
        glutKeyboardFunc(camera.keypress)
        glutSpecialFunc(camera.keypress)
        glutMainLoop()
    def DrawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)    
        self.camera.setLookat()
        for m in self.renderNodes:
            m.draw()                   
        glutSwapBuffers()
        
    def __init__(self,opt):
        self.renderNodes=opt["renderNodes"]
        loop=opt["loop"]  #  False  #  True  #  
        width=opt["width"]
        height=opt["height"]
        self.width=width
        self.height=height

        self.camera = Camera()
        # self.camera.positionSet(2213.0870081831645,  23, -1888.057576657758)

        if loop:
            glutInit()
            glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
            glutInitWindowSize(width,height)
            glutInitWindowPosition(0,0)
            glutCreateWindow("opengl")
        else:
            glutInit()
            glutCreateWindow("opengl")
            pygame.display.set_mode((width,height), DOUBLEBUF | OPENGL)
        def InitGL(width,height):
            glClearColor(1,1,1,1)#(0.1,0.1,0.5,0.1)#背景颜色
            glClearDepth(1.0)
            glMatrixMode(GL_PROJECTION)#设置投影矩阵
            glLoadIdentity()
            gluPerspective(90,float(width)/float(height),0.1,30000)#初始化视图矩阵  
        InitGL(width, height)
        
        if loop:
            self.loop()
        
    def getPanorama(self):
        camera=self.camera
        def cut(r,name):
            camera.rotationSet(r[0],r[1])
            self.DrawGLScene()
            image_buffer = glReadPixels(0, 0, self.width,self.height, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
            image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(self.width,self.height, 3)
            cv2.imwrite(name, image)# pygame.quit()
        rotations=[#z偏航角;y俯仰角
            [0,0],
            [math.pi/2,0],
            [math.pi,0],
            [3*math.pi/2,0],
            [0,math.pi/2],
            [0,1e-10-math.pi/2]
        ]
        for i in range(6):
            cut(rotations[i],str(i)+".png")
    def render(self,x,y,z):
        self.camera.positionSet(x,y,z)
        camera=self.camera
        def getImag(r):
            camera.rotationSet(r[0],r[1])
            self.DrawGLScene()
            image_buffer = glReadPixels(0, 0, self.width,self.height, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
            image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(self.width,self.height, 3)
            return image
        rotations=[#z偏航角;y俯仰角
            [0,0],
            [math.pi/2,0],
            [math.pi,0],
            [3*math.pi/2,0],
            [0,math.pi/2],
            [0,1e-10-math.pi/2]
        ]
        result={}
        for i in range(6):
            image=getImag(rotations[i])
            result[i]=image
        return result
        
    @staticmethod
    def getMesh0(mesh,matrix,id):
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
        return Mesh0(id,vertex0,np.array(mesh.face)-1)
