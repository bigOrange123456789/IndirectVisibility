import numpy as np
import os
from lib.Tool import Tool as T
from lib.Clustering import Clustering
class ClusteringViewer:
  def __init__(self,d0_,nameList0,opt):
    import time as t
    t0=t.time()
    self.opt=opt
    if os.path.exists(self.opt["out2.d0"]) and os.path.exists(self.opt["out2.nameList"]) and os.path.exists(self.opt["out2"]):
        d0=T.r(self.opt["out2.d0"])
        nameList=T.r_txt(self.opt["out2.nameList"])
        redunList=T.loadJson(self.opt["out2"])
    else:
        d0,nameList,redunList=self.clustering(d0_,nameList0,self.opt["step"])
        T.w(d0,self.opt["out2.d0"])
        T.w(nameList,self.opt["out2.nameList"])
        T.saveJson(self.opt["out2"],redunList)
    print("step2.执行时间："+str(((t.time()-t0)/60))+" min")
    self.result=[d0,nameList,redunList,t.time()-t0]#d0,nameList,redunList
  def getRedundancy(self,clustAssing,k,tagList):#每个元素的类别，质心个数
    result=[]
    for i in range(len(clustAssing)):
        result.append(i)
    for i in range(k):
        nearestIndex=-1#最近点的编号，最近的距离
        nearestDist=-1#最近的距离
        for j in range(len(clustAssing)):
            if clustAssing[j][0]==i:
                if nearestIndex==-1 or clustAssing[j][1]<nearestDist:
                    nearestIndex=j
                    nearestDist=clustAssing[j][1]
        for j in range(len(clustAssing)):
            if clustAssing[j][0]==i:
                result[j]=nearestIndex
    for i in range(len(result)):
        result[i]=tagList[result[i]]
    return result
  def clustering(self,dataSet_,tagList,step):
    if step==1:#如果步长为1就不进行冗余去除
        return dataSet_,tagList,{}
    dataSet=T.clone(dataSet_)
    print("2.1 开始聚类")#centroids:质心位置, clustAssing:每个元素对应的质心及到质心的距离
    centroids, clustAssing = Clustering(self.opt).kMeans(dataSet,step)#聚类
    print("2.2 分析冗余关系")
    redun=self.getRedundancy(clustAssing,len(centroids),tagList)
    #T.w2(redun,"Redun",tagList)
    print("2.3 计算冗余列表")
    dataSet2=[]
    tagList2=[]
    redunList={}
    for i in range(len(dataSet)):
        viewPoint=tagList[i]
        centroid=redun[i]
        if viewPoint==centroid:#这个视点就是质心
            dataSet2.append(dataSet[i])
            tagList2.append(viewPoint)
        else:#这个视点是冗余视点
            redunList[viewPoint]=centroid
    #T.saveJson("redunList.json",redunList)
    return dataSet2,tagList2,redunList

if __name__ == "__main__":#用于测试
    print()