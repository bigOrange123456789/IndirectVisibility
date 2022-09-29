class SplitLoose:
    def __init__(self, mesh):
        self.mesh = mesh
        for i in range(len(mesh.vertex)):
            j = i + 1
            while j < len(mesh.vertex):
                if mesh.vertex[i][0] == mesh.vertex[j][0] and mesh.vertex[i][1] == mesh.vertex[j][1] and mesh.vertex[i][
                    2] == mesh.vertex[j][2]:
                    print("有重复的顶点", mesh.vertex[i])
                j = j + 1
        self.computeNeighbor()

    def computeNeighbor(self):
        # 计算每个点对应哪些面
        v_f = []
        for vertex0 in mesh.data['v ']:
            v_f.append([])
        i = 0
        for face0 in mesh.face:
            v1 = face0[0] - 1
            v2 = face0[3] - 1
            v3 = face0[6] - 1
            v_f[v1].append(i)
            v_f[v2].append(i)
            v_f[v3].append(i)
            i = i + 1

        # 计算每个面的相邻面
        neighbor = []
        for face0 in mesh.face:
            neighbor.append({})
        i = 0
        for face0 in mesh.face:
            v1 = face0[0] - 1
            v2 = face0[3] - 1
            v3 = face0[6] - 1
            for fi in v_f[v1]:
                neighbor[i][fi] = True
            for fi in v_f[v2]:
                neighbor[i][fi] = True
            for fi in v_f[v3]:
                neighbor[i][fi] = True
            i = i + 1
        self.neighbor = neighbor
        # print(self)

    def split(self):
        l = len(mesh.face)
        hasPrint = self.zeros(l)  # 为0表示这个面还没有被输出

        area = self.getArea(0)
        part = 0

        while (True):
            self.save(self.mesh.name + '_' + str(part) + '.obj', area)
            part = part + 1
            for i in range(l):
                hasPrint[i] = hasPrint[i] + area[i]  # 不为0表示这个面还没有被输出

            index = 0
            while index < l:
                if hasPrint[index] == 0:
                    break
                index = index + 1
            if index < l:
                print("搜索起点：", index)
                area = self.getArea(index)
            else:
                break
        print("切分完成")

    def save(self, path, list):
        lines = []
        for att in self.mesh.attributes:
            if att == "f ":
                index = 0
                while index < len(self.mesh.data[att]):
                    # print("list[index]",list[index])
                    line = self.mesh.data[att][index]
                    # print()
                    if (list[index] > 0):
                        lines.append(att + line + "\n")
                    index = index + 1
            else:
                for line in self.mesh.data[att]:
                    lines.append(att + line + "\n")
        f2 = open(path, "w", encoding="utf-8")
        f2.write(''.join(lines))

    def zeros(self, n):
        arr = []
        for i in range(n):
            arr.append(0)
        return arr

    def getArea(self, start):
        faceFlag = self.zeros(len(mesh.face))  # 0表示尚未确定
        # 找出从start可达的所有面
        faceFlag[start] = 1
        while (True):
            i = 0
            while i < len(faceFlag):
                flag = faceFlag[i]
                if flag == 1:
                    faceFlag[i] = 1
                    for j in self.neighbor[i]:
                        if faceFlag[j] == 0:
                            faceFlag[j] = 1
                    faceFlag[i] = 2  # 2表示已经分析完相邻区域
                    break
                i = i + 1
            if i == len(faceFlag):
                break
        return faceFlag


if __name__ == "__main__":  # 用于测试
    from Mesh import Mesh

    mesh = Mesh("input/window.obj")
    SplitLoose(mesh).split()
