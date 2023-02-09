from ecdsa import SECP256k1, util,  ellipticcurve
import random 

fail_pow = 50

g_curve = SECP256k1
def generate_random_str(randomlength):
    """
    生成一个指定长度的随机字符串
    """
    random_str =''
    base_str = 'ABCDEFabcdef0123456789'
    length =len(base_str) -1
    for i in range(randomlength):
        random_str +=base_str[random.randint(0, length)]
    return random_str


def encode_msg_point(msg, curve, fail_pow):
    m = msg*fail_pow
    for j in range(fail_pow):
        m_ = m + j
        y_2 = (pow(m_, 3, curve.p()) + curve.a()*m_ + curve.b())%curve.p()
        y = pow(y_2,(curve.p()+1)//4,curve.p())

        if pow(y,2,curve.p()) == y_2:
            return m_, int(y)
    
    raise Exception("Encode Curve Failed")

def decode_msg_curve(msg):
    return int(msg)//fail_pow

def ex_prepare(curve, G, K):
    pass
    # 将公钥组寄给对方

def encrypt_data(msg, curve, K, fail_pow):
    msg_int = util.string_to_number(bytes(msg,'utf-8'))
    x,y =encode_msg_point(msg_int, curve.curve, fail_pow)
    msg_point = ellipticcurve.Point(curve=curve.curve, x=x, y=y)
    M = msg_point
    rand_num = util.randrange(curve.order, None)
    # 加密
    C2 = rand_num*curve.curve.generator
    temp = K*rand_num
    C1 = M + temp
    return C1, C2

def decrypt_data(C1, C2, k, curve):
    temp = -k*C2
    M_ = C1 + temp
    msg = util.number_to_string(decode_msg_curve(M_.x(), fail_pow), curve.order)
    return msg

'''
#generator is G
secexp = util.randrange(g_curve.order, None)
#SigningKey.from_secret_exponent(secexp, NIST521p, sha1)
#pri_key = eddsa.PrivateKey(NIST521p.generator, rand_num)
pub_point = g_curve.generator * secexp
pub_key = VerifyingKey.from_public_point(pub_point, curve=g_curve, hashfunc=sha1)
pri_key = ecd.Private_key(public_key=pub_key, secret_multiplier=secexp)
pri_key.order = g_curve.order
#print(pri_key.secret_multiplier, pub_key.to_string())
K = pub_point
G = g_curve.generator
#verifying_key = VerifyingKey.from_string(pub_key.public_key(), curve=NIST521p)

base_len = (cp.bit_length(g_curve.curve.p()) + 1 + 7) // 8
msg = generate_random_str(randomlength=16)

print(msg)
print(msg_int)
#print(util.string_to_number(msg.encode()))
#msg = binascii.b2a_hex(util.number_to_string(msg, NIST521p.order))
#print(msg)

print(x,y)

de_msg = decode_msg_curve(x)

M = msg_point
rand_num = util.randrange(g_curve.order, None)
# 加密
C2 = rand_num*g_curve.generator
temp = K*rand_num
C1 = M + temp
# 解密
temp = -rand_num*secexp*g_curve.generator
M_ = C1 + temp
msg_ex = M.x()
msg_rev = M_.x()
msg_ex = util.number_to_string(decode_msg_curve(msg_ex), g_curve.order)
msg_rev = util.number_to_string(decode_msg_curve(msg_rev), g_curve.order)
print(msg_ex.decode('utf-8'), msg_rev.decode('utf-8'))
'''





