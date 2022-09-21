from Mesh import Mesh
from Rasterization import Rasterization
import numpy as np
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
    def __init__(self,opt):
        t0=t.time()
        w=opt["w"]#800#257
        h=opt["h"]#800#257
        inpath=opt["inpath"]
        depthMap=sys.float_info.max*np.ones([w,h])
        idMap=-1*np.ones([w,h])

        matrices_all=self.loadJson(inpath+'/matrices_all.json')
        for e in matrices_all:
            e.append([1,0,0,0, 0,1,0,0, 0,0,1,0])
        for e in matrices_all:
            for matrix in e:
                matrix.append(0)
                matrix.append(0)
                matrix.append(0)
                matrix.append(1)
        t1=t.time()
        for i in range(500):#range(len(matrices_all)):
            print(i)
            m0 = Mesh(inpath+'/obj/'+str(i)+'.obj')
            for matrix in matrices_all[i]:
                Rasterization(
                    matrix,
                    m0,
                    opt["m"],opt["v"],opt["p"],
                    depthMap,#深度图不断更新
                    i, idMap #构件标记图不断更新
                )
        print((t1-t0)/60,"min")
        print((t.time()-t1)/60,"min")

        image=np.ones([w,h,3])
        for i in range(w):
            for j in range(h):
                c=depthMap[j][i]
                image[i][j][0]=c
                image[i][j][1]=c
                image[i][j][2]=c
        self.saveImg(image,"depthMap4.jpg")

        for i in range(w):
            for j in range(h):
                c=int(idMap[j][i])
                if c<0:c=0xffffff
                image[i][j][0]=c&0xff0000
                image[i][j][1]=c&0x00ff00
                image[i][j][2]=c&0x0000ff
        self.saveImg(image,"idMap4.jpg")
        

if __name__ == "__main__":#用于测试
  import sys
  if len(sys.argv)<2:
    print("ERR:请指定config.json的路径")
    exit(0)
  path=sys.argv[1]
  config=Main.loadJson(path)
  Main(config)
