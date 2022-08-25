import numpy as np
import sys

from src_py.ReduceError import ReduceError
sys.path.append("src_py")
from Tool import Tool as T
from ToolG import ToolG as TG
from Loader import Loader as Loader
from ClusteringViewer import ClusteringViewer
from NoiseReduction import NoiseReduction
from SimMat import SimMat
from Lists import Lists
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
        "sim":False,#True,#是否简化计算流程 #简化流程后只计算直接可见度，不计算间接可见度
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
  #5.间接可见度
  def mul(self,a,b):
    a=np.array(a)
    b=np.array(b)
    return np.matmul(a, b)
  #6.计算资源加载列表
  #7.缩小误差
    
  def start(self,step):
    print("起始步骤：",step)
    print("opt")
    for i in self.opt:
        print("  "+i+":",self.opt[i])
    import time as t
    t0=t.time()
    print('1.直接可见度')#第一步必须要执行
    nameList0,d0_,t1=Loader(self.opt).result
    print("2.去除冗余")
    d0,nameList,redunList,t2=ClusteringViewer(d0_,nameList0,self.opt).result
    print('3.获取特征')
    e,t3=NoiseReduction(self.opt,d0).result#进行降维去噪
    print('4.相关矩阵')
    if not self.opt["sim"]:#不计算间接可见度时不需要相关矩阵
     s,t4=SimMat(self.opt,e).result#SimMat().getSimMat(e)#self.getSimMat(e)#
    print('5.间接可见度')
    t5_=t.time()
    if not self.opt["sim"]:#不计算间接可见度
     if step>5:
        d1=T.r(self.opt["out5"])
     else:
        d1=self.mul(d0,s)#一次间接可见度
        T.w(d1,self.opt["out5"])
    t5=t.time()
    print("step5.执行时间："+str(((t5-t5_)/60))+" min")
    print('6.计算资源加载列表')
    if self.opt["sim"]:
        ls1,t6=Lists(self.opt,d0,d1,redunList,nameList).result
    else:
        ls1,nameList,t6=Lists(self.opt,d0,d1,redunList,nameList).result
    print('7.缩小误差')
    ReduceError(self.opt,d0_,nameList0,ls1,nameList).result#self.reduceError(d0_,nameList0,ls1,nameList)

    print("finish!")
    tl=t.time()
    print("step1.执行时间："+str((t1/60/1000))+" min")
    print("step2.执行时间："+str((t2/60/1000))+" min")
    print("step3.执行时间："+str((t3/60/1000))+" min")
    print("step4.执行时间："+str((t4/60/1000))+" min")
    print("step5.执行时间："+str((t5/60/1000))+" min")
    print("step6.执行时间："+str((t6/60/1000))+" min")
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
