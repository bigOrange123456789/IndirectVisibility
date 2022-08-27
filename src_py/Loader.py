import json
import os
class Loader:#主要作用是给出直接可见度
   def __init__(self,opt):
    from Tool import Tool as T
    import time as t
    t0=t.time()
    self.opt=opt
    if os.path.exists(self.opt["out1"]+".json"):
        d0_,nameList0=T.r2(self.opt["out1"])
    else:
        data,nameList0=self.loading()
        d0_=self.direct(data)
        T.w2(d0_,self.opt["out1"],nameList0)
    print("step1.执行时间："+str(((t.time()-t0)/60))+" min")
    self.result=[nameList0,d0_,t.time()-t0]
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
    number=self.getMax(data)#构件的最大编号
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
if __name__ == "__main__":#用于测试
    print()