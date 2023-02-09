from UnionTools.PBFT.Node import Node
from UnionTools.Identity import Identity
from UnionTools.PBFT.PBFTRequest import Request,Pre_Prepare,Prepare,Commit,CheckPoint,ViewChange,Reply
import time

class PBFTSlaveNode(Node):
    def __init__(self, identity: Identity, client_ids) -> None:
        super().__init__(identity, client_ids)
        
    
    def request_stage(self, o, m, main_node): # request 阶段
        t = time.time()
        r_request = Request(t, o, self.identity.id, m)
        r_request.set_digest(self.sign_msg(m))
        msg_digest = self.sign_request(r_request)
        r_request.convert_into_dict()
        info = {'Package':r_request.param_dict,'digest':msg_digest}
        res = self.send_msg(main_node, info, "/requestStage")
        return res
        

