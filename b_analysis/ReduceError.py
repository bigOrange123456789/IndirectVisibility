import os
class ReduceError:
  def __init__(self,opt,d0_,nameList0,ls1,nameList):
    import time as t
    t0=t.time()
    self.opt=opt
    from lib.Tool import Tool as T
    if opt["step"]==1:#如果没有进行视点合并就不进行误差纠正
        ls1_new=ls1
    elif os.path.exists(self.opt["out1"]):
        ls1_new,nameList=T.r2(self.opt["out7_d"])
    else:
        ls1_new=self.reduceError(d0_,nameList0,ls1,nameList)
        T.w2(ls1_new,self.opt["out7_d"],nameList)

    self.result=[ls1_new,t.time()-t0]
  def reduceError(self,d0_,nameList0,ls1,nameList):#减少由视点合并引起的误差
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
    
if __name__ == "__main__":#用于测试
    print()