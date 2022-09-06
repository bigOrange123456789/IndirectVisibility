import time as t
import sys
sys.path.append("src_py")
from Main import Main as IndirectVisibility
if __name__ == "__main__":#用于测试
    print('version:2022.09.05-1')
    iv=IndirectVisibility({
        "in":"1.move_all",
        
        })
    iv.opt0["out.ClusteringComponent.groups_arr"]="groups_arr"
    iv.opt0["sim"]=True
    iv.opt0["step"]=1
    iv.opt0["useGPU"]=False
    iv.opt0["step_component"]=1
    iv.opt0["groups_outEachStep"]=True
    iv.opt0["multidirectionalSampling"]=True
    iv.opt0["CentralVisibility"]=True
    iv.start()

