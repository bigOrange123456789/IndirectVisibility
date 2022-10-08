import numpy as np
import cv2
import math
import os
import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *
from renderLib.Camara import Camera
class Rasterization:  
    def loop(self):
        def mouseButton( button, mode, x, y ):    
            if button == GLUT_RIGHT_BUTTON:
                self.camera.mouselocation = [x,y]
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
        glutMotionFunc(self.camera.mouse)
        glutKeyboardFunc(self.camera.keypress)
        glutSpecialFunc(self.camera.keypress)
        glutMainLoop()
    def DrawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)    
        self.camera.setLookat()
        for m in self.renderNodes:
            m.draw()       
        return  
    def __init__(self,opt):
        self.renderNodes=opt["renderNodes"]
        loop=opt["loop"]  #  False  #  True  #  
        width=opt["width"]
        height=opt["height"]
        self.width=width
        self.height=height
        self.camera = Camera()
        # self.camera.positionSet(2213.0870081831645,  23, -1888.057576657758)

        def InitGL(width,height):
            os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d"%(-1000,-1000)
            glClearColor(1,1,1,1)#(0.1,0.1,0.5,0.1)#背景颜色
            glClearDepth(1.0)
            glMatrixMode(GL_PROJECTION)#设置投影矩阵
            glLoadIdentity()
            gluPerspective(90,float(width)/float(height),0.1,30000)#初始化视图矩阵  
        if loop:
            glutInit()
            glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
            glutInitWindowSize(width,height)
            glutInitWindowPosition(0,0)
            glutCreateWindow("opengl")
            InitGL(width, height)
        # else:
        #     # os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d"%(-1000,-1000)
        #     glutInit()
        #     glutCreateWindow("lzc test1")
        #     # glutInitWindowSize(1,1)
        #     # glutInitWindowPosition(-1000,-1000)
        #     os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d"%(-1000,-1000)
        #     icon=pygame.image.load("icon.png")
        #     pygame.display.set_icon(icon)
        #     pygame.display.set_mode((width,height), DOUBLEBUF | OPENGL)
        #     pygame.display.set_caption("lzc test2")
        #     InitGL(width, height)
        else:
            pygame.init()
            os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d"%(-1000,-1000)
            icon=pygame.image.load("icon.png")
            pygame.display.set_icon(icon)
            pygame.display.set_mode((width,height), DOUBLEBUF | OPENGL)
            pygame.display.set_caption("lzc test2")
            InitGL(width, height)
        if loop:
            self.loop()
    def getPanorama(self,x,y,z):
        result=self.render(x,y,z)
        for i in range(6):
            name=str(i)+".png"
            image=result[i]
            cv2.imwrite(name, image)
    @staticmethod
    def getPos2(x,y,z):#threeJS与openGL里的都是右手坐标系 
        return x,-z,y#右手坐标系变换后还是右手坐标系 #这里影响相机的实时漫游
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
            [0,         0],
            [math.pi/2, 0],
            [math.pi,   0],
            [3*math.pi/2,0],
            [0,         math.pi/2],
            [0,         1e-5-math.pi/2]
        ]
        result={}
        for i in range(6):
            image=getImag(rotations[i])
            result[i]=image
        return result

