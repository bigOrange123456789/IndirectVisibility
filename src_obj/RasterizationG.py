import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import cv2
import math
class Mesh0():
    def __init__(self,id,V,F):
        self.color=np.array([
            id&0xff0000,
            id&0x00ff00,
            id&0x0000ff
            ])#/255
        self.face=np.array(F).reshape(-1)
        self.vertex=np.array(V).reshape(-1)
        self.createVAO()
    def createVAO(this):
        this.vbo = vbo.VBO(np.array(this.vertex,'f'))
        this.ebo = vbo.VBO(np.array(this.face,'H'),target = GL_ELEMENT_ARRAY_BUFFER)
        this.vboLength = len(this.vertex)
        this.eboLength = len(this.face)
        this.bCreate = True
    def draw(this):
        this.vbo.bind()
        glInterleavedArrays(GL_V3F,0,None)
        this.ebo.bind()
        glDrawElements(GL_TRIANGLES,this.eboLength,GL_UNSIGNED_SHORT,None)   

class camera:#摄像机漫游
     origin = [0.0,0.0,0.0]
     length = 1.
     yangle = 0.
     zangle = 0.
     __bthree = False
     def __init__(this):
         this.mouselocation = [0.0,0.0]
         this.offest = 0.1#0.01
         this.zangle = 0. if not this.__bthree else math.pi
     def setthree(this,value):
         this.__bthree = value
         this.zangle = this.zangle + math.pi
         this.yangle = -this.yangle          
     def eye(this):
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
         print("move",x,y,z)
         sinz,cosz = math.sin(this.zangle),math.cos(this.zangle)        
         xstep,zstep = x * cosz + z * sinz,z * cosz - x * sinz
         if this.__bthree : 
             xstep = -xstep
             zstep = -zstep
         this.origin = [this.origin[0] + xstep,this.origin[1] + y,this.origin[2] + zstep]        
     def rotate(this,z,y):
         this.zangle,this.yangle = this.zangle - z,this.yangle + y if not this.__bthree else -y
     def setLookat(this):
         ve,vt = this.eye(),this.target()
         #print ve,vt
         glLoadIdentity()
         gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2],0.0,1.0,0.0)        
     def keypress(this,key,x,y):
         print("key",key,key in ('e',b'e'))
         if key in ('e', 'E',b'e', b'E'):
             print(key,this.offest)
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
         if key in (b'v', b'V'):
             #this.__bthree = not this.__bthree
             this.setthree(not this.__bthree)
         if key == GLUT_KEY_UP:
             this.offest = this.offest + 0.1
         if key == GLUT_KEY_DOWN:
             this.offest = this.offest - 0.1
     def mouse(this,x,y):  
         rx = (x - this.mouselocation[0]) * this.offest * 0.1
         ry = (y - this.mouselocation[1]) * this.offest * -0.1
         this.rotate(rx,ry)
         print(x,y)
         this.mouselocation = [x,y]

class Rasterization:  
    def __init__(self,renderNodes,v):
        DISPLAY_WIDTH = 800
        DISPLAY_HEIGHT = 800

        # pygame.init()
        # pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DOUBLEBUF | OPENGL)#设置主屏窗口# pygame.display.iconify()#最小化窗口
        # gluPerspective(45, (DISPLAY_WIDTH / DISPLAY_HEIGHT), 0.01, 30000)#45, 1, 0.1, 30000

        # glEnable(GL_TEXTURE_2D)
        # glEnable(GL_DEPTH_TEST)
        # glDepthFunc(GL_LEQUAL)
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # from pyquaternion import Quaternion
        # viewMat=np.array(v).reshape(4,4)
        # viewMat=np.linalg.inv(viewMat)
        # pos=[viewMat[3][0], viewMat[3][1], viewMat[3][2]]
        # print("viewMat",viewMat)
        # print("viewMat.T",viewMat.T)
        # print("相机的位置是",viewMat[3][0], viewMat[3][1], viewMat[3][2])

        # q=Quaternion(matrix=viewMat)
        # print("相机的方向是",q)
        # print(q[0],q[1],q[2],q[3])
        DISPLAY_WIDTH = 900
        DISPLAY_HEIGHT = 900

        pygame.init()
        pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DOUBLEBUF | OPENGL)
        # gluPerspective(170, (DISPLAY_WIDTH / DISPLAY_HEIGHT), 0.01, 12)
        gluPerspective(150, (DISPLAY_WIDTH / DISPLAY_HEIGHT), 0.01, 30000)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        glRotatef(-90, 1, 0, 0) # Straight rotation
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(285, 0, 0, 1) # Rotate yaw
        glTranslatef(0.5, 0, 0) # Move to position
        #x前 z下

        pygame.display.flip()#清空缓存？
        
        # glRotatef(q[0],q[1],q[2],q[3])
        # glRotatef( 0.4419090995611076, -0.0318063933263847, 0.894182671434427, 0.06435876921640081)

        # glRotatef(-0.0016620083011163155,  0.9074593333491037,  0.0035899291585582025,  0.42012130207196596)
        # glTranslatef(pos[0],pos[1],pos[2])
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # for node in renderNodes:
        #     node.draw()
        

        vertices =(
            ( 2262.647750509834,  35.16944995510646,  -1877.92384968343),#(1,-1,-1),
            (1,1,-1),
            (-1,1,-1),
            (-1,-1,-1),
            (1,-1,1),
            (1,1,1),
            (-1,-1,1),
            (-1,1,1),
        )

        surfaces = (
            (0,1,2,3),
            (0,2,7,6),
            (0,7,5,4),
            (0,5,1,0),
            (0,5,7,2),
            (0,0,3,6)
        )
        surfaces2=np.array(surfaces)[:,0:2]
        
        while True:#启动循环---
            event = pygame.event.poll()#事件检测
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):break#定义退出机制，在pygame的while循环中，这一步必备设置
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)#清除屏幕
            # glRotatef(0.1,0,0.1,0)#glRotatef(1,0,1,0)#摄像机旋转
            # glTranslatef(0.5, 0, 0)
            
            Mesh0(
                0xfffff,
                vertices,
                surfaces2
            ).draw()
            pygame.display.flip()#刷新画面
        
        Mesh0(
            0xfffff,
            vertices,
            surfaces2
        ).draw()
        

        # 
        # pygame.time.wait(10)
        if True:
            image_buffer = glReadPixels(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
            image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(DISPLAY_WIDTH, DISPLAY_HEIGHT, 3)
            cv2.imwrite(r"image.png", image)
        
    @staticmethod
    def getMesh0(mesh,matrix,id):
        # print(mesh.vertex)
        # print(mesh.face)
        
        matrixInstance=np.array(matrix).reshape(4,4).T
        vertex0=np.array(mesh.vertex)
        vertex0=np.c_[vertex0,np.ones(vertex0.shape[0])] #c_是column(列)的缩写，就是按列叠加两个矩阵，就是把两个矩阵左右组合，要求行数相等。
        vertex0=np.dot(vertex0,matrixInstance)[:,0:3]
        # print(vertex0,np.array(mesh.face)-1)
        # exit(0)
        return Mesh0(id,vertex0,np.array(mesh.face)-1)
