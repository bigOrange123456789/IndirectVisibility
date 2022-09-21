import numpy as np
class ProcessTopology:
    def __init__(self, vertex, face):
        self.v = vertex
        self.f = face

    def deDedundancy(self):  # 去除没有三角面索引的冗余点
        # 创建flag
        flag = []
        for i in range(len(self.v)):
            flag.append(0)
        # 统计每个顶点被三角面使用的次数
        for f0 in self.f:
            for i in range(3):
                index = f0[3 * i] - 1
                flag[index] = flag[index] + 1
        # 计算每个顶点的新序号
        i = 0
        v = 0
        while i < len(flag):
            if flag[i] == 0:
                flag[i] = -1  # -1表示顶点未被使用
            else:
                flag[i] = v
                v = v + 1
            i = i + 1
        # 修改face
        for k in range(len(self.f)):
            f0 = self.f[k]
            for j in range(3):
                i = f0[3 * j]
                if flag[i - 1] == -1:
                    print("错误")
                f0[3 * j] = flag[i - 1] + 1
        # 修改vertex
        old = self.v
        self.v = []
        for i in range(len(flag)):
            if not flag[i] == -1:
                v0 = old[i]
                self.v.append(v0)
    
    def getEdge(self):#从1开始 #获取全部边
        em=[]
        for i in range(len(self.v)):
            em.append([])
            for j in range(len(self.v)):
                em[i].append(0)
        if len(self.f)>0:
            k=int(len(self.f[0])/3)
            for i in range(len(self.f)):
                a=self.f[i][0]
                b=self.f[i][k]
                c=self.f[i][2*k]
                if a>b:
                    em[a-1][b-1]=1
                else:
                    em[b-1][a-1]=1
                if a>c:
                    em[a-1][c-1]=1
                else:
                    em[c-1][a-1]=1
                if b>c:
                    em[b-1][c-1]=1
                else:
                    em[c-1][b-1]=1
        e=[]
        for i in range(len(self.v)):
            for j in range(len(self.v)):
                if em[i][j]==1:
                    e.append([i+1,j+1])
        return e
    def getTriangle(self,i):#获取一个三角形的三个顶点，通过三角形序号获取顶点，顶点
        f=self.f[i]
        #print("f",f)
        step=int(len(f)/3)
        v0=self.v[f[0]-1]#三角形三个顶点坐标
        v1=self.v[f[step]-1]
        v2=self.v[f[step*2]-1]
        #print("v0,v1,v2",v0,v1,v2)
        
        m=np.mean([v0,v1,v2], axis=0).tolist()#三角形的中心点坐标
        #print("m",m)
        a=np.array(v1)-np.array(v0)
        b=np.array(v2)-np.array(v0)
        c=np.cross(a,b)
        s=np.linalg.norm(c)#三角形面积
        #print("s",s)
        
        return [v0,v1,v2],m,s
        

if __name__ == "__main__":  # 用于测试
    vertex = [[1], [2], [3], [4], [5], [6], [7], [8], [9],[10]]
    face = [
        [2, 0, 0, 3, 0, 0, 4 , 0, 0],
        [3, 0, 0, 4, 0, 0, 5 , 0, 0],
        [7, 0, 0, 8, 0, 0, 10, 0, 0],
    ]
    pt = ProcessTopology(vertex, face)
    pt.deDedundancy()
    import numpy as np

    print("v:\n", np.array(pt.v))
    # vertex = [  [2], [3], [4], [5],    [7], [8], [9]]
    print("f:\n", np.array(pt.f))
    # [1, 0, 0,   2, 0, 0,   3, 0, 0]
    # [2, 0, 0,   3, 0, 0,   4, 0, 0]
    # [5, 0, 0,   6, 0, 0,   7, 0, 0]
