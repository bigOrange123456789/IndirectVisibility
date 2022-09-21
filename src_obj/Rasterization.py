import numpy as np
import math
class Rasterization:  # 基于PCA
    def __init__(self,matrix,mesh, m,v,p,depthMap,id,idMap):
        self.mesh=mesh
        self.id=id
        self.CoordinateSystemTransformation(matrix,m,v,p)
        self.depthMapNew,self.idMapNew=self.getDepthMapNew(depthMap,idMap)
    def CoordinateSystemTransformation(self,matrix,m,v,p):
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

        vertex3[:,0]=vertex3[:,0]/vertex3[:,3]
        vertex3[:,1]=-1*vertex3[:,1]/vertex3[:,3]#除以第四维的原因？
        vertex4=vertex3[:,0:2]#-1~1
        vertex4=0.5+vertex4/2#0~1
        vertex5=np.c_[vertex4,vertex3[:,2]]#加上深度

        mesh.vertex_cst=vertex5
        return vertex5
    def getDepthMapNew(self,depthMap,idMap):
        def inScreen(v1,v2,v3):
            def pointInScreen(v):
                return 0<=v[0] and v[0]<=1 and 0<=v[1] and v[1]<=1 
            return pointInScreen(v1) or pointInScreen(v2) or pointInScreen(v3)  
        def getRectangle(v1,v2,v3,w,h):
            xmin=min(v1[0],v2[0],v3[0])
            xmax=max(v1[0],v2[0],v3[0])
            ymin=min(v1[1],v2[1],v3[1])
            ymax=max(v1[1],v2[1],v3[1])
            xmin=max(0,xmin)
            ymin=max(0,ymin)
            xmax=min(1,xmax)
            ymax=min(1,ymax)
            xmin=math.floor(xmin*(w-1))
            ymin=math.floor(ymin*(h-1))
            xmax=math.ceil(xmax*(w-1))
            ymax=math.ceil(ymax*(h-1))
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
        #depthMap=np.ones([w,h])
        # print(depthMap)
        vs=m0.vertex_cst
        test_i=0
        for f in m0.face:
            test_i=test_i+1
            print("m0.face",len(m0.face),test_i,end="\r")
            t=int(len(f)/3)
            v1=vs[f[0]-1]
            v2=vs[f[t]-1]
            v3=vs[f[2*t]-1]
            if inScreen(v1,v2,v3):#三角形可以投影到屏幕上
                xmin,xmax,ymin,ymax=getRectangle(v1,v2,v3,w,h)
                i=xmin
                while i<=xmax:
                    j=ymin
                    while j<=ymax:
                        p1=[v1[0]*(w-1),v1[1]*(h-1)]
                        p2=[v2[0]*(w-1),v2[1]*(h-1)]
                        p3=[v3[0]*(w-1),v3[1]*(h-1)]
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
    from Mesh import Mesh
    m0 = Mesh('../in/man2.obj')
    m=[
        1.9999999999999694,
        1.8517135996128464e-21,
        3.4969112000000264e-7,
        0,
        6.11419378517136e-14,
        1.9999999999999694,
        -3.4969111999999734e-7,
        0,
        -3.4969111999999734e-7,
        3.4969112000000264e-7,
        1.999999999999939,
        0,
        0,
        -1.8,
        0,
        1
    ]
    v=[
        0.9998000066665783,
        -0.004099717415124123,
        0.019573936411109053,
        0,
        8.673617379884035e-19,
        0.9787620700563638,
        0.20499953711894459,
        0,
        -0.01999866669330765,
        -0.20495853857816623,
        0.9785663241673466,
        0,
        -0.015101537208743064,
        -1.5041766730047286,
        -0.7748754048755101,
        1
    ]
    p=[
        1.4281480067421146,
        0,
        0,
        0,
        0,
        1.4281480067421146,
        0,
        0,
        0,
        0,
        -1.0002000200020003,
        -1,
        0,
        0,
        -0.20002000200020004,
        0
    ]
    w=257
    h=257
    depthMap=np.ones([w,h])
    Rasterization(
        m0,
        m,v,p,
        depthMap
        )

    image=np.ones([w,h,3])
    for i in range(w):
        for j in range(h):
            c=int(depthMap[j][i]*255)
            image[i][j][0]=c
            image[i][j][1]=c
            image[i][j][2]=c
    import cv2
    cv2.imwrite("depthMap.jpg",image)
