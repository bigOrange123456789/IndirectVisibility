import time as t

from Check import Check
from Loader import Loader  #1.直接可见度
from CentralVisibility import CentralVisibility  
from ClusteringViewer import ClusteringViewer  #2.去除冗余视点
from ClusteringComponent import ClusteringComponent
from NoiseReduction import NoiseReduction  #3.获取特征,通过特征矩阵进行降噪
from SimMat import SimMat
from Lists import Lists
from List2Arr import List2Arr
from Mul import Mul
from ReduceError import ReduceError

class Main:
  @staticmethod
  def mkdir(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path) 
  def optSet(self,out):
    self.mkdir(out)
    self.opt={
        "in":"./in",
        "out.config2":"./"+out+"/config2",#直接可见度矩阵，txt
        "out.ClusteringComponent.groups_arr":"./"+out+"/ClusteringComponent.groups_arr",#元素聚类后的分组情况
        "out.ClusteringComponent.d0":"./"+out+"/ClusteringComponent.d0",
        "out1":"./"+out+"/1.direct",#直接可见度矩阵，txt
        "CentralVisibility":False,#以8个视点的中心为新的视点
        "out2":"./"+out+"/2.redunList.json",#冗余视点列表
        "out2.d0":"./"+out+"/2.d0",
        "out2.groups_arr":"./"+out+"/2.groups_arr",
        "groups_outEachStep":False,#是否输出距离过程中每一次迭代的结果
        "out2.nameList":"./"+out+"/2.nameList",
        "step":2,#聚类个数的步长
        "step_component":1,#构件聚类个数的步长
        "useGPU":True,#是否使用GPU
        "out3":"./"+out+"/3.e",#特征矩阵，txt
        "out4":"./"+out+"/4.simMat",#视觉相关度矩阵，txt
        "out5":"./"+out+"/5.d1",#间接相关度矩阵，txt
        "out6":"./"+out+"/6.ls",#资源加载列表，txt.json
        "out6_d":"./"+out+"/6.ls_d",#资源加载列表，txt.json
        "sim":False,#True,#是否简化计算流程 #简化流程后只计算直接可见度，不计算间接可见度
        "out6_i":"./"+out+"/6.ls_i",#资源加载列表，txt.json
        "out7_d":"./"+out+"/7.ls_d",
        "out7_d_arr":"./"+out+"/7.ls_d_arr",
        "out7_d_index":"./"+out+"/7.ls_d_index",
        "areaMin":0,#构件的投影面积小于这个数值视为不可见 #在ReduceError.py中发挥作用
        "multidirectionalSampling":False,#True,#False,#True,#不同方向的采样结果分开存储
        'startNow':False,#是否在对象初始化阶段执行start()方法
        }
    for i in self.opt0:
      self.opt[i]=self.opt0[i]
  def __init__(self,opt):
      self.opt0=opt
      self.optSet("out")
      if self.opt['startNow']==True:
        self.start()
  def process(self,d0_,nameList0):
    print("2.去除冗余(视点)")
    d0,nameList,redunList,t2=ClusteringViewer(d0_,nameList0,self.opt).result
    print('3.获取特征,通过特征矩阵进行降噪')
    e,t3=NoiseReduction(self.opt,d0).result#进行降维去噪
    if self.opt["sim"]:#简化版只计算直接可见度，不计算间接可见度
      d1=[]#简化版中后面不会用到间接可见度
    else:
      print('4.相关矩阵')
      s,t4=SimMat(self.opt,e).result#SimMat().getSimMat(e)#self.getSimMat(e)#
      print('5.间接可见度')
      d1,t5=Mul(self.opt,d0,s).result
      
    print('6.计算资源加载列表')
    ls,ls1,ls2,nameList,t6=Lists(self.opt,d0,d1,redunList,nameList).result
    ls1_arr,ls1_index=List2Arr(self.opt,ls1,nameList).result
    print('7.缩小误差')
    ls1,t7=ReduceError(self.opt,d0_,nameList0,ls1,nameList).result#self.reduceError(d0_,nameList0,ls1,nameList)
    print("step2.执行时间："+str((t2/60/1000))+" min")
    print("step3.执行时间："+str((t3/60/1000))+" min")
    print("step6.执行时间："+str((t6/60/1000))+" min")
    self.nameList=nameList#用于测试中的断言
    return ls#用于测试中的断言
  def start(self):
    self.optSet("out")
    t0=t.time()
    print("opt")
    for i in self.opt:
        print("  "+i+":",self.opt[i])
    Check(self.opt)
    print('1.直接可见度')#第一步必须要执行
    loader=Loader(self.opt)
    nameList0_old,d0_,t1=loader.result
    nameList0,d0_=CentralVisibility(self.opt,nameList0_old,d0_).result
    # exit(0)
    print("2.去除冗余(构件)")
    d0_,groups_arr=ClusteringComponent(d0_,self.opt).result
    #如果是多方向采样下面的计算过程中不需要d0_ #print(groups_arr)
    if self.opt["multidirectionalSampling"]:
      self.opt0["out.config2"]=self.opt["out.config2"]#config2的存储位置不变
      for direct in loader.dataSplit:
        data0=loader.dataSplit[direct]#某个方向上的数据
        d0_=loader.directSplit(data0,groups_arr)#每个方向单独计算直接可见度
        nameList0,d0_=CentralVisibility(self.opt,nameList0_old,d0_).result#[nameList0,d0_]似乎是残缺的
        self.optSet("out"+direct)
        ls=self.process(d0_,nameList0)
    else:
      ls=self.process(d0_,nameList0)
    print("finish!")
    tl=t.time()
    print("step1.执行时间："+str((t1/60/1000))+" min")
    print("总执行时间："+str(((tl-t0)/60))+" min")
    #以下代码用于测试中的断言
    self.ls={}
    for i in range(len(self.nameList)):
      self.ls[self.nameList[i]]=ls[i]
  @staticmethod
  def remove(dir_path):
        import os
        if not os.path.exists(dir_path):
            return
        if os.path.isfile(dir_path):
            try:
                os.remove(dir_path) # 这个可以删除单个文件，不能删除文件夹
            except BaseException as e:
                print(e)
        elif os.path.isdir(dir_path):
            file_lis = os.listdir(dir_path)
            for file_name in file_lis:
                # if file_name != 'wibot.log':
                tf = os.path.join(dir_path, file_name)
                Main.remove(tf)
if __name__ == "__main__":#用于测试
    print()