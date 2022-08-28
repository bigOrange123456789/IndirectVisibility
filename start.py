import time as t
import sys
sys.path.append("src_py")
from Check import Check
from Loader import Loader  #1.直接可见度
from ClusteringViewer import ClusteringViewer  #2.去除冗余视点
from ClusteringComponent import ClusteringComponent
from NoiseReduction import NoiseReduction  #3.获取特征,通过特征矩阵进行降噪
from SimMat import SimMat
from Lists import Lists
from Mul import Mul
from ReduceError import ReduceError

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
        "out2.groups_arr":"./out/2.groups_arr",
        "groups_outEachStep":False,#是否输出距离过程中每一次迭代的结果
        "out2.nameList":"./out/2.nameList",
        "step":2,#聚类个数的步长
        "step_component":1,#构件聚类个数的步长
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
        'startNow':False,#是否在对象初始化阶段执行start()方法
        }
      for i in opt:
          self.opt[i]=opt[i]
      if self.opt['startNow']==True:
        self.start()
  def process(self,d0,d0_,nameList0,nameList,redunList):
    print('3.获取特征,通过特征矩阵进行降噪')
    e,t3=NoiseReduction(self.opt,d0).result#进行降维去噪
    print('4.相关矩阵')
    s,t4=SimMat(self.opt,e).result#SimMat().getSimMat(e)#self.getSimMat(e)#
    print('5.间接可见度')
    d1,t5=Mul(self.opt,d0,s).result
    print('6.计算资源加载列表')
    ls,ls1,ls2,nameList,t6=Lists(self.opt,d0,d1,redunList,nameList).result
    print('7.缩小误差')
    ReduceError(self.opt,d0_,nameList0,ls1,nameList).result#self.reduceError(d0_,nameList0,ls1,nameList)

    print("step3.执行时间："+str((t3/60/1000))+" min")
    print("step4.执行时间："+str((t4/60/1000))+" min")
    print("step5.执行时间："+str((t5/60/1000))+" min")
    print("step6.执行时间："+str((t6/60/1000))+" min")

    return ls

  def start(self):
    t0=t.time()
    print("opt")
    for i in self.opt:
        print("  "+i+":",self.opt[i])
    Check(self.opt)
    print('1.直接可见度')#第一步必须要执行
    nameList0,d0_,t1=Loader(self.opt).result
    print("2.去除冗余")
    d0_,groups_arr=ClusteringComponent(d0_,self.opt).result
    d0,nameList,redunList,t2=ClusteringViewer(d0_,nameList0,self.opt).result
    
    if self.opt["multidirectionalSampling"]:
      ls=self.process(d0,d0_,nameList0,nameList,redunList)
    else:
      ls=self.process(d0,d0_,nameList0,nameList,redunList)

    print("finish!")
    tl=t.time()
    print("step1.执行时间："+str((t1/60/1000))+" min")
    print("step2.执行时间："+str((t2/60/1000))+" min")
    print("总执行时间："+str(((tl-t0)/60))+" min")
    #以下代码用于测试中的断言
    self.ls={}
    for i in range(len(nameList)):
      self.ls[nameList[i]]=ls[i]
if __name__ == "__main__":#用于测试
    print('version:2022.08.28-1')
    # iv=IndirectVisibility({"in":"in/test"})
    iv=IndirectVisibility({"in":"in/test_component2_multidirection"})
    iv.opt["sim"]=False#True#
    iv.opt["step"]=1
    iv.opt["useGPU"]=False
    iv.opt["step_component"]=2
    iv.opt["groups_outEachStep"]=True
    iv.opt["multidirectionalSampling"]=True
    iv.start()
if False:#用于测试
    print('version:2022.08.28-1')
    # iv=IndirectVisibility({"in":"in/test"})
    iv=IndirectVisibility({"in":"in/test_component"})
    iv.opt["sim"]=False#True#
    iv.opt["step"]=1
    iv.opt["useGPU"]=False
    iv.opt["step_component"]=2
    iv.opt["groups_outEachStep"]=True
    iv.start()
