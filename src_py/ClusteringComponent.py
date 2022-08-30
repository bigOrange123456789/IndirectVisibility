import numpy as np
import os
from lib.Tool import Tool as T
from lib.Clustering import Clustering
class ClusteringComponent:
  def __init__(self,d0_,opt):
    self.opt=opt
    if os.path.exists(self.opt["out.ClusteringComponent.groups_arr"]+".json") :
      groups_arr=T.loadJson(self.opt["out.ClusteringComponent.groups_arr"]+".json")
      if self.opt["multidirectionalSampling"]:
        d0=[]
      else:
        d0=T.loadJson(self.opt["out.ClusteringComponent.d0"]+".json")
    else:
      d0,groups_arr=self.clustering(
          d0_,
          self.opt["step_component"]
      )
      T.saveJson(self.opt["out.ClusteringComponent.groups_arr"]+".json",groups_arr)
      T.saveJson(self.opt["out.ClusteringComponent.d0"]+".json",d0)
    self.result=[d0,groups_arr]#d0,nameList,redunList

  def clustering(self,dataSet,step):
    if step==1:#如果步长为1就不进行冗余去除
        return dataSet,[]
    dataSet=np.array(dataSet).T.tolist()
    if self.opt["groups_outEachStep"]:
      clustering=Clustering(self.opt)
      centroids, clustAssing, clusterChanged =clustering.kMeans_one(dataSet,step)
      group_index=0
      while clusterChanged:
        centroids, clustAssing, clusterChanged =clustering.kMeans_next()
        group_index=group_index+1
        groups_arr=self.get_groups_arr(clustAssing.tolist())
        T.saveJson(self.opt["out2.groups_arr"]+str(group_index)+".json",groups_arr)
      dataSet=centroids.T.tolist()
      clustAssing=clustAssing.tolist()
    else:
      centroids, clustAssing = Clustering(self.opt).kMeans(dataSet,step)#聚类#centroids:质心位置, clustAssing:每个元素对应的质心及到质心的距离
      dataSet=np.array(centroids).T.tolist()

      groups_arr=self.get_groups_arr(clustAssing)
      T.saveJson(self.opt["out2.groups_arr"]+".json",groups_arr)
    return dataSet, groups_arr
  def get_groups_arr(self,clustAssing):
    groups_arr=[]
    groupId_max=-1
    for i in range(len(clustAssing)):
        groupId=int(clustAssing[i][0])
        if groupId_max<groupId:
            groupId_max=groupId
    for i in range(groupId_max+1):
        groups_arr.append([])
    for i in range(len(clustAssing)):
        groupId=int(clustAssing[i][0])
        groups_arr[groupId].append(i)
    return groups_arr

if __name__ == "__main__":#用于测试
    print()