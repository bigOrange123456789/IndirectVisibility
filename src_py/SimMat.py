# from asyncio.windows_events import NULL
import numpy as np
import os
class SimMat:
  def __init__(self,opt,e):
    from lib.Tool import Tool as T
    import time as t
    t0=t.time()
    self.opt=opt
    if self.opt["sim"]:#不计算间接可见度
      s=[]#NULL
    else:
      if os.path.exists(self.opt["out1"]):
        s=T.r(self.opt["out4"])
      else:
        s=self.getSimMat(e)
        T.w(s,opt["out4"])
    self.result=[s,t.time()-t0]
    print("step4.执行时间："+str(((t.time()-t0)/60))+" min")
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
  
if __name__ == "__main__":#用于测试
    print()