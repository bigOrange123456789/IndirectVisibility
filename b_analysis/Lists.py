import os
from lib.Tool import Tool as T
from lib.ToolG import ToolG as TG
import numpy as np
class Lists:
  def __init__(self,opt,d0,d1,redunList,nameList):
    import time as t
    t0=t.time()
    self.opt=opt
    if self.opt["sim"]:#不计算间接可见度
        if os.path.exists(self.opt["out6"]):
            ls,nameList=T.r2(self.opt["out6"])
        else:
            ls=self.getLists_sim(d0)
            T.w2(ls,self.opt["out6"],nameList)
        ls1=ls
        ls2=[]
    else:
        if os.path.exists(self.opt["out6"]) and os.path.exists(self.opt["out6_i"]):
            ls,nameList=T.r2(self.opt["out6"])
            ls1,anonymous=T.r2(self.opt["out6_d"])
        else:
            ls,ls1,ls2=self.getLists(d0,d1)
            ls,ls1,ls2,nameList=self.addRedunList(ls,ls1,ls2,nameList,redunList)#ls,ls1,ls2,nameList
            T.w2(ls,self.opt["out6"],nameList)
            T.w2(ls2,self.opt["out6_i"],nameList)
    self.result=[ls,ls1,ls2,nameList,t.time()-t0]
    print("step6.执行时间："+str((t.time()-t0)/60)+" min")
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
        def sort(arr):
            keys=[]
            values=[]
            for index in range(len(arr)):
                if arr[index]>0:
                    keys.append(index)
                    values.append(arr[index])
            if len(keys)==0:
                return []
            index2=np.argsort(-np.array(values))
            return np.array(keys)[index2].tolist()
        for i in range(len(d0)):#对每一行进行排序
            print("sort",i,"/",len(d0),"\t\t\t",end="\r")
            list_d=sort(d0[i])
            lists_d.append(list_d)
        print()
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
  
if __name__ == "__main__":#用于测试
    print()