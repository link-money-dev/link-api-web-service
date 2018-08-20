#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import random
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES
import constant as CONSTANT

def generate_random_key_pair(lenth=16):
    raw=list('`1234567890-=][poiuytrewqasdfghjkl;.,mnbvcxz~!@#$%^&*()_+}{POIUYTREWQASDFGHJKL:"?><MNBVCXZ')
    nums=list('0123456789')
    lenth_raw = len(raw)
    iv=[]
    result=[]
    for i in range(lenth):
        postion_raw=random.randint(0,lenth_raw-1)
        postion_iv=random.randint(0,9)
        result.append(raw[postion_raw])
        iv.append(nums[postion_iv])
    key="".join(result)
    iv="".join(iv)
    return (key,iv)

class Prpcrypt():
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        # 补位
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        def hex_to_str(b):
            s = ''
            for i in b:
                s += '{0:0>2}'.format(str(hex(i))[2:])
            return (s)
        text = self.pad(text)
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 目前AES-128 足够目前使用
        ciphertext = cryptor.encrypt(text)
        # 把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return self.unpad(plain_text.rstrip('\0'))


def decrypt(text, key='', iv=''):
    if key=='' or iv=='':
        key,iv=CONSTANT.Constant('test').AES_KEY,CONSTANT.Constant('test').AES_IV
    prp=Prpcrypt(key=key,iv=iv)
    r=prp.decrypt(text).decode()
    return r

if __name__ == '__main__':
    key,iv=('NL(o<`Kb$#Qv^V`U','7965595995737331')
    pc = Prpcrypt(key, iv)  # 初始化密钥 和 iv

    e = pc.encrypt('SCOLXP6MRK2MH3CEIP5XTLP2A5ABK2JC6ACPA5ALED3MTW57H3BHKNQ4')  # 加密
    # assert e=='ad9347236820eadafa523c596d5cfe6d8ecbe0a9df1604841aee110d23441ceb73c3f267141f0b61b30349d11d58cd55624aaa7731981df58c08ef30aed82e38'
    d = pc.decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)
    print("长度:", len(d))
