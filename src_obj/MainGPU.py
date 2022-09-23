from Mesh import Mesh
from RasterizationG import Rasterization
import time as t
class Main:
    @staticmethod
    def mkdir(path):
        import os
        if not os.path.exists(path):
            os.makedirs(path) 
    @staticmethod
    def loadJson(path):
        import json
        return json.load(open(path))
    @staticmethod
    def saveImg(image,name):
        import cv2
        cv2.imwrite(name,image)
    @staticmethod
    def remove(dir_path):
        import os
        # os.walk会得到dir_path下各个后代文件夹和其中的文件的三元组列表，顺序自内而外排列，如 o下有1文件夹，1下有2文件夹：[('o\1\2', [], ['a.py','b']), ('o\1', ['2'], ['c']), ('o', ['1'], [])]
        for root, dirs, files in os.walk(dir_path, topdown=False):
            #root: 各级文件夹绝对路径
            #dirs: root下一级文件夹名称列表，如 ['文件夹1','文件夹2']
            #files: root下文件名列表，如 ['文件1','文件2']
            for name in files:# 第一步：删除文件
                os.remove(os.path.join(root, name))  # 删除文件
            for name in dirs:# 第二步：删除空文件夹
                os.rmdir(os.path.join(root, name)) # 删除一个空目录
    def __init__(self,opt):
        self.opt=opt
        inpath=opt["inpath"]

        matrices_all=self.loadJson(inpath+'/matrices_all.json')
        for e in matrices_all:
            e.append([1,0,0,0, 0,1,0,0, 0,0,1,0])
        for e in matrices_all:
            for matrix in e:
                matrix.append(0)
                matrix.append(0)
                matrix.append(0)
                matrix.append(1)
        self.matrices_all=matrices_all

        print("load start")
        t0=t.time()
        numTriangular=0
        self.meshes=[]
        for i in range(100):#range(len(matrices_all)):#(1):# range(5000):# i in  # 500-244704 ,51684-15250776
            m0 = Mesh(inpath+'/obj/'+str(i)+'.obj')
            self.meshes.append(m0)
            numTriangular=numTriangular+len(m0.face)*len(matrices_all[i])
            print("loading",len(matrices_all),i,end="\t\r")
        print("加载时间：",(t.time()-t0)/60,"min\t\t\t")
        print("三角面片总个数：",numTriangular)
        
    def render(self,m,v,p):
        print("矩阵计算 start")
        t0=t.time()
        w=self.opt["w"]#800#257
        h=self.opt["h"]#800#257

        renderNodes=[]
        for i in range(len(self.meshes)):#range(len(matrices_all)):
            print("rendering",len(self.meshes),i,end="\t\r")
            m0 = self.meshes[i]
            m0.vs2=[]
            for matrix in self.matrices_all[i]:
                renderNodes.append(
                    Rasterization.getMesh0(m0,matrix,i)
                )
        print("矩阵计算时间：",(t.time()-t0)/60,"min")


        print("render start")
        t0=t.time()
        w=self.opt["w"]#800#257
        h=self.opt["h"]#800#257
        Rasterization(
            renderNodes,v
        )
        print("渲染时间：",(t.time()-t0)/60,"min")
        
        # outpath=self.opt["outpath"]
        # self.mkdir(outpath)
        # self.remove(outpath)

        # image=np.ones([w,h,3])
        # for i in range(w):
        #     for j in range(h):
        #         c=depthMap[j][i]
        #         image[i][j][0]=c
        #         image[i][j][1]=c
        #         image[i][j][2]=c
        # self.saveImg(image,outpath+"/depthMap.jpg")

        # for i in range(w):
        #     for j in range(h):
        #         c=int(idMap[j][i])
        #         if c<0:c=0xffffff
        #         image[i][j][0]=c&0xff0000
        #         image[i][j][1]=c&0x00ff00
        #         image[i][j][2]=c&0x0000ff
        # self.saveImg(image,outpath+"/idMap.jpg")

if __name__ == "__main__":#用于测试
    import sys
    if len(sys.argv)<2:
        print("ERR:请指定config.json的路径")
        exit(0)
    path=sys.argv[1]
    config=Main.loadJson(path)
    Main(config).render(
        config["m"],config["v"],config["p"]
    )
