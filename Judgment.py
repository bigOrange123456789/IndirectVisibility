import sys
sys.path.append("b_analysis")
from Main import Main as IndirectVisibility
class Judgment:
    def __init__(self):
        self.flagNumber=1
    def judgment(self,tag,config,result):
        IndirectVisibility.remove("out")
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
    for useGPU in ["GPU","noGPU"]:
        for sim in ["计算间接可见度","不算间接可见度"]:
            jud.judgment(
                "以8个视点的中心为新的视点("+useGPU+","+sim+")",
                {
                    "in":"in/test_sort",
                    "sim":sim=="计算间接可见度",
                    "step":1,
                    "step_component":1,
                    "startNow":True,
                    "useGPU":useGPU=="GPU",
                    "CentralVisibility":True
                },
                {
                    "0.5,0.5,0.5":[2,0,3,1,5,4]
                })
    