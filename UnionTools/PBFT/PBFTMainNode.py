from UnionTools.PBFT.Node import Node
from UnionTools.Identity import Identity
from UnionTools.PBFT.PBFTRequest import Request,Pre_Prepare,Prepare,Commit,CheckPoint,ViewChange,Reply
import time

class PBFTMainNode(Node):
    def __init__(self, identity: Identity, client_ids) -> None:
        super().__init__(identity, client_ids)
    
    def pre_prepare(self, info):
        r_request = Request.clean_init()
        self.resolve_info(r_request, info['Package'])
        msg_digest = info['msg_digest']
        vk = self.pubkey_dict[str(r_request.client_id)]   
         
        if vk.verify(msg_digest, info['Package']) is False:
            raise Exception("客户端签名不正确")
        
        pre_prepare_reqeust = Pre_Prepare()