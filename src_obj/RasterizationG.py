# -*- coding: UTF-8 -*-
# NUMBAPRO_NVVM=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\nvvm\bin\nvvm64_33_0.dll
# NUMBAPRO_LIBDEVICE=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\nvvm\libdevice
# from numba import cuda
import numpy as np
GPU_PARAM={
    "max1":800,#THREAD_INDEX_MAX1,
    "max2":600,#THREAD_INDEX_MAX2,
    "max3":500#THREAD_INDEX_MAX3
}
# @cuda.jit
# def addGPU(A,B,C):
#     i=cuda.blockIdx.x
#     j=cuda.threadIdx.x
#     C[i][j]=A[i][j]+B[i][j]

# cuda.np=np
# @cuda.jit
# def addGPU(A,B,C,t):
#     i=cuda.blockIdx.x
#     j=cuda.threadIdx.x
#     # import numpy as np
#     # print(cuda)
#     # test=np.array([
#     #     [2,0],
#     #     [0,-1]
#     # ])
#     # test=np.linalg.det(
#     #     np.linalg.inv(test)
#     # )
#     # test=1
#     def test(n):
#         return n+10
#     print(t)
#     C[i][j]=A[i][j]+B[i][j]+test(10)

import math
class Rasterization:  # 基于PCA
    def __init__(self,matrix,mesh, m,v,p,depthMap,id,idMap):
        self.mesh=mesh
        self.id=id
        self.CoordinateSystemTransformation(
            matrix,
            m,v,p,
            depthMap.shape[0],depthMap.shape[1]
            )
        self.depthMapNew,self.idMapNew=self.getDepthMapNew(depthMap,idMap)
    def CoordinateSystemTransformation(self,matrix,m,v,p,w,h):
        mesh=self.mesh
        vertex0=mesh.vertex#getVertexHead()
        vertex0=np.array(vertex0)
        vertex0=np.c_[vertex0,np.ones(vertex0.shape[0])] #c_是column(列)的缩写，就是按列叠加两个矩阵，就是把两个矩阵左右组合，要求行数相等。
        matrixInstance=np.array(matrix).reshape(4,4).T
        modelMat=np.array(m).reshape(4,4)
        viewMat=np.array(v).reshape(4,4)
        projectMat=np.array(p).reshape(4,4)

        vertex0=np.dot(vertex0,matrixInstance)
        vertex1=np.dot(vertex0,modelMat)
        vertex2=np.dot(vertex1,viewMat)
        vertex3=np.dot(vertex2,projectMat)

        vertex3[:,0]=vertex3[:,0]/vertex3[:,3]#-1~1#除以第四维的原因？
        vertex3[:,0]=(vertex3[:,0]/2+0.5)#vertex3[:,0]=(vertex3[:,0]/2+0.5)*(w-1)# -1~1 -> 0~w
        vertex3[:,0]=(w-1)*vertex3[:,0]
        vertex3[:,1]=-1*vertex3[:,1]/vertex3[:,3]#-1~1
        vertex3[:,1]=(vertex3[:,1]/2+0.5)#vertex3[:,1]=(vertex3[:,1]/2+0.5)*(h-1)# -1~1 -> 0~h
        vertex3[:,1]=(h-1)*vertex3[:,1]
        vertex4=vertex3[:,0:2]#-1~1
        # vertex4=0.5+vertex4/2#0~1
        vertex5=np.c_[vertex4,vertex3[:,2]]#加上深度

        mesh.vertex_cst=vertex5
        return vertex5
    def getDepthMapNew(self,depthMap,idMap):

        def inScreen(v1,v2,v3,w,h):
            def pointInScreen(v):
                return 0<=v[0] and v[0]<=w-1 and 0<=v[1] and v[1]<=h-1 and 0<=v[2]
            return pointInScreen(v1) or pointInScreen(v2) or pointInScreen(v3)  
        def clockwise(v1,v2,v3):#判断三个点在屏幕上是否为顺时针
            a=[v2[0]-v1[0],v2[1]-v1[1]]
            b=[v3[0]-v1[0],v3[1]-v1[1]]
            return a[0]*b[1]-b[0]*a[1]>0
        def getRectangle(v1,v2,v3,w,h):
            xmin=min(v1[0],v2[0],v3[0])
            xmax=max(v1[0],v2[0],v3[0])
            ymin=min(v1[1],v2[1],v3[1])
            ymax=max(v1[1],v2[1],v3[1])
            xmin=max(0,xmin)
            ymin=max(0,ymin)
            xmax=min(w,xmax)
            ymax=min(h,ymax)
            xmin=math.floor(xmin)
            ymin=math.floor(ymin)
            xmax=math.ceil(xmax)
            ymax=math.ceil(ymax)
            return [xmin,xmax,ymin,ymax]
        def getLinearCoefficient(p1,p2,p3,p):
            M=np.array([p1,p2,p3])
            M=np.c_[M,np.ones(3)]
            if np.linalg.det(M)==0:
                return [0,0,0]
            else:
                return np.dot(
                    np.array([p[0],p[1],1]),
                    np.linalg.inv(M)
                )
        def updateDepthMap(depthMap,i,j,k1,k2,k3,d1,d2,d3,idMap):
            if 0<=k1 and k1<=1 and 0<=k2 and k2<=1 and 0<=k3 and k3<=1:#像素在三角形内
                d=k1*d1+k2*d2+k3*d3
                # print("像素在三角形内",i,j,d)
                if depthMap[i][j]>d:
                    depthMap[i][j]=d
                    idMap[i][j]=self.id
        m0=self.mesh
        w=depthMap.shape[0]
        h=depthMap.shape[1]
        vs=m0.vertex_cst
        test_i=0
        for f in m0.face:#遍历每个三角形
            test_i=test_i+1
            # print("m0.face",len(m0.face),test_i,end="\r")
            t=int(len(f)/3)
            v1=vs[f[0]-1]
            v2=vs[f[t]-1]
            v3=vs[f[2*t]-1]
            if inScreen(v1,v2,v3,w,h) and clockwise(v1,v2,v3): #三角形可以投影到屏幕上并且三角面正面朝向相机 
                depthMin=np.min([v1[2],v2[2],v3[2]])
                xmin,xmax,ymin,ymax=getRectangle(v1,v2,v3,w,h)
                i=xmin
                while i<=xmax:
                    j=ymin
                    while j<=ymax:
                        if depthMin<depthMap[i][j]:#该像素所在位置有可能会看到三角形 
                            p1=[v1[0],v1[1]]
                            p2=[v2[0],v2[1]]
                            p3=[v3[0],v3[1]]
                            d1=v1[2]
                            d2=v2[2]
                            d3=v3[2]
                        
                            p=[i,j]
                            k1,k2,k3=getLinearCoefficient(p1,p2,p3,p)
                            if not k1+k2+k3 == 0:
                                updateDepthMap(depthMap,i,j,k1,k2,k3,d1,d2,d3,idMap)
                        j=j+1
                    i=i+1
        return depthMap,idMap
if __name__ == "__main__":  # 用于测试
    #demo0
    if False:
        from OpenGL.GL import *
        from OpenGL.GLU import *
        from OpenGL.GLUT import *
 
        def drawFunc():
            glClear(GL_COLOR_BUFFER_BIT)
            glutWireTeapot(0.5)
            glFlush()
 
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
        glutInitWindowSize(400, 400)
        # 参数为b类型而不是string。我查资料时，很多网上代码未指出导致报错。
        glutCreateWindow(b"First")
        glutDisplayFunc(drawFunc)
        # glutIdleFunc(drawFunc)
        glutMainLoop()
        exit(0)

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
 
 
#---定义画立方体函数---
def drawcube():# "绘制正方体"，zip和list法
    CUBE_POINTS = ((0.5, -0.5, -0.5), (0.5, 0.5, -0.5),(-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),(0.5, -0.5, 0.5), (0.5, 0.5, 0.5),(-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5))#定义正方体的xyz坐标点
    CUBE_COLORS = ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),(1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1))#定义RGB颜色
    allpoints = list(zip(CUBE_POINTS, CUBE_COLORS))
    
    #画面积---开始---
    glBegin(GL_QUADS)
    CUBE_QUAD_VERTS = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),(4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))# 定义面，四个点构成一个面
    for face in CUBE_QUAD_VERTS:
        for vert in face:
            pos, color = allpoints[vert]
            glColor3fv(color)
            glVertex3fv(pos)
    glEnd()#结束---
 
    #边线颜色黑色
    glColor3f(0, 0, 0)

    # 绘制线---开始---
    CUBE_EDGES = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7),(6,3), (6,4), (6,7), (5,1), (5,4), (5,7),)# 定义线，两个点构成一个线
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex3fv(pos)
    glEnd()#结束---
 
#---主函数---
def main():
    #---初始化pygame和定义窗口大小---
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)#创建一个 OPENGL 渲染的显示 #DOUBLEBUF:双缓冲模式（推荐和 HWSURFACE 或 OPENGL 一起使用）
 
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)#初始化 摄像头
    gluPerspective(45.0,640/480.0,0.1,100.0)#透视相机
    glTranslatef(0.0, 0.0, -3.0)
    glRotatef(25, 1, 0, 0)#摄像机旋转
    
    while True:#启动循环---
        event = pygame.event.poll()#事件检测
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):break#定义退出机制，在pygame的while循环中，这一步必备设置
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)#清除屏幕
        glRotatef(1,0,1,0)#摄像机旋转
        drawcube()
        pygame.display.flip()#刷新画面
 
if __name__ == '__main__':
    main()

    
