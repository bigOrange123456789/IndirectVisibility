from start import IndirectVisibility
import os
def del_file(path_data):#删除文件夹下面的所有文件(只删除文件,不删除文件夹)
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)
class Judgment:
    def __init__(self):
        self.flagNumber=1
    def remove(self,dir_path):
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
                self.remove(tf)
    def judgment(self,tag,config,result):
        self.remove("out")
        print(str(self.flagNumber)+":开始"+tag)
        self.assert0(
            IndirectVisibility(config).ls,
            result
        )
        print("完成"+tag+"-"+str(self.flagNumber)+"-\n")
        self.flagNumber=self.flagNumber+1
    def assert0(self,a,b):
        assert type(a)==type(b)==type({})
        assert self.lenValues(a)==self.lenValues(b)
        for id in a:
            if not type(a[id])==type(b[id]):
                print(type(a[id]),type(b[id]))
                exit(0)
            if type(a[id])==type([]):
                assert len(a[id])==len(b[id])
                for i in range(len(a[id])):
                    assert a[id][i]==b[id][i]
            else:
                assert a[id]==b[id]
    def lenValues(self,a):
        n=0
        for i in a : n=n+1
        return n
if __name__ == "__main__":#用于测试
    jud=Judgment()
    jud.judgment(
        "检验间接可见度计算",
        {
            "in":"in/test",
            "sim":False,
            "step":1,
            "startNow":True
        },
        {
            "0,0,0":[0,1,2],
            "0,0,1":[2,1,0,3],
            "0,1,0":[3,2,1],
            "0,1,1":[4],
            "1,0,0":[5],
            "1,0,1":[],
            "1,1,0":[],
            "1,1,1":[]
        })
    jud.judgment(
        "验证视点聚类算法",
        {
            "in":"in/test_viewerPoint",
            "sim":False,
            "step":2,
            "startNow":True
        },
        {
            "0,0,0":[0,1,2],
            "0,0,1":[2,1,0,3],
            "0,1,0":[3,2,1],
            "0,1,1":[4],
            "1,0,0":[5],
            "1,0,1":[],
            "1,1,0":"1,0,1",
            "1,1,1":"1,0,1",
            "2,0,0":"0,0,0",
            "2,0,1":"0,0,1",
            "2,1,0":"0,1,0",
            "2,1,1":"0,1,1",
            "3,0,0":"1,0,0",
            "3,0,1":"1,0,1",
            "3,1,0":"1,0,1",
            "3,1,1":"1,0,1"
        })
    for useGPU in ["GPU","noGPU"]:
        for groups_outEachStep in ["输出中间结果","不输出中间结果"]:
            jud.judgment(
                "检验构件分组("+useGPU+","+groups_outEachStep+")",
                {
                    "in":"in/test_component2",
                    "sim":False,
                    "step":1,
                    "step_component":2,
                    "startNow":True,
                    "useGPU":useGPU=="GPU",
                    "groups_outEachStep":groups_outEachStep=="输出中间结果",
                },
                {
                    "0,0,0":[0,1,2],
                    "0,0,1":[2,1,0,3],
                    "0,1,0":[3,2,1],
                    "0,1,1":[4],
                    "1,0,0":[5],
                    "1,0,1":[],
                    "1,1,0":[],
                    "1,1,1":[]
                })
    for useGPU in ["GPU","noGPU"]:
        for sim in ["计算间接可见度","不算间接可见度"]:
            jud.judgment(
                "检验排序("+useGPU+","+sim+")",
                {
                    "in":"in/test_sort",
                    "sim":sim=="计算间接可见度",
                    "step":1,
                    "step_component":1,
                    "startNow":True,
                    "useGPU":useGPU=="GPU"
                },
                {
                    "0,0,0":[2,0,3,1,5,4],
                    "0,0,1":[],
                    "0,1,0":[],
                    "0,1,1":[],
                    "1,0,0":[],
                    "1,0,1":[],
                    "1,1,0":[],
                    "1,1,1":[]
                })
    