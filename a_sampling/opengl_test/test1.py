import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
 
def drawcube():# "绘制正方体"，zip和list法
    CUBE_POINTS = ((0.5, -0.5, -0.5), (0.5, 0.5, -0.5),(-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),(0.5, -0.5, 0.5), (0.5, 0.5, 0.5),(-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5))#定义正方体的xyz坐标点
    CUBE_COLORS = ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),(1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1))#定义RGB颜色
    allpoints = list(zip(CUBE_POINTS, CUBE_COLORS))
    
    #画面---开始---
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
        glRotatef(0.1,0,0.1,0)#glRotatef(1,0,1,0)#摄像机旋转
        drawcube()
        pygame.display.flip()#刷新画面
 
if __name__ == '__main__':
    main()

    