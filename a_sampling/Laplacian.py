import numpy as np
class Laplacian():
    def __init__(self, mesh):
        self.mesh=mesh
        self.v = mesh.vertex # numpy array with shape of [n_v, 3], n_v is the number of  vertices
        self.f = self.getFace() # numpy array with shape of [n_f, 3], n_f is the number of vertices
        self.nv = len(self.v)

        self.matLap=self.getMatLap()
        print('已获取Laplacian矩阵')

        self.posLap=self.getPosLap()
        print('已获取Laplacian坐标')
    def getFace(self):
        face=[]
        for i in range(len(self.mesh.face)):
            face.append([])
            for j in range(len(self.mesh.face[i])):
                face[i].append(self.mesh.face[i][j])

        #开始归并位置相同的点
        l=[]#记录每个顶点修改的值
        for i in range(len(self.v)):
            l.append(i)
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                if i<j:
                    a=self.v[i]
                    b=self.v[j]
                    if abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])==0:
                        l[j]=i
        for i in range(len(self.mesh.face)):
            for j in range(len(self.mesh.face[i])):
                k=self.mesh.face[i][j]
                face[i][j]=l[k-1]+1
        #mesh.updateFace()
        self.l=l
        return face
    def correctVertex(self,vertex):
        for i in range(len(vertex)):
            j=self.l[i]#l是通过self.getFace这个方法获取的
            if not i==j:
                for k in range(len(vertex[0])):
                    vertex[j][k]=vertex[i][k]
        return vertex
    def useAnchor(self,indexes,ps):#使用锚点对网格进行形变
        weight=0.5  # 0.5~5 #设置锚点在形变中的权重
        import copy
        matLap2 = copy.deepcopy(self.matLap)#复制list对象
        posLap2 = copy.deepcopy(self.posLap)

        for index in indexes:
            vector=self.initMat(1,self.nv)[0]
            vector[index]=weight
            matLap2.append(vector)
        for pos in ps:
            for k in range(len(pos)):
                pos[k]=pos[k]*weight
            posLap2.append(pos)
        print('开始求解超定齐次线性方程')
        #self.correctVertex()
        return self.solveLinearEquation(matLap2,posLap2)
    def transform(self,indexes,ps):
        v2=self.useAnchor(indexes,ps)

        v2=self.correctVertex(v2)

        self.mesh.vertex=v2
        self.mesh.updateVertex()

        self.v = v2
        self.posLap=self.getPosLap()
    def transform2(self,list,list_move):
        list_pos=list_move
        for i in range(len(list)):
            n=list[i]
            pos=self.mesh.vertex[n]
            #print(i,pos)
            for j in range(3):
                list_pos[i][j]=list_pos[i][j]+pos[j]
            #print(i,list_pos[i])
        self.transform(#input/spirit.obj
                            list,
                            list_pos)
        self.mesh.download("output/tansform2.obj")
    def solveLinearEquation(self,A,B):
        from numpy.linalg import lstsq # 解超定方程
        a=np.mat(A)#A=[[2, 3], [1, 3], [1, 1]]
        b=np.mat(B)#B=[5, 4, 2]
        result=lstsq(a, b, rcond=None)#ax=b #a'ax=a'b
        return result[0].tolist()
    def getPosLap(self):#拉普拉斯坐标 (n,n)*(n,3)
        p=np.array(self.v)
        l=np.array(self.matLap)
        posLap=np.dot(l,p)
        return posLap.tolist()
    @staticmethod
    def initMat(i,j):
        m=[]
        for k1 in range(i):
            m.append([])
            for k2 in range(j):
                m[k1].append(0)
        return m
    def getMatLap(self):#计算均值拉普拉斯矩阵
        #创建0矩阵
        matLap=self.initMat(self.nv,self.nv)

        #根据self.f给矩阵赋值
        for face0 in self.f:
            if len(face0)==3:
                a=face0[0]-1
                b=face0[1]-1
                c=face0[2]-1
            else:
                a=face0[0]-1
                b=face0[3]-1
                c=face0[6]-1
            #matLap[b][a]=matLap[a][b]=matLap[a][b]+1
            #matLap[c][a]=matLap[a][c]=matLap[a][c]+1
            #matLap[c][b]=matLap[b][c]=matLap[b][c]+1
            matLap[b][a]=matLap[a][b]=1
            matLap[c][a]=matLap[a][c]=1
            matLap[c][b]=matLap[b][c]=1

        for i in range(self.nv):
            k=0
            for j in range(self.nv):
                k=k+matLap[i][j]

            for j in range(self.nv):
                if not matLap[i][j]==0:
                    matLap[i][j]=-1/k
            matLap[i][i]=1
        return matLap
#以下为测试代码
class Test():#用于无模型测试
      def __init__(self, v,f):
        self.vertex=v
        self.face=f
def f0():
    m0 = Test([
                  [1,2,3],
                  [1,2,3],
                  [1,2,3],
                  [1,2,3]
              ],
              [
                  [0,1,3],
                  [1,2,3]
              ]
          )

    l=Laplacian(m0)
    v2=l.useAnchor(
                [1],
                [
                    [1.5,2.5,3.5]
                ])
    print(v2)
def f6():#有模型测试
    m0 = Mesh('input/man_new.obj')#spirit
    #m0 = Mesh('input/spirit_sim.obj')#
    l=Laplacian(m0)
    list=[
        0,
        1,
        40,#头
        #26,#腰部
        11
        ]
    list_move=[
        [0,0,0.2],
        [0,0,0.2],
        [0,-0,-0.1],
        #[0,-0,0.2],
        [0,0,-0.2]
        ]
    print(list_move)
    
    for i in range(22):
        n=i*10*2
        list.append(n)
        list_move.append([0,0,0])
        
    l.transform2(list,list_move)
def getPos(n):
    m0 = Mesh('input/man_new.obj')
    v=m0.vertex
    print(v[n])
    return v[n]
def setPos(n):
    m0 = Mesh('input/man_new.obj')
    v=m0.vertex[n]
    print(v)
    v[0]=v[0]+0.5
    v[1]=v[1]+0.5
    v[2]=v[2]+0.5
    print()
    m0.updateVertex()
    m0.download("output/man_show"+str(n)+".obj")
if __name__ == "__main__":
    m0 = Test([
                  [1,2,3],
                  [1,2,3],
                  [1,2,3],
                  [1,2,3]
              ],
              [
                  [0,1,3],
                  [1,2,3]
              ]
          )

    l=Laplacian(m0)
    v2=l.useAnchor(
                [1],
                [
                    [1.5,2.5,3.5]
                ])
    print(v2)
    #for i in range(44):
    #    setPos(i*10)
