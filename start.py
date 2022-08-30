import sys
sys.path.append("src_py")
from Main import Main as IndirectVisibility

if False:# if __name__ == "__main__":#用于测试
    print('version:2022.08.28-1')
    # iv=IndirectVisibility({"in":"in/test"})
    iv=IndirectVisibility({"in":"in/test_sort"})
    iv.remove("out")
    iv.opt0["sim"]=False#True#
    iv.opt0["step"]=1
    iv.opt0["useGPU"]=False
    iv.opt0["step_component"]=1
    iv.opt0["groups_outEachStep"]=True
    iv.opt0["CentralVisibility"]=True
    iv.start()
if __name__ == "__main__":#用于测试
    print('version:2022.08.28-1')
    # iv=IndirectVisibility({"in":"in/test"})
    iv=IndirectVisibility({"in":"in/test_component2_multidirection"})
    iv.remove("out")
    iv.opt0["sim"]=False#True#
    iv.opt0["step"]=1
    iv.opt0["useGPU"]=False
    iv.opt0["step_component"]=2
    iv.opt0["groups_outEachStep"]=True
    iv.opt0["multidirectionalSampling"]=True
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
