from UnionTools.Identity import Identity, Public_Key
from ecdsa import SECP256k1, VerifyingKey, ellipticcurve
import json

class Node():
    def __init__(self, identity:Identity, client_ids) -> None:
        self.identity = identity
        self.pubkey_dict = {}
        self.ip_dict = self.set_ip_dict(client_ids)
        self.client_ids = client_ids
        self._view_number = -1
        self._h = 0
        self._H = 20

    def broadcast_msg(self, msg, url):
        for client in self.client_ids:
            self.send_msg(self.ip_dict[str(client)], msg, url)
    
    def verify_msg_digest(self, pbft_request, digest, client_id): # 验证签名是否有效
        pub_point = self.pubkey_dict[str(client_id)]
        proposer_pub_point = ellipticcurve.Point(curve=SECP256k1.curve, x=pub_point.x, y=pub_point.y)
        vk = VerifyingKey.from_public_point(proposer_pub_point, SECP256k1)
        if vk.verify(digest, pbft_request.to_string()) is False:
            raise Exception("对方签名无效")
        return True
    

    def sign_request(self, pbft_request): # 给request签名
        return self.sign_msg(pbft_request.to_string())


    def sign_msg(self, msg):
        return self.identity.private_key.sign(msg)


    def send_pubkey(self, remote_host, host): # 发送公钥
        info = {'id':host,'pubkey_x':self.identity.pub_point.x, 'pubkey_y':self.identity.pub_point.y}
        try:
            res = self.send_msg(remote_host,info,url="/recvpubKey")
            if res.status_code != 200:
                raise Exception("发送公钥失败 错误码:"+str(res.status_code))
            return res
        except:
            raise Exception("发送公钥失败")


    def recv_pubkey(self, info):
        client_id = info['id']
        if client_id in self.client_ids:
            self.add_pubkey(info)
        else:
            res = {'code':1,'msg':'不是组内节点'}
            return res
        res = {'code': 0, 'id':self.identity.id,'pubkey_x':self.identity.pub_point.x, 'pubkey_y':self.identity.pub_point.y}
        return res
    

    def exchange_pubkey(self, remote_host):
        res = self.send_pubkey(remote_host, self.id)
        res_dir = json.dump(res.text)
        if res_dir['code'] == 0:
            self.recv_pubkey(res)
        else:
            raise Exception(res_dir['msg'])

    
    def add_pubkey(self, info): # 把别人的密钥加入字典，并用client_id进行索引
        pub_key = Public_Key.clean_init()
        self.resolve_info(pub_key, info)
        for key in info:
            if key == 'client_id' or 'id':
                client_id = info[key]
        self.pubkey_dict[str(client_id)] = pub_key


    def add_client(self, client_id):
        self.client_ids.append(client_id)


    def resolve_info(self, entity, info): # 把字典里的值解析成对象
        for key in info:
            key_index = str(key).lower()
            if key_index in entity.param_dict:
                entity.param_dict[key_index] = info[key]
        entity.convert_dict2obj()


    def send_msg(self, host, msg, url):
        self.identity.send(host, msg, url)

    
    def set_view_number(self,view_number):
        self._view_number = view_number
    
    
    def set_h(self, h):
        self._h = h
    
    
    def set_H(self, H):
        self._H = H
    
    def set_ip_dict(self, client_ids):
        pass