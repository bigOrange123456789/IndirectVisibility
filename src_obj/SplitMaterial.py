class SplitMaterial:
    def __init__(self,mesh):
        self.mesh=mesh
        mesh.updateVertex()
        mesh.updateFace()#修改索引
        index=0
        print(mesh.materialsName)
        print("文件个数",len(mesh.materialsName))
        for us in mesh.materialsName:
            lines=[]
            for att in mesh.attributes:
                if att!="us" and att!="f ":
                    for line in mesh.data[att]:
                        lines.append(att+line+"\n")
            for material in mesh.materials:
                if material['us'][0]==us:
                    for line in material['us']:
                        lines.append('us'+line+"\n")
                    for line in material['f ']:
                        lines.append('f '+line+"\n")
            f2 = open(mesh.name+str(index)+".obj","w",encoding="utf-8")
            f2.write( ''.join(lines))
            index=index+1
if __name__ == "__main__":#用于测试
    from Mesh import Mesh
    mesh=Mesh("input/untitled.obj")
    SplitMaterial(mesh)
