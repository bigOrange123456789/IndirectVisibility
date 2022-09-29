import numpy as np
class Mul:
  def __init__(self,opt,d0,s):
    from lib.Tool import Tool as T
    import time as t
    t0=t.time()
    import os
    if opt["sim"]:
      d1=[]
    else:
      if os.path.exists(opt["out5"]):
        d1=T.r(opt["out5"])
      else:
        d1=self.mul(d0,s)#一次间接可见度
        T.w(d1,opt["out5"])
    self.result=[d1,t.time()-t0]
    print("step5.执行时间："+str(((t.time()-t0)/60))+" min")
  #5.间接可见度
  def mul(self,a,b):
    a=np.array(a)
    b=np.array(b)
    return np.matmul(a, b)
if __name__ == "__main__":#用于测试
    print()