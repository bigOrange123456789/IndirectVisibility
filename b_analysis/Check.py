import json
import os
import math
from lib.Tool import Tool
class Check:
  def __init__(self,opt):
    self.opt=opt
    self.jsonPathErr=[]
    config=self.getJson(self.opt["in"]+"/config.json")
    self.check(config)
  @staticmethod
  def getJson(path):
    try:
        return json.load(
            open(path,"r")
        )
    except Exception as e:
        print("无法解析的json文件:",path,e)
        # self.jsonPathErr.append(path)#exit(0)
  def isNull(self,path):
    if os.path.getsize(path)==0:
        self.jsonPathErr.append(path)#exit(0)
  @staticmethod
  def getName(config,i1,i2,i3):
    min=config["min"]
    step=config["step"]
    max=config["max"]
    if step[0]==0:
        x0=min[0]
    else:
        x0=min[0]+(max[0]-min[0])*i1/step[0]
    if step[1]==0:
        y0=min[1]
    else:
        y0=min[1]+(max[1]-min[1])*i2/step[1]
    if step[2]==0:
        z0=min[2]
    else:
        z0=min[2]+(max[2]-min[2])*i3/step[2]
    if math.floor(x0)==x0:x0=int(x0)
    if math.floor(y0)==y0:y0=int(y0)
    if math.floor(z0)==z0:z0=int(z0)
    return str(x0)+","+str(y0)+","+str(z0)
  def check(self,config):
    step=config["step"]
    flag_nopath=False
    # print("step",step)
    for i1 in range(step[0]+1):
        print(i1,"\t",step[0]+1,end="\r")
        for i2 in range(step[1]+1):
            for i3 in range(step[2]+1):
                path=self.opt["in"]+"/"+self.getName(config,i1,i2,i3)+".json"
                file_exists=os.path.exists(path)
                if not file_exists:
                    print("文件不存在:",path)
                    flag_nopath=True
                else:
                    self.isNull(path)#data[path]=getJson(path)
    print("已检测完全部构件     ")
    if len(self.jsonPathErr)==0:
        print("没有无法解析的文件")
    else:
        print("error:无法解析的json文件数量为",len(self.jsonPathErr))
        Tool.saveJson("jsonPathErr.json",self.jsonPathErr)
        exit(0)
    if not flag_nopath:
        print("没有缺失的文件")
    else:
        print("error:存在文件缺失")
        exit(0)
if __name__ == "__main__":#用于测试
    print()
