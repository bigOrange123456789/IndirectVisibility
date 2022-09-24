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
    @staticmethod
    def parse(image):
        result={}
        
        image=256*256*image[:,:,0]+256*image[:,:,1]+image[:,:,2]

        # xm,ym,_=image.shape
        # for i1 in range(xm):
        #     for i2 in range(ym):
        #         # pixel=image[i1][i2] 
        #         # id=256*256*pixel[0]+256*pixel[1]+pixel[2]
        #         id=image[i1][i2] 
        #         if not id==0xffffff:
        #             id=str(id)
        #             if id in result: result[id]=result[id]+1
        #             else:            result[id]=1
        
        for k in np.unique(image):
            if not id==0xffffff:
                result[str(k)] = image[ image == k ].size

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