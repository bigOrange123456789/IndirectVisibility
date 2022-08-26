import numpy as np
from Tool import Tool as T
from ToolG import ToolG as TG
class Clustering:
  def __init__(self,opt):
    self.opt=opt
  def kMeans(self,dataSet, step):#dataSet中每一行是一个元素
    print("聚类步长：",step)
    import math as math
    n = np.shape(dataSet)[1] #数据集的列数
    k= math.floor(np.shape(dataSet)[0]/step)#质心个数
    centroids = np.mat(np.zeros((k, n)))#用于存储所有质心
    for i in range(k):
        for j in range(n):
            centroids[i,j]=dataSet[i*step][j]
    print("质心初始位置：\n",centroids)
    dataSet=np.mat(dataSet)
    m = np.shape(dataSet)[0] #数据集的行数(个数)
    clusterAssment = np.mat(np.zeros((m, 2)))# m*2的零矩阵 用来记录每个点最近的中心和距离
    clusterChanged = True
    timer=0#记录迭代次数
    while clusterChanged:#直到聚类结果不变时再停止
        clusterChanged = False
        if self.opt["useGPU"]:
            distTG=TG.getDist(centroids,dataSet)#每个行向量到每个中心的距离
        for i in range(m): #寻找每个元素最近的质心  #遍历每个元素
            print("1:"+str(i)+"/"+str(m),end="\r")
            minDist = 0
            minIndex = -1
            for j in range(k):#遍历所有质心
                if self.opt["useGPU"]:
                    distJI = distTG[j][i]
                else:
                    distJI = np.sum(np.power(centroids[j, :]- dataSet[i, :], 2))#计算元素到质心的距离平方 #比较大小不需要开根号
                if minIndex==-1 or distJI < minDist:
                    minDist = distJI
                    minIndex = j#质心编号
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist # 每个元素：【质心编号，到质心的距离】
        nullNumber=0#记录空集个数
        for cent in range(k):   #更新质心的位置   #遍历所有质心
            print("2:"+str(cent+1)+"/"+str(k),end="\r")
            ptsInClust = dataSet[np.nonzero(clusterAssment[:, 0].A == cent)[0]]
            if not len(ptsInClust)==0:#该质心对应的点不为空
                centroids[cent, :] = np.mean(ptsInClust, axis=0)
            else:
                nullNumber=nullNumber+1
        timer=timer+1
        print("\t\t\t\t空集比例:"+str(nullNumber)+"/"+str(k)+"\t迭代次数："+str(timer))
    print()
    return centroids.tolist(), clusterAssment.tolist()   # 返回：质心，每个元素的类别 
  def kMeans0(self,dataSet, step):#dataSet中每一行是一个元素
    print("聚类步长：",step)
    import math as math
    n = np.shape(dataSet)[1] #数据集的列数
    k= math.floor(np.shape(dataSet)[0]/step)#质心个数
    centroids = np.mat(np.zeros((k, n)))#用于存储所有质心
    for i in range(k):
        for j in range(n):
            centroids[i,j]=dataSet[i*step][j]
    print("质心初始位置：\n",centroids)
    dataSet=np.mat(dataSet)
    m = np.shape(dataSet)[0] #数据集的行数(个数)
    clusterAssment = np.mat(np.zeros((m, 2)))# m*2的零矩阵 用来记录每个点最近的中心和距离
    clusterChanged = True
    timer=0#记录迭代次数
    while clusterChanged:#直到聚类结果不变时再停止
        clusterChanged = False
        if self.opt["useGPU"]:
            distTG=TG.getDist(centroids,dataSet)#每个行向量到每个中心的距离
        for i in range(m): #寻找每个元素最近的质心  #遍历每个元素
            print("1:"+str(i)+"/"+str(m),end="\r")
            minDist = 0
            minIndex = -1
            for j in range(k):#遍历所有质心
                if self.opt["useGPU"]:
                    distJI = distTG[j][i]
                else:
                    distJI = np.sum(np.power(centroids[j, :]- dataSet[i, :], 2))#计算元素到质心的距离平方 #比较大小不需要开根号
                if minIndex==-1 or distJI < minDist:
                    minDist = distJI
                    minIndex = j#质心编号
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist # 每个元素：【质心编号，到质心的距离】
        nullNumber=0#记录空集个数
        for cent in range(k):   #更新质心的位置   #遍历所有质心
            print("2:"+str(cent+1)+"/"+str(k),end="\r")
            ptsInClust = dataSet[np.nonzero(clusterAssment[:, 0].A == cent)[0]]
            if not len(ptsInClust)==0:#该质心对应的点不为空
                centroids[cent, :] = np.mean(ptsInClust, axis=0)
            else:
                nullNumber=nullNumber+1
        timer=timer+1
        print("\t\t\t\t空集比例:"+str(nullNumber)+"/"+str(k)+"\t迭代次数："+str(timer))
    print()
    return centroids.tolist(), clusterAssment.tolist()   # 返回：质心，每个元素的类别 
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
    print("2.1 开始聚类")
    centroids, clustAssing = self.kMeans(dataSet,step)#聚类
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
            #print(dataSet[i])
            dataSet2.append(dataSet[i])
            tagList2.append(viewPoint)
        else:#这个视点是冗余视点
            redunList[viewPoint]=centroid
    #T.saveJson("redunList.json",redunList)
    return dataSet2,tagList2,redunList

if __name__ == "__main__":#用于测试
    print()