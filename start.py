import numpy as np
import sys
sys.path.append("src_py")
from Tool import Tool as T
from ToolG import ToolG as TG
from Loader import Loader as Loader
from ClusteringViewer import ClusteringViewer
from NoiseReduction import NoiseReduction
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
  #2.0 合并相似构件
  #2.去除冗余视点
  #3.通过特征矩阵进行降噪
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
        nameList0,d0_=Loader(self.opt).result
        T.w2(d0_,self.opt["out1"],nameList0)
    t1=t.time()
    print("step1.执行时间："+str(((t1-t0)/60))+" min")
    print("2.去除冗余")
    if step>2:#跳过第2步
        d0=T.r(self.opt["out2.d0"])
        nameList=T.r_txt(self.opt["out2.nameList"])
        redunList=T.loadJson(self.opt["out2"])
    else:
        d0,nameList,redunList=ClusteringViewer(d0_,nameList0,self.opt).result
        T.w(d0,self.opt["out2.d0"])
        T.w(nameList,self.opt["out2.nameList"])
        T.saveJson(self.opt["out2"],redunList)
    t2=t.time()
    print("step2.执行时间："+str(((t2-t1)/60))+" min")
    
    print('3.获取特征')
    e=d0#不进行降维去噪
    e=NoiseReduction.eigenMat(d0)#进行降维去噪
    T.w(e,self.opt["out3"])
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
    iv=IndirectVisibility({"in":"in/test_viewerPoint"})
    #iv=IndirectVisibility({"in":"in/KaiLiNan02"})
    #iv=IndirectVisibility({"in":"in.HaiNing.22.02.14/all"})
    #iv=IndirectVisibility({"in":"in.KaiLiNan22.01.16-1"})
    # iv=IndirectVisibility({"in":"1.move_all"})
    iv.opt["sim"]=False#True#
    iv.opt["step"]=2
    iv.start(1)
