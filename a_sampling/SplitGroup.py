class SplitGroup:
    def __init__(self,mesh):
        self.mesh=mesh
        l=len(mesh.meshes)
        for i in range(l):
            self.downloadSplit(mesh.name+str(i)+".obj",i)
    def downloadSplit(self,path,index):
        self.mesh.updateVertex()
        self.mesh.updateFace()#attributesLocal
        mesh=self.mesh.meshes[index]
        lines=[]
        for att in self.mesh.attributesGlobal:
            for line in self.mesh.data[att]:
                lines.append(att+line+"\n")
        for att in self.mesh.attributesLocal:
            for line in mesh[att]:
                lines.append(att+line+"\n")

        f2 = open(path,"w",encoding="utf-8")
        f2.write( ''.join(lines))
if __name__ == "__main__":#用于测试
    from Mesh import Mesh
    mesh=Mesh("input/house.obj")
    SplitGroup(mesh)
