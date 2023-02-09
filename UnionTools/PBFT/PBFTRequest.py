import time

class BaseRequest():
    def __init__(self, req_type) -> None:
        self.param_dict = {}
        self.req_type = req_type


    def to_string(self):
        self.convert_into_dict()
        return str(self.param_dict)
    
    
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
        

class Request(BaseRequest):
    def __init__(self, timestamp, operation, client_id, msg) -> None:
        super(BaseRequest, self).__init__('Request')
        self.timestamp = timestamp
        self.operation = operation
        self.client_id = client_id
        self.msg = msg.encode('UTF-8')
        self.param_list = ['timestamp', 'operation', 'client_id', 'msg']

    @classmethod
    def clean_init(cls):
        return cls(None, None, None, None)


    def set_digest(self, digest):
        self.digest = digest


class Pre_Prepare(BaseRequest):
    def __init__(self, v, n, d) -> None:
        super(BaseRequest, self).__init__('Pre-Prepare')
        self.v = v # 视图编号view number
        self.n = n # 消息序号 msg num
        self.d = d # 签名 digest
        self.param_list = ['v', 'n', 'd']
    
    @classmethod
    def clean_init(cls):
        return cls(None, None, None)

class Prepare(BaseRequest):
    def __init__(self, v, n, d, i)-> None:
        super(BaseRequest, self).__init__('Prepare')
        self.v = v # 视图编号 view num
        self.n = n # 消息序号 msg num
        self.d = d # 签名 digest
        self.i = i # 当前副本节点编号 node num
        self.param_list = ['v', 'n', 'd', 'i']
    
    @classmethod
    def clean_init(cls):
        return cls(None, None, None, None)

class Commit(BaseRequest):
    def __init__(self, v, n, d, i)-> None:
        super(BaseRequest, self).__init__('Commit')
        self.v = v # 视图编号 view num
        self.n = n # 消息序号 msg num
        self.d = d # 签名 digest
        self.i = i # 当前副本节点编号 node num
        self.param_list = ['v', 'n', 'd', 'i']
    
    @classmethod
    def clean_init(cls):
        return cls(None, None, None, None)

class Reply(BaseRequest):
    def __init__(self, v, c, i, r) -> None:
        super(BaseRequest, self).__init__('Reply')
        self.v = v
        self.t = time.time()
        self.c = c # 发出请求的客户端id
        self.i = i
        self.r = r # reply
        self.param_list = ['v', 't', 'c', 'i', 'r']
    
    @classmethod
    def clean_init(cls):
        return cls(None, None, None, None)
    

class CheckPoint(BaseRequest):
    def __init__(self, n, d, i) -> None:
        super(BaseRequest, self).__init__('CheckPoint')
        self.n = n
        self.d = d
        self.i = i
        self.param_list = ['n','d','i']
    
    @classmethod
    def clean_init(cls):
        return cls(None, None, None)
    

class ViewChange(BaseRequest):
    def __init__(self, v, n, C, P, i) -> None:
        super(BaseRequest).__init__('ViewChange')
        self.v = v + 1
        self.n = n
        self.C = C # 2f+1验证过的CheckPoint消息集合
        self.P = P # 当前副本节点未完成的请求的PRE-PREPARE和PREPARE消息集合
        self.i = i
        self.param_list = ['v', 'n', 'C', 'P', 'i']
    
    @classmethod
    def clean_init(cls):
        return cls(None, None, None, None, None)