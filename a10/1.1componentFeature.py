print("获取所有构件的可见特征")
import numpy as np
import json
import os
import math
import time as t

jsonPathErr=[]#记录错误的路径
def loadJson(path):
   import json
   return json.load(open(path))
def getJson(path):
    try:
        return json.load(
            open(path,"r")
        )
    except Exception as e:
        print("无法解析的json文件:",path,e)
        jsonPathErr.append(path)#exit(0)
def isNull(path):
    if os.path.getsize(path)==0:
        print("空文件:",path)
        jsonPathErr.append(path)#exit(0)
def saveJson(path,data):
    json.dump(
        data,
        open(path,"w")
    )
class Traverse:
    def __init__(self,path_pre):
        self.path_pre=path_pre
        self.config=getJson(self.path_pre+"/config.json")
        # self.run()
    def getName(self,i1,i2,i3):
        config=self.config
        min=config["min"]
        step=config["step"]
        max=config["max"]
        x0=min[0]+(max[0]-min[0])*i1/step[0]
        y0=min[1]+(max[1]-min[1])*i2/step[1]
        z0=min[2]+(max[2]-min[2])*i3/step[2]
        if math.floor(x0)==x0:x0=int(x0)
        if math.floor(y0)==y0:y0=int(y0)
        if math.floor(z0)==z0:z0=int(z0)
        return str(x0)+","+str(y0)+","+str(z0)
    
    def run0(self):
        config=self.config#def check(config):
        step=config["step"]
        for i1 in range(step[0]+1):
            print(i1,"\t",step[0]+1,end="\r")
            for i2 in range(step[1]+1):
                for i3 in range(step[2]+1):
                    path=self.path_pre+"/"+self.getName(i1,i2,i3)+".json"
                    self.fun0(path)
    def fun0(self,path):#输出 print功能
        print(getJson(path))
    
    def run05(self):
        print("输出第一个文件名称")
        config=self.config#def check(config):
        step=config["step"]
        for i1 in range(step[0]+1):
            print(i1,"\t",step[0]+1,end="\r")
            for i2 in range(step[1]+1):
                for i3 in range(step[2]+1):
                    path=self.path_pre+"/"+self.getName(i1,i2,i3)+".json"
                    print("第一个文件的路径为:",path)
                    exit(0)

    def run1(self):#获取当前视点下可见构件的最大编号
        print("获取当前视点下可见构件的最大编号")
        indexMax=-1
        config=self.config#def check(config):
        step=config["step"]
        for i1 in range(step[0]+1):
            print(i1,"\t",step[0]+1,end="\r")
            for i2 in range(step[1]+1):
                for i3 in range(step[2]+1):
                    path=self.path_pre+"/"+self.getName(i1,i2,i3)+".json"
                    index=self.fun1(path)
                    if index>indexMax:indexMax=index
        return indexMax
    def fun1(self,path):
        data=getJson(path)
        component_maxIndex=-1#sys.maxsize * -1  #  min_int 
        for direction in data:
            for index in data[direction]:
                if int(index)>component_maxIndex:
                    component_maxIndex=int(index)
        return component_maxIndex
    
    def run2(self,component0_index):#获取某个构件的可见特征
        self.featureTemp=[]
        config=self.config#def check(config):
        step=config["step"]
        for i1 in range(step[0]+1):
            for i2 in range(step[1]+1):
                for i3 in range(step[2]+1):
                    path=self.path_pre+"/"+self.getName(i1,i2,i3)+".json"
                    self.fun2(path,component0_index)
        self.w(
            component0_index,
            self.featureTemp
            )
        return self.featureTemp
    def fun2(self,path,component0_index):#获取某个构件的可见特征
        data=getJson(path)
        for direction in data:
            d=data[direction]
            if str(component0_index) in d:
                self.featureTemp.append(d[str(component0_index)])
            else :
                self.featureTemp.append(0)
            # print("component0_index",component0_index)
            # print("path",path)
            # print("direction",direction)
            # print("component0_index in d",component0_index in d)
            # print("str(component0_index) in d",str(component0_index) in d)
            # # print("d[component0_index]",d[component0_index])
            # print("self.featureTemp",self.featureTemp)
            # exit(0)
    
    def w(self,id,data):#path='data.npy'
        path=self.path_pre+"/../npy_component_feature/"
        np.save(
            path+str(id)+".npy",
            np.array(data)
        )# 将数据保存为.npy文件
        # print("特征的保存位置是：",str(id)+".npy")
        # np.save(
        #     str(id)+".npy",
        #     np.array(data)
        # )# 将数据保存为.npy文件
    def r(self,id):# 读取.npy文件
        path=self.path_pre+"/../npy_component_feature/"
        return np.load(path+str(id)+'.npy').tolist()

import sys
if __name__ == "__main__":#用于测试
    if len(sys.argv)<2:
        print("ERR:请指定config.json的路径")
        exit(0)
    path=sys.argv[1]
    config=loadJson(path)
    path_pre=config["in_temp"]
    traverse=Traverse(path_pre)

    print("获取最大的构件编号")
    maxindex=799  # traverse.run1()

    print("获取所有构件的特征")
    for index0 in range(maxindex+1):
        print(index0,"\t",maxindex+1,end="\r")
        traverse.run2(index0)

    # data=np.load('23.npy').tolist()
    # print("开始检索")
    # sum=0
    # for i in range(len(data)):
    #     sum=sum+data[i]
    #     if not data[i]==0:
    #         print("i",i)
    # print("完成检索")
    # print("sum",sum)
    # print("len(data)",len(data))
    # print(data[0])

    # feature=[1,2,3,1,2,4]
    # traverse.w(0,feature)
    # print(traverse.r(0))
    
    # print("正在获取构件23的可见特征")
    # feature =traverse.run2(23)
    # print("可见特征为",feature)
    # feature =traverse.r(23)
    # print("feature[0]",feature[0])
