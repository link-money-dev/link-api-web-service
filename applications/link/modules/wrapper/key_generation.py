# -*- coding: UTF-8 -*-

# 本程序生成若干个客户私钥，只要下面的参数KEY和IV不丢失不泄露，理论上是安全的
# 本程序从自己启动，外部只能调用其方法
# 生成的私钥存储在sqlite数据库中
# 本程序的主入口程序为 main()

# 请填写下面几个参数：
# 第一个参数为生成的密钥对的数量
NUMBER=10000
# 第二个参数为AES加密类实例的key，必须为16位ascii字符，必须由 第一人 妥善保存
KEY='a'*16
# 第三个参数为AES加密类实例的iv，必须为16为数字，必须由 第二人 妥善保存
IV='1'*16
# 并发度，默认为单线程，单线程快38%
CONCURRENCY=1


import time
from wrapper import keypair as KEYPAIR
from wrapper import encryption as ENCRYPTION

def generate_keypairs(number, key='', iv='', encrypted=False):
    '''
    生成 number 个随机公私钥对
    最好能提供key和iv
    不做错误处理
    :param number: 待生成的数量
    :param key: AES加密私钥时使用的第一个密码, 如果留空，则生成随机key, 必须是16位
    :param iv: AES加密私钥时使用的第二个密码, 如果留空，则生成随机iv，必须是16位
    :return: 一个元组的数列，元组第一个值是加密后的私钥，第二个是地址明文
    '''
    keypairs=[]
    if key=='' or iv=='':
        key,iv=ENCRYPTION.generate_random_key_pair()
        print('key=%s\niv=%s' % (key,iv))
        # f=open('passphrase'+str(time.time()),'w')
        # f.write(str(key)+'\n'+str(iv))
        # f.flush()
        # f.close()

    # 创建一个AES256加密类的实例
    prpcrypt=ENCRYPTION.Prpcrypt(key,iv)

    # 一个方法：
    def some_method():
        keypair = KEYPAIR.Keypair.random()
        seed = keypair.seed().decode('utf-8')
        if encrypted==True:
            seed = (prpcrypt.encrypt(seed)).decode()
        address = keypair.address().decode()
        keypairs.append((seed, address))

    if CONCURRENCY == 1:
        # print("Single-threading mode, the statistics is accurate...")
        for i in range(number):
            some_method()
            progress=i*1.0/number*100
            if progress == int(progress):
                # print("%d%% is done..." % progress)
                pass
    else:
        import threading
        print("Multi-threading mode, the statistics may be inaccurate...")
        # 每次并发执行生成{{CONCURRENCY}}个私钥，并写入sqlite
        for i in range(number/CONCURRENCY):
            threads=[]
            for j in range(CONCURRENCY):
                thread = threading.Thread(target=some_method)
                threads.append(thread)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            print()


    return keypairs

def main():
    import sqlite3
    t=time.time()
    keypairs = generate_keypairs( NUMBER,KEY,IV)
    print('time used: %d seconds' % int(time.time()-t))

if __name__ == "__main__":
    main()








