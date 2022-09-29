import numpy as np
from lib.Tool import Tool as T
from lib.ToolG import ToolG as TG
import time as t
class Clustering:#目前使用欧式距离
  def __init__(self,opt):
    self.opt=opt
  def kMeans(self,dataSet, step):#dataSet中每一行是一个元素
    if not self.opt["useGPU"]:#不用GPU的话kMeans2性能更高一些
        return self.kMeans2(dataSet, step)
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
    nextFlag = True
    timer=0#记录迭代次数
    while nextFlag:#直到聚类结果不变时再停止
        nextFlag = False
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
                nextFlag = True
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
        print("\t\t\t\t空集比例:"+str(nullNumber)+"/"+str(k)+"\t迭代次数:"+str(timer))
    print()
    return centroids.tolist(), clusterAssment.tolist()   # 返回：质心，每个元素的类别 
  def kMeans2(self,dataSet, step):
    data=np.array(dataSet)
    k= int(np.shape(dataSet)[0]/step)#质心个数
    centers = data[ (np.array(range(k))*step).tolist(),:]             #np.mat(np.zeros((k, n)))#用于存储所有质心
    for i in range(500): # 首先利用广播机制计算每个样本到簇中心的距离，之后根据最小距离重新归类
        classifications = np.argmin(((data[:, :, None] - centers.T[None, :, :])**2).sum(axis=1), axis=1)#计算每个元素最近的质心
        new_centers = np.array([data[classifications == j, :].mean(axis=0) for j in range(k)])# 对每个新的簇计算簇中心
        if (new_centers == centers).all():break# 簇中心不再移动的话，结束循环
        else: centers = new_centers
    return  centers.tolist(), classifications[:, None].tolist()#return  centers.tolist(), classifications.tolist()
  def kMeans_one(self,dataSet, step):#dataSet中每一行是一个元素#只进行一次迭代
    if not self.opt["useGPU"]:#不用GPU的话kMeans_next2性能更高一些
        return self.kMeans_one2(dataSet, step)
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
    
    self.timer=0#timer+1
    self.m=m#定值 表示元素个数
    self.k=k#定值 表示质心个数
    self.dataSet=dataSet

    self.centroids=centroids#保存质心 用于下一次迭代
    self.clusterAssment=clusterAssment#保存分组信息 用于下一次迭代
    return centroids,clusterAssment,True#质心 类别 是否继续迭代    #return centroids.tolist(), clusterAssment.tolist()   # 返回：质心，每个元素的类别 
  def kMeans_next(self):#dataSet中每一行是一个元素#只进行一次迭代
    if not self.opt["useGPU"]:#不用GPU的话kMeans_next2性能更高一些
        return self.kMeans_next2()
    t0=t.time()
    centroids=self.centroids#读取上一次迭代的结果
    clusterAssment=self.clusterAssment#读取上一次迭代的结果
    m = self.m#数据集的行数(个数)
    k = self.k
    dataSet=self.dataSet
    nextFlag = True
    if True:#只执行一次 #while nextFlag:#直到聚类结果不变时再停止
        nextFlag = False
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
                nextFlag = True
            clusterAssment[i, :] = minIndex, minDist # 每个元素：【质心编号，到质心的距离】
        nullNumber=0#记录空集个数
        for cent in range(k):   #更新质心的位置   #遍历所有质心
            print("2:"+str(cent+1)+"/"+str(k),end="\r")
            ptsInClust = dataSet[np.nonzero(clusterAssment[:, 0].A == cent)[0]]
            if not len(ptsInClust)==0:#该质心对应的点不为空
                centroids[cent, :] = np.mean(ptsInClust, axis=0)
            else:
                nullNumber=nullNumber+1
        self.timer=self.timer+1
        print("空集比例:"+str(nullNumber)+"/"+str(k)+"\t迭代次数:"+str(self.timer),"\t迭代计算耗时:"+str((t.time()-t0)/60/1000),"min\t\t")
    print()
    return centroids,clusterAssment,nextFlag#质心 类别 是否结束    #return centroids.tolist(), clusterAssment.tolist()   # 返回：质心，每个元素的类别 
  def kMeans_one2(self,dataSet, step):
    self.dataSet=np.array(dataSet)
    self.k= int(np.shape(dataSet)[0]/step)#质心个数
    self.centroids = self.dataSet[ (np.array(range(self.k))*step).tolist(),:]             #np.mat(np.zeros((k, n)))#用于存储所有质心
    # print("self.dataSet",self.dataSet)
    # print("self.centroids",self.centroids)
    return  self.centroids, [],True#return  centers.tolist(), classifications.tolist()
  def kMeans_next2(self):#dataSet中每一行是一个元素#只进行一次迭代
    data=self.dataSet
    centers=self.centroids
    k=self.k    
    classifications = np.argmin(((data[:, :, None] - centers.T[None, :, :])**2).sum(axis=1), axis=1)#计算每个元素最近的质心
    new_centers = np.array([data[classifications == j, :].mean(axis=0) for j in range(k)])# 对每个新的簇计算簇中心
    nextFlag=not (new_centers == centers).all()#是否进行下一次迭代 
    if nextFlag:
        import math
        def cleanedList(centers0): 
            return np.array([x.tolist() for x in centers0 if (math.isnan(x[0]) == False)])
        new_centers_clean=cleanedList(new_centers)
        centers_clean=cleanedList(centers)
        if new_centers_clean.shape[0] ==centers_clean.shape[0]:
            nextFlag=not (new_centers_clean == centers_clean).all()
    self.centroids=new_centers
    return new_centers,classifications[:, None],nextFlag#质心 类别 是否进行下一次迭代    #return centroids.tolist(), clusterAssment.tolist()   # 返回：质心，每个元素的类别 
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