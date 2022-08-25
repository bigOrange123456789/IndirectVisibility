import json
class Loading:
   def __init__(self,opt):
    self.opt=opt
    print()
   #1.直接可见度
   def loading(self):
      print("采样集:",self.opt["in"])
      data=[]
      nameList=[]
      import os
      numberAll=len(os.listdir(self.opt["in"]))
      numberIndex=0
      for fileName in os.listdir(self.opt["in"]):
          if fileName=="config.json" or not len(fileName.split(".json"))==2:
              continue
          f1=open(self.opt["in"]+"/"+fileName, encoding='gb18030', errors='ignore')
          j=json.load(f1)
          if self.opt["multidirectionalSampling"]:#分成多个方向分别存储
            j_all={}
            for direct in j:
                for componet_id in j[direct]:
                    j_all[componet_id]=j[direct][componet_id]
            j=j_all
          data.append(j)
          nameList.append(fileName.split(".json")[0])
          numberIndex=numberIndex+1
          print(str(numberIndex)+"/"+str(numberAll),end="\r")
      print()
      return data,nameList
if __name__ == "__main__":#用于测试
    print()