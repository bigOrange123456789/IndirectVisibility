#from Mesh import Mesh
import math
import numpy as np
class Simplify:
    def __init__(self, mesh,ratio):#ratio为压缩率
        self.mesh=mesh
        self.face=self.mesh.face
        self.vertex=self.mesh.vertex
        self.check()#合并重叠点
        self.normal=self.getNoraml()#法线不需要实时更新
        count=int((1-ratio)*len(self.vertex))#要合并的次数
        self.start(count)

    def start(self,count):
        edge=self.mesh.getEdge()
        for ii in range(count):
            #self.normal=self.getNoraml()#每次压缩都要重新计算法线
            print(""+str( round(100*ii/count,2) )+'%')
            listMerge=[]#记录所有合并方式
            for e in edge:
                if not e[0]==e[1]:
                    p1=self.vertex[e[0]-1]
                    p2=self.vertex[e[1]-1]
                    p3=[]
                    for j in range(3):
                        p3.append( (p1[j]+p2[j])/2 )
                    listMerge.append([ e[0],e[1],p1 ])
                    listMerge.append([ e[0],e[1],p2 ])
                    listMerge.append([ e[0],e[1],p3 ])
            if len(listMerge)==0:
                print('len(listMerge)==0')
                break
            param=listMerge[0]
            cMin=self.cost(param[0],param[1],param[2])
            #print()
            #print(cMin,param)
            for i in listMerge:
                c0=self.cost(i[0],i[1],i[2])
                #print(c0,i)
                if c0<cMin:
                    cMin=c0
                    param=i
            self.merge(param[0],param[1],param[2])
            for e in edge:
                for j in range(2):
                    if e[j]==param[1]:
                        e[j]=param[0]

        self.mesh.deDedundancy()
        self.mesh.updateFace()
        self.mesh.updateVertex()
         
    def getNoraml(self):
        normal=[]
        k=int(len(self.face[0])/3)
        for i in range(len(self.face)):
            i0=self.face[i][0]-1
            i1=self.face[i][k]-1
            i2=self.face[i][2*k]-1
            a=np.array(self.vertex[i0])
            b=np.array(self.vertex[i1])
            c=np.array(self.vertex[i2])
            v1=a-b
            v2=a-c
            v3=np.cross(v1, v2)
            v3=v3/np.linalg.norm(v3)
            normal.append(v3.tolist())
            #print(v1, v2,v3)
            #print(a,c,v2)#三个点的坐标
        return normal
    def check(self):#检查网格是否有重叠点
        for i in range(len(self.vertex)):
            for j in range(len(self.vertex)):
                if i<j:
                    a=self.vertex[i]
                    b=self.vertex[j]
                    if abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])==0:
                        print(i,j)#l[j]=i

    def deleteErrorFace(self):#删除错误的三角面
        print('简化前-面个数：'+str(len(self.face)))
        if len(self.face)>0:            
            flag=[]#标记哪些边需要被删除
            for i in range(len(self.face)):
                flag.append(0)
            k=int(len(self.face[0])/3)
            for i in range(len(self.face)):
                a=self.face[i][0  ]
                b=self.face[i][k  ]
                c=self.face[i][2*k]
                if a==b or a==c or b==c:
                    flag[i]=1
            self.mesh.face=[]
            for i in range(len(flag)):
                if flag[i]==0:
                    self.mesh.face.append(self.face[i])
            self.face=self.mesh.face
            print('简化后-面个数：'+str(len(self.face)))
    def merge(self,v1,v2,pos):#修改v1 删除v2
        self.vertex[v1-1][0]=pos[0]
        self.vertex[v1-1][1]=pos[1]
        self.vertex[v1-1][2]=pos[2]
        if len(self.face)>0:
            k=int(len(self.face[0])/3)
            for i in range(len(self.face)):
                a=self.face[i][0  ]
                b=self.face[i][k  ]
                c=self.face[i][2*k]
                if a==v2:
                    self.face[i][0  ]=v1
                if b==v2:
                    self.face[i][k  ]=v1    
                if c==v2:
                    self.face[i][2*k]=v1   
    def cost(self,v1,v2,pos):
        import numpy as np
        vector1=np.array(self.vertex[v1-1])-np.array(pos)
        vector2=np.array(self.vertex[v2-1])-np.array(pos)
        c=0
        for i in range(len(self.face)):
            f=self.face[i]
            n=np.array(self.normal[i])
            #print(n,vector1,vector2)
            if f[0]==v1 or f[1]==v1 or f[2]==v1:
                c=c+abs( np.dot(n,vector1) )
            if f[0]==v2 or f[1]==v2 or f[2]==v2:
                c=c+abs( np.dot(n,vector2) )
        if math.isnan(c):
            c=999999
        return c
        #self.normal