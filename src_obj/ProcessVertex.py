class ProcessVertex:
    def __init__(self, vertex):
        self.vertex = vertex
        self.computeBox()

    def move(self, x, y, z):
        vertex = self.vertex
        self.vertex = []
        for v0 in vertex:
            v0 = [v0[0] + x, v0[1] + y, v0[2] + z]
            self.vertex.append(v0)

    def scale(self, x, y, z):
        vertex = self.vertex
        self.vertex = []
        for v0 in vertex:
            v0 = [v0[0] * x, v0[1] * y, v0[2] * z]
            self.vertex.append(v0)

    def applyMatrix(self, m):  # condition: mesh only have face and vertice
        for i in range(len(m)):
            if len(m[i]) < 4:
                m[i].append(0)
        vertex = self.vertex
        self.vertex = []
        for v0 in vertex:
            x = v0[0]
            y = v0[1]
            z = v0[2]
            x1 = x * m[0][0] + y * m[0][1] + z * m[0][2] + m[0][3]
            y1 = x * m[1][0] + y * m[1][1] + z * m[1][2] + m[1][3]
            z1 = x * m[2][0] + y * m[2][1] + z * m[2][2] + m[2][3]
            self.vertex.append([x1, y1, z1])

    def computeBox(self):
        self.max=[self.vertex[0][0],self.vertex[0][1],self.vertex[0][2]]
        self.min=[self.vertex[0][0],self.vertex[0][1],self.vertex[0][2]]
        for v0 in self.vertex:
            for i in range(3):
                if v0[i]>self.max[i]:
                    self.max[i]=v0[i]
                if v0[i]<self.min[i]:
                    self.min[i]=v0[i]
        self.center=[(self.max[0]+self.min[0])/2,(self.max[1]+self.min[1])/2,(self.max[2]+self.min[2])/2]

    def rotation(self,x,y,z):#不可编译
        import cv2
        R, j = cv2.Rodrigues((x,y,z))
        self.applyMatrix(R.tolist())

if __name__ == "__main__":  # 用于测试
    from Mesh import Mesh

    mesh = Mesh("input/m1.obj")
    pv = ProcessVertex(mesh.vertex)
    #print(pv.max,pv.min,pv.center)
    #pv.move(-1*pv.center[0],-1*pv.center[1],-1*pv.center[2])
    #pv.rotation(3.1415926/2,0,0)
    pv.rotation(0.1,1.7,4.1)
    pv.applyMatrix([
        [1, 0, 0,0],
        [0, 0, -1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ])
    mesh.vertex = pv.vertex
    mesh.save()

