from ecdsa import SECP256k1, VerifyingKey, ellipticcurve
import utils.Encrypt as Encrypt
import requests
import json

class ContrastMgr():
    def __init__(self, id, secexp, pri_key, pub_point) -> None:
        self.id = id
        self.secexp = secexp
        self.private_key = pri_key
        self.pub_point = pub_point
        self.fail_pow = 50
        self.msg = None
    
    
    def propose_deal(self, contrast_content, ex_host):
        self.set_request(contrast_content)
        info = self.resolve_res(self.exchange_pubkey(ex_host, self.id))
        res = self.propose_contrasct_msg(info, ex_host)
        if self.res_valid(res) is False:
            raise Exception("发起合同失败")
        info = self.resolve_res(res)
        self.verify_contrast(info)
    

    def agree_deal(self, infos, contrast_content):
        if infos['content']['contrast'] != contrast_content:
            raise Exception("收到合同与原合同不符！！请谨慎确认合同内容！")
        
        if self.verify_contrast(infos) is False:
            raise Exception("对方签名无效！请谨慎确认合同内容和对方身份！")
        
        res = self.agree_contrast(infos)
        if self.res_valid(res) is False:
            raise Exception("合同签订失败！")
        return True


    def resolve_res(self, res):
        return json.dumps(res.text, ensure_ascii=False)
        


    def res_valid(self, res):
        if res.status_code != 200:
            return False
        return True


    def set_request(self, request):
        self.msg = request
    

    def sign_contrast(self): # 加密摘要————签名
        signature = self.private_key.sign(str(self.msg).encode("utf8"))
        return  signature
    

    def propose_contrasct_msg(self, recver_pubkey, recver):# 发起一个合约并发送给对方
        recver_pub = ellipticcurve.Point(curve=SECP256k1.curve, x=recver_pubkey.x, y=recver_pubkey.y)
        msg_encrypt_C1, msg_encrypt_C2 = Encrypt.encrypt_data(self.msg, curve=SECP256k1, K=recver_pub, fail_pow=recver_pubkey.fail_pow)
        msg_sig = self.sign_contrast()
        info={'from':self.id, 'signature':msg_sig, 'content':{'C1':msg_encrypt_C1, 'C2':msg_encrypt_C2, 'contrast':self.msg}, 'public_key':self.pub_point}
        try:
            return self.send(info, recver, "/SignContrast")
        except:
            raise Exception("发送错误")

    
    def agree_contrast(self, info):
        proposer_pubkey = info['publick_key']
        proposer_id = info['from']
        proposer_signature = info['signature']
        proposer_pub_point = ellipticcurve.Point(curve=SECP256k1.curve, x=proposer_pubkey.x, y=proposer_pubkey.y)
        vk = VerifyingKey.from_public_point(proposer_pub_point, SECP256k1)
        C1 = info['content']['C1']
        C2 = info['content']['C2']
        msg = Encrypt.decrypt_data(C1=C1, C2=C2, k=self.secexp, curve=SECP256k1)
        if vk.verify(proposer_signature,msg) is False:
            raise Exception("对方签名无效")
        self.msg.msg = msg
        msg_encrypt_C1, msg_encrypt_C2 = Encrypt.encrypt_data(self.msg, curve=SECP256k1, K=proposer_pub_point, fail_pow=self.fail_pow)
        msg_sig = self.sign_contrast()
        info={'from':self.id, 'signature':msg_sig, 'content':{'C1':msg_encrypt_C1, 'C2':msg_encrypt_C2}, 'public_key':self.pub_point}
        try:
            return self.send(info, proposer_id,"/SignContrast")
        except:
            raise Exception("send error")
        

    def verify_contrast(self, info):
        agreer_pubkey = info['publick_key']
        agreer_signature = info['signature']
        agreer_pub_point = ellipticcurve.Point(curve=SECP256k1.curve, x=agreer_pubkey.x, y=agreer_pubkey.y)
        vk = VerifyingKey.from_public_point(agreer_pub_point, SECP256k1)
        C1 = info['content']['C1']
        C2 = info['content']['C2']
        msg = Encrypt.decrypt_data(C1=C1, C2=C2, k=self.secexp, curve=SECP256k1)
        if vk.verify(agreer_signature,msg) is False:
            raise Exception("对方签名无效")
        return True


    def send_pubkey(self, remote_host, host): # 发送公钥
        info = {'id':host,'pubkey_x':self.pub_point.x, 'pubkey_y':self.pub_point.y}
        try:
            res = self.send(remote_host,info,url="/recvpubKey")
            if res.status_code != 200:
                raise Exception("发送公钥失败 错误码:"+str(res.status_code))
            return res
        except:
            raise Exception("发送公钥失败")

    def recv_pubkey(self, info):
        client_id = info['id']
        if client_id in self.client_ids:
            res = {'id':client_id, 'pubkey_x':info['pubkey_x'], 'pubkey_y':info['pubkey_y']}
            return res 
        else:
            res = {'code':1,'msg':'不是组内节点'}
            return res
    

    def send(self, host, info, url):
        url=host+url
        res = requests.post(url=url, data=info)
        return res