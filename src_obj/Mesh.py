from Loader import Loader
from ProcessVertex import ProcessVertex
from ProcessTopology import ProcessTopology

class Mesh:
    def __init__(self, path):
        if path:
            myLoad = Loader(path)
            self.name = myLoad.name

            self.attributesGlobal = myLoad.attributesGlobal
            self.attributesLocal = myLoad.attributesLocal
            self.attributes = myLoad.attributes

            self.data = myLoad.data  # 没有归类的数据 #旧的数据管理
            self.meshes = myLoad.meshes  # 已经归类的数据
            self.materials = myLoad.materials  # 为了基于材质进行归类   #只存放三角面信息
            self.materialsName = myLoad.materialsName  # 材质名称#us去重后的结果

            self.vertex = myLoad.vertex
            self.face = myLoad.face

    def clone(self):
        new = Mesh(False)
        new.name = self.name

        new.attributesGlobal = self.cloneObj(self.attributesGlobal)
        new.attributesLocal = self.cloneObj(self.attributesLocal)
        new.attributes = self.cloneObj(self.attributes)

        new.data = self.cloneObj(self.data)
        new.meshes = self.cloneObj(self.meshes)
        new.materials = self.cloneObj(self.materials)
        new.materialsName = self.cloneObj(self.materialsName)

        new.vertex = self.cloneObj(self.vertex)
        new.face = self.cloneObj(self.face)
        return new

    @staticmethod
    def cloneObj(obj):
        if isinstance(obj, dict):
            new = {}
            for i in obj:
                new[i] = Mesh.cloneObj(obj[i])
        elif isinstance(obj, list):
            new = []
            for i in obj:
                new.append(i)
        else:
            new = obj
        return new

    def updateVertex(self):
        # 整体
        self.data['v '] = []
        for arr in self.vertex:
            v0 = str(arr[0]) + " " + str(arr[1]) + " " + str(arr[2])
            self.data['v '].append(v0)
        # 局部
        for mesh in self.meshes:
            mesh['v '] = []
            for arr in mesh['vertex']:
                v0 = str(arr[0]) + " " + str(arr[1]) + " " + str(arr[2])
                mesh['v '].append(v0)

    def updateFace(self):
        # 整体
        self.data['f '] = []
        for i in self.face:
            arr = []
            for i0 in i:
                if i0 > 0:
                    arr.append(str(i0))
                else:
                    arr.append("")

            f0 = ""
            f0 = f0 + str(arr[0]) + "/" + str(arr[1]) + "/" + str(arr[2])
            f0 = f0 + " "
            f0 = f0 + str(arr[3]) + "/" + str(arr[4]) + "/" + str(arr[5])
            f0 = f0 + " "
            f0 = f0 + str(arr[6]) + "/" + str(arr[7]) + "/" + str(arr[8])

            self.data['f '].append(f0)
        # 局部
        for mesh in self.meshes:
            mesh['f '] = []
            for arr in mesh['face']:
                f0 = str(arr[0]) + "/" + str(arr[1]) + "/" + str(arr[2]) + " " + str(arr[3]) + "/" + str(
                    arr[4]) + "/" + str(arr[5]) + " " + str(arr[6]) + "/" + str(arr[7]) + "/" + str(arr[8])
                mesh['f '].append(f0)

    def updateFace(self):
        # 整体
        self.data['f '] = []
        for i in self.face:
            arr = []
            for i0 in i:
                if i0 > 0:
                    arr.append(str(i0))
                else:
                    arr.append("")

            f0 = ""
            f0 = f0 + str(arr[0]) + "/" + str(arr[1]) + "/" + str(arr[2])
            f0 = f0 + " "
            f0 = f0 + str(arr[3]) + "/" + str(arr[4]) + "/" + str(arr[5])
            f0 = f0 + " "
            f0 = f0 + str(arr[6]) + "/" + str(arr[7]) + "/" + str(arr[8])

            self.data['f '].append(f0)
        # 局部
        for mesh in self.meshes:
            mesh['f '] = []
            for arr in mesh['face']:
                f0 = str(arr[0]) + "/" + str(arr[1]) + "/" + str(arr[2]) + " " + str(arr[3]) + "/" + str(
                    arr[4]) + "/" + str(arr[5]) + " " + str(arr[6]) + "/" + str(arr[7]) + "/" + str(arr[8])
                mesh['f '].append(f0)

    def download(self, path):
        lines = []
        for att in self.attributes:
            for line in self.data[att]:
                lines.append(att + line + "\n")
        f2 = open(path, "w", encoding="utf-8")
        f2.write(''.join(lines))

    def save(self):
        self.updateVertex()
        self.download(self.name + "_save.obj")

    def getConfig(self):
        result = []
        for att in self.data:
            print(att, len(self.data[att]))
            result.append([att, len(self.data[att])])
        return result

    # 以下为调用其它包来实现的功能

    def move(self, x, y, z):
        pv = ProcessVertex(self.vertex)
        pv.move(x, y, z)
        self.vertex = pv.vertex
        self.updateVertex()

    def rotation(self, x, y, z):
        pv = ProcessVertex(self.vertex)
        pv.rotation(x, y, z)
        self.vertex = pv.vertex
        self.updateVertex()
    def scale(self, x, y, z):
        pv = ProcessVertex(self.vertex)
        pv.applyMatrix([[x,0,0],[0,y,0],[0,0,z]])
        self.vertex = pv.vertex
        self.updateVertex()
    def applyMatrix(self, mat):
        pv = ProcessVertex(self.vertex)
        pv.applyMatrix(mat)
        self.vertex = pv.vertex
        self.updateVertex()

    def deDedundancy(self):
        pt = ProcessTopology(self.vertex, self.face)
        print("最初的顶点个数", len(self.vertex))
        pt.deDedundancy()
        self.vertex = pt.v
        self.face = pt.f
        self.updateVertex()
        print("完成的顶点个数", len(self.vertex))
        self.updateFace()

    def getEdge(self):
        pt = ProcessTopology(self.vertex, self.face)
        return pt.getEdge()
    def getTriangle(self,i):
        pt = ProcessTopology(self.vertex, self.face)
        return pt.getTriangle(i)
    def merge(self,otherMeshPath):
        m1 = self
        m2 = Mesh(otherMeshPath)#print('会破坏两个另一个mesh')
        v1 = m1.vertex
        f1 = m1.face
        v2 = m2.vertex
        f2 = m2.face
        n2 = len(v2)
        import math
        for i in v2:
            v1.append(i)
        t = math.floor(len(f2[0]) / 3)
        for i in f2:
            i[0] = i[0] + n2
            i[t] = i[t] + n2
            i[2 * t] = i[2 * t] + n2
            f1.append(i)
        self.updateVertex()
        self.updateFace()




#开始进行测试
def deDedundancy_test():
    m0 = Mesh('input/spirit1_0.obj')
    m0.deDedundancy()
    m0.download("output/test.obj")
if __name__ == "__main__":  # 用于测试
    print('start')
    deDedundancy_test()