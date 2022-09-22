from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
 
def cube():       
    vertices = np.array([
        -0.5, 0.5, 0.5,   
        0.5, 0.5, 0.5,   
        0.5, -0.5, 0.5,   
        -0.5, -0.5, 0.5,  
        -0.5, 0.5, -0.5,  
        0.5, 0.5, -0.5,  
        0.5, -0.5, -0.5,  
        -0.5, -0.5, -0.5 
        ],'f')
    indices = np.array([
        0, 1, 2, 3, 
        4, 5, 1, 0, 
        3, 2, 6, 7, 
        5, 4, 7, 6, 
        1, 5, 6, 2, 
        4, 0, 3, 7  
        ],'H')
    
    vbo1 = vbo.VBO(vertices)
    vbo2 = vbo.VBO(indices,target = GL_ELEMENT_ARRAY_BUFFER)
 
    vbo1.bind()
    glInterleavedArrays(GL_V3F,0,None)
    vbo2.bind()
    glDrawElements(GL_QUADS,len(indices),GL_UNSIGNED_SHORT,None)
    vbo2.unbind()
    vbo1.unbind()
    
def Draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    cube()                         
    glutSwapBuffers()
    
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
 
glutInitWindowSize(600, 600)
glutInitWindowPosition(300, 200)
glutCreateWindow('cube')
    
glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)          
glDepthFunc(GL_LEQUAL)
 
glutDisplayFunc(Draw)               
    
glutMainLoop()  
