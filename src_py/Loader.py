import json
import os
import numpy as np
class Loader:#主要作用是给出直接可见度
   def __init__(self,opt):
    from lib.Tool import Tool as T
    import time as t
    t0=t.time()
    self.opt=opt
    if not self.opt["out1"]=="" and os.path.exists(self.opt["out1"]+".json"):
        d0_,nameList0=T.r2(self.opt["out1"])
    else:
        data,nameList0=self.loading()
        t1=t.time()
        print("加载时间:"+str(((t1-t0)/60))+" min")
        d0_=self.direct(data)
        t2=t.time()
        print("解析时间:"+str(((t2-t1)/60))+" min")
        T.w2(d0_,self.opt["out1"],nameList0)
    print("step1.执行时间："+str(((t.time()-t0)/60))+" min")
    self.result=[nameList0,d0_,t.time()-t0]
   #1.直接可见度
   def loading(self):
      print("采样集:",self.opt["in"])
      data=[]
      if self.opt["multidirectionalSampling"]:#分成多个方向分别存储
        self.dataSplit={}
        for i in range(6):
            direct=str(i+1)
            self.dataSplit[direct]=[]
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
                self.dataSplit[direct].append(j[direct])#
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
    number=self.getMax(data)#构件的最大编号
    print("正在给data2(直接可见度矩阵)分配空间")
    data2=np.zeros([len(data),number]).tolist()
    for i in range(len(data)):#每一行是一个视点
        print("getData2:",str(i)+"/"+str(len(data))+"\t\t",end="\r")
        for j in data[i]:
            data2[i][int(j)]=data[i][j]
    print("\n视点个数:",len(data2))
    print("构件个数:",number)
    return data2#行表示视点，列表示构件
   def getComponent2group(self,groups_arr):
    max=0
    for i in groups_arr:
        if len(i)>0:
            max0=np.max(np.array(i))
            if max0>max:
                max=max0
    component2group=np.zeros(max+1).tolist()
    for group_id in range(len(groups_arr)):
        for component_id in groups_arr[group_id]:
            component2group[component_id]=group_id
    return component2group
    
   def directSplit(self,data,groups_arr):#对于四个方向的采样结果分开处理
    #groups_arr
    component2group=self.getComponent2group(groups_arr)
    number=len(groups_arr) # self.getMax(data)#构件的最大编号
    data2=np.zeros([len(data),number]).tolist()
    for i in range(len(data)):#每一行是一个视点
        for j in data[i]:
            group_id=component2group[int(j)]
            data2[i][group_id]=data[i][j]
    print("视点个数:",len(data2))
    print("构件个数:",number)
    return data2#每一列是一个特征
if __name__ == "__main__":#用于测试
    print()