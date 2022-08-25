import numpy as np
import sys
sys.path.append("lib_py")
from Tool import Tool as T
from ToolG import ToolG as TG
from Loading import Loading as Loading
import json
np.set_printoptions(precision=2)
class IndirectVisibility:
  @staticmethod
  def mkdir(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path) 
  def __init__(self,opt):
      self.mkdir("out")
      self.opt={
        "in":"./in/test.json",
        "out1":"./out/1.direct",#直接可见度矩阵，txt
        "out2":"./out/2.redunList.json",#冗余视点列表
        "out2.d0":"./out/2.d0",
        "out2.nameList":"./out/2.nameList",
        "step":2,#聚类个数的步长
        "useGPU":True,#是否使用GPU
        "out3":"./out/3.e",#特征矩阵，txt
        "out4":"./out/4.simMat",#视觉相关度矩阵，txt
        "out5":"./out/5.d1",#间接相关度矩阵，txt
        "out6":"./out/6.ls",#资源加载列表，txt.json
        "out6_d":"./out/6.ls_d",#资源加载列表，txt.json
        "sim":True,#是否简化计算流程 #简化流程后只计算直接可见度，不计算间接可见度
        "out6_i":"./out/6.ls_i",#资源加载列表，txt.json
        "out7_d":"./out/7.ls_d",
        "areaMin":64,#构件的投影面积小于这个数值视为不可见
        "multidirectionalSampling":False,#True,#不同方向的采样结果分开存储
        }
      for i in opt:
          self.opt[i]=opt[i]

  #1.直接可见度
  def loading(self):
      print("采样集:",self.opt["in"])
      data=[]
      nameList=[]
      import os
      numberAll=len(os.listdir(self.opt["in"]))
      numberIndex=0
      for fileName in os.listdir(self.opt["in"]):
          if fileName=="config.json" or not len(fileName.split(".json"))==2:
              continue
          f1=open(self.opt["in"]+"/"+fileName, encoding='gb18030', errors='ignore')
          j=json.load(f1)
          if self.opt["multidirectionalSampling"]:#分成多个方向分别存储
            j_all={}
            for direct in j:
                for componet_id in j[direct]:
                    j_all[componet_id]=j[direct][componet_id]
            j=j_all
          data.append(j)
          nameList.append(fileName.split(".json")[0])
          numberIndex=numberIndex+1
          print(str(numberIndex)+"/"+str(numberAll),end="\r")
      print()
      return data,nameList
  def getMax(self,data):#获取构件的最大编号 既构件编号
    max=-1
    for i in data:
        for j in i:
            j=int(j)
            if j>max:
                max=j
    return max+1
  def direct(self,data):#获得直接可见度
    number=self.getMax(data)+1#构件个数 
    data2=[]
    for i in range(len(data)):#每一行是一个视点
        data2.append([])
        for j in range(number):
            data2[i].append(0)
        for j in data[i]:
            data2[i][int(j)]=data[i][j]
    print("视点个数:",len(data2))
    print("构件个数:",number)
    return data2#每一列是一个特征
  #2.0 合并相似构件
  
  #2.去除冗余视点
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

  #3.特征矩阵
  def eigenMat(self,data2):#获得特征矩阵
    #data2=np.array(data2).T
    U,Sigma,VT=np.linalg.svd(data2)
    Sigma_sum=np.sum(Sigma)

    for i in range(len(Sigma)):
        if np.sum(Sigma[0:i+1])>=1.*Sigma_sum:
            break
    dim=i+1

    s=np.mat(np.eye(dim)*Sigma[:dim])
    sI=np.linalg.inv(s)

    temp=np.matmul(U[:,0:dim],sI)
    temp=np.matmul(np.array(data2).T,temp)
    temp=temp.T

    return temp.tolist()
    #return data2#每一列是一个特征
  #4.相关矩阵
  def sim(self,inA,inB):#相关程度 （注：inA,inB的1范式为定值）
    inA=np.array(inA).T
    inB=np.array(inB).T
    return float(inA.dot(inB))
  def getSimMat(self,data):#获得相似度矩阵 (列向量之间)
    d=np.array(data).T
    n=len(data[0])#构件个数
    simMat = np.zeros((n, n))
    #return simMat
    timesAll=0
    for i in range(n):
        for j in range(i+1):
            timesAll=timesAll+1
    times=0
    for i in range(n):
        #print(str(round(100*i/n,2))+"%","\t",str(i)+"/"+str(n),end="\r")
        for j in range(i+1):
            simMat[i,j]=simMat[j,i]=self.sim(d[i],d[j])
            times=times+1
            print(str(round(100*times/timesAll,2))+"%","\t",str(times)+"/"+str(timesAll),end="\r")
    print()
    sum=np.sum(simMat, axis=0)
    for i in range(n):
        #print(str(i)+"/"+str(n))
        for j in range(n):
            if not sum[i]==0:
                simMat[i,j]=simMat[i,j]/sum[i]
    #print('np.sum(simMat, axis=0)',np.sum(simMat, axis=0))
    return simMat
  #5.间接可见度
  def mul(self,a,b):
    a=np.array(a)
    b=np.array(b)
    return np.matmul(a, b)
  #6.计算资源加载列表
  def getlist(self,arr1,arr2,maxL):#直接可见度，间接可见度，最大长度
    for i in range(len(arr1)):
        if not arr1[i]==0:
            arr2[i]=0
    list=[]
    list_d=[]#直接可见度资源列表
    list_i=[]#间接可见度资源列表
    obj1=[]#排序
    for i in range(len(arr1)):
        obj1.append({"n":arr1[i],"data":i})
    print("\t s1",end="\r")
    T.sort(obj1)
    for i in obj1:
        if i['n']==0:
            break
        if len(list)<maxL:
            list.append(i["data"])
            list_d.append(i["data"])
    obj2=[]
    for i in range(len(arr2)):
        obj2.append({"n":arr2[i],"data":i})
    print("\t s2",end="\r")
    T.sort(obj2)
    print("\t 计算list",end="\r")
    for i in obj2:
        if i['n']==0:
            break
        #print("i",i)
        if len(list)<maxL:
            print(len(list),maxL,end="\r")
            list.append(i["data"])
            list_i.append(i["data"])
    return list, list_d, list_i
  def getlistG(self,arr1,arr2,o1,o2,maxL):#直接可见度，间接可见度，最大长度
    list=[]
    list_d=[]#直接可见度资源列表
    list_i=[]#间接可见度资源列表
    for index in o1:
        index=int(index)
        element=arr1[index]
        if element==0:
            break
        if len(list)<maxL:
            list.append(index)
            list_d.append(index)
    for index in o2:
        index=int(index)
        element=arr2[index]
        if element==0:
            break
        if len(list)<maxL:
            list.append(index)
            list_i.append(index)      
    return list, list_d, list_i
  def getlistG_sim(self,arr1,o1):#直接可见度，间接可见度，最大长度
    list_d=[]#直接可见度资源列表
    for index in o1:
        index=int(index)
        element=arr1[index]
        if element==0:
            break
        list_d.append(index)    
    return list_d
  def getLists_sim(self,d0):
    lists_d=[]#直接可见度资源列表
    if self.opt["useGPU"]:
        order0=TG.sort(d0)
        for i in range(len(d0)):
            list_d=self.getlistG_sim(d0[i],order0[i])
            lists_d.append(list_d)
            print("\t\t",str(round(100*(i+1)/len(d0),2))+"%","\t",str(i+1)+"/"+str(len(d0)),end="\r")
        print()
    else:#不使用GPU
        print("必须使用GPU")
    return lists_d
  def getLists(self,d0,d1):
    lists=[]
    lists_d=[]#直接可见度资源列表
    lists_i=[]#间接可见度资源列表
    if self.opt["useGPU"]:
        for a in range(len(d1)):
            for b in range(len(d1[a])):
                if not d0[a][b]==0:
                    d1[a][b]=0
        order0=TG.sort(d0)
        order1=TG.sort(d1)
        for i in range(len(d0)):
            list,list_d,list_i=self.getlistG(d0[i],d1[i],order0[i],order1[i],500)
            lists.append(list)
            lists_d.append(list_d)
            lists_i.append(list_i)
            print("\t\t",str(round(100*(i+1)/len(d0),2))+"%","\t",str(i+1)+"/"+str(len(d0)),end="\r")
        print()
    else:#不使用GPU
        for i in range(len(d0)):
            list,list_d,list_i=self.getlist(d0[i],d1[i],500)
            lists.append(list)
            lists_d.append(list_d)
            lists_i.append(list_i)
            #break
            print("\t\t",str(round(100*(i+1)/len(d0),2))+"%","\t",str(i+1)+"/"+str(len(d0)),end="\r")
        print()
    return lists,lists_d,lists_i
  def addRedunList(self,ls,ls1,ls2,nameList,redunList):
    for tag in redunList:
        data=redunList[tag]
        ls.append(data)
        ls1.append(data)
        ls2.append(data)
        nameList.append(tag)
    return ls,ls1,ls2,nameList
  #7.缩小误差
  def reduceError(self,d0_,nameList0,ls1,nameList):
      import math as math
      areaMin=self.opt["areaMin"]*2*4*math.pi/(800*800*6)
      ls1_len=0
      for i in ls1:
          ls1_len=ls1_len+1
      # d0_:全部采样视点的直接可见度,数组类型 
      # nameList0:
      # ls1:
      # nameList:
      numberIncrease=0#用于统计新增构件个数
      for i in range(len(nameList)):#ls1
          for j in range(len(nameList0)):#d0_
                if nameList[i] == nameList0[j]:#同一个视点位置
                    d=d0_[j]#直接可见度数组
                    l=ls1[i]#数据包加载顺序的数组
                    if isinstance(l,str):
                        for k in range(len(nameList)):#ls1
                            if nameList[k]==l:
                                l=ls1[k]
                    for ii in range(len(d)):
                        if d[ii]>areaMin:#if not d[ii]==0:
                            flag=False#假设l里面不包括数据包ii
                            for e in l:
                                if e==ii:
                                    flag=True#l里面包括数据包ii
                            if not flag:#如果l里面不包括数据包ii
                                l.append(ii)
                                numberIncrease=numberIncrease+1
          print( str(round(100*(i+1)*(j+1)/(len(nameList)*len(nameList0)),2))+"%","\t",str((i+1)*(j+1))+"/"+str(len(nameList)*len(nameList0)),end="\r")
      print()
      print("新增构件个数为:"+str(numberIncrease))
      return ls1
        
  def start(self,step):
    print("起始步骤：",step)
    print("opt",self.opt)
    import time as t
    t0=t.time()
    print('1.直接可见度')#第一步必须要执行
    if step>1:
        d0_,nameList0=T.r2(self.opt["out1"])
    else:
        data,nameList0=self.loading()#Loading.loading(self.opt)#
        d0_=self.direct(data)#degree
        T.w2(d0_,self.opt["out1"],nameList0)
    t1=t.time()
    print("step1.执行时间："+str(((t1-t0)/60))+" min")
    # exit(0)
    
    print("2.去除冗余")
    if step>2:#跳过第2步
        d0=T.r(self.opt["out2.d0"])
        nameList=T.r_txt(self.opt["out2.nameList"])
        redunList=T.loadJson(self.opt["out2"])
    else:
        d0,nameList,redunList=self.clustering(d0_,nameList0,self.opt["step"])
        T.w(d0,self.opt["out2.d0"])
        T.w(nameList,self.opt["out2.nameList"])
        T.saveJson(self.opt["out2"],redunList)
    t2=t.time()
    print("step2.执行时间："+str(((t2-t1)/60))+" min")
    
    print('3.获取特征')
    e=d0#不进行降维去噪
    #e=self.eigenMat(d0)#进行降维去噪
    #T.w(e,self.opt["out3"])
    t3=t.time()
    print("step3.执行时间："+str(((t3-t2)/60))+" min")
    
    print('4.相关矩阵')
    if not self.opt["sim"]:#不计算间接可见度时不需要相关矩阵
     if step>4:
        s=T.r(self.opt["out4"])
     else:
        s=self.getSimMat(e)
        T.w(s,self.opt["out4"])
    t4=t.time()
    print("step4.执行时间："+str(((t4-t3)/60))+" min")
    
    print('5.间接可见度')
    if not self.opt["sim"]:#不计算间接可见度
     if step>5:
        d1=T.r(self.opt["out5"])
     else:
        d1=self.mul(d0,s)#一次间接可见度
        T.w(d1,self.opt["out5"])
    t5=t.time()
    print("step5.执行时间："+str(((t5-t4)/60))+" min")

    print('6.计算资源加载列表')
    if step>6:
        ls,nameList=T.r2(self.opt["out6"])
        ls1,anonymous=T.r2(self.opt["out6_d"])
        ls2,anonymous=T.r2(self.opt["out6_i"])
    else:
        if self.opt["sim"]:
            ls1=self.getLists_sim(d0)
        else:
            ls,ls1,ls2=self.getLists(d0,d1)
            ls,ls1,ls2,nameList=self.addRedunList(ls,ls1,ls2,nameList,redunList)
            T.w2(ls,self.opt["out6"],nameList)
            T.w2(ls2,self.opt["out6_i"],nameList)
        T.w2(ls1,self.opt["out6_d"],nameList)
        print("开始加载顺序使用数组的方式进行存储")
    t6=t.time()
    print("step6.执行时间："+str(((t6-t5)/60))+" min")
    
    print('7.缩小误差')
    if self.opt["step"]>1:
        ls1_new=self.reduceError(d0_,nameList0,ls1,nameList)
    else:
        ls1_new=ls1
    T.w2(ls1_new,self.opt["out7_d"],nameList)

    print("finish!")
    tl=t.time()
    print("step1.执行时间："+str(((t1-t0)/60))+" min")
    print("step2.执行时间："+str(((t2-t1)/60))+" min")
    print("step3.执行时间："+str(((t3-t2)/60))+" min")
    print("step4.执行时间："+str(((t4-t3)/60))+" min")
    print("step5.执行时间："+str(((t5-t4)/60))+" min")
    print("step6.执行时间："+str(((t6-t5)/60))+" min")
    print("总执行时间："+str(((tl-t0)/60))+" min")
if __name__ == "__main__":#用于测试
    print('version:2022.02.16-01')
    iv=IndirectVisibility({"in":"in/test"})
    #iv=IndirectVisibility({"in":"in/KaiLiNan02"})
    #iv=IndirectVisibility({"in":"in.HaiNing.22.02.14/all"})
    #iv=IndirectVisibility({"in":"in.KaiLiNan22.01.16-1"})
    # iv=IndirectVisibility({"in":"1.move_all"})
    iv.opt["sim"]=False#True#
    iv.opt["step"]=1
    iv.start(1)
