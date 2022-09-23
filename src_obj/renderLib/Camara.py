import OpenGL
import math
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
     def rotationSet(this,z,y):
        this.zangle,this.yangle = z,y
     def setLookat(this):
         ve,vt = this.eye(),this.target()
         OpenGL.GL.glLoadIdentity()
         OpenGL.GLU.gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2],0.0,1.0,0.0)  #视角朝向的控制
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
         if key == OpenGL.GLUT.GLUT_KEY_UP:
             this.offest = this.offest + 0.1
         if key == OpenGL.GLUT.GLUT_KEY_DOWN:
             this.offest = this.offest - 0.1
     def mouse(this,x,y):  
         rx = (x - this.mouselocation[0]) * this.offest * 0.1
         ry = (y - this.mouselocation[1]) * this.offest * -0.1
         this.rotate(rx,ry)
         this.mouselocation = [x,y]#记录鼠标此刻的位置
