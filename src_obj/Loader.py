class Loader:
    def getName(self):
        arr = self.path.split("/")
        l = len(arr)
        name = arr[l - 1].split(".obj")[0]
        return name

    def __init__(self, path):
        self.path = path
        self.attributesGlobal = ['# ', 'mt']
        self.attributesLocal = [
            'g ', 'v ', 'vn', 'vt', 'us', 'f ',
            'o ',
            's '
        ]  # 属性的顺序最好不要修改
        self.attributes = []
        for i in self.attributesGlobal:
            self.attributes.append(i)
        for i in self.attributesLocal:
            self.attributes.append(i)

        self.data = {}  # 没有归类的数据 #旧的数据管理
        self.meshes = []  # 已经归类的数据
        self.materials = []  # 为了基于材质进行归类   #只存放三角面信息
        self.materialsName = {}  # 材质名称#us去重后的结果

        for attribute in self.attributes:
            self.data[attribute] = []
        self.load()

        self.initVertex()
        self.initFace()
        self.name = self.getName()

    def load(self):
        f1 = open(self.path, "r", encoding="utf-8")
        lines = f1.readlines()
        for line in lines:
            # 开始去除每一行记录的尾部
            arr = line.split("\n")
            line = arr[0]
            # 如果某一行长度小于2就跳过
            if len(line) < 2:
                continue
            # 前两个字母作为属性
            att = line[0] + line[1]
            # 开始去除每一行记录的头部
            arr = line.split(att)
            if att == "mt":
                str = arr[1]
                i = 2
                while i < len(arr):
                    str = str + att + arr[i]
                    i = i + 1
                self.data[att].append(str)
            elif len(arr) == 2:
                # 整体
                self.data[att].append(arr[1])
                # 局部
                if att == "g ":  # 添加新的mesh
                    self.newMesh()
                if att == "us":  # usemtl会指明该部分的材质
                    self.newMaterial()
                    self.materialsName[arr[1]] = 1
                if att != "# ":  # 大部分属性都需要被记录到self.meshes中
                    mesh = self.currentMesh()
                    mesh[att].append(arr[1])
                if att == "us" or att == "f ":
                    material = self.currentMaterial()
                    material[att].append(arr[1])
            else:
                print("文件格式错误")
                print(line, len(line))

    def initFace(self):
        # 整体
        f = self.data['f ']
        self.face = []
        import re
        for f0 in f:
            # 处理三角面格式
            f0 = self.processFace(f0)
            # 获取9个数字
            arr = re.findall(r"-*\d+\.?\d*", f0)
            if not len(arr) == 9:
                print("warning 86",end="\r")
                # print("无法解析将面为9个数字：", f0, "\t", arr,end="\r")
            arr2 = []
            for element in arr:
                arr2.append(int(element))
            # print(len(arr2))
            self.face.append(arr2)
        # 局部
        vn_sum = 0
        for mesh in self.meshes:
            mesh['face'] = []
            f = mesh['f ']
            for f0 in f:
                # 处理三角面格式
                f0 = self.processFace(f0)
                # 提取9个数字
                arr = re.findall(r"\d+\.?\d*", f0)
                if not len(arr) == 9:
                    print("warning 104",end="\r")
                    # print("无法解析将面为9个数字：", f0, "\t", arr,end="\r")
                # 变为整数类型
                arr2 = []
                for element in arr:
                    arr2.append(int(element) - vn_sum)
                mesh['face'].append(arr2)
            vn_sum = vn_sum + len(mesh['vertex'])

    def initVertex(self):
        # 整体
        v = self.data['v ']
        self.vertex = []
        import re
        for v0 in v:
            arr = re.findall(r"-*\d+\.?\d*E*-*\d*", v0)
            if not len(arr) == 3:
                print("无法解析为3个普通数字：", v0, "\t", arr)
            arr2 = [float(arr[0]), float(arr[1]), float(arr[2])]
            self.vertex.append(arr2)
        # 局部
        for mesh in self.meshes:
            mesh['vertex'] = []
            v = mesh['v ']
            for v0 in v:
                arr = re.findall(r"-*\d+\.?\d*E*-*\d*", v0)
                if not len(arr) == 3:
                    print("无法解析为3个普通数字：", v0, "\t", arr)
                arr2 = [float(arr[0]), float(arr[1]), float(arr[2])]
                mesh['vertex'].append(arr2)

    def currentMesh(self):
        k = len(self.meshes) - 1
        if k < 0:  # 有的obj文件中没有'g '标签
            self.newMesh()
            return self.meshes[0]
        else:
            return self.meshes[k]

    def newMesh(self):
        self.meshes.append({})
        mesh = self.currentMesh()
        for attribute in self.attributesLocal:
            mesh[attribute] = []

    def currentMaterial(self):
        k = len(self.materials) - 1
        if k < 0:
            self.newMaterial()
            return self.materials[0]
        else:
            return self.materials[k]

    def newMaterial(self):
        self.materials.append({})
        material = self.currentMaterial()
        material['us'] = []  # 材质名称
        material['f '] = []  # 使用该材质的区域

    @staticmethod
    def processFace(f0):
        # 将中间的空的位置补为-1
        arr0 = f0.split("/")
        if len(arr0)==1:
            return f0
        for i in range(len(arr0)):
            if arr0[i] == "":
                arr0[i] = "-1"
        f0 = arr0[0]
        for i in range(6):
            f0 = f0 + "/" + arr0[i + 1]
        return f0
