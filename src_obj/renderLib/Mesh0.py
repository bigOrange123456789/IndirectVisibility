import numpy as np
import OpenGL
class Mesh0():
    def __init__(self,id,V,F):
        def srgb_to_linsrgb (srgb):
            gamma = ((srgb + 0.055) / 1.055)**2.4
            scale = srgb / 12.92
            return np.where (srgb > 0.04045, gamma, scale)
        # id=1+10*256+3*256*256
        self.color=np.array([
            (id&0xff0000)>>16,
            (id&0x00ff00)>>8,
            (id&0x0000ff)
            ])/255
        # self.color = srgb_to_linsrgb(
        #     self.color
        # )
        self.face=np.array(F).reshape(-1)
        self.vertex=np.array(V)
        self.vertex=self.vertex.reshape(-1)
        self.createVAO()
    def createVAO(this):
        import OpenGL
        this.vbo = OpenGL.arrays.vbo.VBO(np.array(this.vertex,'f'))
        this.ebo = OpenGL.arrays.vbo.VBO(np.array(this.face,'H'),target = OpenGL.GL.GL_ELEMENT_ARRAY_BUFFER)
        this.vboLength = len(this.vertex)
        this.eboLength = len(this.face)
        this.bCreate = True
    def draw(this):
        OpenGL.GL.glColor4f(this.color[0], this.color[1], this.color[2], 1.0)  # 设置当前颜色为红色不透明
        this.vbo.bind()
        OpenGL.GL.glInterleavedArrays(OpenGL.GL.GL_V3F,0,None)
        this.ebo.bind()
        OpenGL.GL.glDrawElements(OpenGL.GL.GL_TRIANGLES,this.eboLength,OpenGL.GL.GL_UNSIGNED_SHORT,None)   
