#https://qa.1r1g.com/sf/ask/3613932241/
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2

vertices =(
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,-1,1),
    (-1,1,1),
    )
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

class Mesh0():
    def __init__(self,id,V,F):
        id=0xfffff
        self.color=np.array([
            id&0xff0000,
            id&0x00ff00,
            id&0x0000ff
            ])#/255
        # self.color=[255,255,255]
        # print(self.color)
        self.face=F
        self.vertex=V
    def draw(self):
        glBegin(GL_TRIANGLES)#glBegin(GL_QUADS)
        for surface in self.face:
            for v_i in surface:
                glColor3fv(self.color)
                glVertex3fv(self.vertex[v_i])
        glEnd()

surfaces2=np.array(surfaces)[:,0:2]
def Cube():
    glBegin(GL_TRIANGLES)#glBegin(GL_QUADS)
    for surface in surfaces2:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()
    glBegin(GL_LINES) #tells OpenGL dass code erhalten wird der als line-drawing code benutzt wird
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
def main():
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
    glTranslatef(-5, -3, -2) # Move to position
    
    # #################################################
    # DISPLAY_WIDTH = 900
    # DISPLAY_HEIGHT = 900

    # pygame.init()
    # pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DOUBLEBUF | OPENGL)
    # gluPerspective(90, (DISPLAY_WIDTH / DISPLAY_HEIGHT), 0.01, 12)

    # glEnable(GL_TEXTURE_2D)
    # glEnable(GL_DEPTH_TEST)
    # glDepthFunc(GL_LEQUAL)

    # glRotatef(-90, 1, 0, 0) # Straight rotation
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glRotatef(285, 0, 0, 1) # Rotate yaw
    # glTranslatef(-5, -3, -2) # Move to position
    # #################################################

    Mesh0(
        0xfffff,
        vertices,
        surfaces2
    ).draw()
    # Cube()

    image_buffer = glReadPixels(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
    image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(DISPLAY_WIDTH, DISPLAY_HEIGHT, 3)
    cv2.imwrite(r"image.png", image)
    pygame.quit()


if __name__ == "__main__":
    main()