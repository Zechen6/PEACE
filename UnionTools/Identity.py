from ecdsa import util, SECP256k1, VerifyingKey, ellipticcurve, SigningKey
import uuid
import requests
from UnionTools.Contrast.ConstrastMgr import ContrastMgr

class Public_Key():
    def __init__(self, K_x, K_y, G_x, G_y, curve) -> None:
        self.x = K_x
        self.y = K_y
        self.G_x = G_x
        self.G_y = G_y
        self.curve = curve
        self.param_list = {'curve', 'G_y', 'G_x', 'K_y', 'K_x'}
    
    @classmethod
    def clean_init(cls):
        return cls(None, None, None, None, None)
    
    def convert_into_dict(self):
        self.param_dict = {}
        for name in dir(self):
            value = getattr(self, name)
            if name in self.param_list:
                if isinstance(value, str) is False:
                    self.param_dict[name] = str(value)
                else:
                    self.param_dict[name] = value

    def convert_dict2obj(self):
        for name in dir(self):
            value = getattr(self, name)
            if name in self.param_list:
                setattr(self, name, self.param_dict[name])

class Identity():
    def __init__(self, ip) -> None:
        self.leader = False
        self.id = uuid.uuid4()
        id = uuid.uuid1()
        self.secexp = util.string_to_number(id.bytes.replace(b'-',b''))
        self.private_key = SigningKey.from_secret_exponent(self.secexp,curve=SECP256k1)
        pub_point = SECP256k1.generator*self.secexp
        self.pub_point = Public_Key(pub_point.x(), pub_point.y(), SECP256k1.generator.x(), SECP256k1.generator.y(), 'SECP256k1')
        self.fail_pow = 50
        self.contrast_mgr = ContrastMgr(self.id,self.secexp,self.private_key,self.pub_point)
        self.request = None
        self.address = ip
    
    def set_request(self, request):
        self.request = request

    def send(self, host, info, url):
        url=host+url
        res = requests.post(url=url, data=info)
        return res


